#!/usr/bin/env python3
"""
Gunluk Donchian kirilim + ATR swing sinyal kontrolcusu (2026-07-27, Fable 5 danismanligiyla).

Kullanim:
  python3 swing_donchian.py <twelvedata_daily_json_dosyasi>

twelvedata_daily_json_dosyasi: Twelve Data time_series API'sinin ham JSON cevabi
(interval=1day, en az 25 gun onerilir - Donchian(20)/ATR(14) icin isinma suresi gerekir).

Backtest sonucu (2025-10-02 -> 2026-07-27, 293 gunluk bar, Fable 5 + bagimsiz dogrulama):
  n=7 islem, isabet=%71.4, ortalama R=1.857, toplam R=13.0
  Ilk yari (3 islem) ort R=3.0, ikinci yari (4 islem) ort R=1.0 - KUCUK ORNEKLEM, temkinli ol.
  %5 risk/islem -> ~%6.6/ay, %10 risk/islem -> ~%13.3/ay (20/ay hedefine ULASILAMADI,
  kullanici ile hedef gerekci bir seviyeye - %5-10/ay - guncellendi).

Kural: Donchian(20) onceki 20 gunun (bugun haric) en yuksek/dusuk seviyesini kirarsa sinyal.
Giris: BIR SONRAKI gunun acilisinda (lookahead yok) - bu yuzden script "sinyal var" derse,
gercek giris bir sonraki gun acilista yapilir, bugunku kapanis fiyati degil.
Stop = 1.5xATR(14), hedef = stop mesafesi x 3 (RR=3). Dogal stop %0.5'ten darsa REDDET
(genisletme yok).

NOT: Bu script gunde BIR KEZ anlamli sekilde degisir (yeni gunluk bar kapaninca). 15dk'lik
cron dongusunde her turda calistirmak zararsiz ama gereksiz - orkestrator "bugunku gunluk bar
kapandi mi" kontrolu yapip sadece o zaman bu scripti calistirmali.
"""
import sys, json

N_DONCHIAN = 20
ATR_PERIOD = 14
STOP_ATR_MULT = 1.5
RR = 3.0
MIN_STOP_PCT = 0.005  # %0.5


def compute_atr(bars, period):
    n = len(bars)
    atr = [None] * n
    trs = [None] * n
    for i in range(1, n):
        h, l, pc = bars[i]['h'], bars[i]['l'], bars[i-1]['c']
        trs[i] = max(h-l, abs(h-pc), abs(l-pc))
    for i in range(n):
        if i < period:
            continue
        if atr[i-1] is None:
            window = trs[i-period+1:i+1]
            if any(x is None for x in window):
                continue
            atr[i] = sum(window)/period
        else:
            atr[i] = (atr[i-1]*(period-1)+trs[i])/period
    return atr


def check_signal(bars):
    """Son GUNLUK bar (i = len(bars)-1) icin Donchian kirilim sinyali var mi kontrol eder.
    Sinyal varsa, gercek giris BIR SONRAKI gunun acilisinda yapilmali (bugun degil)."""
    n = len(bars)
    i = n-1
    if i < N_DONCHIAN:
        return {'signal': False, 'reason': f'yetersiz gun (min {N_DONCHIAN})'}
    atr = compute_atr(bars, ATR_PERIOD)
    if atr[i] is None:
        return {'signal': False, 'reason': 'ATR hesaplanamadi (isinma yetersiz)'}

    prior_highs = [bars[j]['h'] for j in range(i-N_DONCHIAN, i)]
    prior_lows = [bars[j]['l'] for j in range(i-N_DONCHIAN, i)]
    donchian_high = max(prior_highs)
    donchian_low = min(prior_lows)

    close = bars[i]['c']
    if close > donchian_high:
        direction = 1
    elif close < donchian_low:
        direction = -1
    else:
        return {'signal': False, 'reason': f'kirilim yok (kapanis={close:.2f}, kanal={donchian_low:.2f}-{donchian_high:.2f})'}

    stop_dist = STOP_ATR_MULT * atr[i]
    if stop_dist / close < MIN_STOP_PCT:
        return {'signal': False, 'reason': f'stop mesafesi cok dar (%{stop_dist/close*100:.3f} < %0.5) - REDDEDILDI, genisletilmedi'}

    if direction == 1:
        stop = close - stop_dist
        target = close + stop_dist * RR
    else:
        stop = close + stop_dist
        target = close - stop_dist * RR

    return {
        'signal': True,
        'direction': 'AL' if direction == 1 else 'SAT',
        'not': 'Giris BIR SONRAKI gunun acilisinda yapilmali, bu kapanis fiyati degil',
        'reference_close': round(close, 2),
        'target': round(target, 2), 'stop': round(stop, 2),
        'target_pct': round(abs(target-close)/close*100, 3),
        'stop_pct': round(stop_dist/close*100, 3),
        'rr': RR,
        'donchian_high': round(donchian_high, 2), 'donchian_low': round(donchian_low, 2),
    }


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        d = json.load(f)
    vals = list(reversed(d['values']))
    bars = [{'dt': v['datetime'], 'o': float(v['open']), 'h': float(v['high']),
             'l': float(v['low']), 'c': float(v['close'])} for v in vals]
    result = check_signal(bars)
    print(json.dumps(result, ensure_ascii=False, indent=2))
