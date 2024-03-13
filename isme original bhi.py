import os
import shutil
import PyPDF2

def compress_pdf_files(directory):
    """
    Compress all PDF files in the given directory.

    :param directory: The directory containing the PDF files.
    """
    original_folder = os.path.abspath(directory)
    original_pdf_folder = os.path.join(original_folder, "Original_PDFs")
    compressed_pdf_folder = os.path.join(original_folder, "Compressed_PDFs")
    os.makedirs(original_pdf_folder, exist_ok=True)  # Create folder for original PDFs
    os.makedirs(compressed_pdf_folder, exist_ok=True)  # Create folder for compressed PDFs

    for root, _, files in os.walk(original_folder):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                # Get the full path of the current file
                file_path = os.path.join(root, filename)
                # Check if the file is compressed
                if "Compressed_PDFs" in file_path:
                    # Move the compressed PDF file to the compressed PDF folder
                    move_to_folder(file_path, compressed_pdf_folder)
                else:
                    # Move the original PDF file to the original PDF folder
                    original_pdf_path = os.path.join(original_pdf_folder, filename)
                    move_to_folder(file_path, original_pdf_path)
                    # Compress the PDF file
                    compressed_file_path = compress_pdf(file_path)
                    if compressed_file_path:
                        print(f'Compressed {file_path} to {compressed_file_path}')
                        # Move the compressed PDF file to the compressed PDF folder
                        move_to_folder(compressed_file_path, compressed_pdf_folder)
                    else:
                        print(f'Failed to compress {file_path}')

def compress_pdf(file_path):
    """
    Compress a PDF file.

    :param file_path: The path of the PDF file to compress.
    :return: The path of the compressed PDF file, or None if compression fails.
    """
    try:
        # Read the PDF file
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            # Get the number of pages in the PDF file
            num_pages = len(reader.pages)
            # Create a new PDF file with the same number of pages
            writer = PyPDF2.PdfWriter()
            for i in range(num_pages):
                # Get the current page
                page = reader.pages[i]
                # Set the compression level for the page
                page.compress_content_streams()
                # Add the compressed page to the new PDF file
                writer.add_page(page)
            # Write the compressed PDF file
            compressed_file_path = f'{file_path[:-4]}_compressed.pdf'
            with open(compressed_file_path, 'wb') as output_file:
                writer.write(output_file)
            return compressed_file_path
    except Exception as e:
        print(f'Error compressing {file_path}: {e}')
        return None

def move_to_folder(file_path, target_folder):
    """
    Move a file to the target folder.

    :param file_path: The path of the file to move.
    :param target_folder: The path of the target folder.
    """
    try:
        shutil.move(file_path, target_folder)
        print(f'Moved {file_path} to {target_folder}')
    except Exception as e:
        print(f'Error moving {file_path} to {target_folder}: {e}')

# Set the directory that contains the PDF files to compress
directory = 'uu'
compress_pdf_files(directory)
