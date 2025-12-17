import tweepy
import os

# GitHub Secrets から環境変数として読み込む
API_KEY = os.getenv("APIKEY")
API_SECRET = os.getenv("APIKEYSECRET")
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")
ACCESS_SECRET = os.getenv("ACCESSTOKENSECRET")

print("DEBUG API_KEY:", API_KEY)

auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
)
api = tweepy.API(auth)

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

    # if previous_tweet:
    #     previous_tweet = api.update_status(
    #         status=tweet,
    #         in_reply_to_status_id=previous_tweet.id,
    #         auto_populate_reply_metadata=True
    #     )
    # else:
    #     previous_tweet = api.update_status(status=tweet)

print("all tweet sent!")
