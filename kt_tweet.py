import os
import sys
import tweepy

# ==============================
# 設定
# ==============================
FILE_PATH = "info_tweet.txt"
MAX_LEN = 140   # 280にしたければ変更

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
# Twitter認証
# ==============================
def twitter_auth():
    try:
        auth = tweepy.OAuth1UserHandler(
            os.environ["API_KEY"],
            os.environ["API_SECRET"],
            os.environ["ACCESS_TOKEN"],
            os.environ["ACCESS_SECRET"],
        )
        return tweepy.API(auth)
    except KeyError as e:
        print(f"❌ 環境変数が不足しています: {e}")
        sys.exit(1)

# ==============================
# メイン処理
# ==============================
def main():
    api = twitter_auth()

    if not os.path.exists(FILE_PATH):
        print("❌ info_tweet.txt が見つかりません")
        sys.exit(1)

    text = read_text_safely(FILE_PATH)

    parts = [p.strip() for p in text.split("---") if p.strip()]

    tweets = []
    current = ""

    for part in parts:
        if len(part) > MAX_LEN:
            if current:
                tweets.append(current)
                current = ""

            buf = ""
            for ch in part:
                if len(buf) + 1 > MAX_LEN:
                    tweets.append(buf)
                    buf = ""
                buf += ch
            if buf:
                tweets.append(buf)
            continue

        if not current:
            current = part
        elif len(current) + 1 + len(part) <= MAX_LEN:
            current += "\n" + part
        else:
            tweets.append(current)
            current = part

    if current:
        tweets.append(current)

    # ==============================
    # ツイート実行
    # ==============================
    for i, tweet in enumerate(tweets, 1):
        print(f"🐦 Tweet {i}/{len(tweets)}")
        api.update_status(tweet)

    print("✅ 全ツイート完了")

if __name__ == "__main__":
    main()
