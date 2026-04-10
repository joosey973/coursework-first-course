from dotenv import load_dotenv

import os

load_dotenv()
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '')