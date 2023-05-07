import pandas as pd
import numpy as np 
import time 
import matplotlib.pyplot as plt 

from Robot import TrainRobot, SetPosition
from Visulasation import SaveBackTest
from objectes import (PriceActionChandles, 
                      Indicators, 
                      SupportVSResistanced)


TICKER_NAME = "XAUUSD"
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
LENGHT_DROW = 200
SEARCH = -2
EPSILON_FOR_TRENDLINE = 0.2
MOVING_AVERAGE_TRENDLINE = 200

df = pd.read_csv("XAUUSD_M5.csv")
df.index = [i for i in range(len(df))]

visulize = SaveBackTest()
episode = 0
for indx in range(0, len(df)): 
	slice_df = df[indx:indx+LENGHT_DROW]
	slice_df["sl"], slice_df["tp"] = np.NaN, np.NaN 
	indicators = Indicators(slice_df["open"], slice_df["low"], slice_df["high"], slice_df["close"])
	algoritm = SupportVSResistanced(slice_df)
	priceaction = PriceActionChandles(slice_df) 
	robot_trade = TrainRobot(slice_df, SEARCH)
	stop_targer = SetPosition(EPSILON_FOR_GAP, EPSILON_FOR_ATR, 
							  TARGETPOINT_NUM_PIPS, STOPPLOSS_NUM_PIPS,
							  LOT, False, MOVING_AVERAGE_TARGETPOINT, TYPES_TRADE, TICKER_NAME, SEARCH)
	slice_df["ATR"] = indicators.AverageTrueRange(number_range=16)
	slice_df["MA50"] = indicators.Moving_Average(days=100)
	levels = []
	for index in range(N_BEFORE, len(slice_df)-N_AFTER):
		if algoritm.support(index, N_BEFORE, N_AFTER):
			l = slice_df["low"].iloc[index]
			if algoritm.isFarFromLevel(l, levels):
				levels.append((index, slice_df["low"].iloc[index]))
		elif algoritm.resistance(index, N_BEFORE, N_AFTER):
			l = slice_df["high"].iloc[index]
			if algoritm.isFarFromLevel(l, levels):
				levels.append((index, slice_df["high"].iloc[index]))
	real, lines, upper, lower = robot_trade.BetweenLines(levels, EPSILON_FOR_GAP)
	slice_df, chanel_name = robot_trade.get_chandles_pattern()
	slice_df, all_chanel_name, types_trade = robot_trade.TrainChandles(upper, lower, chanel_name)
	sl = stop_targer.Stopp_Loss(dataframe=slice_df, types=TYPE_STOPPLOSS)
	if sl is not None:
		slice_df["sl"] = sl
		visulize.VisulasationOneSave(slice_df, episode)
		episode += 1
		visulize.VisulasationForMA(df[slice_df.index[0]:slice_df.index[-1]+15], episode, MOVING_AVERAGE_TARGETPOINT)
		indicators = Indicators(slice_df["open"], slice_df["low"], slice_df["high"], slice_df["close"])
		slice_df[f"MA{MOVING_AVERAGE_TARGETPOINT}"] = indicators.Moving_Average(days=MOVING_AVERAGE_TARGETPOINT)
		if types_trade=="buy":
			targetpoint = stop_targer.Target_Point_MA(slice_df, type_trade="Buy")
		else:
			targetpoint = stop_targer.Target_Point_MA(slice_df, type_trade="Sell")

		if targetpoint:
			slice_df['tp'] = slice_df["close"].iloc[SEARCH]
			episode += 1
			# visulize.VisulasationForTargetPoint(slice_df, episode)
			
