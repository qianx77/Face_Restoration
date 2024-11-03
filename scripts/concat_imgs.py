import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# def load_images_from_folders(folders):
#     images_dict = {}
#     for folder in folders:
#         for filename in os.listdir(folder):
#             if filename.endswith(('.png', '.jpg', '.jpeg')):  # 可根据需要添加更多格式
#                 img_path = os.path.join(folder, filename)
#                 if filename not in images_dict:
#                     images_dict[filename] = {}
#                 images_dict[filename][folder] = Image.open(img_path)
#     return images_dict

# def create_comparison_image(images_dict, method_names, images_per_row, line_width=10):
#     # 计算拼接图像的宽度和高度
#     rows = (len(images_dict) + images_per_row - 1) // images_per_row
#     max_height = max(img.size[1] for img in images_dict.values() for img in img.values())
#     total_width = sum(max(img.size[0] for img in images_dict.values() for img in img.values()) for _ in range(images_per_row)) + line_width * (images_per_row + 1)

#     comparison_image = Image.new('RGB', (total_width, rows * (max_height + line_width) + line_width), color='white')
    
#     draw = ImageDraw.Draw(comparison_image)
    
#     x_offset = line_width
#     y_offset = line_width
    
#     for i, (filename, images) in enumerate(images_dict.items()):
#         if i > 0 and i % images_per_row == 0:
#             y_offset += max_height + line_width
#             x_offset = line_width
        
#         for j, (folder, img) in enumerate(images.items()):
#             comparison_image.paste(img, (x_offset, y_offset))
#             draw.rectangle([x_offset, y_offset + img.size[1], x_offset + img.size[0], y_offset + img.size[1] + line_width], fill='white')
#             draw.text((x_offset + 5, y_offset + img.size[1] + 5), method_names[j], fill='black')
#             x_offset += img.size[0] + line_width

#     return comparison_image

# def main(folders, method_names, images_per_row=3):
#     images_dict = load_images_from_folders(folders)
#     comparison_image = create_comparison_image(images_dict, method_names, images_per_row)
#     comparison_image.show()  # 显示拼接后的图片
#     comparison_image.save('comparison_image.png')  # 保存拼接后的图片

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def load_images_from_folders(folders):
    images_dict = {}
    for folder in folders:
        for filename in os.listdir(folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):  # 可根据需要添加更多格式
                img_path = os.path.join(folder, filename)
                if filename not in images_dict:
                    images_dict[filename] = {}
                images_dict[filename][folder] = Image.open(img_path)
    return images_dict

def create_comparison_image(images_dict, method_names, images_per_row, output_folder, index, line_width=10):
    # 计算拼接图像的宽度和高度
    rows = (len(images_dict) + images_per_row - 1) // images_per_row
    max_height = max(img.size[1] for img in images_dict.values() for img in img.values())
    total_width = sum(max(img.size[0] for img in images_dict.values() for img in img.values()) for _ in range(images_per_row)) + line_width * (images_per_row + 1)

    # 额外增加下方文字的高度
    text_height = 40  # 调整文字区域的高度
    comparison_image = Image.new('RGB', (total_width, rows * (max_height + line_width + text_height) + line_width), color='white')
    
    draw = ImageDraw.Draw(comparison_image)

    # 使用默认字体或指定字体
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # 增大字体
    except IOError:
        font = ImageFont.load_default()

    x_offset = line_width
    y_offset = line_width

    for i, (filename, images) in enumerate(images_dict.items()):
        if i > 0 and i % images_per_row == 0:
            y_offset += max_height + line_width + text_height
            x_offset = line_width
        
        for j, (folder, img) in enumerate(images.items()):
            comparison_image.paste(img, (x_offset, y_offset))
            draw.rectangle([x_offset, y_offset + img.size[1], x_offset + img.size[0], y_offset + img.size[1] + text_height], fill='white')
            draw.text((x_offset + 5, y_offset + img.size[1] + 5), method_names[j], fill='black', font=font)
            x_offset += img.size[0] + line_width

    output_path = os.path.join(output_folder, f'comparison_image_{index}.png')
    comparison_image.save(output_path)  # 保存拼接后的图片

def main(folders, method_names, images_per_row=3, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)  # 创建输出文件夹
    images_dict = load_images_from_folders(folders)

    for index, (filename, images) in enumerate(images_dict.items()):
        create_comparison_image({filename: images}, method_names, images_per_row, output_folder, index)




# if __name__ == '__main__':
#     # 例子：输入不同去噪方法的文件夹和名称
#     folders = ['path/to/folder1', 'path/to/folder2', 'path/to/folder3']
#     method_names = ['Method 1', 'Method 2', 'Method 3']
#     images_per_row = 3  # 一行展示多少张图片
#     main(folders, method_names, images_per_row)


if __name__ == '__main__':
    # 例子：输入不同去噪方法的文件夹和名称
    folders = [r"inputs\cropped_faces",r'results\gfpgan1.4\restored_imgs', r'results\CodeFormer\restored_imgs', r'results\GPEN\restored_imgs']
    method_names = ['input', 'GFPGANv1.4', 'CodeFormer','GPEN']
    images_per_row = 4  # 一行展示多少张图片
    main(folders, method_names, images_per_row,"assets")
