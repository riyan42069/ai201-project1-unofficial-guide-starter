import pdfplumber

import pdfplumber
pdf = pdfplumber.open("foundations_of_cybersecurity.pdf")
text = "\n\n".join(p.extract_text() for p in pdf.pages if p.extract_text())