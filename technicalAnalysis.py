#bars and indizes as args
import models as m
type Bars = list[m.Bar]

def atr(bars: Bars, currentIndex : int, length : int):
    atr = 0
    runningIndex = currentIndex
    if currentIndex >= length:
        for i in range(length):
            currentBar = bars[runningIndex]
            atr += currentBar.high - currentBar.low
            runningIndex -= 1

        return atr/length
    else:
        return None

def pivotHigh(bars : Bars, currentIndex: int, left: int):
    pivot_index = currentIndex - 1

    if pivot_index < left or currentIndex >= len(bars):
        return None

    ph = bars[pivot_index].high

    if bars[currentIndex].high >= ph:
        return None

    for i in range(pivot_index - left, pivot_index):
        if bars[i].high > ph:
            return None

    return ph
            

    
def pivotLow(bars : Bars, currentIndex: int, left: int):
    pivot_index = currentIndex - 1

    if pivot_index < left or currentIndex >= len(bars):
        return None

    pl = bars[pivot_index].low

    if bars[currentIndex].high <= pl:
        return None

    for i in range(pivot_index - left, pivot_index):
        if bars[i].high < pl:
            return None

    return pl
                