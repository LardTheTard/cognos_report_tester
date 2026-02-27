import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

XSRF = os.getenv("XSRF")
API_BASE = os.getenv("API_BASE")

url = API_BASE + "/groups"
headers = {
    "IBM-BA-Authorization": XSRF
}

res = requests.get(
    url, 
    headers=headers,
    verify=False
)

print(res.text)
print(res.status_code)