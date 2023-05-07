import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import time 


class TrainRobot:

    def __init__(self, main_df, search):
        self.df = main_df
        self.search = search


    def TrainChandles(self, upper, lower, chanles_pattern_name): # ---> One
        for col in self.df.columns:
            if col in chanles_pattern_name:
                self.df[col].replace(0, np.NaN, inplace=True)

        self.df["Buy"] = np.NaN
        self.df["Sell"] = np.NaN
        what_type = None
        for name in chanles_pattern_name:
            for u, d in zip(upper, lower):           
                if name=="Pin_Bar":
                    if self.df[name].iloc[-3]==-100 and u>self.df["high"].iloc[-2]>d and self.df["high"].iloc[-3]>self.df["high"].iloc[-2] and self.df["MA50"]>self.df["close"]: # Bearish
                        print(f"we take a position in this price {self.df['close'].iloc[-1]} SELL opportunity")
                        self.df["Sell"].iloc[-1] = self.df["close"].iloc[-1]
                        what_type = "sell"
                    elif self.df[name].iloc[-3]==100 and u>self.df["low"].iloc[-2]>d and self.df["low"].iloc[-3]<self.df["low"].iloc[-2] and self.df["MA50"]<self.df["close"]: # Bullish
                        print(f"we take a position in this price {self.df['close'].iloc[-1]} BUY opportunity")
                        self.df["Buy"].iloc[-1] = self.df["close"].iloc[-1]
                        what_type = "buy"

                else:
                    if self.df[name].iloc[-2]==-100 and u>self.df["high"].iloc[-2]>d and self.df["MA50"]>self.df["close"]: # Bearish
                        print(f"we take a position in this price {self.df['close'].iloc[-1]} SELL opportunity")
                        self.df["Sell"].iloc[-1] = self.df["close"].iloc[-1]
                        what_type = "sell"
                    elif self.df[name].iloc[-2]==100 and u>self.df["low"].iloc[-2]>d and self.df["MA50"]<self.df["close"]: # Bullish
                        print(f"we take a position in this price {self.df['close'].iloc[-1]} BUY opportunity")
                        self.df["Buy"].iloc[-1] = self.df["close"].iloc[-1]
                        what_type = "buy"

        return self.df, chanles_pattern_name, what_type


    def BetweenLines(self, lvl): # ---> One
        values = [i[1] for i in lvl]
        lines = [i[0] for i in lvl]
        upper = []
        lower = []
        for real in values:
            if 0<real<2:
                fake = round(np.mean(abs(self.df["open"]-self.df["high"])), 3) * EPSILON_FOR_GAP
                lower.append(abs(fake-real))
                upper.append(abs(fake+real))

            else:
                if round(np.var(abs(self.df["open"]-self.df["close"])), 3)>round(np.mean(abs(self.df["open"]-self.df["close"])), 3):
                    fake = round(np.mean(abs(self.df["open"]-self.df["close"])), 3)# * EPSILON_FOR_GAP
                    lower.append(abs(fake-real))
                    upper.append(abs(fake+real))
                else:
                    fake = round(np.var(abs(self.df["open"]-self.df["close"])), 3) * EPSILON_FOR_GAP
                    lower.append(abs(fake-real))
                    upper.append(abs(fake+real))

        return values, lines, upper, lower

    
    def TrainRSI(self, MATrendLine): # ---> Tow
        if self.df["close"].iloc[self.search]<self.df[f"MA{MATrendLine}"].iloc[self.search] and self.df["RSI"].iloc[self.search]>75:
            return "Sell"
        elif self.df["close"].iloc[self.search]>self.df[f"MA{MATrendLine}"].iloc[self.search] and self.df["RSI"].iloc[self.search]<25:
            return "Buy"
        else:
            return None  


    def Check_Chandlesticks_Patterns(self, main_df): # --> Tow
        main_df, chanel_name = self.get_chandles_pattern(self.df)
        for name in chanel_name:
            for u, d in zip(main_df["Upper_trendline"], main_df["Lower_trendline"]):
                if name=="Pin_Bar" and name=="DragonflyDoji":
                    if main_df[name].iloc[self.search-1]==-100 and  main_df["high"].iloc[self.search-1]>main_df["high"].iloc[self.search] and u>main_df["close"].iloc[self.search]>d:
                        return False 
                    elif main_df[name].iloc[self.search-1]==100 and  main_df["low"].iloc[self.search-1]<main_df["low"].iloc[self.search] and u>main_df["close"].iloc[self.search]>d:
                        return False
                else:
                    if main_df[name].iloc[self.search]==-100 and  u>main_df["close"].iloc[self.search]>d:
                        return False 
                    elif main_df[name].iloc[self.search]==100 and u>main_df["close"].iloc[self.search]>d:
                        return False
        return True

    
    def get_trend_line(self, MOVING_AVERAGE_TRENDLINE, eps_trendline): # --> Tow
        epsilon = self.df[f"MA{MOVING_AVERAGE_TRENDLINE}"].std() * eps_trendline
        up_trend = self.df[f"MA{MOVING_AVERAGE_TRENDLINE}"] + epsilon
        down_trend = self.df[f"MA{MOVING_AVERAGE_TRENDLINE}"] - epsilon
        return up_trend, down_trend



