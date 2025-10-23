import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def filterLinks(filer, filew, pattern, buffer, links):

    try:
        with open(filer, "r", encoding="utf-8") as fr:
            with open(filew, "w", encoding="utf-8") as fw:
                while True:
                    char = fr.read(1)

                    if not char:
                        break

                    buffer.append(char)

                    if len(buffer) > len(pattern):
                        temp = buffer.pop(0)
                        links.append(temp)

                    if pattern == "".join(buffer):
                        fw.write("\n")
                        link = "".join(links)
                        fw.write(link)
                        links.clear()

    except:
        pass

md_generator = DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
)

config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=md_generator
)

# async def main():
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun("https://www.akgec.ac.in/", config=config)
        # with open("data.txt", "w") as f:
        #     f.write(result)
#         print("Raw Markdown length:", len(result.markdown.raw_markdown))
#         print(result.markdown.fit_markdown)
        
async def sequential_crwal(urls):
    crawler = AsyncWebCrawler()
    await crawler.start()

    try:
        session_id = "session1"  # Reuse the same session across all URLs
        for url in urls:
            result = await crawler.arun(
                url=url,
                config=config,
                session_id=session_id
            )
            if result.success:
                print(f"Successfully crawled: {url}")
                # E.g. check markdown length
                # print(f"Markdown length: {len(result.markdown.fit_markdown)}")
                with open("raw_data.txt", "a", encoding="utf-8") as f:
                    f.write(result.markdown.raw_markdown)
                    f.write("\n\n---------------------------------------------------------------------------\n\n")
                
            else:
                print(f"Failed: {url} - Error: {result.error_message}")
    finally:
        # After all URLs are done, close the crawler (and the browser)
        await crawler.close()

URLs = []
with open("akg_links.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        URLs.append(line)

# print(URLs)
asyncio.run(sequential_crwal(urls=URLs))