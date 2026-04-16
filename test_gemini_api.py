import os
import time
import subprocess
import requests
from google import genai
from google.genai import errors


def get_gh_token():
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except:
        return None


def fetch_gemini_key(repo_full_name, var_name):
    """Fetches the variable from GitHub's Repo API."""
    token = get_gh_token()
    if not token: return None

    url = f"https://api.github.com/repos/{repo_full_name}/actions/variables/{var_name}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        val = response.json().get("value")
        # SUCCESS PRINT STATEMENT
        print(f"✅ [SUCCESS] Retrieved {var_name} key from GitHub Cloud.")
        return val
    else:
        print(f"❌ GitHub API Error {response.status_code}: {response.json().get('message')}")
        return None

def call_gemini_with_retry(client, model_id, prompt, max_retries=2):
    """Retries the call if the server is busy (503)."""
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(model=model_id, contents=prompt)
        except errors.ServerError as e:
            if "503" in str(e) and attempt < max_retries - 1:
                wait = (2 ** attempt) + 1  # Exponential backoff: 1s, 3s, 5s...
                print(f"⚠️ Server busy. Retrying in {wait}s... (Attempt {attempt + 1})")
                time.sleep(wait)
            else:
                raise e


def main():
    REPO = "RoboSathi/coding_agent"
    api_key = fetch_gemini_key(REPO, "GEMINI_API_KEY_LOCAL_DEV")

    if api_key:
        client = genai.Client(api_key=api_key)
        # Use the 2026 stability king: Flash-Lite
        MODEL = "gemini-3.1-flash-lite-preview"

        print(f"🔄 Connected. Using {MODEL}...")
        try:
            response = call_gemini_with_retry(client, MODEL, "Hello who are you?")
            print(f"\n🤖 Gemini: {response.text}")
        except Exception as e:
            print(f"❌ Critical Error: {e}")
    else:
        print("❌ Could not fetch key from GitHub.")


if __name__ == "__main__":
    main()