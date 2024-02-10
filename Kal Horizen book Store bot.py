import requests
import time
from bs4 import BeautifulSoup

telegram_bot_token = '6973280612:AAEc48zeUm4VPj5O4U5C2_oYsJcPPB_XEJo'
chat_id = '5115967874'

# Define your URL
url = 'https://www.ethiobookreview.com/amharic'

send_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"

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

def send_message_to_telegram(message, chat_id):
    data = {
        "chat_id": chat_id,
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
    send_message_to_telegram(caption, chat_id)
    time.sleep(60)