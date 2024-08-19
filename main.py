import requests
import os

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("api_key")
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSE&interval=5min&apikey={api_key}'
r = requests.get(url)

data = r.json()["Time Series (Daily)"]
last_two_days = dict(list(data.items())[:2])


for day in last_two_days.values():
    close_value = day["4. close"]
    print(close_value)