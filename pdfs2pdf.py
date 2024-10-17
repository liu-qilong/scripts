#!/usr/bin/env python
"""
usage example:
python pdfs2pdf.py --pdf-folder input/ --output-path output/combined.pdf
"""
import os
import argparse
from PyPDF2 import PdfMerger
from natsort import natsorted


def push_toc_tree(tree, keys, merger):
    for key in keys:
        if key == '':
            continue

        if key not in tree:
            tree[key] = {}
            tree[key]['toc_item'] = merger.add_outline_item(
                title=key,
                page_number=len(merger.pages),
                parent=tree['toc_item']
                )

        tree = tree[key]


def get_toc_tree(tree, keys):
    for key in keys:
        if key == '':
            continue

        if key not in tree:
            return None

        tree = tree[key]
    
    return tree['toc_item']


if __name__ == '__main__':
    # get pdf folder from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf-folder', '-f', help="The path to the pdf folder.", type=str, default='input/')
    parser.add_argument('--output-path', '-o', help="The output file path of the combined pdf. If set as 'auto', the pdf will be outputted to the input folder with the input folder's name", type=str, default='output/combined.pdf')
    args = parser.parse_args()

    if args.output_path == 'auto':
        args.output_path = os.path.join(args.pdf_folder, os.path.basename(os.path.normpath(args.pdf_folder)) + '.pdf')

    # get pdf files
    pdf_ls = []

    for root, _, files in natsorted(os.walk(args.pdf_folder)):
        files = natsorted(files)
        for file in files:
            if file.endswith('.pdf'):
                path = os.path.join(root, file)
                keys = path.replace(args.pdf_folder, '').replace('.pdf', '').split(os.sep)
                pdf_ls.append({
                    'path': path,
                    'keys': keys[:-1],
                    'title': keys[-1],
                    })

    # merge pdf files and create hierarchical table of contents
    merger = PdfMerger()
    toc_tree = {'toc_item': None}

    for pdf in pdf_ls:
        print(f'combining {pdf["path"]}...')
        push_toc_tree(toc_tree, pdf['keys'], merger)
        merger.add_outline_item(
            title=pdf['title'],
            page_number=len(merger.pages),
            parent=get_toc_tree(toc_tree, pdf['keys']),
            )
        merger.append(pdf['path'], import_outline=False)
        
    with open(args.output_path, 'wb') as f_out:
        merger.write(f_out)