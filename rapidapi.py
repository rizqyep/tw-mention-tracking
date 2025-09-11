import re
import json
import urllib.parse
import tweepy
from twscrape import API, Tweet, gather
import tweetdb
import time

global api
api = API()
global tdb
tdb = tweetdb.DB()
mention_tracked_user = "m_hovardas"
rapid_api_key = "14da4ca027msh1426d7eef136643p1f279cjsnfc7150db6cad"
twsession = "H4sIAJaBwmgC/21SS2/iMBCuymNBlaIImtACoRsnIVB6sJIxNRTCX7ETHCfZU8QeWikLf31x4EC165M9+l4z49dDhF1vpXnRGnaHX+WB7bMkjTkTlURNRsYQz/yN2+w3nmy9MQ31FZu4I4ktf+Ynkr1YfnD4U96KaAgCBzylZcRkGDZ+cHu+x+Phw0v40APQ+7NhqD/5zc7jqDvw+NjESTd9NJTMmtQ8a8B6HWezdbOuGUWTVedpZNl05C92cxrSO96WzXDp5S1FUcaRQxfYo1HdQB+wA06p/+8Mugt9ermOn3tzG+4Nky2tF2u5+gE5ScVqK9fid2w0muOBmOt3Fgqhv2rdN5wevbNH3jwy2zB7doxw70HyYZto3TYG7TwZqCwEfBqARonKkaYkTokEHAu5z0msAMGWws7TXPcCESSXggd5FQRSViIgWRVmIq0E4TJjaZzt3+GGhsmFxrEUGcigkoznlXjnvMqCEFcACd8TxrKzqKItXUDezWYzKbnI+JkU8yxj+5QplIvA0fDybKBArSn1PHD0HXEiSo6Mn3Jx4pUDW8AITrz8is98wc+ncir+Wd4/V1xYR8bKL2PSm4wnxaVSXF+JECd24ieWnRjjBS8KViQ84Z/KG82QBxvtewQDb326PiaKVn5ZdOfOi7JZlNdMJWNFeREv+y7dkuN3i1qYUGRv8UxDdAF170LwecySei4R0nxwVDnmN+M919D1D/3Tdg2LojVVaq9v17Ht8KZW32iryMcOwUjhbIzQNHLqVXU+sGkMF+bP1uHtLzyHXt5rAwAA"


def parse_cookie_json(cookie_json: str):
    try:
        cookies = json.loads(cookie_json)

        # Step 2: Extract name=value pairs and decode URL-encoded values
        cookie_pairs = []
        for cookie in cookies:
            name = cookie["name"]
            value = cookie["value"]

            # Decode URL-encoded values
            try:
                decoded_value = urllib.parse.unquote(value)
                print(f"Cookie {name}: {value} -> {decoded_value}")
            except:
                decoded_value = value
                print(f"Cookie {name}: {value} (no decoding needed)")

            cookie_pairs.append(f"{name}={decoded_value}")

        # Step 3: Join all cookie pairs
        cookie_header = "; ".join(cookie_pairs)
        return cookie_header
    except Exception as e:
        print(f"Error parsing cookie json: {e}")
        return None


