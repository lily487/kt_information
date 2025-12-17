import tweepy
import os

# GitHub Secrets から環境変数として読み込む
API_KEY = os.getenv("APIKEY")
API_SECRET = os.getenv("APIKEYSECRET")
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")
ACCESS_SECRET = os.getenv("ACCESSTOKENSECRET")

print("DEBUG",
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

tweets = []
current_tweet = ""

# info_tweet.txt を読み込む
with open("info_tweet.txt", "r", encoding="utf-8") as f:
    lines = f.read().split("---")

    for part in lines:
        part = part.strip()
        if not part:
            continue

        # 140文字以内に分割
        if len(current_tweet) + len(part) + 1 < 140:
            current_tweet += ("\n" if current_tweet else "") + part
        else:
            tweets.append(current_tweet)
            current_tweet = part

    if current_tweet:
        tweets.append(current_tweet)

# 実際にツイートする（スレッド形式）
previous_tweet = None
for tweet in tweets:
    tweet = tweet.strip()
    if not tweet:
        continue

    if previous_tweet:
        response = client.create_tweet(
            text=tweet,
            in_reply_to_tweet_id=previous_tweet
        )
    else:
        response = client.create_tweet(text=tweet)
        previous_tweet = response.data['id'] 

print("all tweet sent!")
