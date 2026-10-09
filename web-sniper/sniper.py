import urllib.parse  # Tool for parsing URLs and joining relative links
from bs4 import BeautifulSoup  # Tool for parsing HTML and extracting tags
import asyncio  # Library for managing asynchronous execution/event loops
import aiohttp  # Library for making asynchronous HTTP network requests


class WebSpider:
    def __init__(self, start_url: str, max_depth: int = 2):
        # The initial web address where crawling begins
        self.start_url = start_url

        # How many link clicks deep the spider is allowed to go
        self.max_depth = max_depth

        # Extract only the hostname (e.g., "books.toscrape.com") to keep spider on target domain
        self.domain = urllib.parse.urlparse(start_url).netloc

        # Set to track visited URLs and prevent infinite loops/duplicate requests
        self.visited = set()

    # METHOD 1: Fetch raw HTML content from a target URL asynchronously
    async def fetch(self, session, url):
        try:
            # Asynchronously open an HTTP GET request to the URL
            async with session.get(url) as response:
                # HTTP 200 means the server successfully returned the page
                if response.status == 200:
                    # Download and return the raw HTML string
                    return await response.text()
        except Exception as e:
            # Catch network errors (timeouts, 404s, SSL failures) without crashing
            print(f"Error Fetching {url}: {e}")

        # Return None if the fetch failed or status wasn't 200
        return None

    # METHOD 2: Parse HTML text and extract all internal links
    def extract_links(self, html, current_url):
        # Parse raw HTML text into a searchable DOM tree
        soup = BeautifulSoup(html, "html.parser")
        links = []

        # Find all <a> tags that contain an 'href' link attribute
        for anchor in soup.find_all("a", href=True):
            # Extract raw link string (could be relative like 'page.html')
            raw_link = anchor["href"]

            # Convert relative links into absolute URLs using the current page address
            absolute_url = urllib.parse.urljoin(current_url, raw_link)

            # Ensure the link stays on our target domain (skip external sites like twitter.com)
            if urllib.parse.urlparse(absolute_url).netloc == self.domain:
                links.append(absolute_url)

        return links

    # METHOD 3: Main recursive crawling loop
    async def crawl(self, session, crawl_url, depth_url):
        # Stop crawling if depth limit reached OR URL already visited
        if depth_url > self.max_depth or crawl_url in self.visited:
            return

        # Record this URL in our visited notebook immediately
        self.visited.add(crawl_url)
        print(f"[Depth {depth_url}] Crawling: {crawl_url}")

        # Fetch HTML content for the current URL
        html_url = await self.fetch(session, crawl_url)

        # Skip link extraction if page failed to load
        if not html_url:
            return

        # Extract all valid internal links on this page
        links_list = self.extract_links(html_url, crawl_url)

        # Recursively visit each extracted link at the next depth level
        for single_link in links_list:
            if single_link not in self.visited:
                await self.crawl(session, single_link, depth_url + 1)


# MAIN EXECUTION BLOCK: Setting up the async event loop
async def main():
    # Instantiate the spider with start URL and maximum crawling depth
    spider = WebSpider(start_url="https://books.toscrape.com/", max_depth=2)

    # Open a shared asynchronous HTTP connection pool
    async with aiohttp.ClientSession() as session:
        print(f"--- Starting Spider on {spider.start_url} ---\n")

        # Start the recursive crawl at Depth 0
        await spider.crawl(session, spider.start_url, depth_url=0)

        # Print summary of total unique pages visited
        print(f"\n---Done! Total pages visited: {len(spider.visited)}")


# Script entry point: runs main() inside the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())