class SetPosition:

    def __init__(self, eps_gap, eps_atr,
                 pips_target, pips_stop, lot, 
                 MA_target, ticker_name, search,
                 type_trade, train_with_pips=False ): #type trade --> MA, chandlestick, Pips
        
        self.eps_atr = eps_atr
        self.eps_gap = eps_gap
        self.pips_stop = pips_stop
        self.pips_target = pips_target
        self.lot = lot 
        self.MA_target = MA_target
        self.type_trade = type_trade
        self.ticker_name = ticker_name
        self.search = search


    def Stopp_Loss(self, dataframe, types="PiP"): # types ---> PiP, ATR
        arr_buy = dataframe["Buy"].isnull()       # --> One and Tow
        arr_sell = dataframe["Sell"].isnull()
        if types=="ATR":
            if not arr_buy.iloc[-1]:
                stoploss = dataframe["Buy"].iloc[-1] - (dataframe["ATR"].iloc[-1] * self.eps_atr)
                print(f"SET as ATR and the StoppLoss is {stoploss}")
                return stoploss

            if not arr_sell.iloc[-1]:
                stoploss = dataframe["Sell"].iloc[-1] + (dataframe["ATR"].iloc[-1] * self.eps_atr)
                print(f"SET as ATR and the StoppLoss is {stoploss}")
                return stoploss


    def Target_Point(self, dataframe, 
                    name_chandles, types="chandlestick", 
                    order_type="buy"): # types ---> PiP, chandlestick, MA 
                                       # --> One
        if order_type=="buy":
            if types=="chandlestick":
                for name in name_chandles:
                    if name=="Pin_Bar":
                        if dataframe.loc[-3, name]==-100 and dataframe["close"].iloc[-3]>dataframe["close"].iloc[-2]:
                            targetpoint = dataframe["close"].iloc[-1]  
                            print(f"\n[[exit]] the order {targetpoint}")
                            return targetpoint

                    else:
                        if dataframe.loc[-2, name]==-100:
                            targetpoint = dataframe["close"].iloc[-1]
                            print(f"\n[[exit]] the order {targetpoint}")
                            return targetpoint

        else:
            if types=="chandlestick":
                for name in name_chandles:
                    if name=="Pin_Bar":
                        if dataframe.loc[-3, name]==100 and dataframe["close"].iloc[-3]>dataframe["close"].iloc[-2]:
                            targetpoint = dataframe["close"].iloc[-1]  
                            print(f"\n[[exit]] the order {targetpoint}")
                            return targetpoint

                    else:
                        if dataframe.loc[-2, name]==100:
                            targetpoint = dataframe["close"].iloc[-1]
                            print(f"\n[[exit]] the order {targetpoint}")
                            return targetpoint


    def Target_Point_MA(self, main_df, type_trade="Buy"):  # --> One Option and Tow 
        if type_trade=="Buy":
            if main_df[f"MA{self.MA_target}"].iloc[self.search]>main_df["low"].iloc[self.search]:
                return True
                
        else:
            if main_df[f"MA{self.MA_target}"].iloc[self.search]<main_df["high"].iloc[self.search]:
                return True
        return None



