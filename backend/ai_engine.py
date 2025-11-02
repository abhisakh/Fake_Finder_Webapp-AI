import os
import wikipedia
from google import genai
from google.genai import types
from backend.utils import load_env

# --- Load environment variables first ---
load_env()

# Retrieve the API key value immediately after loading the environment
# We know this is now successful thanks to our previous debug step.
API_KEY = os.getenv("GEMINI_API_KEY")

def get_article_from_wikipedia(title: str) -> str:
    """
    Fetch the full content of a Wikipedia article.
    """
    try:
        page = wikipedia.WikipediaPage(title=title)
        return page.content
    except (wikipedia.exceptions.PageError,
            wikipedia.exceptions.DisambiguationError) as e:
        print(f"⚠️ Wikipedia fetch error for '{title}': {e}")
        return ""

def generate_facts(article_content: str, level: str) -> str:
    """
    Generate 1 fake and 3 true statements using the Gemini API.
    """
    if not API_KEY:
         raise RuntimeError("CRITICAL: GEMINI_API_KEY value is missing despite loading.")

    try:
        # CRITICAL FIX: Explicitly pass the API_KEY to the client constructor
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize Gemini client even with explicit key. Details: {e}"
        )

    prompt = (
        f"# Article Content:\n{article_content}\n\n"
        f"# Difficulty: {level}\n\n"
        "Generate 4 statements based on the text:\n"
        "- 1 fake statement (False)\n"
        "- 3 true statements (True)\n\n"
        "# Rules\n"
        "- Sentences must not exceed 25 words.\n"
        "- The fake statement must be first.\n"
        "- Use the difficulty level to control subtlety.\n\n"
        "# Output Format (Strictly Adhere to this):\n"
        "(fake_sentence @ False) | (fact_1 @ True) | "
        "(fact_2 @ True) | (fact_3 @ True)"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7),
        )
        return response.text
    except Exception as e:
        # If the key is valid, this error is typically due to billing/quota issues
        # or a specific network block.
        print(f"❌ FATAL ERROR DURING GENERATE_FACTS API CALL: {e}")
        raise RuntimeError(f"Gemini API call failed: {e}. Check console for traceback.")
