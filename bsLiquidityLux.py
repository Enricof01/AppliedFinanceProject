#Indicator for buy and sellside liquidity
#imports ---
import numpy as np
import technicalAnalysis as ta
import models as m
#----


#Constants:
liqLen = 7
liqMar = 10

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
dummyLiq = m.Liquidity()
#Function
def bsLiquidity(bars : Bars):
    #initialization of containers ---
    aZZ = m.ZZ()
    b_liq : LiquidityColl = []
    b_liq.append(dummyLiq)
    #---------
    #constants ---
    maxSize = 50
    #------
    x1 = None
    y1 = None
    x2 = None
    y2 = None
    d = None
    per = True #change --- only the last 500 bars are to watch

    for i, b in enumerate(bars):
        pivotHigh = ta.pivotHigh(bars=bars, currentIndex=i, left=7)
        if b.index > 0: x2 = b.index - 1 
        else: continue
           

        atr = ta.atr(bars=bars, currentIndex=i, length=10)

        if pivotHigh:
            dir = aZZ.direction[0]
            x1  = aZZ.x[0]
            y1  = aZZ.y[0]
            if i > 0:  y1 =  b.h[i - 1] 
            else: continue

            if dir < 1:
                aZZ.in_and_out(1, x2, y2)
            else: 
                if dir == 1 and pivotHigh > y1:
                    aZZ.index.insert(0,x2), aZZ.price.insert(0,y2)
            
            if per:
                count = 0
                st_P  = 0.
                st_B  = 0
                minP  = 0.
                maxP  = 10e6

                for i in range(maxSize - 1):
                    if aZZ.d[i] == 1:
                        if aZZ.y[i] > pivotHigh + (atr/liqMar):
                            break
                        else: 
                            if aZZ.y[i] > pivotHigh - (atr/liqMar) and aZZ.y[i] < pivotHigh + (atr/liqMar):
                                count += 1
                                st_B = aZZ.x[i]
                                st_P = aZZ.y[i]
                                if aZZ.y[i] > minP:
                                    minP =  aZZ.y[i]
                                if aZZ.y[i] < maxP:
                                    maxP = aZZ.y[i]
                if count > 2:
                    getB = b_liq[0].start_index

               
            

        print(b)
        
    print("no fkn way") 



def main():
    #hier die probedaten laden
    b = m.Bar()
    n = b.close
    ta.pivotHigh()
    print("test")
    bars : Bars = []
    for i in range(5):
        b = m.Bar()
        bars.append(b)
    bsLiquidity(bars)


if __name__ == "__main__":
    main()

