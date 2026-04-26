"""
NOTE: You no longer need to run this script!
MetaBot now auto-logs in to the sandbox using admin credentials.

Just set your GEMINI_API_KEY in .env and run:
    uvicorn main:app --reload --port 8000

This script is kept here only if you want to manually test the sandbox connection.
"""

import requests

SANDBOX_URL = "https://sandbox.open-metadata.org"
EMAIL = "admin@open-metadata.org"
PASSWORD = "Admin@1234"


def test_connection():
    print("=" * 55)
    print("  MetaBot — Sandbox Connection Test")
    print("=" * 55)
    print(f"\n🌐 Connecting to: {SANDBOX_URL}")

    try:
        res = requests.post(
            f"{SANDBOX_URL}/api/v1/users/login",
            json={"email": EMAIL, "password": PASSWORD},
            headers={"Content-Type": "application/json"},
            timeout=15,
        )
        res.raise_for_status()
        token = res.json().get("accessToken", "")

        if token:
            print("✅ Sandbox connection successful!")
            print("✅ Auto-login is working.")
            print("\nYou only need GEMINI_API_KEY in your .env file.")
            print("MetaBot will handle OpenMetadata login automatically.")
        else:
            print("❌ Connected but no token returned.")
            print("Response:", res.json())

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect. Check your internet connection.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_connection()
