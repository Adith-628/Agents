import os
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
co = cohere.Client(os.getenv("COHERE_API_KEY"))
stability_api_key = os.getenv("STABILITY_API_KEY") 