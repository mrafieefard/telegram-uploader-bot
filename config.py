from dotenv import load_dotenv
from decouple import config

load_dotenv()

TOKEN = config('TOKEN')
