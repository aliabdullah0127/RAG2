import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import os

BASE_URL = "https://www.primuspartners.in/"

# Step 1: Get homepage
response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Find all navbar links
navbar_links = []
for link in soup.select("nav a"):
    href = link.get("href")
    if href and href != "#" and (href.startswith("http") or href.startswith("/")):
        full_url = urljoin(BASE_URL, href)
        navbar_links.append(full_url)

navbar_links = list(set(navbar_links))
print("Found navbar links:", navbar_links)

# Step 3: Create PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Add title page
pdf.add_page()
pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, "Primus Partners Website Content", ln=True, align="C")
pdf.ln(10)

# Step 4: Scrape each section
for idx, url in enumerate(navbar_links, start=1):
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        page_soup = BeautifulSoup(resp.text, "html.parser")

        # Add section title
        
        title_tag = page_soup.find('title')
        page_title = title_tag.get_text(strip=True) if title_tag else url
        pdf.set_font("Helvetica", "B", 14)
        pdf.multi_cell(0, 8, f"Section {idx}: {page_title}")
        pdf.ln(2)

        # Extract text from <p> and <h1>-<h4>
        pdf.set_font("Helvetica", "", 12)
        for tag in page_soup.find_all(['h1','h2','h3','h4','p']):
            text = tag.get_text(strip=True)
            if text:
                pdf.multi_cell(0, 6, text)
                pdf.ln(1)
    except Exception as e:
        print("An error occurred:", e)
try:
    pdf_file = "primuspartners.pdf"
    # your code that might raise an error
except Exception as e:
    print("An error occurred:", e)


      
# Step 5: Save PDF
pdf_file = "primuspartners.pdf"
pdf.output(pdf_file)
print(f"PDF saved as {pdf_file} in folder: {os.getcwd()}")
