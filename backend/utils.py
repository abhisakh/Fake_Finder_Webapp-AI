import os
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """
    Loads environment variables from the .env file located in the project root
    and includes debugging checks.
    """
    # Path to the current file (e.g., /path/to/project/backend/utils.py)
    current_file_path = Path(__file__).resolve()

    # Path to the root directory (parent of 'backend')
    # This navigates up two levels from utils.py to the project root: utils -> backend -> root
    root_dir = current_file_path.parent.parent

    # Full path to the .env file
    dotenv_path = root_dir / '.env'

    print(f"\n--- Environment Loading Check ---")
    print(f"Attempting to load .env from: {dotenv_path}")

    if dotenv_path.exists():
        # Load environment variables
        load_dotenv(dotenv_path=dotenv_path, override=True)
        print(f"✅ .env file found and loaded.")

        # Check for the key and obfuscate its value for safety
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            # Show the start and end of the key to confirm it was loaded
            obfuscated_key = api_key[:4] + '...' + api_key[-4:]
            print(f"✅ GEMINI_API_KEY successfully loaded: {obfuscated_key}")
        else:
            print(f"❌ GEMINI_API_KEY NOT found in environment after loading.")
            print(f"*** Action Needed: Please ensure your .env file contains: GEMINI_API_KEY=\"YOUR_KEY\" ***")

    else:
        print(f"❌ ERROR: .env file not found at: {dotenv_path}")
        # This will prevent the server from starting if the file is missing
        raise FileNotFoundError(
            "The .env file must be in the project root to load the API key."
        )

    print(f"---------------------------------\n")
