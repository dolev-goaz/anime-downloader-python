import requests
from bs4 import BeautifulSoup
import re

SOURCE_REGEX = re.compile('var VidStreaming = \"(.*)\";')

r = requests.get("https://animekisa.tv/the-rising-of-the-shield-hero-episode-1")

string = r.content.decode('ascii')

result = SOURCE_REGEX.search(string)

url = ""

if result:
    url = result.group(1).replace("load.php", "download")

if url:
    print(url)
else:
    print("not found")
