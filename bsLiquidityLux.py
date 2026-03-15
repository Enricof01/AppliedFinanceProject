#Indicator for buy and sellside liquidity
#imports ---
import numpy as np
import technicalAnalysis as ta
import models as m
import yfinance as yf
import pandas as pd
from data_pipeline import load_bitget_btcusdt_5m
#----


#Constants:
liqLen = 7
liqMar = 1.4492

liqBuy = True
marBuy = 2.3
cLIQ_B = "4caf50"

liqSel = True
marSel = 2.3
cLIQ_S = "f23645"

lqVoid = False
cLQV_B = "4caf50"
cLQV_S = "f23645"

mode   = "Present"
visLiq = 3


print("---runs---")

    
type Bars = list[m.Bar]
type LiquidityColl = list[m.Liquidity]
dummyBox = m.Box(0,0,0,0)
dummyBar = m.Bar()
dummyLiq = m.Liquidity()
dummyLiq.bx = dummyBox
dummyLiq.start_bar = dummyBar
#Function
def bsLiquidity(bars : Bars):
    #initialization of containers ---
    aZZ = m.ZZ()
    b_liq : LiquidityColl = []
    b_liq.append(dummyLiq)
    #---------
    #constants ---
    maxSize = 50
    loop = 0
    #------
    x1 = None
    y1 = None
    x2 = None
    y2 = None
    d = None
    per = True #change --- only the last 500 bars are to watch

    for i, b in enumerate(bars):
        loop += 1
        pivotHigh = ta.pivotHigh(bars=bars, currentIndex=i, left=liqLen)
        pivotLow = ta.pivotLow(bars=bars, currentIndex=i, left=liqLen)
        if b.index > 0: x2 = b.index - 1 
        else: continue
           

        atr = ta.atr(bars=bars, currentIndex=i, length=10)

        if pivotHigh:
            dir = aZZ.direction[0]
            x1  = aZZ.x[0]
            y1  = aZZ.y[0]
            
            if i > 0:
                y2 = bars[i - 1].high
            else:
                continue

            if dir < 1:
                aZZ.in_and_out(1, x2, y2)
            else: 
                if dir == 1 and pivotHigh > y1:
                    aZZ.x[0] = x2
                    aZZ.y[0] = y2
            
            if per:
                count = 0
                st_P  = 0.
                st_B  = 0
                minP  = 0.
                maxP  = 10e6
                liqtouches = []

                for j in range(len(aZZ.direction)):
                    if aZZ.direction[j] == 1 and atr != None:
                        if aZZ.y[j] > pivotHigh + (atr/liqMar):
                            break
                        else: 
                            if aZZ.y[j] > pivotHigh - (atr/liqMar) and aZZ.y[j] < pivotHigh + (atr/liqMar):
                                count += 1
                                st_B = aZZ.x[j]
                                st_P = aZZ.y[j]
                                if aZZ.y[j] > minP:
                                    minP =  aZZ.y[j]
                                if aZZ.y[j] < maxP:
                                    maxP = aZZ.y[j]
                                liqtouches.append(st_P)
                if count > 2:
                    getB = b_liq[0]
                    if st_B == getB.start_index:
                        getB.bx.top = ((minP + maxP) / 2) + (atr/liqMar)
                        getB.bx.bottom = ((minP + maxP) / 2) - (atr/liqMar)
                        getB.bx.right = b.index + 10
                        print("Liqiuidity was updated")
                    
                    else: 
                        bxl = m.Box(bottom=((minP + maxP) / 2) - (atr/liqMar), top=((minP + maxP) / 2) + (atr/liqMar), left=st_B, right=b.index+10)
                        # bzl = m.Box()
                        l = m.Liquidity(bx=bxl,  broken=False, level = st_P, start_bar=bars[st_B])
                        l.start_index = st_B
                        b_liq.insert(0, l)

                        print(f"Liqiuidity was created at  time {b.time} and price {st_P} \n")
                        print([t for t in liqtouches])
                if len(b_liq) > visLiq:
                    b_liq.pop()
       

        if pivotLow:                    
            dir = aZZ.direction[0]
            x1  = aZZ.x[0]
            y1  = aZZ.y[0]
            
            if i > 0:
                y2 = bars[i - 1].low
            else:
                continue

            if dir > -1:
                aZZ.in_and_out(-1, x2, y2)
            else: 
                if dir == -1 and pivotLow < y1:
                    aZZ.x[0] = x2
                    aZZ.y[0] = y2
               
            
        if len(b_liq) >= 1: 
            for bl in b_liq:
                if bl.bx.top != 0:
                    if b.high > bl.bx.top:
                        bl.broken = True
                if bl.broken:
                 b_liq.remove(bl)
            
        
    # return {"d": aZZ.direction,"y" : aZZ.y}
    return b_liq
        
   



def main():
    #hier die probedaten laden
    # l = m.Liquidity()
    p : Bars = []
    # for i in range(100):
    #     c = m.Bar(i,i,i,i)
    #     p.append(c)
    # bsLiquidity(p)

    # ticker = "BTC-USD"
    # data = yf.download(tickers=ticker, period="5d", interval="5m")
    # closeList = data["Close"]["BTC-USD"].tolist()
    # openList = data["Open"]["BTC-USD"].tolist()
    # highList = data["High"]["BTC-USD"].tolist()
    # lowList = data["Low"]["BTC-USD"].tolist()
    # timestamp = data["Close"].index.to_list()


    # i = 0
    # for c,o,h,l,t in zip(closeList, openList, highList,lowList, timestamp):
    #     bar = m.Bar(open = o, low = l, high = h, close = c, index=i, time=t)
    #     p.append(bar)
    #     i = i+1

    data = load_bitget_btcusdt_5m()
    closeList = data["close"].tolist()
    openList = data["open"].tolist()
    highList = data["high"].tolist()
    lowList = data["low"].tolist()
    timestamp = data["timestamp"].to_list()

    i = 0
    for c,o,h,l,t in zip(closeList, openList, highList,lowList, timestamp):
        bar = m.Bar(open = o, low = l, high = h, close = c, index=i, time=t)
        p.append(bar)
        i = i+1




    bl = bsLiquidity(p)
    

    for li in bl:
        print ("active " , li.level, li.start_bar.time)


if __name__ == "__main__":
    main()

