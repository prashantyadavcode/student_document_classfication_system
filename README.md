# Student Document Classification System

## Overview

This project implements an OCR-based document classification system for processing student-submitted PDF files. It extracts text from each page using Tesseract OCR and classifies the content into predefined document categories such as Aadhaar, 12th Certificate, Registration Form, or Unknown.

The system is designed to assist in automating document verification workflows by identifying document types at the page level.

---

## Objective

Educational institutions frequently receive multiple documents bundled in a single PDF file. Manual verification and segregation of these documents is time-consuming and prone to errors. This project aims to:

- Automatically extract text from PDF documents  
- Classify each page into a document category  
- Provide a structured output of detected document types  

---

## Features

- Page-wise document classification  
- OCR-based text extraction from PDFs  
- Rule-based classification using keyword matching  
- Modular and extensible code structure  

---

## Technology Stack

- Python  
- Pandas  
- Tesseract OCR  
- pdf2image  
- Pillow (PIL)  

---

## Installation

### 1. Clone the Repository

git clone https://github.com/your-username/document-classifier.git  
cd document-classifier

### 2. Install Python Dependencies

pip install pandas pytesseract pdf2image pillow

### 3. Install Tesseract OCR

Download and install Tesseract OCR from the official repository:

https://github.com/tesseract-ocr/tesseract

After installation, configure the executable path if required:

pytesseract.pytesseract.tesseract_cmd = r"/path/to/tesseract"

---

## Project Structure

document-classifier/
│
├── students_pdfs/        # Directory containing input PDF files
├── main.py               # Main script for processing documents
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation

---

## How It Works

1. The system reads PDF files from the input directory.  
2. Each PDF is converted into images, one per page.  
3. OCR is applied to extract text from each page.  
4. Extracted text is analyzed using keyword-based rules.  
5. Each page is classified into a document category.  

---

## Classification Logic

The classification is based on keyword matching within the extracted text:

- Aadhaar: keywords such as "aadhaar", "uidai"  
- 12th Certificate: keywords such as "marksheet", "board", "certificate"  
- Registration Form: keywords such as "registration", "application form"  
- Unknown: when no relevant keywords are detected  

---

## Usage

1. Place PDF files inside the students_pdfs/ directory.  
2. Run the main script:

python main.py

3. The system will output the classification results for each page in the console.  

---

## Example Output

Processing: student1.pdf

Page 1: Aadhaar  
Page 2: 12th Certificate  
Page 3: Registration Form  
Page 4: Unknown  

---

## Limitations

- The system uses rule-based classification and may not generalize well to all document formats.  
- OCR accuracy depends on the quality and clarity of the input PDFs.  
- Text extraction and name identification are basic and may require improvement for production use.  

---

## Future Enhancements

- Replace rule-based classification with a machine learning model  
- Improve text extraction accuracy using preprocessing techniques  
- Extract structured information such as identification numbers and personal details  
- Develop an API interface for integration with other systems  
- Add support for batch processing and logging  

---

## License

This project is available under the MIT License
