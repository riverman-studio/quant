import requests
import yfinance as yf
from bs4 import BeautifulSoup
from pprint import *
import mtranslate as mt
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 


def translate_text(text, target_language='en'):
    translated_text = mt.translate(text, target_language)
    return translated_text.lower()

device = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def get_yahopo_ticker(stock_symbol):
    stock_info = yf.Ticker(stock_symbol + ".PA")
    return stock_info

def estimate_sentiment(news):
    if news:
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]


def scrape_boursorama_finance_news(stock_symbol, yticker):
    # Construct the URL
    url = f"https://www.boursorama.com/cours/actualites/1rP{stock_symbol}/"
    companyName = yticker.info["shortName"].lower()
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all news articles
        articles = soup.find_all('li', {'class': 'c-list-details-news__line / o-flag'})

      
        # Extract news headlines and summaries
        news_list = []
        for article in articles:
            # headline = article.find('h3', {'class': 'c-faceplate__actualite__title'}).text.strip()
            # summary = article.find('p', {'class': 'c-faceplate__actualite__excerpt'}).text.strip()
            headline = article.find('div', {'class': 'c-list-details-news__title'}).text.strip()
            headlineEn = translate_text(headline)

            if( companyName not in headlineEn):
                continue

            summary = article.find('p', {'class': 'u-nomargin c-list-details-news__content'}).text.strip()
            summaryEn = translate_text(summary)

            if( companyName not in summaryEn):
                continue            

            tensor, sentiment = estimate_sentiment([summaryEn])

            news_list.append({'headline': headlineEn, 'sentiment': sentiment, 'summary': summaryEn})
        
        return news_list
    
    else:
        return "Failed to fetch data"

# Example usage

stock_symbol = "RNO"  # Change this to the desired stock symbol
yticker = get_yahopo_ticker(stock_symbol)
stock_news = scrape_boursorama_finance_news(stock_symbol, yticker)
for idx, news in enumerate(stock_news, start=1):
    print(f"News {idx}:")
    print(f"Headline: {news['headline']} [{news['sentiment']}]")
    print(f"Summary: {news['summary']}")
    print()
