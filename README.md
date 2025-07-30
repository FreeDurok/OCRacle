# **OCRacle**

<p align="center">
    <img src=".img/OCRacle_Logo.png" alt="OCRacle Logo" width="300"/>
</p>

OCRacle is a modular Python tool (optionally portable) that recursively scans directories, extracts text from PDF and image files (native PDF text and OCR), and searches for keywords or regex patterns. Results can be printed on the console and optionally saved to JSON or CSV.
It is also useful as a service component for Data Loss Prevention (DLP) software.

## **Main Features**

* Recursive scan of directories and subdirectories
* Supported file types:
  * **PDF** (native text extraction via PyMuPDF, fallback to OCR)
  * **Images** (JPG, PNG, TIFF, etc.)
* Multiple keyword/regex rules
* Output:
  * Console
  * JSON
  * CSV

---

## **Dependencies**

Python **3.9+** is recommended.

Required libraries:

```
pytesseract
pdf2image
PyMuPDF
Pillow
```

OCRacle includes a portable, pre-configured **Tesseract OCR** binary and tessdata in the `core` directory, no extra setup needed.

For PDF OCR, **Poppler** (or Ghostscript) is still required for `pdf2image`. This can also be made portable as shown below.

---

## **Portable / Offline Setup (Air‑Gapped)**

To deploy OCRacle in an isolated environment without internet:

### **On an online machine**

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Freeze dependencies:

   ```bash
   pip freeze > requirements.txt
   ```

4. Download all packages as `.whl` files:

   ```bash
   mkdir wheels
   pip download -r requirements.txt -d wheels
   ```

Copy the **entire OCRacle folder (including wheels/, requirements.txt, and code)** to the offline machine.

---

### **On the offline machine**

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install packages from the local wheels:

   ```bash
   pip install --no-index --find-links=wheels -r requirements.txt
   ```

3. Ensure that **Tesseract** (binary + tessdata folder) and, if required, **Poppler** are included in the project directory and configured in `core/text_extractor.py`.

4. Run:

   ```bash
   python main.py /path/to/folder
   ```

---

## **Usage**

Console only:

```bash
python main.py /path/to/folder
```

Save results:

```bash
python main.py /path/to/folder --json results.json --csv results.csv
```

---

## **Configuration**

Edit `config.py`:

* `ESTENSIONS` → file extensions to scan
* `RULES` → regex patterns to search

---

## **Output**

Example console output:

```
[INFO] Processing file: /docs/invoice1.pdf
[MATCH] Rule=iban File=/docs/invoice1.pdf
```

Example JSON:

```json
[
  {"rule": "iban", "file": "/docs/invoice1.pdf"},
  {"rule": "secret_word", "file": "/images/photo.png"}
]
```

