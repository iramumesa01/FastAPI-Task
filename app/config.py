import os
from dotenv import load_dotenv


load_dotenv()


POSTCODE = os.getenv("POSTCODE", "12345")  