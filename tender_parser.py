import pdfplumber
import re

def parse_tender_pdf(file_path):
    emd = None
    deadline = None
    scope = ""

    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Extract EMD
    emd_match = re.search(r'EMD.*?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', text, re.IGNORECASE)
    if emd_match:
        emd = float(emd_match.group(1).replace(",", ""))

    # Extract Deadline
    date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    if date_match:
        from datetime import datetime
        deadline = datetime.strptime(date_match.group(1), "%d/%m/%Y")

    # Extract Scope (very basic logic)
    scope_index = text.lower().find("scope of work")
    if scope_index != -1:
        scope = text[scope_index:scope_index+500]  # Take nearby text

    return emd, deadline, scope
