from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, re

app = FastAPI(title="Ingram Brochure Proxy")

# Allow calls from Excel Online or anywhere
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
    Given a SKU, fetch the Ingram Micro NZ search page and extract brochure PDF links.
    Example: /ingram?sku=9X481UT
    """
    url = f"https://nz.ingrammicro.com/Site/Search#keywords%3A{sku}"
    try:
        r = requests.get(url, timeout=10)
        html = r.text

        # Find any Manufacturer-Brochure PDF URLs
        pdfs = re.findall(
            r"https:\/\/inquirecontent2\.ingrammicro\.com\/Manufacturer-Brochure\/[0-9A-Za-z_-]+\.pdf",
            html
        )

        if pdfs:
            return {"sku": sku, "count": len(pdfs), "brochures": pdfs}
        else:
            return {"sku": sku, "count": 0, "brochures": []}

    except Exception as e:
        return {"error": str(e), "sku": sku}
