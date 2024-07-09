import os
import sys
from glob import glob
import PyPDF2
from PyPDF2 import PdfReader
from tqdm import tqdm


def pdf_full_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text_list = list()
    for page in pdf_reader.pages:
        text_list.append(page.extract_text())
    return ' '.join(text_list).replace('\x00','')


def main(country_code):
    rel_in_path = os.path.join('data', country_code, 'pdfs')
    input_dir = os.path.abspath(rel_in_path)
    rel_out_path = os.path.join('data', country_code, 'txts')
    output_dir = os.path.abspath(rel_out_path)
    os.makedirs(output_dir, exist_ok=True)

    all_wildcard = os.path.join(input_dir, "**/*")
    all_files = glob(all_wildcard, recursive=True)
    all_ext = list(set([os.path.splitext(file)[1] for file in all_files]))
    print("All found extensions:", all_ext)
    pdf_wildcard = os.path.join(input_dir, '**/*.pdf')
    pdf_files = glob(pdf_wildcard, recursive=True)
    for pdf_file in tqdm(pdf_files):
        file_basename = os.path.basename(pdf_file)
        file_name, _ = os.path.splitext(file_basename)
        destination_basename = '{}.txt'.format(file_name)
        destination_file_path = os.path.join(output_dir, destination_basename)
        if not os.path.exists(destination_file_path):
            try:
                full_text = pdf_full_text(pdf_file)
            except PyPDF2.errors.PdfReadError:
                print("Corrupted PDF: {}".format(file_basename))
            with open(destination_file_path, 'w') as destination_file:
                destination_file.write(full_text)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Enter country code as first positional argument.")
    else:
        main(sys.argv[1])