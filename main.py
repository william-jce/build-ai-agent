import os
import sys
from dotenv import load_dotenv
from google import genai



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = sys.argv
    if len(prompt) <= 1:
        print("no prompt provided")
        sys.exit(1)
    user_prompt = " ".join(prompt[1:])

    print("Hello from build-ai-agent!")
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=user_prompt
    )
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
