
import torch
import onnx
import onnxruntime as ort
import numpy as np
from PIL import Image
import argparse
from face_restoration.archs.gfpgan.gfpganv1_clean_onnx_arch import GFPGANv1CleanOnnx

def convert_to_onnx(model, weight,input_tensor, onnx_file_path):
    weight = torch.load(weight)
    model.load_state_dict(weight['params_ema'],strict=False)
    # 将模型设为评估模式
    model.eval()
    with torch.no_grad():
        torch.onnx.export(model, input_tensor, onnx_file_path, export_params=True, 
                          opset_version=11, do_constant_folding=True, 
                          input_names=['input'], output_names=['output'])
    print(f'Model exported to {onnx_file_path}')




def validate_model(model, input_tensor, onnx_file_path):
    # PyTorch 推理
    with torch.no_grad():
        pytorch_output = model(input_tensor)

    # ONNX 推理
    onnx_session = ort.InferenceSession(onnx_file_path)
    onnx_input = {onnx_session.get_inputs()[0].name: input_tensor.numpy()}
    onnx_output = onnx_session.run(None, onnx_input)[0]

    # 比较结果
    pytorch_output_np = pytorch_output[0].numpy()
    
    print('PyTorch Output Shape:', pytorch_output_np.shape)
    print('ONNX Output Shape:', onnx_output.shape)
    print('Outputs are equal:', np.allclose(pytorch_output_np, onnx_output, atol=1e-5))

    return pytorch_output_np, onnx_output

def load_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((512, 512))  # 根据模型要求调整大小
    image = torch.tensor(np.array(image)).permute(2, 0, 1).float() / 255.0
    # 归一化
    image = (image - 0.5) / 0.5
    return image.unsqueeze(0)  # 添加批次维度

def save_output_image(output_tensor, output_path):
    output_image = (output_tensor.squeeze(0).permute(1, 2, 0).numpy() * 0.5 + 0.5) * 255
    output_image = np.clip(output_image, 0, 255).astype(np.uint8)
    output_image = Image.fromarray(output_image)
    output_image.save(output_path)

# 示例使用
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        default='inputs/whole_imgs',
        help='Input image or folder. Default: inputs/whole_imgs')
    parser.add_argument('-o', '--output', type=str, default='results', help='Output folder. Default: results')
    model = GFPGANv1CleanOnnx(out_size=512,channel_multiplier=2,input_is_latent=True,different_w=True,sft_half=True,decoder_load_path=None)
    #model.load_state_dict()
    weight = 'experiments\pretrained_models\GFPGANv1.4.pth'
    
    input_tensor = load_image(r'inputs\cropped_faces\Adele_crop.png')
    
    onnx_file_path = r'experiments\onnx\GFPGANv1.4.onnx'
    convert_to_onnx(model,weight, input_tensor, onnx_file_path)
    
    pytorch_output, onnx_output = validate_model(model, input_tensor, onnx_file_path)

    save_output_image(torch.tensor(pytorch_output), 'results\onnx_val\pytorch_output.jpg')
    save_output_image(torch.tensor(onnx_output), 'results\onnx_val\onnx_output.jpg')
