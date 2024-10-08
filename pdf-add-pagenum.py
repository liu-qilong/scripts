"""
usage example:
python pdf-add-pagenum.py --pdf-path temp/file.pdf --output-path output/numbered.pdf
"""
import os
import io
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from PyPDF2 import PdfWriter, PdfReader

def add_page_numbers(input_pdf, output_pdf, page_number_color=colors.black):
    input_pdf_reader = PdfReader(open(input_pdf, "rb"))
    output_pdf_writer = PdfWriter()
    total_pages = len(input_pdf_reader.pages)

    # get the dimensions of the first page
    # and calculate font size based its size
    page = input_pdf_reader.pages[0]
    page_width = page.mediabox.width
    font_size = float(page_width) * 0.02  # 2% of the smaller dimension

    for page_num in range(total_pages):
        # create a PDF with the page number
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFillColor(page_number_color)  # set the color of the page number
        can.setFont("Courier", font_size)  # Set the font size
        can.drawString(10, 10, f'{page_num + 1}/{total_pages}')  # position the page number
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        page_number_pdf = PdfReader(packet)

        # merge the page number pdf with the input pdf page
        page = input_pdf_reader.pages[page_num]
        page.merge_page(page_number_pdf.pages[0])
        output_pdf_writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        output_pdf_writer.write(output_file)


if __name__ == '__main__':
    # get arguments from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-path', '-f', help="The path to the pdf file.", type=str, default='input/file.pdf')
    parser.add_argument('--output-path', '-o', help="The output file path of the page-numbered pdf. If set as 'auto', the pdf will be outputted to the same folder with the original pdf", type=str, default='output/numbered.pdf')
    args = parser.parse_args()

    if args.output_path == 'auto':
        args.output_path = args.file_path.replace(
            os.path.basename(args.file_path), 'numbered.pdf')

    add_page_numbers(args.file_path, args.output_path, page_number_color=colors.red)