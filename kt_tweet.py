# import tweepy
# import os

# # GitHub Secrets から環境変数として読み込む
# API_KEY = os.getenv("APIKEY")
# API_SECRET = os.getenv("APIKEYSECRET")
# ACCESS_TOKEN = os.getenv("ACCESSTOKEN")
# ACCESS_SECRET = os.getenv("ACCESSTOKENSECRET")

# print("DEBUG",
#       API_KEY is not None,
#       API_SECRET is not None,
#       ACCESS_TOKEN is not None,
#       ACCESS_SECRET is not None)

# client = tweepy.Client(
#     consumer_key=API_KEY,
#     consumer_secret=API_SECRET,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_SECRET
# )

# # info_tweet.txt を読み込む
# if not os.path.exists("info_tweet.txt"):
#     print("file not found")
#     exit(0)

# with open("info_tweet.txt", "r", encoding="utf-8") as f:
#     # --- で分割して各パーツを取得
#     parts = f.read().split("---")

# final_tweets = []
# current_block = ""

# for part in parts:
#     part = part.strip()
#     if not part:
#         continue

#     # 1つのパーツ（---と---の間）自体が140文字を超えている場合の処理
#     if len(part) > 140:
#         # すでに溜まっているcurrent_blockがあれば先に追加
#         if current_block:
#             final_tweets.append(current_block)
#             current_block = ""
        
#         # 140文字ごとに強制分割して追加
#         for i in range(0, len(part), 140):
#             final_tweets.append(part[i:i+140])
#         continue

#     # 現在のブロックにこのパーツを足しても140文字以内かチェック
#     # +1 は区切りの改行分
#     if len(current_block) + len(part) + 2 <= 140:
#         current_block += ("\n\n" if current_block else "") + part
#     else:
#         # 超えるなら今のブロックを確定させて、新しいブロックを開始
#         final_tweets.append(current_block)
#         current_block = part

# # 最後に残ったブロックを追加
# if current_block:
#     final_tweets.append(current_block)

# # 実際にツイートする（スレッド形式）
# previous_tweet_id = None
# for tweet_text in final_tweets:
#     try:
#         if previous_tweet_id:
#             # 2回目以降：直前のツイートへのリプライとして投稿
#             response = client.create_tweet(
#                 text=tweet_text,
#                 in_reply_to_tweet_id=previous_tweet_id
#             )
#         else:
#             # 1回目：新規ツイート
#             response = client.create_tweet(text=tweet_text)
        
#         # 投稿に成功したら、そのIDを「次の返信先」として保存
#         previous_tweet_id = response.data['id']
#         print(f"Sent: {tweet_text[:15]}...")
        
#     except Exception as e:
#         print(f"Error: {e}")

# print("All tweets sent!")

import tweepy
import os

# ===== 設定 =====
MAX_LEN = 140

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

# info_tweet.txt を読み込む
if not os.path.exists("info_tweet.txt"):
    print("file not found")
    exit(0)

with open("info_tweet.txt", "r", encoding="utf-8") as f:
    parts = [p.strip() for p in f.read().split("---") if p.strip()]

# ===== ここが本体ロジック =====

header = parts[0]          # 🐸今日〜 + 【ライブ】
live_parts = parts[1:]     # 各ライブ

final_tweets = []

# 最初のツイートはヘッダ入り
current = header

for part in live_parts:
    # ライブ1本自体がMAX超えた場合（保険）
    if len(part) > MAX_LEN:
        # 先に今までの内容を確定
        if current:
            final_tweets.append(current)
            current = ""

        # 強制分割（基本起きない想定）
        for i in range(0, len(part), MAX_LEN):
            final_tweets.append(part[i:i + MAX_LEN])
        continue

    # 今のツイートにこのライブを足せるか？
    candidate = current + "\n\n" + part

    if len(candidate) <= MAX_LEN:
        # まだ入る → 同じツイートに詰める
        current = candidate
    else:
        # 入らない → 今のツイート確定、次はライブから
        final_tweets.append(current)
        current = part

# 残りを追加
if current:
    final_tweets.append(current)

# ===== ツイート投稿（スレッド） =====

previous_tweet_id = None

for tweet_text in final_tweets:
    try:
        if previous_tweet_id:
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=previous_tweet_id
            )
        else:
            response = client.create_tweet(text=tweet_text)

        previous_tweet_id = response.data["id"]
        print(f"Sent: {tweet_text.splitlines()[0]}")

    except Exception as e:
        print("Error while tweeting:")
        print(tweet_text)
        print(e)
        break

print("All tweets sent!")
