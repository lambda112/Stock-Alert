import requests
import os
import datetime
import smtplib
from email.mime.text import MIMEText

# STOCK DATA
stock_key = os.environ.get("stock_api")
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSE&interval=5min&apikey={stock_key}'

# get data
stock_data = requests.get(url)
stock_data.raise_for_status()
stock_data = stock_data.json()["Time Series (Daily)"]

# get data for last two days only
last_two_days = dict(list(stock_data.items())[:2])
close_list = []

# get data for close value
for day in last_two_days.values():
    close_value = day["4. close"]
    close_list.append(float(close_value))

# find percent diff
today_price = close_list[0]
previous_price = close_list[1]
percent_diff = (today_price - previous_price) / ((today_price + previous_price) / 2) * 100
percent_diff = round(abs(percent_diff), 2)

# check if difference is 10% or larger
if percent_diff >= 5:
    with open("data.txt", "w") as f:

        # check decrease or increase
        f.write("STOCK DATA-----------------------------\n")
        f.write(f"Todays closing price: {today_price}\nYesterdays closing price: {previous_price}\n")
        
        if today_price > previous_price:
            f.write(f"Price increased by {percent_diff}%\n\n")
        else: 
            f.write(f"Price decreased by {percent_diff}%\n\n")

        # NEWS API
        news_key = os.environ.get("api_key")
        todays_date = datetime.date.today() - datetime.timedelta(days=2)
        url = f"https://newsapi.org/v2/everything?q=bandai-namco&searchIn=description&language=en&pageSize=1&from={todays_date}&to={todays_date}&sortBy=popularity&apiKey={news_key}"

        # get news data
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()["articles"][0]

        # print in suitable format
        f.write("NEWS DATA-----------------------------\n")
        for k,v in content.items():
            f.write(f"{str.upper(k)}: {v}\n")

    # read file and get text
    with open("data.txt", "r") as read_file:
        text = read_file.read()
        print(text)

    # setup email
    msg = MIMEText(text)
    msg['Subject'] = 'Stock Information'
    msg['From'] = "lambdaa112@gmail.com"
    msg['To'] = 'kamazim121212@gmail.com'

    # send email
    password = os.environ("password")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user = "lambdaa112@gmail.com", password = password)
        connection.send_message(msg = msg)


    

