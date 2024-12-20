import urllib.parse
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def parse_youtube_history(file_path):
    with open(urllib.parse.unquote(file_path), "r", encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "lxml")
    history_entries = soup.find_all("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
    watch_history = []

    for entry in history_entries:
        try:
            title_elem = entry.find("a")
            if title_elem:
                title = title_elem.text
                link = title_elem["href"]
            else:
                continue

            text_content = entry.get_text(separator='\n').split('\n')
            timestamp = [line.strip() for line in text_content if line.strip()][-1]

            # Parse the timestamp into a datetime object
            try:
                timestamp_str = timestamp.split(' GMT')[0]  # Remove timezone
                dt = datetime.strptime(timestamp_str, '%b %d, %Y, %I:%M:%S %p')
            except:
                print(f"Could not parse timestamp: {timestamp}")
                continue

            watch_history.append({
                "title": title,
                "link": link,
                "timestamp": timestamp,
                "datetime": dt  # Store parsed datetime for sorting
            })
        except Exception as e:
            print(f"Error parsing entry: {e}")
            continue

    # Sort by datetime
    watch_history.sort(key=lambda x: x['datetime'], reverse=True)
    return watch_history


file_path = "/Users/nusret/Desktop/Sabancı Fall 2024-2025/DSA 210/Term Project/Takeout/YouTube and YouTube Music/history/watch-history.html"
history = parse_youtube_history(file_path)

#Save to data/raw/watch-history.json


df = pd.DataFrame(history)
df['datetime'] = pd.to_datetime(df['datetime'])  # Ensure datetime is properly formatted
df = df.sort_values('datetime', ascending=False)
df.to_json('../../data/raw/watch-history.json', index=False)
print("\nData saved to watch-history.json")