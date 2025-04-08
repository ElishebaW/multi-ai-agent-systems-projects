from langchain.tools import BaseTool
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
from pydantic import Field


class WebScraperTool(BaseTool):
    name: str = "Web Scraper"
    description: str = (
        "Scrapes data from coding websites about MAANG interview preparation"
    )
    default_urls: List[str] = Field(
        default=[
            "https://neetcode.io/",
            "https://leetcode.com/",
            "https://codesignal.com/",
            "https://hackerrank.com/",
            "https://hellointerview.com/",
        ]
    )

    def _run(self, url: Optional[str] = "") -> Dict[str, str]:
        # If no specific URL is provided, scrape all default URLs
        urls_to_scrape = self.default_urls if not url else [url]
        scraped_data = {}

        for url in urls_to_scrape:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                scraped_data[url] = soup.title.string  # Example: Extract page title
            except Exception as e:
                scraped_data[url] = f"Error: {str(e)}"

        return scraped_data

    def _arun(self, url: Optional[str] = "") -> Dict[str, str]:
        """Async implementation of the tool"""
        raise NotImplementedError("Async not implemented")
