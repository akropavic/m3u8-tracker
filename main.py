
import asyncio
from playwright.async_api import async_playwright

PAGES = {
    "BIRINCI SINIF": "https://selcuksports180.top/matches?id=bein-sports-1",
    "IKINCI SINIF": "https://selcuksports180.top/matches?id=bein-sports-2",
    "UCUNCU SINIF": "https://selcuksports180.top/matches?id=bein-sports-max-1",
    "DORDUNCU SINIF": "https://selcuksports180.top/matches?id=bein-sports-max-2",
}

async def main():
    results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        for name, url in PAGES.items():
            print(f"Kontrol ediliyor: {name}")
            found = []

            page = await context.new_page()

            page.on(
                "request",
                lambda request: found.append(request.url)
                if ".m3u8" in request.url.lower()
                else None
            )

            try:
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                # Ağ isteklerinin tamamlanmasını bekle
                await page.wait_for_timeout(20000)

            except Exception as e:
                print(f"Hata: {e}")

            unique = list(dict.fromkeys(found))
            results[name] = unique

            print(f"Bulunan M3U8: {len(unique)}")

            await page.close()

        await browser.close()

    with open("stream.txt", "w", encoding="utf-8") as f:
        for name, links in results.items():
            f.write(f"# {name}\n")

            if links:
                for link in links:
                    f.write(link + "\n")
            else:
                f.write("BULUNAMADI\n")

            f.write("\n")

    print("stream.txt güncellendi!")

asyncio.run(main())
