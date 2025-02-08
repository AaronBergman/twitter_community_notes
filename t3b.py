import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ProcessPoolExecutor, as_completed
import re

# Create output folder
output_folder = "tweet_outputs"
os.makedirs(output_folder, exist_ok=True)

def get_next_start_line(output_folder):
    """Find the highest tweet number processed and return the next line number."""
    tweet_files = [f for f in os.listdir(output_folder) if f.startswith("tweet_") and f.endswith(".txt")]
    tweet_numbers = []
    for file in tweet_files:
        match = re.match(r"tweet_(\d+)\.txt", file)
        if match:
            tweet_numbers.append(int(match.group(1)))
    if tweet_numbers:
        return max(tweet_numbers) + 1
    else:
        return 1  # Start from the first line if no tweets have been processed

start_line = get_next_start_line(output_folder)

# Read tweet URLs from file and replace "x.com" with "twitter.com"
with open('cn_tweet_urls.txt', 'r') as f:
    urls = []
    for idx, line in enumerate(f, start=1):
        if idx >= start_line and line.strip():
            urls.append((idx, line.strip().replace("x.com", "twitter.com")))

print(f"Found {len(urls)} tweets to process starting from line {start_line}")

# HTML template using the provided embed markup.
html_template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <blockquote class="twitter-tweet" data-dnt="true">
      <p lang="en" dir="ltr"><a href="{tweet_url}"></a></p>
    </blockquote>
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
  </body>
</html>
"""

def process_tweet(idx, tweet_url):
    """Process a single tweet: create local HTML, load it in a browser,
    extract tweet text, and save it."""
    # Write the local HTML file with the tweet embed
    local_html_filename = os.path.join(output_folder, f"embed_{idx}.html")
    with open(local_html_filename, "w", encoding="utf-8") as f:
        f.write(html_template.format(tweet_url=tweet_url))

    # Setup Chrome options with a random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    ]
    chrome_options = Options()
    chrome_options.add_argument("user-agent=" + random.choice(user_agents))
    # Uncomment next line to run headless
    # chrome_options.add_argument("--headless")

    # Create a new driver for this process
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the local HTML file in the browser
        file_url = "file://" + os.path.abspath(local_html_filename)
        driver.get(file_url)

        # Wait for the iframe injected by Twitter to appear
        iframe = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )

        # Switch to the tweet iframe and allow time to render
        driver.switch_to.frame(iframe)
        time.sleep(2)
        try:
            tweet_text = driver.find_element(By.TAG_NAME, "body").text.strip()
        except Exception as e:
            tweet_text = f"Error extracting tweet text: {e}"

        # Switch back to main content
        driver.switch_to.default_content()

        # Save extracted tweet text to a file
        output_filename = os.path.join(output_folder, f"tweet_{idx}.txt")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(tweet_text)

        print(f"Processed tweet {idx}: content saved to {output_filename}")
    except Exception as ex:
        print(f"Error processing tweet {idx} ({tweet_url}): {ex}")
    finally:
        driver.quit()

if __name__ == '__main__':
    # Adjust max_workers as needed. Here we use min(8, total tweets).
    max_workers = min(8, len(urls))
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for idx, tweet_url in urls:  # Changed to unpack the tuple
            futures.append(executor.submit(process_tweet, idx, tweet_url))
        # Wait for all tasks to complete
        for future in as_completed(futures):
            # Exceptions, if any, will be raised here
            future.result()
