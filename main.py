import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def fetch_match_data(url: str):
    """AiScore benzeri canlı maç sayfasından veri çek"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await asyncio.sleep(2)
        html = await page.content()
        await browser.close()
        return html

def parse_stats(html: str):
    """Sayfadaki temel istatistikleri ayrıştır"""
    soup = BeautifulSoup(html, "html.parser")
    stats = {"atak": 0, "tehlikeli_atak": 0, "isabetli_sut": 0}
    
    # Sayfa yapısına göre bu kısım düzenlenebilir
    # Örnek veri çekme
    text = soup.get_text().lower()
    stats["atak"] = text.count("atak")
    stats["tehlikeli_atak"] = text.count("tehlikeli")
    stats["isabetli_sut"] = text.count("şut")

    return stats

def predict_goal_chance(stats):
    """Basit tahmin modeli"""
    score = stats["tehlikeli_atak"] * 0.5 + stats["isabetli_sut"] * 1.2
    if score > 20:
        return "Gol olasılığı yüksek (Üst)"
    elif score > 10:
        return "Gol olabilir (Orta)"
    else:
        return "Gol düşük (Alt)"

async def main():
    url = input("Maç linkini gir (örnek: https://m.aiscore.com/tr/match/...): ")
    html = await fetch_match_data(url)
    stats = parse_stats(html)
    tahmin = predict_goal_chance(stats)
    print("\n📊 İstatistikler:", stats)
    print("🔮 Tahmin:", tahmin)

if __name__ == "__main__":
    asyncio.run(main())
