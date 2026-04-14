
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "You are a fraud detection agent. Is a transaction of ₹95,000 sent to an unknown account suspicious?"
        }
    ]
)

print(message.content[0].text)