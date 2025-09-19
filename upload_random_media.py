import tweepy
import requests
import re
import time
import random

tw_api_key = "fSK4IQjD8Ipg7fGey3EW3TAAL"
tw_api_secret = "Q4iP2Mfm2U39FFCAbtd2rIzN2ZrYD0e0pPnRtqQZlmBZheXz9Z"
tw_access_token = "1965827120837570564-ZO6ovPq7Oa75rxnrNQHYK3JR2gIRJ2"
tw_access_secret = "sk43NOwJ570f7TpBCpAbZeWI1hrNlHHuqOIyUC6pdrLFh"
tw_client_id = "NnROMG9WbGxCQWh5SkhVakR6LWk6MTpjaQ"
tw_client_secret = "dLHJjOenfAkynAlG5p4YK3s0CaixNyGrmUDAF5na8vpCnAN1vP"


def upload_random_media():
    import os
    import glob

    try:
        tweepy_auth = tweepy.OAuth1UserHandler(
            consumer_key=tw_api_key,
            consumer_secret=tw_api_secret,
            access_token=tw_access_token,
            access_token_secret=tw_access_secret,
        )
        tweepy_api = tweepy.API(tweepy_auth)
        media_id = None

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

        print(f"Found {len(media_files)} media files to upload:")
        for file in media_files:
            print(f"  - {file}")

        media_file = random.choice(media_files)
        media_id = None
        try:
            print(f"Uploading: {media_file}")

            # Get file extension to determine media type
            file_ext = os.path.splitext(media_file)[1].lower()

            # Upload the media file with proper media type
            if file_ext in [".jpg", ".jpeg", ".png"]:
                # For images, use simple_upload
                post = tweepy_api.simple_upload(media_file)
            elif file_ext in [".gif"]:
                # For GIFs, use simple_upload (they're treated as images)
                post = tweepy_api.simple_upload(media_file)
            elif file_ext in [".mp4", ".mov"]:
                # For videos, use media_upload without chunked upload for smaller files
                file_size = os.path.getsize(media_file)
                if file_size > 15 * 1024 * 1024:  # 15MB threshold
                    post = tweepy_api.media_upload(media_file, chunked=True)
                else:
                    post = tweepy_api.media_upload(media_file)
            else:
                raise Exception(
                    f"Unsupported file type: {file_ext} - skipping {media_file}"
                )

            text = str(post)
            media_id = re.search("media_id=(.+?),", text).group(1)
            print(f"Successfully uploaded {media_file} with ID: {media_id}")

        except Exception as e:
            print(f"Error uploading {media_file}: {e}")

        return media_id

    except Exception as e:
        print(f"Error in upload_media: {e}")
        raise e


# print(upload_random_media())
