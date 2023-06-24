import requests
import bs4
import pandas as pd


def scrape_and_save_pages(start_page, end_page):
    all_data = []

    for i in range(start_page, end_page + 1):
        pages = []
        prices = []
        ratings = []
        title = []
        urls = []

        url = "https://books.toscrape.com/catalogue/page-{}.html".format(i)
        pages.append(url)

        for item in pages:
            page = requests.get(item)
            soup = bs4.BeautifulSoup(page.text, "html.parser")

            for t in soup.findAll("h3"):
                titless = t.getText()
                title.append(titless)

            for p in soup.findAll("p", class_="price_color"):
                price = p.getText()
                prices.append(price)

            for s in soup.findAll("p", class_="star-rating"):
                for k, v in s.attrs.items():
                    star = v[1]
                    ratings.append(star)

            divs = soup.find_all("div", class_="image_container")

            for thumbs in divs:
                tagss = thumbs.find("img", class_="thumbnail")
                links = "http://books.toscrape.com/" + str(tagss["src"])
                newlinks = links.replace("..", "")
                urls.append(newlinks)

        web_data = {"Title": title, "Prices": prices, "Ratings": ratings, "URL": urls}

        data = pd.DataFrame(web_data)
        all_data.append(data)

    # Concatenate all dataframes
    combined_data = pd.concat(all_data, ignore_index=True)

    # Save combined data to a single CSV file
    combined_data.to_csv("combined_data.csv", index=False)


# Usage example:
scrape_and_save_pages(1, 50)
