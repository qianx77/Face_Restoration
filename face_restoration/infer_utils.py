import cv2
import os
import torch
from basicsr.utils import img2tensor, tensor2img
from basicsr.utils.download_util import load_file_from_url
from facexlib.utils.face_restoration_helper import FaceRestoreHelper
from torchvision.transforms.functional import normalize

from face_restoration.archs.gfpgan.gfpgan_bilinear_arch import GFPGANBilinear
from face_restoration.archs.gfpgan.gfpganv1_arch import GFPGANv1
from face_restoration.archs.gfpgan.gfpganv1_clean_arch import GFPGANv1Clean
from face_restoration.archs.RestoreFormer.vqvae_arch import VQVAEGANMultiHeadTransformer

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Restorer():
    """Helper for restoration with GFPGAN.

    It will detect and crop faces, and then resize the faces to 512x512.
    GFPGAN is used to restored the resized faces.
    The background is upsampled with the bg_upsampler.
    Finally, the faces will be pasted back to the upsample background image.

    Args:
        model_path (str): The path to the GFPGAN model. It can be urls (will first download it automatically).
        upscale (float): The upscale of the final output. Default: 2.
        arch (str): The GFPGAN architecture. Option: clean | original. Default: clean.
        channel_multiplier (int): Channel multiplier for large networks of StyleGAN2. Default: 2.
        bg_upsampler (nn.Module): The upsampler for the background. Default: None.
    """

    def __init__(self, model_path, upscale=2, arch='clean', channel_multiplier=2, bg_upsampler=None, device=None):
        self.upscale = upscale
        self.bg_upsampler = bg_upsampler

        # initialize model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device
        # initialize the GFP-GAN
        if arch == 'gfpgan_clean':
            self.model = GFPGANv1Clean(
                out_size=512,
                num_style_feat=512,
                channel_multiplier=channel_multiplier,
                decoder_load_path=None,
                fix_decoder=False,
                num_mlp=8,
                input_is_latent=True,
                different_w=True,
                narrow=1,
                sft_half=True)
        elif arch == 'CodeFormer':
            from face_restoration.archs.codeformer.codeformer_arch import CodeFormer
            self.model = CodeFormer(dim_embd=512, codebook_size=1024, n_head=8, n_layers=9, 
                                            connect_list=['32', '64', '128', '256'])
        elif arch == 'GPEN':
            from face_restoration.archs.gpen.gpen_arch import GPEN
            self.model = GPEN(size=512,style_dim=512,n_mlp=8,channel_multiplier= 2,narrow = 1,)
        elif arch == 'RestoreFormer':
            self.model = VQVAEGANMultiHeadTransformer(head_size = 8, ex_multi_scale_num = 0)
        elif arch == 'RestoreFormer++':
            self.model = VQVAEGANMultiHeadTransformer(head_size = 4, ex_multi_scale_num = 1)
        elif arch =="VQFRv2":
            from face_restoration.archs.vqfr.vqfrv2_arch import VQFRv2
            self.model = VQFRv2(
                base_channels=64,
                channel_multipliers=[1, 2, 2, 4, 4, 8],
                num_enc_blocks=2,
                use_enc_attention=True,
                num_dec_blocks=2,
                use_dec_attention=True,
                code_dim=256,
                inpfeat_dim=32,
                align_opt={
                    'cond_channels': 32,
                    'deformable_groups': 4
                },
                code_selection_mode='Predict',  # Predict/Nearest
                quantizer_opt={
                    'type': 'L2VectorQuantizer',
                    'num_code': 1024,
                    'code_dim': 256,
                    'spatial_size': [16, 16]
                })

        # initialize face helper
        self.face_helper = FaceRestoreHelper(
            upscale,
            face_size=512,
            crop_ratio=(1, 1),
            det_model='retinaface_resnet50',
            save_ext='png',
            use_parse=True,
            device=self.device,
            model_rootpath='face_restoration/weights')

        if model_path.startswith('https://'):
            model_path = load_file_from_url(
                url=model_path, model_dir=os.path.join(ROOT_DIR, 'face_restoration/weights'), progress=True, file_name=None)
        loadnet = torch.load(model_path)
        if 'params_ema' in loadnet:
            keyname = 'params_ema'
            self.model.load_state_dict(loadnet[keyname], strict=False)
        elif 'params' in loadnet:
            keyname = 'params'
            self.model.load_state_dict(loadnet[keyname], strict=False)
        else:
            self.model.load_state_dict(loadnet, strict=False)
        self.model.eval()
        self.model = self.model.to(self.device)

    @torch.no_grad()
    def enhance(self, img, has_aligned=False, only_center_face=False, paste_back=True, weight=0.5,w=0.5):
        self.face_helper.clean_all()

        if has_aligned:  # the inputs are already aligned
            img = cv2.resize(img, (512, 512))
            self.face_helper.cropped_faces = [img]
        else:
            self.face_helper.read_image(img)
            # get face landmarks for each face
            self.face_helper.get_face_landmarks_5(only_center_face=only_center_face, eye_dist_threshold=5)
            # eye_dist_threshold=5: skip faces whose eye distance is smaller than 5 pixels
            # TODO: even with eye_dist_threshold, it will still introduce wrong detections and restorations.
            # align and warp each face
            self.face_helper.align_warp_face()

        # face restoration
        for cropped_face in self.face_helper.cropped_faces:
            # prepare data
            cropped_face_t = img2tensor(cropped_face / 255., bgr2rgb=True, float32=True)
            normalize(cropped_face_t, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True)
            cropped_face_t = cropped_face_t.unsqueeze(0).to(self.device)

            try:
                output = self.model(cropped_face_t, return_rgb=False, weight=weight,w=w)[0]
                #self.model(cropped_face_t, w=w, adain=True)[0]
                # convert to image
                restored_face = tensor2img(output.squeeze(0), rgb2bgr=True, min_max=(-1, 1))
            except RuntimeError as error:
                print(f'\tFailed inference for GFPGAN: {error}.')
                restored_face = cropped_face

            restored_face = restored_face.astype('uint8')
            self.face_helper.add_restored_face(restored_face)

        if not has_aligned and paste_back:
            # upsample the background
            if self.bg_upsampler is not None:
                # Now only support RealESRGAN for upsampling background
                bg_img = self.bg_upsampler.enhance(img, outscale=self.upscale)[0]
            else:
                bg_img = None

            self.face_helper.get_inverse_affine(None)
            # paste each restored face to the input image
            restored_img = self.face_helper.paste_faces_to_input_image(upsample_img=bg_img)
            return self.face_helper.cropped_faces, self.face_helper.restored_faces, restored_img
        else:
            return self.face_helper.cropped_faces, self.face_helper.restored_faces, None
