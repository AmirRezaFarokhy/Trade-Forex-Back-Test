import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import os

TICKER_NAME = "XAUUSD"

class SaveBackTest:

	def chandlesPlot(self, d, o, h, l, c):
		plt.figure(figsize=(24, 14))
		color = []
		for open_p, close_p in zip(o, c):
			if open_p<close_p:
				color.append("g")
			else:
				color.append("r")

		plt.bar(d, height=np.abs(o-c), 
				width=0.8, 
				color=color, 
				bottom=np.min((o, c), axis=0))
		plt.bar(d, height=h-l, width=0.3, color=color, bottom=l)

	def VisulasationThreeSave(self, df):

		def chandlesPlots(d, o, h, l, c):
			color = []
			for open_p, close_p in zip(o, c):
				if open_p<close_p:
					color.append("g")
				else:
					color.append("r")

			ax0.bar(d, height=np.abs(o-c), 
					width=0.8, 
					color=color, 
					bottom=np.min((o, c), axis=0))
			ax0.bar(d, height=h-l, width=0.3, color=color, bottom=l)	
		fig, (ax0, ax1) = plt.subplots(2, 1, 
									gridspec_kw={'height_ratios': [3, 1]}, 
									figsize=(24, 14))

		chandlesPlots(df.index, df["open"], 
					df["high"], df["low"], 
					df["close"])
		ax0.plot(df["Upper_trendline"], label="Upper Trend Line")
		ax0.plot(df["Lower_trendline"], label="Lower Trend Line")
		ax0.set_title(TICKER_NAME)
		ax0.set_xlabel("Index")
		ax0.set_ylabel("Price")
		ax0.legend(loc="lower left") 
		ax1.plot(df.index, df["RSI"], label="RSI value")
		down = [30.0 for i in range(len(df))]
		up = [70.0 for i in range(len(df))]
		ax1.plot(df.index, down, linestyle="--", c="black")
		ax1.plot(df.index, up, linestyle="--", c="black")
		ax1.set_title(f"{TICKER_NAME} RSI")
		ax1.set_xlabel("Index")
		ax1.set_ylabel("RSI")
		ax1.legend(loc="lower left") 
		fig.tight_layout()
		if os.path.exists('img'):
			fig.savefig(f"img/{episode}.jpg")
		else:
			os.mkdir("img")
			fig.savefig(f"img/{episode}.jpg")
			


	def VisulasationTowSave(self, df, episode): 
		self.chandlesPlot(df.index, df["open"], 
					df["high"], df["low"], 
					df["close"])
		plt.scatter(df.index, df["Buy"] , color="g", linewidths=15, label="Buy")
		plt.scatter(df.index, df["Sell"] , color="r", linewidths=15, label="Sell")
		plt.title(TICKER_NAME)
		plt.xlabel("Index")
		plt.ylabel("Price")
		plt.legend(loc="lower left")  
		if os.path.exists('img'):
			plt.savefig(f"img/{episode}.jpg")
			plt.close()
		else:
			os.mkdir("img")
			plt.savefig(f"img/{episode}.jpg")
			plt.close()


	def VisulasationOneSave(self, df, episode):
		self.chandlesPlot(df.index, df["open"], 
					df["high"], df["low"], 
					df["close"])
		plt.scatter(df.index, df["Buy"] , color="g", linewidths=15, label="Buy")
		plt.scatter(df.index, df["Sell"] , color="r", linewidths=15, label="Sell")
		plt.plot(df.index, df["sl"], label="Stopp_Loss")
		plt.title(TICKER_NAME)
		plt.xlabel("Index")
		plt.ylabel("Price")
		plt.legend(loc="lower left")  
		if os.path.exists('img'):
			plt.savefig(f"img/{episode}.jpg")
			plt.close()
		else:
			os.mkdir("img")
			plt.savefig(f"img/{episode}.jpg")
			plt.close()


	def VisulasationForTargetPoint(self, df, episode):
		self.chandlesPlot(df.index, df["open"], 
			df["high"], df["low"], 
			df["close"])
		plt.scatter(df.index, df["Buy"] , color="g", linewidths=15, label="Buy")
		plt.scatter(df.index, df["Sell"] , color="r", linewidths=15, label="Sell")
		plt.plot(df.index, df["tp"], label="Trget_Point")
		plt.title(TICKER_NAME)
		plt.xlabel("Index")
		plt.ylabel("Price")
		plt.legend(loc="lower left")  
		if os.path.exists('img'):
			plt.savefig(f"img/{episode}.jpg")
			plt.close()
		else:
			os.path.mkdir("img")
			plt.savefig(f"img/{episode}.jpg")
			plt.close()


	def VisulasationForMA(self, df, episode, moving_averages_ma):
		self.chandlesPlot(df.index, df["open"], 
			df["high"], df["low"], 
			df["close"])
		#plt.scatter(df.index, df["Buy"] , color="g", linewidths=15, label="Buy")
		#plt.scatter(df.index, df["Sell"] , color="r", linewidths=15, label="Sell")
		#plt.plot(df.index, df[f"MA{moving_averages_ma}"], label="MATarget")
		plt.title(TICKER_NAME)
		plt.xlabel("Index")
		plt.ylabel("Price")
		plt.legend(loc="lower left")  
		if os.path.exists('img'):
			plt.savefig(f"img/{episode}.jpg")
			plt.close()
		else:
			os.mkdir("img")
			plt.savefig(f"img/{episode}.jpg")
			plt.close()
