import pandas as pd
import numpy as np 
import time 
import matplotlib.pyplot as plt 

from Robot import TrainRobot, SetPosition 
from Visulasation import SaveBackTest
from objectes import (Indicators, 
                      SupportVSResistanced)


TYPE_STOPPLOSS = "ATR" # tow option for stopploss 1.ATR // 2.PiP 
N_BEFORE = 4
N_AFTER = 3
EPSILON_FOR_GAP = 1.15
EPSILON_FOR_ATR = 1.95
TARGETPOINT_NUM_PIPS = 60 
STOPPLOSS_NUM_PIPS = 30
LOT = 0.01 # number of volumn to buy or sell
TRADE_WITH_DEFAULT_SETTING = True # whitout using pips 1.True // 2.False
MOVING_AVERAGE_TARGETPOINT = 10
TYPES_TRADE = "MA" # MA, chandlestick
LENGHT_DROW = 400
SEARCH = -2
EPSILON_FOR_TRENDLINE = 0.2
MOVING_AVERAGE_TRENDLINE = 200
TICKER_NAME = "XAUUSD"

df = pd.read_csv("XAUUSD_M5.csv")

df.index = [i for i in range(len(df))]

visulize = SaveBackTest()
episode = 0

for indx in range(0, len(df)):
	slice_df = df.iloc[indx:indx+LENGHT_DROW]	
	indicators = Indicators(slice_df["open"], slice_df["low"], slice_df["high"], slice_df["close"])	
	slice_df["RSI"] = indicators.RSI(periods=14)
	slice_df[f"MA{MOVING_AVERAGE_TRENDLINE}"] = indicators.Moving_Average(days=MOVING_AVERAGE_TRENDLINE)
	robot_trade = TrainRobot(slice_df, SEARCH)
	slice_df["Upper_trendline"], slice_df["Lower_trendline"] = robot_trade.get_trend_line(MOVING_AVERAGE_TRENDLINE, EPSILON_FOR_ATR)

	stop_targer = SetPosition(EPSILON_FOR_GAP, EPSILON_FOR_ATR, 
							  TARGETPOINT_NUM_PIPS, STOPPLOSS_NUM_PIPS,
							  LOT, MOVING_AVERAGE_TARGETPOINT, TYPES_TRADE, TICKER_NAME, SEARCH)
	slice_df.dropna(inplace=True)

	position_values = robot_trade.TrainRSI(MOVING_AVERAGE_TRENDLINE)
	slice_df["Buy"] = np.NaN
	slice_df["Sell"] = np.NaN
	if position_values is not None:
		slice_df["Buy"].iloc[SEARCH] = slice_df["close"].iloc[SEARCH]
		slice_df["Sell"].iloc[SEARCH] = slice_df["close"].iloc[SEARCH]
		visulize.VisulasationOneSave(slice_df, episode)
		visulize.VisulasationForTargetPoint(df.iloc[slice_df.index[0]:slice_df.index[-1]+25], episode+1)

	episode += 1

