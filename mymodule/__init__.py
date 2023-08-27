__import__("pysqlite3")
import sys

from dotenv import load_dotenv

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
load_dotenv()
