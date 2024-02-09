import requests
import time
from bs4 import BeautifulSoup

telegram_bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
telegram_bot_username = 'YOUR_TELEGRAM_BOT_USERNAME'

# Define your URL
url = 'https://www.example.com'

response = requests.get(url)
content2 = response.content

def scrape_data(html_code):
    soup = BeautifulSoup(html_code, "lxml")
    books = []
    items = soup.find_all("div", class_="product")
    for item in items:
        # Extracting Image URL
        image_url = item.find("img")["src"] if item.find("img") else "Image URL not found"
        # Extracting Author
        author_tag = item.find("h5")
        author = author_tag.text.strip() if author_tag else "Author not found"
        # Extracting Category
        category_tag = item.find("h6")
        category = category_tag.text.strip() if category_tag else "Category not found"
        # Extracting Price
        price_tag = item.find("h5", style="color:red; padding-top:5px;")
        price = price_tag.text.strip() if price_tag else "Price not found"
        books.append({
            "Image URL": image_url,
            "Author": author,
            "Category": category,
            "Price": price
        })
    return books

def send_message_to_telegram(message):
    send_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        "chat_id": telegram_bot_username,  # Use bot's username instead of chat_id
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(send_message_url, data=data)
    if response.status_code != 200:
        print("Failed to send message to Telegram bot.")

books_data = scrape_data(content2)
for book in books_data:
    caption = f"<b>Author:</b> {book['Author']}\n"
    caption += f"<b>Category:</b> {book['Category']}\n"
    caption += f"<b>Price:</b> {book['Price']}\n"
    caption += f"<b>Image URL:</b> {book['Image URL']}"
    send_message_to_telegram(caption)
    time.sleep(60)
