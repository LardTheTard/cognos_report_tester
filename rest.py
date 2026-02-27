import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

xsrf = os.getenv("XSRF")
api_base = os.getenv("API_BASE")
headers = {
    "IBM-BA-Authorization": xsrf
}

def update_header():
    global xsrf, api_base, headers
    xsrf = os.getenv("XSRF")
    api_base = os.getenv("API_BASE")
    headers = {
        "IBM-BA-Authorization": xsrf
    }

def session():
    return requests.get(
        api_base + "/session", 
        headers=headers,
        verify=False
    )