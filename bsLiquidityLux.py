#Indicator for buy and sellside liquidity
#imports ---
import technicalAnalysis as ta
import models as m
# import pandas as pd
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

#Function
def bsLiquidity(bars : Bars):
    #initialization of containers ---
    aZZ = m.ZZ()
    b_liq : LiquidityColl = []
    s_liq : LiquidityColl = []

    #---------
    #constants ---
    maxSize = 50
    loop = 0
    #------
    x1  = None
    y1  = None
    x2  = None
    y2  = None
    d   = None
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
                updated = False

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
                    if len(b_liq) > 0:
                        getB = b_liq[0]
                   
                   
                        if st_B == getB.bx.left:
                            getB.bx.top = ((minP + maxP) / 2) + (atr/liqMar)
                            getB.bx.bottom = ((minP + maxP) / 2) - (atr/liqMar)
                            getB.bx.right = b.index + 10
                            print("Buyside Liqiuidity was updated")
                            updated = True
                        
                    if not updated: 
                        bxl = m.Box(bottom=((minP + maxP) / 2) - (atr/liqMar), top=((minP + maxP) / 2) + (atr/liqMar), left=st_B, right=b.index+10)
                        # bzl = m.Box()
                        l = m.Liquidity(bx=bxl,  broken=False, level = st_P, start_bar=bars[st_B])
                        l.start_index = st_B
                        b_liq.insert(0, l)

                        print(f"Buyside Liqiuidity was created at  time {b.time} and price {st_P}")
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
            if per:
                count = 0
                st_P  = 0.
                st_B  = 0
                minP  = 0.
                maxP  = 10e6
                liqtouches = []
                updated = False

                for j in range(len(aZZ.direction)):
                    if aZZ.direction[j] == -1 and atr != None:
                        if aZZ.y[j] < pivotLow - (atr/liqMar):
                            break
                        else: 
                            if aZZ.y[j] > (pivotLow - (atr/liqMar)) and aZZ.y[j] < (pivotLow + (atr/liqMar)):
                                count += 1
                                st_B = aZZ.x[j]
                                st_P = aZZ.y[j]
                                if aZZ.y[j] > minP:
                                    minP =  aZZ.y[j]
                                if aZZ.y[j] < maxP:
                                    maxP = aZZ.y[j]
                                liqtouches.append(st_P)

                if count > 2:
                   
                    if len(s_liq) > 0:
                        getB = s_liq[0]
                    

                        if st_B == getB.bx.left:
                            getB.bx.top = ((minP + maxP) / 2) + (atr/liqMar)
                            getB.bx.bottom = ((minP + maxP) / 2) - (atr/liqMar)
                            getB.bx.right = b.index + 10
                            print(f"Sellside Liqiuidity was updated at {b.time}")
                            updated = True
                    
                    if not updated: 
                        bxl = m.Box(bottom=((minP + maxP) / 2) - (atr/liqMar), top=((minP + maxP) / 2) + (atr/liqMar), left=st_B, right=b.index+10)
                        # bzl = m.Box()
                        l = m.Liquidity(bx=bxl,  broken=False, level = st_P, start_bar=bars[st_B])
                        l.start_index = st_B
                        s_liq.insert(0, l)

                        print(f"Sellside Liqiuidity was created at  time {b.time} and price {st_P}")
                        print([t for t in liqtouches])
                    if len(s_liq) > visLiq:
                        s_liq.pop()                                                

            
        if len(b_liq) >= 1: 
            for bl in b_liq:
                if bl.level is not None and b.high > bl.bx.top:
                    bl.broken = True
                    print(f"bsl was broken at {b.time}")

            b_liq = [bl for bl in b_liq if not bl.broken]

        if len(s_liq) >= 1: 
            for sl in s_liq:
                if sl.level is not None and b.low < sl.bx.bottom:
                    sl.broken = True
                    print(f"ssl was broken at {b.time}")

            s_liq = [sl for sl in s_liq if not sl.broken]            
            
        
    # return {"d": aZZ.direction,"y" : aZZ.y}
    return b_liq, s_liq
        
   



def main():

    p : Bars = []


    data = load_bitget_btcusdt_5m(limit=330)
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




    bl, sl = bsLiquidity(p)
    

    for li in bl:
        print ("active buyside" , li.level, li.start_bar.time)
    for si in sl:
        print ("active sellside" , si.level, si.start_bar.time)        


if __name__ == "__main__":
    main()

