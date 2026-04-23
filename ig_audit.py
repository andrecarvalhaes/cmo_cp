#!/usr/bin/env python3
import json, urllib.request, urllib.error, time
from datetime import datetime, timedelta

TOKEN = "EAAVsQTj3ptIBRLp7ZAUBJKjq4brVVe58UBldMHawQ1KZCgLW7THBPJpaPpJXBcuJXEZCSh95lwXj7iKZABirbZAle3KRbdpzcYAtSqDaIo6ZAYZBzrSmjdfC499xzY5voF4byuX50EJJPOEhQpGMyZCN2PG64IxZBwAI2dqGsl4pj2hpMKNneaIHfwt4GZC3R58WQv"
IG_ID = "17841407201741175"
BASE = "https://graph.facebook.com/v21.0"

def api_get(ep, params=None):
    url = BASE + "/" + ep
    if params is None: params = {}
    params["access_token"] = TOKEN
    qs = "&".join(k + "=" + urllib.request.quote(str(v)) for k, v in params.items())
    req = urllib.request.Request(url + "?" + qs)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print("  [API ERROR] " + str(e.code) + ": " + body[:300])
        return None
    except Exception as e:
        print("  [ERROR] " + str(e))
        return None

def fmt(n):
    if isinstance(n, float): return "{:,.2f}".format(n)
    if isinstance(n, int): return "{:,}".format(n)
    return str(n)

def trunc(s, mx=120):
    if not s: return "(sem caption)"
    return s[:mx] + "..." if len(s) > mx else s

def dfmt(ts):
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except: return ts

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SEP = "=" * 80
print(SEP)
print("  INSTAGRAM PROFILE AUDIT - @clubpetro")
print("  Data: " + datetime.now().strftime("%d/%m/%Y %H:%M"))
print(SEP)

# 1. PROFILE INFO
print()
print(SEP)
print("  1. PROFILE INFO")
print(SEP)
profile = api_get(IG_ID, {"fields": "id,username,name,biography,website,followers_count,follows_count,media_count,profile_picture_url"})
fc = 22044
if profile:
    fc = profile.get("followers_count", 22044)
    print()
    print("  Name:                " + str(profile.get("name", "N/A")))
    print("  Username:            @" + str(profile.get("username", "N/A")))
    print("  Followers:           " + fmt(profile.get("followers_count", 0)))
    print("  Following:           " + fmt(profile.get("follows_count", 0)))
    print("  Total Posts:         " + fmt(profile.get("media_count", 0)))
    print("  Website:             " + str(profile.get("website", "N/A")))
    print("  Profile Picture:     " + str(profile.get("profile_picture_url", "N/A")))
    print()
    print("  --- BIOGRAPHY (full text) ---")
    bio = profile.get("biography", "N/A")
    for bline in str(bio).split(chr(10)):
        print("  " + bline)
    print("  --- END BIOGRAPHY ---")
else:
    print("  [WARN] Could not fetch profile.")

# 2. LAST 25 POSTS
print()
print(SEP)
print("  2. LAST 25 POSTS + ENGAGEMENT")
print(SEP)
md = api_get(IG_ID + "/media", {"fields": "id,caption,media_type,timestamp,like_count,comments_count,permalink,thumbnail_url,media_url", "limit": "25"})
posts = md.get("data", []) if md else []
print("  Fetched " + str(len(posts)) + " posts")
print()
for i, p in enumerate(posts, 1):
    lk = p.get("like_count", 0)
    cm = p.get("comments_count", 0)
    eng = lk + cm
    er = (eng / fc * 100) if fc > 0 else 0
    p["_eng"] = eng
    p["_er"] = er
    mt = p.get("media_type", "?")
    type_map = {"IMAGE": "[IMG]", "VIDEO": "[VID/REEL]", "CAROUSEL_ALBUM": "[CAROUSEL]"}
    tl = type_map.get(mt, "[" + mt + "]")
    print("  --- Post #" + str(i) + " ---")
    print("  ID:          " + str(p.get("id", "N/A")))
    print("  Type:        " + tl + " " + mt)
    print("  Date:        " + dfmt(p.get("timestamp", "")))
    print("  Likes:       " + fmt(lk))
    print("  Comments:    " + fmt(cm))
    print("  Engagement:  " + fmt(eng) + "  |  ER: {:.3f}%".format(er))
    print("  Permalink:   " + str(p.get("permalink", "N/A")))
    mu = p.get("media_url", "")
    tu = p.get("thumbnail_url", "")
    if mu: print("  Media URL:   " + str(mu)[:120])
    if tu: print("  Thumb URL:   " + str(tu)[:120])
    cap = p.get("caption", "")
    print("  Caption:")
    if cap:
        for cl in str(cap).split(chr(10)):
            print("    " + cl)
    else:
        print("    (sem caption)")
    print()