async def get_mentions():
    """
    Get followings for a specific user
    Returns: {"username": true} format
    """
    try:
        cookie_json = """[
{
    "domain": ".x.com",
    "expirationDate": 1757576446.250669,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__cf_bm",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "T8XeKGzylHWmbp3iEKSwZjL1ubeWmEp2u7TI.g7FsIo-1757574646-1.0.1.1-FBcDHf_GdxWeB.rVwP8jgDPEGRG_HU0DcybiC1EAgJVm9d5Se6pOUUkX1.2wESSwWk9mbOVzylUQnnpEl8aweb7bT76PO7e0ZtZ_yZjUtcA",
    "id": 1
},
{
    "domain": ".x.com",
    "expirationDate": 1792132176,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__cuid",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "2d1ccd02f59c4f90bab536b6c1a37458",
    "id": 2
},
{
    "domain": ".x.com",
    "expirationDate": 1792131158.843245,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1195100199.1757492251",
    "id": 3
},
{
    "domain": ".x.com",
    "expirationDate": 1792131158.915865,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_KEWZ1G5MB3",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS2.2.s1757571158$o2$g0$t1757571158$j60$l0$h0",
    "id": 4
},
{
    "domain": ".x.com",
    "expirationDate": 1792131151.157801,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_RJGMY4G45L",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS2.1.s1757571149$o3$g0$t1757571151$j58$l0$h0",
    "id": 5
},
{
    "domain": ".x.com",
    "expirationDate": 1757657558,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_gid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.252191106.1757492251",
    "id": 6
},
{
    "domain": ".x.com",
    "expirationDate": 1757604605.547248,
    "hostOnly": false,
    "httpOnly": true,
    "name": "att",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1-iJJVnz1PUVHfRGlLEFSSnlLGdl8AB1nGl1OwfsI0",
    "id": 7
},
{
    "domain": ".x.com",
    "expirationDate": 1792078204.900764,
    "hostOnly": false,
    "httpOnly": true,
    "name": "auth_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "48ba808a20bd6a85dd107fb780d819434a1abb9e",
    "id": 8
},
{
    "domain": ".x.com",
    "expirationDate": 1792078205.247869,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ct0",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "089dc63ab292651e38cb98f68bd9cd55d1a586528a838a24d0c45813904125a6bd8173840d2ca8382fa1cdba6ff2beb8444d4ce37a00ebec63d18a13524c3134fe5f38f94bb4f951f5ab7763c3a986f2",
    "id": 9
},
{
    "domain": ".x.com",
    "expirationDate": 1792052213.139826,
    "hostOnly": false,
    "httpOnly": false,
    "name": "des_opt_in",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "Y",
    "id": 10
},
{
    "domain": ".x.com",
    "expirationDate": 1792078160.837448,
    "hostOnly": false,
    "httpOnly": false,
    "name": "dnt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 11
},
{
    "domain": ".x.com",
    "expirationDate": 1792078161.237412,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175751816111755278",
    "id": 12
},
{
    "domain": ".x.com",
    "expirationDate": 1792132176.379673,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_ads",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175751816111755278",
    "id": 13
},
{
    "domain": ".x.com",
    "expirationDate": 1792132176.379778,
    "hostOnly": false,
    "httpOnly": false,
    "name": "guest_id_marketing",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1%3A175751816111755278",
    "id": 14
},
{
    "domain": ".x.com",
    "expirationDate": 1792078204.900452,
    "hostOnly": false,
    "httpOnly": true,
    "name": "kdt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "iAlN6pxNxwOtF6dWj22aDpJuJqmN1vRAjnVLcSwY",
    "id": 15
},
{
    "domain": ".x.com",
    "expirationDate": 1792078161.156966,
    "hostOnly": false,
    "httpOnly": false,
    "name": "personalization_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "v1_igtnv8ubsdfRgtjBLMY/yA==",
    "id": 16
},
{
    "domain": ".x.com",
    "expirationDate": 1789107194,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "%7B%22distinct_id%22%3A%22019932b2-8b9d-7ab7-ba28-2e1059eff96f%22%2C%22%24sesid%22%3A%5B1757571194214%2C%2201993767-dd2d-760a-9cb1-035a3f76896c%22%2C1757571177773%5D%7D",
    "id": 17
},
{
    "domain": ".x.com",
    "expirationDate": 1789108181.988464,
    "hostOnly": false,
    "httpOnly": false,
    "name": "twid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "u%3D1720376180942237696",
    "id": 18
},
{
    "domain": "x.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "lang",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "en",
    "id": 19
}
]"""
        print("parsing cookie json")
        cookies = parse_cookie_json(cookie_json)

        if not cookies:
            return {"error": "Failed to parse cookie json"}

        print("adding account")

        print("cookies", cookies)
        await api.pool.delete_inactive()
        await api.pool.add_account(
            username="itsdevkalteng",
            password="",
            email="",
            email_password="",
            cookies=cookies,
        )

        print("getting target mention")
        q = f"(@{mention_tracked_user}"

        # Use the Latest tab
        results = await gather(api.search(q, limit=10, kv={"product": "Latest"}))

        for tweet in results:
            # tweet is an SNScrape-like model
            print(
                f"Sender {tweet.user.username} is replying to {mention_tracked_user} with tweet id {tweet.id}"
            )
            print("Content: ", tweet.rawContent)

        return results
    except Exception as e:
        print(f"Error in get_mentions: {e}")
        return {"error": str(e)}


