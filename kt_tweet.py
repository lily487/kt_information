import os
import sys
import tweepy

# ==============================
# 設定
# ==============================
FILE_PATH = "info_tweet.txt"
MAX_LEN = 140   # 280にしたければ 280 に変更

# ==============================
# 文字コード安全読み込み
# ==============================
def read_text_safely(path):
    for enc in ("utf-8", "utf-8-sig", "cp932"):
        try:
            with open(path, "r", encoding=enc) as f:
                text = f.read()
            print(f"✅ info_tweet.txt read with encoding: {enc}")
            return text
        except UnicodeDecodeError:
            continue

    print("❌ info_tweet.txt をどの文字コードでも読めませんでした")
    sys.exit(1)

# ==============================
# Twitter 認証（OAuth1）
# ==============================
def twitter_auth():
    required_envs = [
        "APIKEY",
        "APIKEYSECRET",
        "ACCESSTOKEN",
        "ACCESSTOKENSECRET",
    ]

    missing = [k for k in required_envs if not os.getenv(k)]
    if missing:
        print("❌ 環境変数が不足しています:", ", ".join(missing))
        sys.exit(1)

    auth = tweepy.OAuth1UserHandler(
        os.getenv("APIKEY"),
        os.getenv("APIKEYSECRET"),
        os.getenv("ACCESSTOKEN"),
        os.getenv("ACCESSTOKENSECRET"),
    )
    return tweepy.API(auth)

# ==============================
# メイン処理
# ==============================
def main():
    if not os.path.exists(FILE_PATH):
        print("❌ info_tweet.txt が見つかりません")
        sys.exit(1)

    api = twitter_auth()
    text = read_text_safely(FILE_PATH)

    parts = [p.strip() for p in text.split("---") if p.strip()]

    tweets = []
    current = ""

    for part in parts:
        # 単体で制限超えた場合は強制分割
        if len(part) > MAX_LEN:
            if current:
                tweets.append(current)
                current = ""

            buf = ""
            for ch in part:
                if len(buf) >= MAX_LEN:
                    tweets.append(buf)
                    buf = ""
                buf += ch
            if buf:
                tweets.append(buf)
            continue

        if not current:
            current = part
        elif len(current) + 2 + len(part) <= MAX_LEN:
            current += "\n\n" + part
        else:
            tweets.append(current)
            current = part

    if current:
        tweets.append(current)

    # ==============================
    # ツイート送信（スレッド）
    # ==============================
    previous_id = None

    for i, tweet in enumerate(tweets, 1):
        print(f"🐦 Tweet {i}/{len(tweets)}")
        if previous_id:
            res = api.update_status(
                status=tweet,
                in_reply_to_status_id=previous_id,
                auto_populate_reply_metadata=True
            )
        else:
            res = api.update_status(status=tweet)

        previous_id = res.id

    print("🎉 全ツイート完了")

if __name__ == "__main__":
    main()
