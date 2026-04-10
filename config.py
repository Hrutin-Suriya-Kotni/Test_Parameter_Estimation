# Configuration settings for the CRED conversation analysis project
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Local OpenChat API settings
OPENCHAT_API_URL = "http://192.168.30.239:8000/chat"
OPENCHAT_MODEL = "openchat/openchat-3.5-1210"
OPENCHAT_MAX_TOKENS = 512  # Reduced for faster inference and focused responses
OPENCHAT_TEMPERATURE = 0.1  # Slightly increased for better JSON formatting while keeping consistency

# Google Gemini API settings (loaded from .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# File paths
# Get the absolute path to the project root directory (where this config.py file is located)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CRED_DATA_PATH = os.path.join(PROJECT_ROOT, "data")  # Absolute path to data directory
# Primary conversation dataset (CSV/TSV/XLSX)
# This is what the test runners consume via `data_loader.load_all_conversations()`.
# Defaults to the concatenated TSV produced by `concat_transcripts_by_request.py` when present.
CRED_FILE_NAME = "concatenated_by_request.tsv"

# Excel settings (kept for backward compatibility if you switch back to xlsx)
CRED_TRANSCRIPT_SHEET = "Transcript"
CRED_PRIMARY_INFO_SHEET = "Primary Info"

# Processing settings
REQUEST_TIMEOUT = 60
RETRY_DELAY = 2  # seconds between API calls 