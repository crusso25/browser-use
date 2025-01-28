from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.browser.context import BrowserContextConfig
from browser_use.browser.browser import Browser, BrowserConfig
import asyncio

async def main():
    config = BrowserConfig(
        headless=False,
        disable_security=True,
        chrome_instance_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
        extra_chromium_args=[
            "--user-data-dir=C:\\Users\\carso\\AppData\\Local\\Google\\Chrome\\User Data",
            "--profile-directory=Default"  
        ]
    )
    my_browser = Browser(config=config)
    agent = Agent(
        task = """
Navigate to https://optionshawk.com/optionshawk-trading-hub/, stay on this webpage, and process all posts within the time frame starting from 1/27/2025 at 16:00 to the beginning of posts on 1/14/2025. For each post within this time frame that mentions the CRM ticker, perform the following steps:

1. Save the content of the post using the `save_post_content` function in the JSON format provided below:

{
  "date": "<date and time of the post>",
  "author": "<author of the post>",
  "content": "<full post content>",
  "color": "<color of the post's border (green, red, yellow, or grey)>",
  "ticker": "<ticker name included in the content>"
}

2. Ensure the extracted data includes:
   - The **date and time** of the post.
   - The **author** of the post.
   - The **full content** of the post.
   - The **border color** of the post (green, red, yellow, or grey) based on its visual appearance.
   - The **CRM ticker name**, if mentioned in the content.

3. Load more posts:
   - To retrieve posts that are not immediately viewable, click the "Load More" button at the bottom of the page to load additional posts. Continue this process until you reach the beginning of the posts on 1/14/2025.

4. Filter and save only relevant posts:
   - Only save posts where the **CRM ticker** is mentioned. Skip posts that do not include the CRM ticker in their content.

5. Stop the process once you reach the first post of 1/14/2025.

Ensure all saved data is accurate and complete for each relevant post, adhering to the JSON structure provided.
"""
,
#        task = """
# Navigate to https://optionshawk.com/optionshawk-trading-hub/, starting from the post dated 1/21/2025 at 15:57. For each post, extract and save its content using the `save_post_content` function in the following JSON format:

# {
#   "date": "<date and time of the post>",
#   "author": "<author of the post>",
#   "content": "<full post content>",
#   "color": "<color of the post's border (green, red, yellow, or grey)>",
#   "ticker": "<ticker name included in the content>"
# }

# Ensure the extracted data accurately reflects the post's details:
# 1. Include the **border color** (green, red, yellow, or grey) based on the visual appearance of the post.
# 2. Parse and include the **ticker name** from the content, if mentioned.

# Save one post at a time and proceed sequentially to the next until reaching the last post at 16:00.
# """,
        llm=ChatOpenAI(model="gpt-4o-mini"),
        browser=my_browser
    )
    result = await agent.run()
    print(result)

asyncio.run(main())