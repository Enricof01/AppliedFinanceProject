import models as m
type Bars = list[m.Bar]

def atr(bars, currentIndex, length):
    if currentIndex < length - 1:
        return None

    def true_range(i):
        high = bars[i].high
        low = bars[i].low

        if i == 0:
            return high - low

        prev_close = bars[i - 1].close
        return max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )

    # erster ATR-Wert bei Index length-1
    atr_value = sum(true_range(i) for i in range(length)) / length

    # rekursiv bis currentIndex
    for i in range(length, currentIndex + 1):
        tr = true_range(i)
        atr_value = (atr_value * (length - 1) + tr) / length

    return atr_value

def pivotHigh(bars : Bars, currentIndex: int, left: int):
    pivot_index = currentIndex - 1

    if pivot_index < left or currentIndex >= len(bars):
        return None

    ph = bars[pivot_index].high

    if bars[currentIndex].high > ph:
        return None

    for i in range(pivot_index - left, pivot_index):
        if bars[i].high > ph:
            return None

    return ph
            

    
def pivotLow(bars: Bars, currentIndex: int, left: int):
    pivot_index = currentIndex - 1

    if pivot_index < left or currentIndex >= len(bars):
        return None

    pl = bars[pivot_index].low

    if bars[currentIndex].low < pl:
        return None

    for i in range(pivot_index - left, pivot_index):
        if bars[i].low < pl:
            return None

    return pl
                