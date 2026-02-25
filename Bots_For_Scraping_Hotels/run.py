# Driver file that initiates the project and fetches all the raw html items inside the 'data' subfolder.
from bot.book import Book
from bs4 import BeautifulSoup
import os
import pandas as pd

d = dict()

with Book() as b:
    b.land_first_page()
    b.remove_cookie_mssg()
    b.remove_popup()
    b.select_website()
    b.select_lan_cur()
    d = b.get_items()
    b.quit()

collection = {"Name": [], "Price-Per-Night": [], "Best-Deal-At": [], "URL": []}
num = 1

for item in d:
    try:
        with open(d[item][1]) as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')

        t = soup.find('span', attrs={"itemprop": "name"})
        title = t.get_text()
        s = soup.find("strong", attrs={"data-testid": "recommended-price-partner", "data-cos": "advertiser", "itemprop": "offeredBy"})
        site_offering_best_deal = s.get_text()
        p = soup.find("span", attrs={"data-testid": "recommended-price", "data-cos": "recommendedPrice", "itemprop": "price"})
        price = p.get_text()

        collection["Name"].append(title)
        collection["Price-Per-Night"].append(price)
        collection["Best-Deal-At"].append(site_offering_best_deal)
        collection["URL"].append(d[item][0])

    except Exception as e:
        print(e)

my_data = pd.DataFrame(data=collection)
my_data.to_csv("output.csv")




