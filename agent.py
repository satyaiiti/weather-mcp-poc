# agent.py
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from mcp_tool import get_weather

load_dotenv()  # Loads .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful assistant that ONLY answers weather-related questions. "
        "If the user asks anything outside of weather, reply with: "
        "'❌ Sorry, I can only help with weather-related questions.'"
        "If user asks any hi,hello query reply with some greetings "
        "If user not giving city or location asks for weather reply with '❌ Please provide a city or location.'"
    )
}

def ask_weather_agent(user_query: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[SYSTEM_PROMPT,
        {"role": "user", "content": user_query}],
        tools=tool_schema,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        if tool_call.function.name == "get_weather":
            args = json.loads(tool_call.function.arguments)
            return get_weather(args["city"])

    return message.content or "🤖 No valid response."
