import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY is missing.")

genai.configure(api_key=GOOGLE_API_KEY)

# List available models
print("📋 Available Models:")
print("=" * 50)

try:
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f"✅ {model.name}")
except Exception as e:
    print(f"❌ Error listing models: {e}")
