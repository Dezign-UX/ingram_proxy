from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, re, time

app = FastAPI(title="Ingram Brochure Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ingram")
def get_brochure(sku: str):
    """
    Given a SKU, fetch the Ingram Micro brochure URL if available.
    Example: /ingram?sku=9X481UT
    """
    url = f"https://nz.ingrammicro.com/Site/Search#keywords:{sku}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for attempt in range(2):
        try:
            r = requests.get(url, headers=headers, timeout=30)
            html = r.text
            pdfs = re.findall(r'https://inquirecontent2\.ingrammicro\.com/Manufacturer-Brochure/[A-Za-z0-9\-_.]+\.pdf', html)
            return {"sku": sku, "count": len(pdfs), "brochures": pdfs}
        except Exception as e:
            if attempt == 0:
                time.sleep(3)
                continue
            return {"sku": sku, "error": str(e), "note": "Retry failed after timeout"}

