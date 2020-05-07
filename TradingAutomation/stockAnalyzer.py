import os
import smtplib
import imghdr
from email.message import EmailMessage

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators 
#import sys
import random
import time as t

keys = open("keys.txt").read().splitlines()

msg = EmailMessage()
email_address = "[YOUR_EMAIL]"
email_password = "[YOUR_PASSWORD]"
msg["From"] = email_address
msg["To"] = "[RECEIVERS_EMAIL]"
msg["Subject"] = "STOCK ALERT"

tickers = open("tickers.txt").read().splitlines()

key = random.choice(keys)
for ticker in tickers:
	try:
		time = TimeSeries(key=key, output_format="pandas")
		data_ts, meta_data_ts = time.get_intraday(symbol=ticker, interval="60min", outputsize="full")

		techindicator = TechIndicators(key=key, output_format="pandas")
		data_rsi, meta_data_rsi = techindicator.get_rsi(symbol=ticker, interval="60min", time_period=14, series_type="close")
		data_macd, meta_data_macd = techindicator.get_macd(symbol=ticker, interval="60min", series_type="close", signalperiod=26)

		data_ts = data_ts.sort_index(axis=1, ascending=True)
		data_ts = data_ts.iloc[::-1]

		data_macd = data_macd.sort_index(axis=1, ascending=True)
		data_macd = data_macd.iloc[::-1]

		df_price = data_ts["4. close"].iloc[50::]
		df_rsi = data_rsi.iloc[36::]
		df_macd = data_macd

		df_rsi.index = data_macd.index
		df_price.index = df_rsi.index


		total_df = pd.concat([df_price, df_rsi, df_macd], axis=1)
		total_df = total_df.rename(columns={"4. close": "CLOSE"})
		total_df = total_df["2020-05-05 15:30:00":]

		print("\nTicker: "+ticker)
		print(total_df)

		# last_rsi = 11111
		for i in total_df.index:
			watchlist = open("watchlist.txt").read().splitlines()
			if (total_df["RSI"][i]<32):
				if ticker not in watchlist:
					bp = total_df["CLOSE"][i]
					message = ticker + " has BUY potential.\nADDING to watchlist."
					msg.set_content(message)
					with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
						smtp.login(email_address, email_password)
						smtp.send_message(msg)
					print("ADD")
					with open("watchlist.txt", "a") as text_file:
						text_file.write(ticker + "\n")
			elif (total_df["RSI"][i]>40):
				if ticker in watchlist:
					sp = total_df["CLOSE"][i]
					message = ticker + " has a SELL potential. REMOVING from watchlist." 
					msg.set_content(message)
					with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
						smtp.login(email_address, email_password)
						smtp.send_message(msg)
					print("REMOVE")
					watchlist.remove(ticker)
					with open("watchlist.txt", "w") as text_file:
						for tick in watchlist:
							text_file.write(tick + "\n")

			#last_rsi = total_df["RSI"][i]

		t.sleep(60)

	# except KeyboardInterrupt:
	# 	print("\nQuitting program...")
	# 	quit()
	except:
		print("Error getting data")
		t.sleep(60)

