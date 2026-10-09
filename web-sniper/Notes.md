
# Asynchronous Web Spider

A lightweight, concurrent Python web crawler built from scratch to recursively traverse web pages, enforce domain boundaries, and prevent duplicate requests.

## Features

- Asynchronous HTTP fetching with `aiohttp` and `asyncio`
- Non-blocking HTML DOM parsing using BeautifulSoup
- Dynamic relative-to-absolute URL resolution (`urljoin`)
- Domain isolation to prevent off-site traversal
- Constant-time $O(1)$ cycle detection using `set` tracking
- Configurable crawling depth limit (`max_depth`)

## Built With

- Python 3
- `asyncio`
- `aiohttp`
- `beautifulsoup4`
- `urllib.parse`

## What I Learned

While building this project, I practiced:

- Designing asynchronous event loops and coroutines with `async/await`
- Managing connection pools using `aiohttp.ClientSession`
- Preserving instance state across async tasks using `self`
- Parsing DOM structures and extracting specific tag attributes
- Normalizing relative URL paths against base endpoints
- Isolating domain hostnames using `netloc`
- Using sets for efficient duplicate checking
- Controlling recursive graph traversal with depth counters

## Bugs, Errors & Corrections

During development, several issues were encountered and resolved:

### 1. Incorrect BeautifulSoup Tag Search
- **Problem:** Wrote `soup.find_all("a, href=True")` placing keyword parameters inside quotes.
- **Error:** Caused BeautifulSoup to search for literal string tags instead of attribute filters, returning no links.
- **Correction:** Updated to `soup.find_all("a", href=True)` passing `href=True` as a proper keyword argument.

### 2. Missing Parent Context in Relative Links
- **Problem:** Extracted relative URLs like `catalogue/page-1.html` without attaching base domain context.
- **Error:** Passing relative strings directly to `fetch()` caused network connection failures.
- **Correction:** Applied `urllib.parse.urljoin(current_url, raw_link)` to resolve relative paths into valid absolute URLs.

### 3. Missing Argument in Recursive Function Call
- **Problem:** Called `self.extract_links(html_url)` inside `crawl()` without supplying the base URL parameter.
- **Error:** Raised `TypeError: extract_links() missing 1 required positional argument: 'current_url'`.
- **Correction:** Updated call to `self.extract_links(html_url, crawl_url)`.

### 4. Unrestricted Off-Site Crawling
- **Problem:** `extract_links()` appended all valid `href` destinations without host filtering.
- **Error:** Spider traversed external links leading off-site to social media pages.
- **Correction:** Added domain validation `if urllib.parse.urlparse(absolute_url).netloc == self.domain:` to keep execution bound to the target domain.

## How to Run

1. Make sure Python 3 and dependencies are installed:

```bash
pip install aiohttp beautifulsoup4

```

2. Clone this repository.
3. Open the project folder in your terminal.
4. Run:

```bash
python spider.py

```

## Future Improvements

Possible improvements include:

* Extracting specific page data (titles, prices, metadata)
* Saving output directly to JSON or CSV files
* Respecting `robots.txt` rules before fetching
* Adding custom user-agent rotation and rate-limiting delays
* Implementing parallel worker queues (`asyncio.Queue`)

## Project Status

Completed, with possible future improvements.

```

```