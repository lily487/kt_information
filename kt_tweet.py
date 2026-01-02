import tweepy
import os

# ===== Twitter API（GitHub Secrets から取得）=====
API_KEY = os.getenv("APIKEY")
API_SECRET = os.getenv("APIKEYSECRET")
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")
ACCESS_SECRET = os.getenv("ACCESSTOKENSECRET")

print("DEBUG ENV:",
      API_KEY is not None,
      API_SECRET is not None,
      ACCESS_TOKEN is not None,
      ACCESS_SECRET is not None)

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# ===== info_tweet.txt 読み込み =====
if not os.path.exists("info_tweet.txt"):
    print("file not found")
    exit(1)

with open("info_tweet.txt", "r", encoding="utf-8") as f:
    parts = f.read().split("---")

# ===== ツイート組み立て =====
final_tweets = []
current_block = ""

for part in parts:
    part = part.strip()
    if not part:
        continue

    # part = 1ライブ分
    block = part

    # 単体で140字超えた場合（保険）
    if len(block) > 140:
        if current_block:
            final_tweets.append(current_block)
            current_block = ""

        for i in range(0, len(block), 140):
            final_tweets.append(block[i:i+140])
        continue

    # 今のツイートに追加できるか？
    if not current_block:
        current_block = block
    elif len(current_block) + len(block) + 2 <= 140:
        # ライブ間は必ず1行空ける
        current_block += "\n\n" + block
    else:
        final_tweets.append(current_block)
        current_block = block

if current_block:
    final_tweets.append(current_block)

# ===== デバッグ表示 =====
print("\n===== GENERATED TWEETS =====")
for i, t in enumerate(final_tweets):
    print("-----")
    print(f"TWEET {i+1}")
    print(t)
    print("LEN =", len(t))

# ===== ツイート投稿（スレッド）=====
previous_tweet_id = None

for i, tweet_text in enumerate(final_tweets):
    try:
        if previous_tweet_id:
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=previous_tweet_id
            )
        else:
            response = client.create_tweet(text=tweet_text)

        if response.data is None:
            raise Exception("Tweet failed (no response data)")

        previous_tweet_id = response.data["id"]
        print(f"✅ Sent tweet {i+1}")

    except Exception as e:
        print(f"❌ Error at tweet {i+1}:", e)
        break

print("All tweets sent!")
