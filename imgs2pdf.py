"""
usage example:
python imgs2pdf.py 
"""
import os
import argparse
from PIL import Image
from natsort import natsorted

if __name__ == '__main__':
    # get arguments from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', '-f', help="The path to the input folder.", type=str, default='input/')
    parser.add_argument('--output-path', '-o', help="The output file path of the combined pdf. If set as 'auto', the pdf will be outputted to the input folder with the input folder's name", type=str, default='output/numbered.pdf')
    args = parser.parse_args()

    if args.output_path == 'auto':
        args.output_path = os.path.join(args.input_folder, os.path.basename(os.path.normpath(args.input_folder)) + '.pdf')

    # get all image files in the input folder
    image_files = [f for f in os.listdir(args.input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files = natsorted(image_files)

    # open each image and append to a list
    images = []

    for idx, file in enumerate(image_files):
        img_path = os.path.join(args.input_folder, file)

        with Image.open(img_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            images.append(img.copy())
            print(f"append {img_path}")

    # save the list of images as a pdf
    if images:
        images[0].save(args.output_path, save_all=True, append_images=images[1:])
        print(f"-> {args.output_path}")

        for img in images:
            img.close()
    else:
        print("no valid .png or .jpg files found in the input folder")