async def reply_mention(tweepy_api: tweepy.API, tweet_id: str, reply_text: str):
    try:
        tweepy_api.update_status(status=reply_text, in_reply_to_status_id=tweet_id)
    except Exception as e:
        print({"error": str(e)})
        return {"error": str(e)}


from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_content(input_tweet: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates short, engaging replies to tweets. Keep replies under 80 characters. if the tweet is empty or only a mention, then reply with a random cheerful words no more than 80 characters. Mix the language with natural human interaction language, no need to be strict english. make all lowercase",
                },
                {
                    "role": "user",
                    "content": f"Generate a reply to the following tweet: {input_tweet}",
                },
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return content.strip() if content else "Thanks for the mention! 🙏"
    except Exception as e:
        print(f"Error generating content: {e}")
        raise e


def get_tweet_id_from_mentioned_tweet(mentioned_tweet: Tweet):
    tweet_id = None
    if mentioned_tweet.inReplyToTweetIdStr:
        tweet_id = mentioned_tweet.inReplyToTweetIdStr
    elif mentioned_tweet.id_str:
        tweet_id = mentioned_tweet.id_str
    else:
        tweet_id = None
    return tweet_id


import random


def get_random_media():
    media_ids = ["1966093305529401344"]
    return random.choice(media_ids)


import requests


def create_tweet_with_rapid_api(tweet_id: str, tweet: str, media_id: str):
    try:

        data = {
            "tweet_text": tweet,
            "in_reply_to_tweet_id": tweet_id,
        }

        if media_id:
            data["media_id"] = media_id

        response = requests.post(
            "https://twttrapi.p.rapidapi.com/create-tweet",
            data=data,
            headers={
                "twttr-session": twsession,
                "x-rapidapi-key": f"{rapid_api_key}",
                "x-rapidapi-host": "twttrapi.p.rapidapi.com",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Error creating tweet with rapid api: {e}")
        return {"error": str(e)}


async def track_mention_and_reply():
    try:
        tdb = tweetdb.DB()
        tdb.setup_database()

        # Format the time in a friendly string format (e.g., "2025-02-23 14:30:00")
        print("getting mentions")
        mentioned_tweets = await get_mentions()

        mentioned_tweets = sorted(mentioned_tweets, key=lambda x: x.date, reverse=True)

        for mentioned_tweet in mentioned_tweets:
            tweet_id = get_tweet_id_from_mentioned_tweet(mentioned_tweet)
            if tweet_id == None:
                print("No tweet ID found to reply to")
                return
            if tdb.get_replied_tweet_id_by_tweet_id(tweet_id):
                print("Tweet already replied to")
                return

            print("Tweet Date: ", mentioned_tweet.date)

            comment = generate_content(mentioned_tweet.rawContent)
            print(f"Generated comment: {comment}")
            print("replying to tweet")

            print("uploading media")
            media_id = get_random_media()

            create_tweet_with_rapid_api(tweet_id, comment, media_id)
            print("Tweet replied !")
            tdb.store_replied_tweet_id(tweet_id)
            time.sleep(1)

    except Exception as e:
        print(f"Error in track_mention_and_reply: {e}")


"""
For Direct Run , use this code:

import asyncio
asyncio.run(track_mention_and_reply())
"""
