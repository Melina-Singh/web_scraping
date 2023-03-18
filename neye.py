import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Send a request to the website
url = "https://www.bbc.com/news"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all news headline containers
headline_containers = soup.find_all("h3", {"class": "gs-c-promo-heading__title"})

# Create empty lists to store the raw and cleaned headlines
raw_headlines = []
cleaned_headlines = []

# Loop through each headline container and extract the headline text
for container in headline_containers:
    headline = container.text.strip()
    raw_headlines.append(headline)
    cleaned_headline = headline.replace("\n", "").replace("\t", "")
    cleaned_headlines.append(cleaned_headline)


# Write the headlines to a CSV file
with open("headlines.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Raw Headline", "Cleaned Headline"])
    for i, (raw_headline, cleaned_headline) in enumerate(zip(raw_headlines, cleaned_headlines), 1):
        writer.writerow([i, raw_headline, cleaned_headline])
print(" --------------------------- CSV file is saved Successfully ----------------------------")

df = pd.DataFrame(cleaned_headlines, columns=["Headline"])
df.insert(0, "Number", range(1, 1 + len(df)))
df.to_csv("headlines.csv", index=False)
print(df.tail(5))

df["Length"] = df["Headline"].apply(len)
df.plot(kind="bar", x="Number", y="Length")
plt.show()