# 3. ENGAGEMENT SUMMARY
print(SEP)
print("  3. OVERALL ENGAGEMENT METRICS (Last 25 Posts)")
print(SEP)
avg_lk = avg_cm = avg_eng = avg_er = 0.0
best = worst = None
if posts:
    total_lk = sum(p.get("like_count", 0) for p in posts)
    total_cm = sum(p.get("comments_count", 0) for p in posts)
    total_eng = sum(p.get("_eng", 0) for p in posts)
    n = len(posts)
    avg_lk = total_lk / n
    avg_cm = total_cm / n
    avg_eng = total_eng / n
    avg_er = sum(p.get("_er", 0) for p in posts) / n
    best = max(posts, key=lambda x: x.get("_er", 0))
    worst = min(posts, key=lambda x: x.get("_er", 0))
    print()
    print("  Total Likes (25 posts):      " + fmt(total_lk))
    print("  Total Comments (25 posts):   " + fmt(total_cm))
    print("  Total Engagement:            " + fmt(total_eng))
    print("  Avg Likes/Post:              {:.1f}".format(avg_lk))
    print("  Avg Comments/Post:           {:.1f}".format(avg_cm))
    print("  Avg Engagement/Post:         {:.1f}".format(avg_eng))
    print("  Avg Engagement Rate:         {:.3f}%".format(avg_er))
    print()
    ts2 = {}
    for p in posts:
        mt2 = p.get("media_type", "?")
        if mt2 not in ts2: ts2[mt2] = {"c": 0, "l": 0, "cm": 0, "er": 0.0}
        ts2[mt2]["c"] += 1
        ts2[mt2]["l"] += p.get("like_count", 0)
        ts2[mt2]["cm"] += p.get("comments_count", 0)
        ts2[mt2]["er"] += p.get("_er", 0)
    print("  --- Breakdown by Media Type ---")
    print("  {:<18} {:>6} {:>10} {:>10} {:>10}".format("Type", "Count", "Avg Likes", "Avg Comm", "Avg ER"))
    print("  " + "-" * 56)
    for mt2 in sorted(ts2.keys()):
        st = ts2[mt2]
        c = st["c"]
        print("  {:<18} {:>6} {:>10.1f} {:>10.1f} {:>9.3f}%".format(mt2, c, st["l"]/c, st["cm"]/c, st["er"]/c))
    print()
    print("  --- BEST PERFORMING POST ---")
    print("  Permalink:   " + str(best.get("permalink", "N/A")))
    print("  Date:        " + str(best.get("timestamp", "N/A")))
    print("  Type:        " + str(best.get("media_type", "N/A")))
    print("  Likes:       " + fmt(best.get("like_count", 0)))
    print("  Comments:    " + fmt(best.get("comments_count", 0)))
    print("  ER:          {:.3f}%".format(best.get("_er", 0)))
    print("  Caption:     " + trunc(best.get("caption", ""), 200))
    print()
    print("  --- WORST PERFORMING POST ---")
    print("  Permalink:   " + str(worst.get("permalink", "N/A")))
    print("  Date:        " + str(worst.get("timestamp", "N/A")))
    print("  Type:        " + str(worst.get("media_type", "N/A")))
    print("  Likes:       " + fmt(worst.get("like_count", 0)))
    print("  Comments:    " + fmt(worst.get("comments_count", 0)))
    print("  ER:          {:.3f}%".format(worst.get("_er", 0)))
    print("  Caption:     " + trunc(worst.get("caption", ""), 200))

# 4. STORIES
print()
print(SEP)
print("  4. STORIES")
print(SEP)
sd = api_get(IG_ID + "/stories", {"fields": "id,caption,media_type,timestamp,permalink,media_url"})
if sd and "data" in sd and len(sd["data"]) > 0:
    print("  Active stories: " + str(len(sd["data"])))
    for i, s in enumerate(sd["data"], 1):
        print("  Story #" + str(i) + ": " + str(s.get("media_type", "?")) + " - " + str(s.get("timestamp", "?")))
        print("    Permalink: " + str(s.get("permalink", "N/A")))
        si = api_get(str(s["id"]) + "/insights", {"metric": "reach,impressions,replies,shares,total_interactions"})
        if si and "data" in si:
            for m in si["data"]:
                vals = m.get("values", [{}])
                v = vals[0].get("value", "N/A") if vals else "N/A"
                print("    " + str(m.get("name", "")) + ": " + str(v))
else:
    print("  No active stories (expire after 24h).")

# 5. PROFILE INSIGHTS (30 days)
print()
print(SEP)
print("  5. PROFILE INSIGHTS (Last 30 Days)")
print(SEP)
now = datetime.utcnow()
since = int((now - timedelta(days=30)).timestamp())
until = int(now.timestamp())
print("  Period: " + (now - timedelta(days=30)).strftime("%d/%m/%Y") + " to " + now.strftime("%d/%m/%Y"))

