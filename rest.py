import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv(override=True)

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

def content():
    return requests.get(
        api_base + "/content", 
        headers=headers,
        verify=False
    )

def debug_content():
    extension = "Not None"
    while extension != None:
        extension = str(input())
        print(api_base + "/content" + extension)
        res = requests.get(
            api_base + "/content" + extension,
            headers=headers,
            verify=False
        )
        # res = res.json()
        # try:
        #     print(res['defaultName'])
        #     for link in res['links']:
        #         print(link['href'])
        # except KeyError:
        #     for item in res['content']:
        #         print(item['defaultName'])
        #         for link in item['links']:
        #             if link['rel'] != 'self':
        #                 print(link['href'])
        print(res.text)

def test_cms():
    report_id = ''
    url = os.getenv("CMS_BASE") + f"/bi/v1/disp/rds/outputFormats/report/{report_id}?v=3"
    res = requests.get(url, headers={"x-xsrf-token": xsrf}, verify=False)
    res.raise_for_status()
    print(res.text[:500])