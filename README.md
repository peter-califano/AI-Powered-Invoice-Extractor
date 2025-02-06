# **Invoice Data Extraction Pipeline**

## **Overview**
This project automates the extraction of key data from scanned invoices using **computer vision and AI-powered document processing**. The system follows a structured pipeline that:
1. Converts scanned **PDF invoices** into images.
2. Uploads those images to **Imgur** and stores the image URLs.
3. Uses **ChatGPT (GPT-4 Vision)** to extract invoice details based on structured rules.
4. Saves extracted data as **JSON files** and consolidates them into an **Excel sheet** for validation.

## **Project Workflow**
The pipeline consists of four main steps, each handled by a separate Python script.

### **1️⃣ Convert PDFs to Images + Upload Images to Imgur(`pdf2image-imgur-upload.py`)**
- Uses the `pdf2image` library to convert multi-page invoices into individual image files.
- Outputs: PNG images for each invoice page.
- Uses the **Imgur API** to upload the converted images.
- Outputs: A **JSON cache file** (`imgur_uploads.json`) mapping invoice images to their respective **Imgur URLs**.

### **2️⃣ Extract Invoice Data Using ChatGPT (`openai_invoice_processing.py`)**
- Uses **GPT-4 Vision** to analyze invoice images and extract key details, including:
  - **Usage period** (start and end dates)
  - **Energy type** (Electricity, Natural Gas, etc.)
  - **Energy volume** (in kWh, CCF, MMBtu, etc.)
  - **Cost amount** (excluding taxes and fees)
  - **Currency**
- Runs multiple attempts (4 times per invoice) for validation.
- Saves structured **JSON outputs** in `JSON_Output_vision_validation` folder.
- Outputs: JSON files containing extracted invoice data.

### **3️⃣ Convert JSON Data to Excel (`json_to_csv.py`)**
- Reads the **multiple JSON outputs** from ChatGPT.
- Compares extracted data from different attempts to check for inconsistencies.
- Saves two output files:
  1. **`validation_invoice_comparison.csv`** – Detailed comparison of multiple AI extraction attempts.
  2. **`validation_merged_invoices.xlsx`** – Final consolidated invoice data, with inconsistencies highlighted in **red**.
- Outputs: A structured **Excel file** for manual review.

---

## **How to Run the Pipeline**
The entire pipeline can be executed **sequentially** using `run_invoice_pipeline.py`.

### **Running the Pipeline**
1. Ensure you have **Python 3.8+** installed.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the full pipeline:
   ```bash
   python run_invoice_pipeline.py
   ```

This script will:
- Convert PDFs into images.
- Upload images to Imgur.
- Extract invoice data using ChatGPT.
- Save the final results as JSON and Excel files.

### **Running Individual Steps**
If needed, each script can be run independently:

- Convert PDFs to images & upload to Imgur:
  ```bash
  python pdf2image-imgur-upload.py
  ```
- Extract invoice details using ChatGPT:
  ```bash
  python openai_invoice_processing.py
  ```
- Convert extracted JSON data to CSV & Excel:
  ```bash
  python json_to_csv.py
  ```

---

## **File Structure**
```
📂 Invoice Extraction Project
│── pdf2image-imgur-upload.py       # Convert PDFs to images & upload to Imgur
│── openai_invoice_processing.py    # Extract invoice data using GPT-4 Vision
│── json_to_csv.py                  # Convert extracted JSON to CSV & Excel
│── run_invoice_pipeline.py         # Automate the full pipeline
│── imgur_uploads.json              # Cached Imgur URLs
│── requirements.txt                 # Required dependencies
│── validation_invoice_comparison.csv  # Comparison of AI attempts
│── validation_merged_invoices.xlsx   # Final invoice dataset with flagged inconsistencies
│── 📂 JSON_Output_vision_validation   # Folder for AI-generated JSON outputs
│── 📂 Temp_Images                    # Folder for temporary invoice images
│── 📂 Invoices                        # Folder for input PDF invoices
```

