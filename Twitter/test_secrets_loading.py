from dotenv import load_dotenv
import os

load_dotenv()

username = os.environ['X_USERNAME']
email = os.environ['X_EMAIL']
password = os.environ['X_PASSWORD']

print(username, email, password)
assert username is not None
assert email is not None
assert password is not None