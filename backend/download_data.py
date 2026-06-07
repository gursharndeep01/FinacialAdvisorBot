import os
import urllib.request

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/")

PDFS = {
    "amfi_guide.pdf": "https://www.amfiindia.com/Themes/Theme1/downloads/MF-Handbook.pdf",
}

def download_pdfs():
    os.makedirs(DATA_PATH, exist_ok=True)
    for filename, url in PDFS.items():
        path = os.path.join(DATA_PATH, filename)
        if not os.path.exists(path):
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, path)
            print(f"Downloaded {filename}")