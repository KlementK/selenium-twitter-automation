# **Selenium Twitter Automation**

This project is a Python-based automation tool that uses **Selenium WebDriver** to recreate core Twitter interactions. The goal is to automate actions such as **searching**, **liking**, **commenting**, **retweeting**, **quoting**, and **posting tweets** directly from the command line.

The tool provides robust handling of Twitter’s modern UI by integrating Selenium with techniques like ActionChains, explicit waits, and JavaScript click fallbacks to bypass potential DOM changes or overlays.

---

## **Features**

- **Search Tweets**: Search for tweets by keywords or hashtags.
- **Like Tweets**: Like a specific tweet by ID.
- **Post Tweets**: Post new tweets directly.
- **Comment on Tweets**: Add comments to a specific tweet by ID.
- **Retweet**: Retweet a tweet.
- **Quote Tweet**: Quote a tweet with custom text.
- **Follow/Unfollow Users**: Follow or unfollow users by username.
- **Output Results**: Save scraped data in CSV or JSON format.
- **Summarization**: Summarize scraped tweet content.

---

## **Installation**

### **Prerequisites**

1. **Python 3.8+** must be installed.
2. **Firefox Browser** must be installed.
3. **Geckodriver**: must be downloaded.
   - You can download Geckodriver from [Mozilla Geckodriver Releases](https://github.com/mozilla/geckodriver/releases).
4. Ensure `geckodriver.exe` is placed in a folder named `webdriver/` inside the project directory.  
    
---

### **Steps to Install**

1. **Clone the repository**

2. **Create and Activate a virtual environment**.

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

Run the script using the following syntax:

```bash
python main.py -e "your_email@example.com" -p "your_password" [options]
```

### **Available Options**

| Option               | Description                                        | Example Usage                                      |
|----------------------|----------------------------------------------------|---------------------------------------------------|
| `-e, --email`        | Your Twitter account email                         | `-e "user@example.com"`                           |
| `-p, --password`     | Your Twitter account password                      | `-p "password123"`                                |
| `-s, --search`       | Search Twitter for a keyword/hashtag               | `--search "Python"`                               |
| `-lk, --like`        | Like a specific tweet by ID                        | `--like 1613929999999999999`                      |
| `-twt, --tweet`      | Post a tweet with the given content                | `--tweet "Hello world from Selenium!"`           |
| `-com, --comment`    | Comment on a specific tweet by ID                  | `--comment 1613929999999999999`                  |
| `-ret, --retweet`    | Retweet a tweet by ID                              | `--retweet 1613929999999999999`                  |
| `-quo, --quote`      | Quote a tweet by ID with custom text               | `--quote 1613929999999999999`                    |
| `-fol, --follow`     | Follow a user by username                          | `--follow "@username"`                           |
| `-unf, --unfollow`   | Unfollow a user by username                        | `--unfollow "@username"`                         |
| `-out, --output`     | Save output in CSV or JSON format                  | `--output "results.csv"`                         |
| `-sum, --summarize`  | Summarize the scraped tweets                       | `--search "Python" --summarize`                  |

---

### **Example Commands**

1. **Search for tweets and save results**:
   ```bash
   python main.py -e "user@example.com" -p "password123" --search "Python" --output "results.csv"
   ```

2. **Post a new tweet**:
   ```bash
   python main.py -e "user@example.com" -p "password123" --tweet "Automating Twitter with Selenium!"
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

## **Project Structure**

```
selenium-twitter-automation/
│
├── main.py                         # Main entry point for the script
├── requirements.txt                # Python dependencies
├── webdriver/                      # Folder for geckodriver.exe
├── src/
│   ├── __init__.py                 # Marks the src folder as a package
│   ├── argument_parser.py          # Handles command-line argument parsing
│   ├── scraper.py                  # Core scraper logic
│   ├── interaction.py              # Handles interactions like commenting, liking, etc.
│   ├── scroller.py                 # Handles scrolling logic
│   ├── utils.py                    # Utility functions for logging, saving data, etc.
│   ├── tweet.py                    # Class for handling tweet objects
│   └── user.py                     # Handles user-related actions (follow, unfollow, etc.)
└── README.md                       # Project documentation
```

---

## **Known Issues**

1. **ElementClickInterceptedException**:  
   Sometimes elements like the reply button can be obscured by overlays (e.g., cookie banners). The script includes handling for such cases, but if you encounter issues, ensure no overlays block the button.

2. **Login Issues**:  
   If login fails, double-check your credentials or if Twitter’s login flow has changed.

---

## **Contributing**

Contributions are welcome! If you’d like to improve this project, feel free to submit a pull request or open an issue on GitHub.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.
