

## A repository for the inference of face restoration
A list of face restoration papers and codes, can see in [this repository ](https://github.com/yeruiqian/Face_Restoration_Ref.git).
### 

### Update
- **2024.11.03**: Add [GFPGAN](https://github.com/TencentARC/GFPGAN.git)、[CodeFromer](https://github.com/sczhou/CodeFormer.git) 、[GPEN](https://github.com/yangxy/GPEN.git) inference codes. 
  

### TODO
- [ ] Add torch2onnx script
- [ ] Add more face restoration method


### inference results

<p align="center">
  <img src="assets\comparison_image_0.png">
</p>
<p align="center">
  <img src="assets\comparison_image_1.png">
</p>
<p align="center">
  <img src="assets\comparison_image_2.png">
</p>
<p align="center">
  <img src="assets\comparison_image_3.png">
</p>

---


### Installation


1. Clone repo

    ```bash
    git clone https://github.com/yeruiqian/Face_Restoration.git
    cd Face_Restoration
    ```

2. Install dependent packages

    ```bash
    # Install basicsr - https://github.com/xinntao/BasicSR
    pip install basicsr

    # Install facexlib - https://github.com/xinntao/facexlib
    pip install facexlib

    # you also can refer to my own environment 'requirements_self.txt'
    pip install -r requirements.txt
    python setup.py develop

    # If you want to enhance the background (non-face) regions with Real-ESRGAN,
    # you also need to install the realesrgan package
    pip install realesrgan
    ```



### Download weights
download the weights and put them in ```experiments/pretrained_models```
```bash
'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth'
'https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth'
'https://public-vigen-video.oss-cn-shanghai.aliyuncs.com/robin/models/GPEN-BFR-512.pth'

```

### Inference


```bash
python inference.py -i inputs/cropped_faces -o results/GPEN -v GPEN -s 1
python inference.py -i inputs/cropped_faces -o results/GFPGAN1.4 -v GFPGANv1.4 -s 1
python inference.py -i inputs/cropped_faces -o results/CodeFormer -v CodeFormer -s 1
```

```console
Usage: python inference_gfpgan.py -i inputs/whole_imgs -o results -v 1.3 -s 2 [options]...

  -h                   show this help
  -i input             Input image or folder. Default: inputs/cropped_faces
  -o output            Output folder. Default: results
  -v version           Different model. Option: GFPGANv1.4,GPEN,CodeFormer. Default: GFPGANv1.4
  -s upscale           The final upsampling scale of the image. Default: 2
  -bg_upsampler        background upsampler. Default: realesrgan
  -bg_tile             Tile size for background sampler, 0 for no tile during testing. Default: 400
  -suffix              Suffix of the restored faces
  -only_center_face    Only restore the center face
  -aligned             Input are aligned faces
  -ext                 Image extension. Options: auto | jpg | png, auto means using the same extension as inputs. Default: auto
```

### Acknowledgement

This project is based on [BasicSR](https://github.com/XPixelGroup/BasicSR). Codes are brought from [GFPGAN](https://github.com/TencentARC/GFPGAN.git)、[CodeFromer](https://github.com/sczhou/CodeFormer.git) 、[GPEN](https://github.com/yangxy/GPEN.git). Thanks for their awesome works.

