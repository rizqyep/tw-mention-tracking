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
                    "content": "You are a helpful assistant that generates short, engaging replies to tweets. Keep replies under 80 characters.",
                },
                {
                    "role": "user",
                    "content": f"Generate a reply to the following tweet: {input_tweet}",
                },
            ],
            max_tokens=50,
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return content.strip() if content else "Thanks for the mention! 🙏"
    except Exception as e:
        print(f"Error generating content: {e}")
        raise e
