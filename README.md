# **Selenium Twitter Automation**

This project is a Python-based automation tool that uses **Selenium WebDriver** to recreate core Twitter interactions. The goal is to automate actions such as **searching**, **liking**, **commenting**, **retweeting**, **quoting**, and **posting tweets** directly from the command line.

The tool also includes a built-in scraping mechanism to collect tweet data and optionally summarize them.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
  - [Examples](#examples)
- [Data Scraping & Summarization](#data-scraping--summarization)
- [Output Files](#output-files)
- [Known Issues](#known-issues)
- [Disclaimer](#disclaimer)
- [Contributing](#disclaimer)
- [License](#license)

---

## Features

- **Automated Login**: Log in to a Twitter account using email and password.  
- **Tweet Interactions**:  
  - Post a tweet  
  - Like a tweet  
  - Comment on a tweet  
  - Retweet a tweet  
  - Quote a tweet  
- **User Actions**:  
  - Follow or unfollow a user  
  - Open user profile page  
- **Scraping**:  
  - Search for users or hashtags and scrape tweets  
  - Collect tweet metadata (content, likes, retweets, mentions, hashtags, etc.)  
  - Export tweets to CSV or JSON  
- **Summarization**:  
  - (placeholder - will be implemented using OPENAI API later...)

---

## Project Structure

```
selenium-twitter-automation/
│
├── main.py                      # Entry point for CLI usage
├── requirements.txt             # Python dependencies
├── webdriver/                   
   └── geckodriver.exe           # Place geckodriver.exe here!
├── src/
│   ├── __init__.py
│   ├── argument_parser.py       # Parses CLI arguments, routes them to correct actions
│   ├── interaction.py           # Like, comment, retweet, quote, etc. logic
│   ├── scraper.py               # Main TwitterScraper class for login & tweet scraping
│   ├── scroller.py              # Helper class for scrolling the page to load tweets
│   ├── search.py                # Utility function to integrate scraping & search
│   ├── summarizer.py            # Summarizes scraped tweets
│   ├── tweet.py                 # Tweet data extraction logic
│   ├── user.py                  # User-related actions like follow, unfollow, post tweet
│   └── utils.py                 # Helper functions for saving data to CSV or JSON
└── README.md                    # Project documentation
```

---

## **Prerequisites**

1. **Python 3.8+** must be installed.
2. **Firefox Browser** must be installed.
3. **Geckodriver**: must be downloaded.
   - You can download Geckodriver from [Mozilla Geckodriver Releases](https://github.com/mozilla/geckodriver/releases).
4. Ensure `geckodriver.exe` is placed in a folder named `webdriver/` inside the project directory.  
    
---

### **Installation**

1. **Clone the repository**

2. **Create and Activate a virtual environment**.

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

Run the script using the following syntax:

```bash
python main.py [options]
```

---

### **Command-Line Arguments**

| Argument               |  Short | Description                                                       | Example                                                 |
|------------------------|--------|-------------------------------------------------------------------|---------------------------------------------------------|
| **--email**            | `-e`   | **Required.** Your Twitter account email.                         | `-e your_email@example.com`                             |
| **--password**         | `-p`   | **Required.** Your Twitter account password.                      | `-p your_password`                                      |
| **--search**           | `-s`   | Search for a term/hashtag/user.                                   | `-s "selenium"` or `-s "#Python"`                       |
| **--like**             | `-lk`  | Like a tweet by ID.                                               | `-lk 1234567890`                                        |
| **--tweet**            | `-twt` | Post a new tweet with the provided text.                          | `-twt "Hello Twitter!"`                                 |
| **--comment**          | `-com` | Comment on a tweet by ID.                                         | `-com 1234567890`                                       |
| **--retweet**          | `-ret` | Retweet a tweet by ID.                                            | `-ret 1234567890`                                       |
| **--quote**            | `-quo` | Quote-tweet a tweet by ID with added text.                        | `-quo 1234567890`                                       |
| **--follow**           | `-fol` | Follow a user by username.                                        | `-fol TwitterDev`                                       |
| **--unfollow**         | `-unf` | Unfollow a user by username.                                      | `-unf TwitterDev`                                       |
| **--profile**          | `-pr`  | Open your own Twitter profile page.                               | `-pr`                                                   |
| **--summarize**        | `-sum` | Summarize scraped tweets.                                         | `-sum`                                                  |
| **--output**           | `-out` | Output file to save scraped tweets (`CSV` or `JSON`).             | `-out tweets.csv` or `-out tweets.json`                 |
| **--help**             | `-h`   | Shows help message with details of available arguments.           | `-h`                                                    |

> **Note**: Use the `--search` argument to scrape tweets for the given term. By default, a maximum of 50 tweets are collected, unless you change the code or add advanced arguments (will be done later...).  
> **Important**: The script **requires** both `-e / --email` and `-p / --password` for any action that interacts with Twitter’s interface.

---

### **Examples**

1. **Search for tweets and save results**:
   ```bash
   python main.py -e "user@example.com" -p "password123" --search "Python" --output "results.csv"
   ```

2. **Post a new tweet**:
   ```bash
   python main.py -e "user@example.com" -p "password123" --tweet "Hello From Selenium :D"
   ```

3. **Like a specific tweet by ID**:
   ```bash
   python main.py -e "user@example.com" -p "password123" --like 1613929999999999999
   ```

4. **Comment on a tweet**:
   ```bash
   python main.py -e "user@example.com" -p "password123" --comment 1613929999999999999
   ```

---

## Data Scraping & Summarization
- **Scraping**: The project uses Selenium to scroll through the Twitter feed or search results and collects tweet metadata (username, handle, time, text, like/retweet counts, etc.).

- **Summarization**: The summarizer.py module currently does nothin'. It’s a placeholder for more advanced summarization, potentially with OpenAI API.

---

## Output Files
- **CSV or JSON**: By specifying ```--output <filename>```, the scraped tweets are saved in CSV or JSON format.

- **Default**: If no valid file extension is provided, it defaults to CSV.

---

## **Known Issues**

1. **ElementClickInterceptedException**:  
   Sometimes elements like the reply button can be obscured by overlays (e.g., cookie banners). The script includes handling for such cases, but if you encounter issues, ensure no overlays block the button.

2. **Login Issues**:  
   If login fails, double-check your credentials or if Twitter’s login flow has changed.

---

## Disclaimer

This project is intended for **educational **and** personal** use only.
Using Selenium to automate Twitter may violate [Twitter’s Terms of Service](https://x.com/en/tos). 

The authors assume no liability for any misuse or account bans resulting from using this script.

**Use at your own risk.**

---

## **Contributing**

Contributions are welcome! If you’d like to improve this project, feel free to submit a pull request or open an issue on GitHub.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.
