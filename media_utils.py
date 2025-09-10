#!/usr/bin/env python3
"""
Media utilities for handling different file types and upload methods
"""
import os
import mimetypes
import tweepy
from pathlib import Path


def get_media_type(file_path):
    """Determine the media type of a file"""
    file_ext = os.path.splitext(file_path)[1].lower()

    # Image types
    if file_ext in [".jpg", ".jpeg", ".png"]:
        return "image"
    # Video types
    elif file_ext in [".mp4", ".mov", ".avi", ".mkv"]:
        return "video"
    # GIF types
    elif file_ext in [".gif"]:
        return "gif"
    else:
        return "unknown"


def upload_media_file(tweepy_api, file_path):
    """Upload a media file using the appropriate method"""
    try:
        media_type = get_media_type(file_path)
        file_size = os.path.getsize(file_path)

        print(f"Uploading {media_type} file: {file_path} ({file_size} bytes)")

        if media_type == "image":
            # For images, use simple_upload
            post = tweepy_api.simple_upload(file_path)
        elif media_type in ["video", "gif"]:
            # For videos and GIFs, use media_upload with chunked upload
            # Twitter requires chunked upload for files > 5MB
            if file_size > 5 * 1024 * 1024:  # 5MB
                post = tweepy_api.media_upload(file_path, chunked=True)
            else:
                post = tweepy_api.media_upload(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        # Extract media ID from the response
        text = str(post)
        media_id = None

        # Try different patterns to extract media ID
        import re

        patterns = [
            r"media_id=(.+?),",
            r"media_id=(.+)",
            r"'media_id': '(.+?)'",
            r'"media_id": "(.+?)"',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                media_id = match.group(1)
                break

        if not media_id:
            print(f"Could not extract media ID from response: {text}")
            return None

        print(f"Successfully uploaded media with ID: {media_id}")
        return media_id

    except Exception as e:
        print(f"Error uploading media {file_path}: {e}")
        return None


def validate_media_file(file_path):
    """Validate if a file is suitable for Twitter upload"""
    if not os.path.exists(file_path):
        return False, "File does not exist"

    if not os.path.isfile(file_path):
        return False, "Path is not a file"

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        return False, "File is empty"

    # Twitter file size limits
    max_image_size = 5 * 1024 * 1024  # 5MB for images
    max_video_size = 512 * 1024 * 1024  # 512MB for videos

    media_type = get_media_type(file_path)

    if media_type == "image" and file_size > max_image_size:
        return False, f"Image too large: {file_size} bytes (max: {max_image_size})"

    if media_type in ["video", "gif"] and file_size > max_video_size:
        return False, f"Video too large: {file_size} bytes (max: {max_video_size})"

    if media_type == "unknown":
        return False, "Unsupported file type"

    return True, "Valid"


def get_random_media_file(medias_folder="medias"):
    """Get a random media file from the medias folder"""
    import random
    import glob

    if not os.path.exists(medias_folder):
        return None

    # Get all media files
    media_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.mp4", "*.mov"]
    media_files = []

    for ext in media_extensions:
        media_files.extend(glob.glob(os.path.join(medias_folder, ext)))
        media_files.extend(glob.glob(os.path.join(medias_folder, ext.upper())))

    if not media_files:
        return None

    # Filter valid files
    valid_files = []
    for file_path in media_files:
        is_valid, message = validate_media_file(file_path)
        if is_valid:
            valid_files.append(file_path)
        else:
            print(f"Skipping invalid file {file_path}: {message}")

    if not valid_files:
        return None

    return random.choice(valid_files)
