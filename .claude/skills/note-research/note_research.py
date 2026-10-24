# note有料記事リサーチ: キーワードごとに検索し、有料記事のみスキ数順で出力
import csv, json, time, urllib.parse, urllib.request

import argparse

DEFAULT = {"育児": ["育児", "子育て"], "勉強": ["勉強", "勉強法", "資格"], "旅行": ["旅行", "旅"]}
ap = argparse.ArgumentParser()
ap.add_argument("--genre", action="append", metavar="ジャンル=語1,語2",
                help="例: --genre 育児=育児,子育て (省略時は育児・勉強・旅行)")
ap.add_argument("--min-likes", type=int, default=0)
ap.add_argument("--pages", type=int, default=10, help="1語あたりのページ数(1ページ20件)")
ap.add_argument("--out", default="note_paid.csv")
args = ap.parse_args()
KEYWORDS = dict((g.split("=")[0], g.split("=")[1].split(",")) for g in args.genre) if args.genre else DEFAULT
MIN_LIKES, PAGES = args.min_likes, args.pages

def search(q, start):
    url = "https://note.com/api/v3/searches?" + urllib.parse.urlencode(
        {"context": "note", "q": q, "size": 20, "start": start, "sort": "like"})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]["notes"]["contents"]

rows, seen = [], set()
for genre, words in KEYWORDS.items():
    for w in words:
        for p in range(PAGES):
            items = search(w, p * 20)
            if not items:
                break
            for n in items:
                if n["key"] in seen or not n.get("price"):
                    continue
                seen.add(n["key"])
                likes = n.get("like_count", 0)
                if likes < MIN_LIKES:
                    continue
                u = n.get("user", {})
                rows.append({
                    "ジャンル": genre, "キーワード": w, "タイトル": n.get("name"),
                    "価格": n.get("price"), "スキ数": likes,
                    "コメント数": n.get("comment_count", 0),
                    "著者": u.get("nickname"), "フォロワー": u.get("follower_count"),
                    "投稿日": (n.get("publish_at") or "")[:10],
                    "推定売上指標": likes * n.get("price", 0),
                    "URL": f"https://note.com/{u.get('urlname')}/n/{n['key']}",
                })
            time.sleep(1)

rows.sort(key=lambda r: r["スキ数"], reverse=True)
out = args.out
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["empty"])
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)}件 → {out}")
