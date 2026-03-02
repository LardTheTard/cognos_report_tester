import os
import sys
from playwright.sync_api import sync_playwright, expect
from dotenv import find_dotenv, load_dotenv, set_key
from rest import update_header, session, content, debug_content, test_cms

dotenv_path = find_dotenv()
load_dotenv(override=True)

# Consider using requests.Session(), persistent headers across calls with session.headers.update().

# Try calling the api first, if it doesn't work, get a new XSRF token from cookies
xsrf_works = True
res = session()

if res.status_code != 200:
    print("Saved XSRF did not work, opening window for manual authentication.")
    xsrf_works = False
    with sync_playwright() as playwright:
        COGNOS_BASE = os.getenv("COGNOS_BASE")

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(COGNOS_BASE, wait_until="networkidle")
        page.get_by_role("button", name="Continue").click()

        try:
            expect(page).to_have_title("Content", timeout=600000)
            
            cookies = context.cookies()
            xsrf = ''
            
            for cookie in cookies:
                if cookie['name'] == 'cam_passport':
                    xsrf = cookie['value']
            
            context.close()
            browser.close()

            set_key(
                dotenv_path = dotenv_path,
                key_to_set = "XSRF", 
                value_to_set = "CAM " + xsrf,
            )
            
            load_dotenv(override=True)
            update_header()

            res = session()
            
            if res.status_code != 200:
                print(res.text)
                print(res.status_code)
                print("XSRF is incorrect, or cannot get XSRF from cookies")
            else:
                xsrf_works = True
        except AssertionError:
            print("Timed out after 10 minutes, page either did not load in time or user did not log in. (Check if title of the page is still 'Content')")

if not xsrf_works:
    sys.exit(1)

print(res.text)
print(res.status_code)

res = content()

print(res.text)
print(res.status_code)

debug_content()