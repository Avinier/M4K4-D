"""TS divider search for the BQ25798 (charge-path.md sec 5.4).

Finds E96 RT1 (REGN to TS) / RT2 (TS to GND) pairs that keep every tolerance
corner of the cold (VT1_RISE) and hot (VT5_FALL) suspend points inside the
Samsung 25R 0-50 C surface charge window, with a 103AT-2 on the cell.
Run: python3 charge-path-ts.py
"""
import math, itertools
# SEMITEC 103AT table (catalogue 129M), kOhm
T = [-10,0,10,20,25,30,40,50,60,70]
R = [42.47,27.28,17.96,12.09,10.00,8.313,5.827,4.160,3.020,2.228]
def rntc(t, r25=1.0, db=0.0):
    for i in range(len(T)-1):
        if T[i] <= t <= T[i+1]:
            a,b = 1/(T[i]+273.15), 1/(T[i+1]+273.15)
            x = 1/(t+273.15)
            lr = math.log(R[i]) + (math.log(R[i+1])-math.log(R[i]))*(x-a)/(b-a)
            r = math.exp(lr)
            # B tolerance: scale exponent about 25 C
            r *= math.exp(3435*db*(x-1/298.15))
            return r*r25
    raise ValueError(t)
def ratio(t, rt1, rt2, r25=1, db=0, k1=1, k2=1):
    rn = rntc(t, r25, db); p = 1/(1/(rt2*k2)+1/rn); return 100*p/(p+rt1*k1)
def tcross(target, rt1, rt2, **kw):
    lo, hi = -10.0, 70.0
    for _ in range(60):
        mid=(lo+hi)/2
        if ratio(mid, rt1, rt2, **kw) > target: lo=mid
        else: hi=mid
    return (lo+hi)/2
corners = list(itertools.product((0.99,1.01),(-0.01,0.01),(0.99,1.01),(0.99,1.01)))
def window(rt1, rt2):
    # cold suspend: ratio > VT1_RISE (72.4..74.2); hot suspend: ratio < VT5_FALL (33.7..34.7)
    cold = [tcross(v, rt1, rt2, r25=a, db=b, k1=c, k2=d) for v in (72.4,74.2) for a,b,c,d in corners]
    hot = [tcross(v, rt1, rt2, r25=a, db=b, k1=c, k2=d) for v in (33.7,34.7) for a,b,c,d in corners]
    t2 = [tcross(v, rt1, rt2) for v in (68.4,)]   # TS_COOL default rising 68.4 %
    t3 = [tcross(v, rt1, rt2) for v in (44.8,)]   # TS_WARM default falling 44.8 %
    return min(cold), max(cold), min(hot), max(hot), t2[0], t3[0]
for v in (73.3,): pass
E96=[1.00,1.02,1.05,1.07,1.10,1.13,1.15,1.18,1.21,1.24,1.27,1.30,1.33,1.37,1.40,1.43,1.47,1.50,1.54,1.58,1.62,1.65,1.69,1.74,1.78,1.82,1.87,1.91,1.96,2.00,2.05,2.10,2.15,2.21,2.26,2.32,2.37,2.43,2.49,2.55,2.61,2.67,2.74,2.80,2.87,2.94,3.01,3.09,3.16,3.24,3.32,3.40,3.48,3.57,3.65,3.74,3.83,3.92,4.02,4.12,4.22,4.32,4.42,4.53,4.64,4.75,4.87,4.99,5.11,5.23,5.36,5.49,5.62,5.76,5.90,6.04,6.19,6.34,6.49,6.65,6.81,6.98,7.15,7.32,7.50,7.68,7.87,8.06,8.25,8.45,8.66,8.87,9.09,9.31,9.53,9.76]
vals=[x*m for m in (1,10,100) for x in E96]
print("RP-02 5.23k/30.1k:", ["%.1f"%v for v in window(5.23,30.1)])
best=[]
for rt1 in [v for v in vals if 4<v<12]:
    for rt2 in [v for v in vals if 30<v<300]:
        c0,c1,h0,h1,t2,t3 = window(rt1,rt2)
        if c0 >= 0.0 and h1 <= 50.0:
            best.append((h0 - c1, rt1, rt2, c0,c1,h0,h1,t2,t3))
best.sort(reverse=True)
for b in best[:8]: print("span %.1f RT1 %.2fk RT2 %.1fk cold %.1f..%.1f hot %.1f..%.1f T2 %.1f T3 %.1f"%b)
cand=[]
for rt1 in [v for v in vals if 3<v<15]:
    for rt2 in [v for v in vals if 20<v<1000]:
        c0,c1,h0,h1,t2,t3 = window(rt1,rt2)
        cand.append((max(0-c0,0)+max(h1-50,0), rt1, rt2, c0,c1,h0,h1,t2,t3))
cand.sort()
for b in cand[:10]: print("viol %.2f RT1 %.2fk RT2 %.1fk cold %.1f..%.1f hot %.1f..%.1f T2 %.1f T3 %.1f"%b)
