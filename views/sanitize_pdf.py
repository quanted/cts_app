import json
import re
import base64
from typing import Dict, Any, Union, Optional
from bs4 import BeautifulSoup
import re
import html



def sanitize_table_html(html_content: str) -> str:
    """
    Sanitizes HTML table content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    cells = soup.find_all(['td', 'th'])
    for cell in cells:
        original_text = cell.get_text()
        sanitized_text = _sanitize_text(original_text)
        cell.clear()
        cell.string = sanitized_text
    return str(soup)


def _sanitize_text(text: str) -> str:
    """
    Sanitizes text to ensure it's a safe string.
    """
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r'[<>]', '', text)
    text = re.sub(r'[&]', 'and', text)
    text = re.sub(r'["\']', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'[^\w\s\.\-\(\)\+\=\,\/\:]', '', text)
    return text
