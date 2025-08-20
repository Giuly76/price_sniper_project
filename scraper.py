import requests
from bs4 import BeautifulSoup

siti = [
    {
        "nome": "Unieuro",
        "url": "https://www.unieuro.it/online/informatica/Notebook-e-Ultrabook-c128",
        "dominio": "https://www.unieuro.it",
        "contenitore": ("div", "product-grid-item"),
        "titolo": ("a", "product-title"),
        "prezzo": ("span", "price"),
        "link_attr": "href"
    },
    {
        "nome": "Amazon",
        "url": "https://www.amazon.it/s?k=notebook",
        "dominio": "https://www.amazon.it",
        "contenitore": ("div", "s-result-item"),
        "titolo": ("span", "a-text-normal"),
        "prezzo": ("span", "a-offscreen"),
        "link_attr": "href"
    }
]

SOGLIA_PREZZO = 100

def get_suspicious_prices():
    risultati = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    for sito in siti:
        try:
            r = requests.get(sito['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all(sito['contenitore'][0], class_=sito['contenitore'][1])
            for item in items:
                titolo_tag = item.find(sito['titolo'][0], class_=sito['titolo'][1])
                prezzo_tag = item.find(sito['prezzo'][0], class_=sito['prezzo'][1])
                if not titolo_tag or not prezzo_tag:
                    continue
                nome = titolo_tag.get_text(strip=True)
                prezzo_text = prezzo_tag.get_text(strip=True)
                prezzo_clean = prezzo_text.replace("€", "").replace(".", "").replace(",", ".").strip()
                try:
                    prezzo = float(prezzo_clean)
                except:
                    continue
                if prezzo < SOGLIA_PREZZO:
                    risultati.append({
                        "Sito": sito['nome'],
                        "Nome": nome,
                        "Prezzo (€)": prezzo,
                        "Link": sito['dominio']
                    })
        except Exception:
            continue
    return risultati
