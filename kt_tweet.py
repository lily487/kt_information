import tweepy
import os
import sys

# ===== Twitter API（GitHub Secrets / ローカルでは None）=====
API_KEY = os.getenv("APIKEY")
API_SECRET = os.getenv("APIKEYSECRET")
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")
ACCESS_SECRET = os.getenv("ACCESSTOKENSECRET")

print("DEBUG ENV:",
      API_KEY is not None,
      API_SECRET is not None,
      ACCESS_TOKEN is not None,
      ACCESS_SECRET is not None)

# ===== info_tweet.txt 読み込み（UTF-8 固定）=====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "info_tweet.txt")

if not os.path.exists(FILE_PATH):
    print("❌ file not found:", FILE_PATH)
    sys.exit(1)

try:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        parts = f.read().split("---")
except UnicodeDecodeError as e:
    print("❌ Encoding error while reading info_tweet.txt")
    print(e)
    sys.exit(1)

# ===== ツイート組み立て =====
final_tweets = []
current_block = ""

for part in parts:
    part = part.strip()
    if not part:
        continue

    block = part

    # 単体で140字超えた場合（保険）
    if len(block) > 140:
        if current_block:
            final_tweets.append(current_block)
            current_block = ""

        for i in range(0, len(block), 140):
            final_tweets.append(block[i:i+140])
        continue

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

# ===== プレビュー表示 =====
print("\n==============================")
print("  GENERATED TWEETS (PREVIEW)")
print("==============================\n")

for i, tweet in enumerate(final_tweets, start=1):
    print(f"--- TWEET {i} ----------------")
    print(tweet)
    print(f"\n[LENGTH: {len(tweet)}]")
    print("------------------------------\n")

print(f"Total tweets: {len(final_tweets)}")
print("↑ この内容が実際に投稿される想定です\n")

# ===== APIキーが無い場合はここで終了（ローカル確認用）=====
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    print("⚠ APIキーが未設定のため、ツイート送信はスキップします")
    sys.exit(0)

# ===== ツイート投稿 =====
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

previous_tweet_id = None

for i, tweet_text in enumerate(final_tweets, start=1):
    try:
        if previous_tweet_id:
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=previous_tweet_id
            )
        else:
            response = client.create_tweet(text=tweet_text)

        if response.data is None:
            raise Exception(f"No response data: {response}")

        previous_tweet_id = response.data["id"]
        print(f"✅ Sent tweet {i}")

    except Exception as e:
        print(f"❌ Error at tweet {i}: {e}")
        sys.exit(1)

print("🎉 All tweets sent successfully!")
