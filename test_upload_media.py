import tweepy
import requests
import re

tw_client_id = "Q0pzd1ZRM1dSWXN5aTJQTjVuazA6MTpjaQ"
tw_client_secret = "ELESYZg0qiuAbQ9giZaRNJocaVksEkoY-4JLNCPRGJjrley_HH"
tw_api_key = "qlt7cb4OMBm4HfsKX3hOPWYpE"
tw_api_secret = "rEZuTyTczhgepeC3bd133Y1l1aljpW9XTDEJU8BaeDluFss13M"
tw_access_token = "1720376180942237696-4oNllranYyFq4vBByLZXFX7GV0pZwY"
tw_access_secret = "gsXtTGgVicFwpmyHwGQGAtPIgyaLktascSnEp7eIOqtQ2"
tw_bearer_token = "AAAAAAAAAAAAAAAAAAAAAI874AEAAAAAFp3xTwxpKlVb7YPO%2BSxAHjk5Zx4%3DlXkScFqxkZHLdebKXGf3HPmxqWPBhcBRnY15B9Xnbolw487yQN"


def upload_media():
    import os
    import random
    import glob

    try:
        tweepy_auth = tweepy.OAuth1UserHandler(
            consumer_key=tw_api_key,
            consumer_secret=tw_api_secret,
            access_token=tw_access_token,
            access_token_secret=tw_access_secret,
        )
        tweepy_api = tweepy.API(tweepy_auth)

        # Create medias folder if it doesn't exist
        medias_folder = "medias"
        if not os.path.exists(medias_folder):
            os.makedirs(medias_folder)
            print(
                f"Created {medias_folder} folder. Please add some media files (jpg, png, gif, mp4) to it."
            )
            return []

        # Get all media files from the medias folder
        media_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.mp4", "*.mov"]
        media_files = []
        for ext in media_extensions:
            media_files.extend(glob.glob(os.path.join(medias_folder, ext)))
            media_files.extend(glob.glob(os.path.join(medias_folder, ext.upper())))

        if not media_files:
            print(
                f"No media files found in {medias_folder} folder. Please add some media files."
            )
            return []

        # Select a random media file
        selected_media = random.choice(media_files)
        print(f"Selected media: {selected_media}")

        # Get file extension to determine media type
        file_ext = os.path.splitext(selected_media)[1].lower()

        # Upload the selected media file with proper media type
        if file_ext in [".jpg", ".jpeg", ".png"]:
            # For images, use simple_upload
            post = tweepy_api.simple_upload(selected_media)
        elif file_ext in [".gif"]:
            # For GIFs, use simple_upload (they're treated as images)
            post = tweepy_api.simple_upload(selected_media)
        elif file_ext in [".mp4", ".mov"]:
            # For videos, use media_upload without chunked upload for smaller files
            file_size = os.path.getsize(selected_media)
            if file_size > 15 * 1024 * 1024:  # 15MB threshold
                post = tweepy_api.media_upload(selected_media, chunked=True)
            else:
                post = tweepy_api.media_upload(selected_media)
        else:
            print(f"Unsupported file type: {file_ext}")
            return []

        text = str(post)
        media_id = re.search("media_id=(.+?),", text).group(1)
        print(f"Successfully uploaded media with ID: {media_id}")
        return ["{}".format(media_id)]
    except Exception as e:
        print(f"Error uploading media: {e}")
        raise e


upload_media()
