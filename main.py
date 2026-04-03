import os
import fitz
import pytesseract
import cv2
import numpy as np
from PIL import Image
import shutil
from ultralytics import YOLO

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

yolo = YOLO("yolov8m.pt")

INPUT_FOLDER = "./"
OUTPUT_BASE = "A. Student Documentation"

FOLDERS = {
    "registration": "01. Student Registration Form",
    "photo": "02. Student Passport Size Photograph with Name and Roll No",
    "caste": "03. SC_ST_OBC Certificate with Name and Roll No",
    "aadhaar": "04. Aadhaar Card (Front and Back)",
    "marksheet": "05. Grade 12th Certificates_Marksheet",
    "empty": "06. Certificate Distribution Photographs",
    "manual": "07. Manual Review"
}

def create_folders():
    for key in FOLDERS:
        os.makedirs(os.path.join(OUTPUT_BASE, FOLDERS[key]), exist_ok=True)

def extract_text_from_page(page):
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    text = pytesseract.image_to_string(img)
    return text.lower()

def detect_person(img):
    results = yolo(img, verbose=False)
    best = None
    best_area = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)
                if area > best_area:
                    best_area = area
                    best = (x1, y1, x2, y2)
    return best

def extract_images(page, student_name):
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, -1)

    box = detect_person(img)

    if box:
        x1, y1, x2, y2 = box

        w = x2 - x1
        h = y2 - y1

        pad_x = int(w * 0.15)
        pad_y = int(h * 0.25)

        x1 = max(0, x1 - pad_x)
        y1 = max(0, y1 - pad_y)
        x2 = min(img.shape[1], x2 + pad_x)
        y2 = min(img.shape[0], y2 + pad_y)

        crop = img[y1:y2, x1:x2]
    else:
        h, w = img.shape[:2]
        crop = img[int(h*0.1):int(h*0.5), int(w*0.6):int(w*0.95)]

    output_path = os.path.join(
        OUTPUT_BASE,
        FOLDERS["photo"],
        f"{student_name}_photo.png"
    )

    Image.fromarray(crop).save(output_path)

def classify_page(text):
    if "marksheet" in text or "higher secondary" in text:
        return "marksheet"
    elif "aadhaar" in text or "aadhar" in text:
        return "aadhaar"
    elif "caste certificate" in text or "scheduled caste" in text or "obc" in text:
        return "caste"
    return "unknown"

def save_grouped_pdf(doc, pages, output_path):
    if not pages:
        return False
    new_pdf = fitz.open()
    for p in pages:
        new_pdf.insert_pdf(doc, from_page=p, to_page=p)
    new_pdf.save(output_path)
    new_pdf.close()
    return True

def save_manual_pages(doc, student_name):
    student_folder = os.path.join(
        OUTPUT_BASE,
        FOLDERS["manual"],
        student_name
    )

    os.makedirs(student_folder, exist_ok=True)

    for i in range(len(doc)):
        new_pdf = fitz.open()
        new_pdf.insert_pdf(doc, from_page=i, to_page=i)
        new_pdf.save(os.path.join(student_folder, f"page_{i+1}.pdf"))
        new_pdf.close()

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    student_name = os.path.basename(pdf_path).replace(".pdf", "")

    registration_pages = []
    aadhaar_pages = []
    caste_pages = []
    marksheet_pages = []

    for i in range(min(3, len(doc))):
        registration_pages.append(i)
        if i == 0:
            extract_images(doc[i], student_name)

    for i in range(3, len(doc)):
        page = doc[i]
        text = extract_text_from_page(page)
        category = classify_page(text)

        if category == "aadhaar":
            aadhaar_pages.append(i)
        elif category == "caste":
            caste_pages.append(i)
        elif category == "marksheet":
            marksheet_pages.append(i)

    save_grouped_pdf(doc, registration_pages,
        os.path.join(OUTPUT_BASE, FOLDERS["registration"], f"{student_name}_registration.pdf"))

    aadhaar_found = save_grouped_pdf(doc, aadhaar_pages,
        os.path.join(OUTPUT_BASE, FOLDERS["aadhaar"], f"{student_name}_aadhaar.pdf"))

    save_grouped_pdf(doc, caste_pages,
        os.path.join(OUTPUT_BASE, FOLDERS["caste"], f"{student_name}_caste.pdf"))

    save_grouped_pdf(doc, marksheet_pages,
        os.path.join(OUTPUT_BASE, FOLDERS["marksheet"], f"{student_name}_marksheet.pdf"))

    if not aadhaar_found:
        print(f"Aadhaar not detected for {student_name}, sending to manual review")
        save_manual_pages(doc, student_name)

    doc.close()

def main():
    if shutil.which("tesseract") is None:
        raise Exception("Install Tesseract: brew install tesseract")

    create_folders()

    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".pdf"):
            print(f"Processing: {file}")
            process_pdf(os.path.join(INPUT_FOLDER, file))

    print("Done!")

if __name__ == "__main__":
    main()
