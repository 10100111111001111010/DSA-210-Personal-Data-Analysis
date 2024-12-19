import urllib
from bs4 import BeautifulSoup

file_path = urllib.parse.unquote("/Users/nusret/Desktop/Sabancı Fall 2024-2025/DSA 210/Term Project/Takeout/YouTube and YouTube Music/history/watch-history.html")

with open(file_path, "r") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "lxml")

print(soup.prettify())

