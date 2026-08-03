#!/usr/bin/env python3
"""
Design C trend-takip sinyal kontrolcusu (2026-07-26, Fable 5 danismanligiyla).

Kullanim:
  python3 trend_design_c.py <twelvedata_json_dosyasi>

twelvedata_json_dosyasi: Twelve Data time_series API'sinin ham JSON cevabi
(interval=15min, en az 60 bar onerilir - ADX/EMA/RSI icin isinma suresi gerekir).

Backtest sonucu (7.5 hafta + son 1 ay, atr_mult=1.5, adx_min=20, RR=2.0):
  xau_hist.json:  n=67 isabet=%41.8 beklenti=+0.254R
  lastmonth.json: n=42 isabet=%42.9 beklenti=+0.286R
  Zamansal yari-bolme (xau_hist): ilk yari +0.161R (n=31), ikinci yari +0.244R (n=41)

NOT: Bu script sadece SINYAL VAR MI/YOK MU ve giris/hedef/stop seviyelerini hesaplar.
Islem acma/kapama, log yazma, git commit orkestratorun (ust seviye ajan) sorumlulugunda.
"""
import sys, json
from datetime import datetime, timedelta, timezone

def ema_series(closes, period):
    k = 2/(period+1)
    out = [None]*len(closes)
    ema = None
    for i, c in enumerate(closes):
        ema = c if ema is None else c*k + ema*(1-k)
        out[i] = ema
    return out

def true_range(bars, i):
    if i == 0: return bars[i]['h']-bars[i]['l']
    prev_c = bars[i-1]['c']
    return max(bars[i]['h']-bars[i]['l'], abs(bars[i]['h']-prev_c), abs(bars[i]['l']-prev_c))

def adx_series(bars, period=14):
    n = len(bars)
    tr = [0.0]*n; plus_dm = [0.0]*n; minus_dm = [0.0]*n
    for i in range(1, n):
        up = bars[i]['h']-bars[i-1]['h']
        down = bars[i-1]['l']-bars[i]['l']
        plus_dm[i] = up if (up > down and up > 0) else 0.0
        minus_dm[i] = down if (down > up and down > 0) else 0.0
        tr[i] = true_range(bars, i)
    atr = [0.0]*n; p_dm_s = [0.0]*n; m_dm_s = [0.0]*n
    adx = [None]*n; plus_di = [0.0]*n; minus_di = [0.0]*n; dx = [0.0]*n
    for i in range(1, n):
        if i < period: continue
        if i == period:
            atr[i] = sum(tr[1:period+1])/period
            p_dm_s[i] = sum(plus_dm[1:period+1])/period
            m_dm_s[i] = sum(minus_dm[1:period+1])/period
        else:
            atr[i] = (atr[i-1]*(period-1)+tr[i])/period
            p_dm_s[i] = (p_dm_s[i-1]*(period-1)+plus_dm[i])/period
            m_dm_s[i] = (m_dm_s[i-1]*(period-1)+minus_dm[i])/period
        if atr[i] > 0:
            plus_di[i] = 100*p_dm_s[i]/atr[i]
            minus_di[i] = 100*m_dm_s[i]/atr[i]
            denom = plus_di[i]+minus_di[i]
            dx[i] = 100*abs(plus_di[i]-minus_di[i])/denom if denom > 0 else 0
    for i in range(1, n):
        if i < 2*period-1: continue
        if i == 2*period-1:
            adx[i] = sum(dx[period:2*period])/period
        else:
            adx[i] = (adx[i-1]*(period-1)+dx[i])/period
    return adx, atr

def rsi_series(closes, period=14):
    n = len(closes)
    rsi = [None]*n
    gains = [0.0]*n; losses = [0.0]*n
    for i in range(1, n):
        d = closes[i]-closes[i-1]
        gains[i] = max(d, 0); losses[i] = max(-d, 0)
    avg_gain = avg_loss = None
    for i in range(1, n):
        if i < period: continue
        if i == period:
            avg_gain = sum(gains[1:period+1])/period
            avg_loss = sum(losses[1:period+1])/period
        else:
            avg_gain = (avg_gain*(period-1)+gains[i])/period
            avg_loss = (avg_loss*(period-1)+losses[i])/period
        rsi[i] = 100.0 if avg_loss == 0 else 100 - 100/(1+avg_gain/avg_loss)
    return rsi

def regime_net_pct(bars, i, window=8):
    if i-window+1 < 0: return None
    closes = [bars[j]['c'] for j in range(i-window+1, i+1)]
    net_move = closes[-1]-closes[0]
    return abs(net_move)/closes[0]*100

