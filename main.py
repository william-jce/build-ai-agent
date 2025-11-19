import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbosity = "--verbose" in sys.argv
    prompt = sys.argv[1:]
    if not prompt:
        print("no prompt provided")
        sys.exit(1)

    user_prompt = ""
    for part in prompt:
        if not part.startswith("--"):
            user_prompt = part

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    print("Hello from build-ai-agent!")
    generate_response(client, messages, verbosity)

def generate_response(client, messages, verbosity):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages,
    )
    print(response.text)
    if verbosity == True:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
