

## A repository for the inference of face restoration
A list of face restoration papers and codes, can see in [this repository ](https://github.com/yeruiqian/Face_Restoration_Ref.git).


|Year<div style="width:20px">|Pub<div style="width:60px">|Abbreviation<div style="width:45px">|Release<div style="width:45px">|
|:---:|:----:|:----:|:----:|
|2021|CVPR|GFPGAN|✔|
|2021|CVPR|GPEN|✔|
|2022|NeurIPS|CodeFormer|✔|
|2022|CVPR|RestoreFormer|✔|
|2022|ECCV|VQFR|✔|
|2023|TPAMI|RestoreFormer++|✔|


### Update
- **2025.03.07**: Add [VQFR](https://github.com/TencentARC/VQFR)
- **2025.03.05**: Add [RestoreFormer](https://github.com/wzhouxiff/RestoreFormerPlusPlus.git)、[RestoreFormer++](https://github.com/wzhouxiff/RestoreFormerPlusPlus.git) inference codes.
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
Download the weights and put them in ```experiments/pretrained_models```
```bash
链接: https://pan.baidu.com/s/1Dt0YElo1aKyPiZE0By1mGA 提取码: jvbt 
```

### Inference
Method including GPEN、GFPGAN1.4、CodeFormer、RestoreFormer、RestoreFormer++、VQFRv2：

```bash
python inference.py -i inputs/cropped_faces -o results/out -v [method] -s 1
```

```console
Usage: python inference_gfpgan.py -i inputs/whole_imgs -o results -v 1.3 -s 2 [options]...

  -h                   show this help
  -i input             Input image or folder. Default: inputs/cropped_faces
  -o output            Output folder. Default: results
  -v version           Different model. Option: GFPGANv1.4,GPEN,CodeFormer,RestoreFormer,RestoreFormer++,VQFRv2：. Default: GFPGANv1.4
  -s upscale           The final upsampling scale of the image. Default: 2
  -bg_upsampler        background upsampler. Default: realesrgan
  -bg_tile             Tile size for background sampler, 0 for no tile during testing. Default: 400
  -suffix              Suffix of the restored faces
  -only_center_face    Only restore the center face
  -aligned             Input are aligned faces
  -ext                 Image extension. Options: auto | jpg | png, auto means using the same extension as inputs. Default: auto
```

### Acknowledgement

This project is based on [BasicSR](https://github.com/XPixelGroup/BasicSR). Codes are brought from [GFPGAN](https://github.com/TencentARC/GFPGAN.git)、[CodeFromer](https://github.com/sczhou/CodeFormer.git) 、[GPEN](https://github.com/yangxy/GPEN.git)、[RestoreFormer++](https://github.com/wzhouxiff/RestoreFormerPlusPlus)、[VQFR](https://github.com/TencentARC/VQFR). Thanks for their awesome works.

