#!/usr/bin/env python3
"""
Setup script to create medias folder and add sample content
"""
import os
import requests
from pathlib import Path

def create_medias_folder():
    """Create medias folder and add some sample content"""
    medias_folder = "medias"
    
    # Create medias folder
    if not os.path.exists(medias_folder):
        os.makedirs(medias_folder)
        print(f"Created {medias_folder} folder")
    else:
        print(f"{medias_folder} folder already exists")
    
    # Add some sample images (you can replace these with your own)
    sample_images = [
        {
            "url": "https://picsum.photos/400/300?random=1",
            "filename": "sample1.jpg"
        },
        {
            "url": "https://picsum.photos/400/300?random=2", 
            "filename": "sample2.jpg"
        },
        {
            "url": "https://picsum.photos/400/300?random=3",
            "filename": "sample3.jpg"
        }
    ]
    
    print("Downloading sample images...")
    for img in sample_images:
        try:
            response = requests.get(img["url"])
            if response.status_code == 200:
                filepath = os.path.join(medias_folder, img["filename"])
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {img['filename']}")
            else:
                print(f"Failed to download {img['filename']}")
        except Exception as e:
            print(f"Error downloading {img['filename']}: {e}")
    
    # List all files in medias folder
    print(f"\nFiles in {medias_folder} folder:")
    for file in os.listdir(medias_folder):
        filepath = os.path.join(medias_folder, file)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            print(f"  - {file} ({size} bytes)")

if __name__ == "__main__":
    create_medias_folder()
    print("\nSetup complete! You can now add your own media files to the 'medias' folder.")
    print("Supported formats: jpg, jpeg, png, gif, mp4, mov")
