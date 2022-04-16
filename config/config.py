import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_KURATOR = os.getenv("CHANNEL_KURATOR")
CHANNEL_NASTAVNIK = os.getenv("CHANNEL_NASTAVNIK")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
DATABASE = os.getenv("DATABASE")
DBHOST = os.getenv("DBHOST")

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{DBHOST}/{DATABASE}"

if __name__ == '__main__':
    print(DBHOST)
