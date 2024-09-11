import requests
import os
import datetime

# Stock API
stock_key = os.environ.get("stock_api")
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSE&interval=5min&apikey={stock_key}'

stock_data = requests.get(url)
stock_data.raise_for_status()
stock_data = stock_data.json()["Time Series (Daily)"]

last_two_days = dict(list(stock_data.items())[:2])
close_list = []

for day in last_two_days.values():
    close_value = day["4. close"]
    close_list.append(float(close_value))

today_price = close_list[0]
previous_price = close_list[1]
percent_diff = (today_price - previous_price) / ((today_price + previous_price) / 2) * 100
percent_diff = round(abs(percent_diff), 2)

print(f"Todays closing price: {today_price}\nYesterdays closing price: {previous_price}")

if today_price > previous_price:
    print(f"Price increased by {percent_diff}%")
else: 
    print(f"Price decreased by {percent_diff}%")


# News API
news_key = os.environ.get("api_key")
todays_date = datetime.date.today() - datetime.timedelta(days=2)
url = f"https://newsapi.org/v2/everything?q=bandai-namco&searchIn=description&language=en&pageSize=1&from={todays_date}&to={todays_date}&sortBy=popularity&apiKey={news_key}"

response = requests.get(url)
response.raise_for_status()
content = response.json()["articles"][0]

for k,v in content.items():
    print(f"{str.upper(k)}: {v}")