print()
print("  --- 5a. Daily Reach & Follower Count ---")
ins = api_get(IG_ID + "/insights", {"metric": "reach,follower_count", "period": "day", "since": str(since), "until": str(until)})
if ins and "data" in ins:
    for m in ins["data"]:
        vals = m.get("values", [])
        if vals:
            total = sum(v.get("value", 0) for v in vals)
            avg = total / len(vals)
            mx = max(v.get("value", 0) for v in vals)
            mn = min(v.get("value", 0) for v in vals)
            print()
            print("  " + str(m.get("title", m.get("name", ""))) + " (" + str(m.get("name", "")) + "):")
            print("    Total (30d):  " + fmt(total))
            print("    Daily Avg:    {:.1f}".format(avg))
            print("    Daily Max:    " + fmt(mx))
            print("    Daily Min:    " + fmt(mn))
            print("    Last 7 days:")
            for v in vals[-7:]:
                et = v.get("end_time", "")
                try:
                    dt2 = datetime.fromisoformat(et.replace("Z", "+00:00"))
                    ds = dt2.strftime("%d/%m/%Y")
                except: ds = et
                print("      " + ds + ": " + fmt(v.get("value", 0)))
else:
    print("  Could not fetch daily insights.")

print()
print("  --- 5b. Aggregate Metrics (total_value) ---")
agg_metrics = ["accounts_engaged", "total_interactions", "website_clicks", "profile_views", "follows_and_unfollows"]
for mn2 in agg_metrics:
    time.sleep(0.3)
    r = api_get(IG_ID + "/insights", {"metric": mn2, "metric_type": "total_value", "period": "day", "since": str(since), "until": str(until)})
    if r and "data" in r and len(r["data"]) > 0:
        tv = r["data"][0].get("total_value", {})
        val = tv.get("value", "N/A")
        vstr = fmt(val) if isinstance(val, (int, float)) else str(val)
        print()
        print("  " + mn2 + ": " + vstr)
        bds = tv.get("breakdowns", [])
        for bd in bds:
            dk = bd.get("dimension_keys", [])
            res = bd.get("results", [])
            if dk and res:
                print("    Breakdown by " + ", ".join(dk) + ":")
                sres = sorted(res, key=lambda x: x.get("value", 0), reverse=True)[:10]
                for rr in sres:
                    dv = rr.get("dimension_values", [])
                    print("      " + " / ".join(dv) + ": " + fmt(rr.get("value", 0)))
    else:
        print()
        print("  " + mn2 + ": Not available")

# 5c. Top 5 post insights
print()
print("  --- 5c. Detailed Insights for Top 5 Posts ---")
if posts:
    top5 = sorted(posts, key=lambda x: x.get("_eng", 0), reverse=True)[:5]
    for i, p in enumerate(top5, 1):
        pid = str(p.get("id", ""))
        print()
        print("  Top #" + str(i) + " - " + str(p.get("media_type", "?")) + " (" + str(p.get("timestamp", "?"))[:10] + ")")
        print("  Permalink: " + str(p.get("permalink", "N/A")))
        print("  Caption:   " + trunc(p.get("caption", ""), 150))
        print("  Basic:     Likes=" + str(p.get("like_count", 0)) + ", Comments=" + str(p.get("comments_count", 0)) + ", ER={:.3f}%".format(p.get("_er", 0)))
        time.sleep(0.3)
        pi = api_get(pid + "/insights", {"metric": "reach,likes,comments,shares,saved,total_interactions"})
        if pi and "data" in pi:
            idict = {}
            for m in pi["data"]:
                vals = m.get("values", [{}])
                idict[m.get("name", "")] = vals[0].get("value", 0) if vals else 0
            parts = []
            for k in ["reach", "likes", "comments", "shares", "saved", "total_interactions"]:
                parts.append(k.capitalize() + "=" + fmt(idict.get(k, "N/A")))
            print("  Insights:  " + ", ".join(parts))
            reach = idict.get("reach", 0)
            if reach and isinstance(reach, (int, float)) and reach > 0:
                ti = idict.get("total_interactions", 0)
                if isinstance(ti, (int, float)):
                    print("  True ER (interactions/reach): {:.2f}%".format(ti / reach * 100))
        else:
            print("  (Could not fetch detailed insights)")

# FINAL SUMMARY
print()
print()
print(SEP)
print("  SUMMARY FOR PROFILE AUDIT")
print(SEP)
if posts and profile:
    if avg_er < 1.5: bs = "(BELOW benchmark)"
    elif avg_er < 3.0: bs = "(GOOD)"
    else: bs = "(EXCELLENT)"
    print()
    print("  Account:             @" + str(profile.get("username", "clubpetro")) + " (" + str(profile.get("name", "ClubPetro")) + ")")
    print("  Followers:           " + fmt(profile.get("followers_count", 0)))
    print("  Following:           " + fmt(profile.get("follows_count", 0)))
    print("  Total Posts:         " + fmt(profile.get("media_count", 0)))
    print("  Avg Likes:           {:.1f}".format(avg_lk))
    print("  Avg Comments:        {:.1f}".format(avg_cm))
    print("  Avg ER:              {:.3f}%".format(avg_er))
    if best: print("  Best Post ER:        {:.3f}%".format(best.get("_er", 0)))
    if worst: print("  Worst Post ER:       {:.3f}%".format(worst.get("_er", 0)))
    print()
    print("  Benchmark B2B IG:")
    print("    ER > 1.5%  = Good")
    print("    ER > 3.0%  = Excellent")
    print("    Current:     {:.3f}% ".format(avg_er) + bs)
print()
print(SEP)
print("  END OF AUDIT")
print(SEP)
