Tl;dr the files are too big so:

**All related files can be found at the public drive:** [https://drive.google.com/drive/folders/1wZl90T37h3qDG7QnJGoI_F8G1KX2Z_6S?usp=drive_link](https://drive.google.com/drive/folders/1wZl90T37h3qDG7QnJGoI_F8G1KX2Z_6S?usp=drive_link) 

**Current checkpoint data is available for download at:** [https://drive.google.com/uc?export=download&id=1zTJsCLyiPZM5LHWImm4zgHRmeVkzPjA9](https://drive.google.com/uc?export=download&id=1zTJsCLyiPZM5LHWImm4zgHRmeVkzPjA9) 


---

# Twitter Community Notes Data Processing

This repository contains tools and documentation for working with Twitter Community Notes data. The project includes:

- **Downloading Data:** Instructions on accessing the public Community Notes snapshots from Twitter.  
  **Data Source:** All Community Notes data was obtained from [https://x.com/i/communitynotes/download-data](https://x.com/i/communitynotes/download-data) 
- **Scraping Tweet Data:** A Python script that uses Selenium to load tweet embeds and extract tweet text.
- **Data Combination:** An R Markdown (.Rmd) script to join the scraped tweet data with the downloaded Community Notes data, as well as a Python utility to convert scraped files into a single CSV file.

**All related files can be found at the public drive:** [https://drive.google.com/drive/folders/1wZl90T37h3qDG7QnJGoI_F8G1KX2Z_6S?usp=drive_link](https://drive.google.com/drive/folders/1wZl90T37h3qDG7QnJGoI_F8G1KX2Z_6S?usp=drive_link) 

**Current checkpoint data is available for download at:** [https://drive.google.com/uc?export=download&id=1zTJsCLyiPZM5LHWImm4zgHRmeVkzPjA9](https://drive.google.com/uc?export=download&id=1zTJsCLyiPZM5LHWImm4zgHRmeVkzPjA9) 

Obviously, this was written by ChatGPT (o3-mini-high). Thanks Mr. ChatGPT.

---

## Overview

Twitter Community Notes data is released as four normalized TSV files:
- **Notes:** Contains the note details including the note text, author identifiers, tweet IDs, and other metadata.
- **Ratings:** Contains user ratings of notes.
- **Note Status History:** Contains metadata on note status changes over time.
- **User Enrollment:** Contains user enrollment state information.

The datasets can be joined using the `noteId` field, which helps avoid data duplication.

---

## Data Snapshots & File Structure

- **Data Snapshots:**  
  - A new snapshot of the public Community Notes data is released daily (cumulative but limited to notes/ratings created at least 48 hours prior to the snapshot).
  - When notes or ratings are deleted, the corresponding note content is removed from future downloads (though metadata remains in the note status history).

- **File Format:**  
  Each snapshot is provided in TSV (tab-separated values) format with a header row. Columns and their definitions (e.g., `noteId`, `participantId`, `tweetId`, etc.) are documented in the repository.

---

## Subsample Checkpoint Data

A new file, **tweet_data_checkpoint_1_subset.csv**, has been added directly to GitHub. This file is a 1000-row subset of the full checkpoint data and is meant for quick testing or demonstration purposes.

### Data Description

Each row in this CSV represents a tweet along with associated Community Notes metadata. The file includes the following columns:

- **tweet_url:** URL of the tweet.
- **txt_file_path:** Local path to the saved tweet text file.
- **tweet_text:** The extracted tweet text.
- **tweetId:** Tweet identifier.
- **noteId:** Associated Community Note identifier.
- **noteAuthorParticipantId:** Unique identifier of the note author.
- **createdAtMillis:** Timestamp (in milliseconds) of when the note was created.
- **classification:** Classification label (e.g., MISINFORMED_OR_POTENTIALLY_MISLEADING or NOT_MISLEADING).
- **believable, harmful, validationDifficulty:** Various metrics or flags regarding the note's content.
- **misleadingOther, misleadingFactualError, misleadingManipulatedMedia, misleadingOutdatedInformation, misleadingMissingImportantContext, misleadingUnverifiedClaimAsFact, misleadingSatire:** Flags indicating different types of potential misinformation.
- **notMisleadingOther, notMisleadingFactuallyCorrect, notMisleadingOutdatedButNotWhenWritten, notMisleadingClearlySatire, notMisleadingPersonalOpinion:** Flags indicating types of non-misleading characteristics.
- **trustworthySources:** URL or identifier for sources considered trustworthy.
- **summary:** A brief summary or context of the note.
- **isMediaNote:** Indicator if the note is associated with media content.

A brief snippet of the data is shown below:

```csv
tweet_url,txt_file_path,tweet_text,tweetId,noteId,noteAuthorParticipantId,createdAtMillis,classification,believable,harmful,validationDifficulty,misleadingOther,misleadingFactualError,misleadingManipulatedMedia,misleadingOutdatedInformation,misleadingMissingImportantContext,misleadingUnverifiedClaimAsFact,misleadingSatire,notMisleadingOther,notMisleadingFactuallyCorrect,notMisleadingOutdatedButNotWhenWritten,notMisleadingClearlySatire,notMisleadingPersonalOpinion,trustworthySources,summary,isMediaNote
https://twitter.com/user/status/1783159712986382830,tweet_outputs/tweet_1.txt,"Senator Ted Cruz ...",1783159712986382800,1783179305159201e3,C784F04F26E124F4D6EC01658D8F5565005D3092741FB3A6CED3F45089066236,1713978050878,MISINFORMED_OR_POTENTIALLY_MISLEADING,NA,NA,NA,0,0,0,0,1,0,0,0,0,0,0,0,1,"The House failed to pass a border protection law...",0
https://twitter.com/user/status/1783171851818021181,tweet_outputs/tweet_2.txt,"Republicans against Trump ...",1783171851818021e3,1783181538789606e3,C784F04F26E124F4D6EC01658D8F5565005D3092741FB3A6CED3F45089066236,1713978583415,MISINFORMED_OR_POTENTIALLY_MISLEADING,NA,NA,NA,0,1,0,0,0,1,0,0,0,0,0,0,1,"The United States has 50 States ...",0
```

*Note: The actual file contains 1000 rows and the snippet above is just an example.*

---

## Scraping Tweet Data

The repository includes a Python script (`scrape_tweets.py`) to extract tweet content via the Twitter embed. Key steps include:

1. **HTML Template Generation:**  
   An HTML file is generated locally for each tweet using Twitter’s embed markup.
   
2. **Selenium Browser Automation:**  
   - The script uses Selenium with a randomly chosen user-agent.
   - It loads the local HTML file, waits for the Twitter iframe to render, and extracts the tweet text.
   - Extracted tweet text is then saved as a text file in the `tweet_outputs` directory.

3. **Progress Management:**  
   - A helper function determines the next tweet to process by checking the highest tweet number already processed.

Example usage (from command line):
```bash
python scrape_tweets.py
```

---

## Combining Downloaded & Scraped Data

There are two components for data combination:

### R Markdown (.Rmd) Script

The provided R Markdown script performs the following:
- Loads the downloaded Community Notes data (e.g., `notes-00000.tsv`).
- Reads the scraped tweet data (CSV) and filters out empty or "Not found" tweet texts.
- Uses regex to extract `tweetId` from tweet URLs.
- Joins the scraped tweet data with the Community Notes subset based on the `tweetId` field.
- Exports the combined dataset to a CSV checkpoint file.

The R code snippet looks like:
```r
cn <- fread("notes-00000.tsv") %>% as_tibble() %>% mutate(tweetId = as.character(tweetId))
cp1 <- fread("cn_scrape/tweet_data.csv") %>% as_tibble

cp1_filtered <- cp1 %>%
  filter(tweet_text != "" & tweet_text != "Not found") %>%
  mutate(tweetId = str_extract(tweet_url, "\\d+"))

cn_subset <- cn %>%
  filter(tweetId %in% cp1_filtered$tweetId)

cp1_filtered <- cp1_filtered %>%
  inner_join(cn_subset, by = "tweetId")
  
fwrite(cp1_filtered, "cn_scrape/tweet_data_checkpoint_1.csv")
```

### Python Conversion Script

A separate Python script (`convert_scraped_to_csv.py`) converts the individually scraped tweet text files into a single CSV file. It performs the following:
- Reads the tweet URLs from `cn_tweet_urls.txt`.
- Locates all tweet text files (named as `tweet_<number>.txt`) in the `tweet_outputs` folder.
- Writes a CSV file (`tweet_data.csv`) with columns: `tweet_url`, `txt_file_path`, and `tweet_text`.

Example usage:
```bash
python convert_scraped_to_csv.py
```

---

## Requirements

### Python
- Python 3.x
- [Selenium](https://selenium-python.readthedocs.io/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (compatible with your Chrome version)

### R
- R and RStudio (or any R environment)
- Packages: `data.table`, `dplyr`, `readr`, `tibble`, and `stringr`

Ensure all dependencies are installed before running the scripts.

---

## Directory Structure  
*(Note: Files and folders larger than 25MB are excluded from this actual repo)*

```
.
├── README.md
├── scrape_tweets.py              # Python script for scraping tweet content
├── convert_scraped_to_csv.py     # Python script to combine scraped tweet files into CSV
├── cn_tweet_urls.txt             # File containing the list of tweet URLs to process
├── tweet_outputs/                # Folder where scraped tweet text files are stored
├── notes-00000.tsv               # Example Community Notes data file (downloaded)
├── cn_scrape/                    # Folder for combined tweet data output (e.g., tweet_data.csv, tweet_data_checkpoint_1.csv)
└── tweet_data_checkpoint_1_subset.csv  # 1000-row subset of the full checkpoint data (directly on GitHub)
```

---

## Usage

1. **Scrape Tweets:**
   - Update `cn_tweet_urls.txt` with the tweet URLs (ensure "x.com" is replaced with "twitter.com" automatically).
   - Run `scrape_tweets.py` to generate text files in `tweet_outputs/`.

2. **Combine Scraped Data:**
   - Run `convert_scraped_to_csv.py` to generate `tweet_data.csv`.

3. **Join with Downloaded Data:**
   - Use the provided R Markdown script to merge the scraped tweet data with the Community Notes data.
   - The final joined dataset is saved as `cn_scrape/tweet_data_checkpoint_1.csv`.

4. **Exploring the Subset:**
   - For quick testing or demonstration, refer to `tweet_data_checkpoint_1_subset.csv` on GitHub. This file is a 1000-row subset of the checkpoint data, featuring columns for tweet URLs, file paths, tweet texts, tweet and note IDs, metadata flags, and a summary field, among others.

---

## Contributing

Contributions, suggestions, and improvements are welcome.
