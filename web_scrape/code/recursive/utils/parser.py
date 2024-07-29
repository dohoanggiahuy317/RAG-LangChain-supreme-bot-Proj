from bs4 import BeautifulSoup
import re

def extract_title_and_text_from_html(html_content):
    """
    Extract the title and cleaned text content from an HTML document.

    Args:
    html_content (str): The HTML content as a string.

    Returns:
    tuple: A tuple containing the title (str) and cleaned text (str).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title_tag = soup.title
    title = title_tag.string if title_tag else "No Title"
    
    # Extract text content and clean it
    text_content = soup.get_text(separator='.')
    cleaned_text = re.sub(r'\.{2,}', '.', text_content).strip()  # Replace multiple dots with a single dot
    
    return (title, cleaned_text)