def check_signal(bars, adx_min=20, atr_mult=1.5, rr_target=2.0):
    """Son bar (i = len(bars)-1) icin Design C trend sinyali var mi kontrol eder."""
    n = len(bars)
    i = n-1
    closes = [b['c'] for b in bars]
    adx, atr = adx_series(bars, 14)
    ema9 = ema_series(closes, 9)
    ema21 = ema_series(closes, 21)
    rsi = rsi_series(closes, 14)

    if i < 30: return {'signal': False, 'reason': 'yetersiz bar (min 30)'}
    if adx[i] is None or adx[i] < adx_min: return {'signal': False, 'reason': f'ADX={adx[i]}<{adx_min}'}
    if ema9[i-4] is None or ema21[i-5] is None: return {'signal': False, 'reason': 'EMA isinma yetersiz'}
    slope9 = ema9[i]-ema9[i-4]
    slope21 = ema21[i]-ema21[i-5]
    if slope9*slope21 <= 0: return {'signal': False, 'reason': 'EMA9/EMA21 egimi hizali degil'}
    direction = 1 if slope9 > 0 else -1
    if direction == 1 and closes[i] < ema21[i]: return {'signal': False, 'reason': 'fiyat EMA21 altinda (yon=yukari)'}
    if direction == -1 and closes[i] > ema21[i]: return {'signal': False, 'reason': 'fiyat EMA21 ustunde (yon=asagi)'}
    net_pct = regime_net_pct(bars, i, 8)
    if net_pct is None or net_pct < 0.2: return {'signal': False, 'reason': f'8-bar net_pct={net_pct} < 0.2'}
    if direction == 1:
        trigger = closes[i] > max(bars[i-1]['h'], bars[i-2]['h'])
    else:
        trigger = closes[i] < min(bars[i-1]['l'], bars[i-2]['l'])
    if not trigger: return {'signal': False, 'reason': 'devam-mumu tetigi yok (onceki 2 bar kirilmadi)'}
    if rsi[i] is None: return {'signal': False, 'reason': 'RSI hesaplanamadi'}
    if direction == 1 and not (48 <= rsi[i] <= 72): return {'signal': False, 'reason': f'RSI={rsi[i]:.1f} long araligi (48-72) disinda'}
    if direction == -1 and not (28 <= rsi[i] <= 52): return {'signal': False, 'reason': f'RSI={rsi[i]:.1f} short araligi (28-52) disinda'}
    if atr[i] is None or atr[i] == 0: return {'signal': False, 'reason': 'ATR hesaplanamadi'}

    entry = closes[i]
    stop_dist = atr[i]*atr_mult
    stop_price = entry-stop_dist if direction == 1 else entry+stop_dist
    target_dist = stop_dist*rr_target
    target_price = entry+target_dist if direction == 1 else entry-target_dist
    target_pct = abs(target_price-entry)/entry*100
    stop_pct = abs(entry-stop_price)/entry*100

    # gurultu-stop korumasi (genel kural, range-fade ile ayni)
    stop_dist_actual = abs(entry-stop_price)
    recent_extreme = min(bars[i-1]['l'], bars[i]['l']) if direction == 1 else max(bars[i-1]['h'], bars[i]['h'])
    dist_to_extreme = abs(entry-recent_extreme)
    noise_ok = dist_to_extreme > stop_dist_actual/2
    if not noise_ok: return {'signal': False, 'reason': 'gurultu-stop korumasi tetiklendi'}

    return {
        'signal': True, 'direction': 'AL' if direction == 1 else 'SAT',
        'entry': round(entry, 2), 'target': round(target_price, 2), 'stop': round(stop_price, 2),
        'target_pct': round(target_pct, 3), 'stop_pct': round(stop_pct, 3), 'rr': round(target_pct/stop_pct, 2),
        'adx': round(adx[i], 1), 'rsi': round(rsi[i], 1),
    }

def drop_unclosed_last_bar(bars, interval_minutes=15):
    """Twelve Data bazen henuz kapanmamis (olusum halindeki) son bari da donduruyor -
    bu barin kapanis fiyati saniyeler icinde degisebiliyor, bu da sinyalin birkac
    dakika icinde titremesine (once var sonra yok gorunmesine) neden oluyordu.
    Son barin baslangic zamani + interval, simdiki UTC zamanindan sonraysa
    (yani bar henuz kapanmadiysa) o bari at, bir onceki (kesin kapanmis) barla devam et."""
    if not bars:
        return bars
    try:
        last_dt = datetime.fromisoformat(bars[-1]['dt']).replace(tzinfo=timezone.utc)
    except ValueError:
        return bars
    now = datetime.now(timezone.utc)
    bar_close_time = last_dt + timedelta(minutes=interval_minutes)
    if now < bar_close_time:
        return bars[:-1]
    return bars

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        d = json.load(f)
    vals = list(reversed(d['values']))
    bars = [{'dt': v['datetime'], 'o': float(v['open']), 'h': float(v['high']),
             'l': float(v['low']), 'c': float(v['close'])} for v in vals]
    bars = drop_unclosed_last_bar(bars)
    result = check_signal(bars)
    print(json.dumps(result, ensure_ascii=False, indent=2))
