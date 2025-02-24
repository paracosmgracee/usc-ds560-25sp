import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import concurrent.futures
import os
from contextlib import contextmanager
import time
from pathlib import Path

import logging
import threading
from datetime import datetime
import psutil

# Add logging configuration at the top of the file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s',
    handlers=[
        logging.FileHandler(f'Lab_6/pdf_processing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

@contextmanager
def open_pdf(file_path):
    doc = fitz.open(file_path)
    try:
        yield doc
    finally:
        doc.close()

def process_image(page):
    thread_id = threading.get_ident()
    try:
        logging.info(f'Page {page.number}: Starting OCR processing [Thread: {thread_id}]')
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        logging.debug(f'Page {page.number}: Image conversion complete, starting OCR')
        result = pytesseract.image_to_string(img)
        logging.info(f'Page {page.number}: OCR completed successfully [Thread: {thread_id}]')
        return result
    except Exception as e:
        logging.error(f'Page {page.number}: OCR failed [Thread: {thread_id}]: {str(e)}', exc_info=True)
        return f"Error processing page: {str(e)}"

def extract_text_from_pdf(file_path, batch_size=4):
    text = []
    logging.info(f'Starting PDF extraction: {file_path}')
    
    with open_pdf(file_path) as doc:
        logging.info(f'PDF {file_path} opened with {doc.page_count} pages')
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(os.cpu_count(), 4),
            thread_name_prefix='pdf_worker'
        ) as executor:
            futures = []
            for i in range(0, doc.page_count, batch_size):
                batch = [doc[j] for j in range(i, min(i + batch_size, doc.page_count))]
                logging.info(f'Processing {file_path} batch of pages {i} to {min(i + batch_size, doc.page_count)-1}')
                for page in batch:
                    futures.append(executor.submit(process_image, page))
            
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        text.append(result)
                    completed += 1
                    logging.info(f'Completed {file_path}: {completed}/{len(futures)} pages')
                except Exception as e:
                    logging.error(f'Error in thread: {str(e)}')

    return '\n'.join(text)

def process_single_pdf(pdf_path, output_path):
    try:
        start_time = time.time()
        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        logging.info(f'Starting processing of {pdf_path.name} [Memory usage: {memory_usage:.2f} MB]')
        
        pdf_text = extract_text_from_pdf(pdf_path)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(pdf_text)
        
        elapsed_time = time.time() - start_time
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        logging.info(f'Completed {pdf_path.name} in {elapsed_time:.2f}s [Memory: {final_memory:.2f} MB]')
        
        return f"Successfully processed {pdf_path.name}"
    except Exception as e:
        logging.error(f'Failed to process {pdf_path.name}', exc_info=True)
        return f"Error processing {pdf_path.name}: {str(e)}"

if __name__ == '__main__':   
    start_time = time.time()
    
    # Define input and output directories
    input_dir = Path('Lab_6/raw_pdf_data')
    output_dir = Path('Lab_6/processed_data/text')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files
    pdf_files = list(input_dir.glob('*.pdf'))
    
    # Process PDFs in parallel
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=min(os.cpu_count(), 4),
        thread_name_prefix='pdf_processor'
    ) as executor:
        # Create tasks for each PDF
        futures = []
        for pdf_file in pdf_files:
            output_file = output_dir / f"{pdf_file.stem}.txt"
            futures.append(
                executor.submit(process_single_pdf, pdf_file, output_file)
            )
        
        # Process results as they complete
        total_files = len(pdf_files)
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            print(f"[{completed}/{total_files}] {future.result()}")
    
    total_time = time.time() - start_time
    print(f"\nProcessing Summary:")
    print(f"Total files processed: {total_files}")
    print(f"Total processing time: {total_time:.2f} seconds")
    print(f"Average time per file: {total_time/total_files:.2f} seconds")