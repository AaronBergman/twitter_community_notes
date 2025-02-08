import os
import csv
import re

def main():
    tweet_outputs_folder = "tweet_outputs"
    urls_file = "cn_tweet_urls.txt"
    output_csv = "tweet_data.csv"

    # Read tweet URLs from file and apply the same replacement as before
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip().replace("x.com", "twitter.com") for line in f if line.strip()]

    # Find all processed tweet text files matching tweet_<number>.txt in the output folder
    tweet_files = []
    for filename in os.listdir(tweet_outputs_folder):
        match = re.match(r"tweet_(\d+)\.txt$", filename)
        if match:
            idx = int(match.group(1))
            tweet_files.append((idx, os.path.join(tweet_outputs_folder, filename)))
    tweet_files.sort(key=lambda x: x[0])

    # Write the CSV with columns: tweet_url, txt_file_path, tweet_text
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["tweet_url", "txt_file_path", "tweet_text"])

        for idx, txt_path in tweet_files:
            # Get the tweet URL corresponding to the line number (idx)
            tweet_url = urls[idx-1] if 0 < idx <= len(urls) else ""
            # Read the tweet text from the file
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    tweet_text = f.read().strip()
            except Exception as e:
                tweet_text = f"Error reading file: {e}"
            writer.writerow([tweet_url, txt_path, tweet_text])

    print(f"CSV file generated: {output_csv}")

if __name__ == '__main__':
    main()
