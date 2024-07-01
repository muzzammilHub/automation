import os
from PyPDF2 import PdfReader
from io import BytesIO
import fitz
from PIL import Image



def save_image(image, image_path):
    try:
        image.save(image_path)
        
    except Exception as e:
        print(e)


def save_text(text, text_path):
    try:
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(e)


def extract_text_from_pdf(pdf_path, text_dir):
    try:
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            text_filename = os.path.join(text_dir, f'page_{i + 1}_text.txt')
            save_text(text, text_filename)

    except Exception as e:
        print(e)


def extract_images_from_pdf(pdf_path, images_dir):
    try:
        pdf_open = fitz.open(pdf_path)
        images_list = []

        
        for page_num in range(pdf_open.page_count):
            page_content = pdf_open.load_page(page_num)
            images_list.extend(page_content.get_images())

        os.makedirs(images_dir, exist_ok=True)

        for i, image_info in enumerate(images_list):
            print(image_info)
            base_image = pdf_open.extract_image(image_info[0])
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes))

            output_file = os.path.join(images_dir, f"image_{i+1}.png")

            save_image(image, output_file)

    except Exception as e:
        print(e)


def extract_and_save_pdf_content(pdf_path, text_dir, images_dir):
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    extract_text_from_pdf(pdf_path, text_dir)
    
    extract_images_from_pdf(pdf_path, images_dir)

pdf_path = '' #filePath
text_dir = 'pdf_text'
images_dir = 'pdf_images'


extract_and_save_pdf_content(pdf_path, text_dir, images_dir)

