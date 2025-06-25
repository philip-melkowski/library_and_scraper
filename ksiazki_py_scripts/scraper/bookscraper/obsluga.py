import time
from datetime import datetime
import subprocess

start_year = 2024
start_month = 6

today = datetime.today()
end_year = today.year
end_month = today.month

months = []
year = start_year
month = start_month

while (year < end_year) or (year == end_year and month < end_month):
    months.append((year, month))
    month += 1
    if month > 12:
        month = 1
        year += 1

for y, m in months:
    cmd = ["scrapy", "crawl", "book", "-a", f"month={m}", "-a", f"year={y}", "-o", "jsonl/books.jsonl"]
    subprocess.run(cmd)
    time.sleep(15)
    
