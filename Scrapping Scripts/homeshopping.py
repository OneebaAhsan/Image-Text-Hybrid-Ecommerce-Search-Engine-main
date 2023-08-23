""" Scrapping homeshopping """
import os
import shutil
import requests
import bs4
import pandas as pd

import concurrent.futures

threads = 8

# dirname = "DSLR Cameras"

item_dict = {
    "Women Clothing": "https://homeshopping.pk/categories/Women-Clothing-Price-in-Pakistan",
    "Women Watches": "https://homeshopping.pk/categories/Women-Watches-in-Pakistan",
    "Women Bags": "https://homeshopping.pk/categories/Women-Bags-and-Clutches-Price-Pakistan",
    "Jewellery": "https://homeshopping.pk/categories/Women-Jewelry-Price-in-Pakistan",
    "Women Perfumes": "https://homeshopping.pk/categories/Women-Perfumes-Price-in-Pakistan",
    "Men Clothing": "https://homeshopping.pk/categories/Men-Clothing-in-Pakistan",
    "Men Watches": "https://homeshopping.pk/categories/Watches-Price-In-Pakistan",
    "Men Perfumes": "https://homeshopping.pk/categories/Men-Perfumes-Price-in-Pakistan"
}

def scrape(dirname, url):
    i = 1
    item_links = []
    item_dict = {}
    print("Scraping:", url)
    while True:
        new_url = url + f"?page={i}&AjaxRequest=1"
        page = requests.get(new_url)
        if len(page.text) == 0:
            break
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        for h5 in soup.find_all("h5"):
            item_links.append(h5.find("a", href=True))
        i += 1
    print("Done:", url)
    with open(f'./{dirname}.txt', "w", encoding="utf-8") as f:
        # for line in f:
        #     item_links.append(line.strip())
        for item_link in item_links:
            f.write(str(item_link['href']))
            f.write("\n")

    if(not os.path.exists(dirname)):
        os.mkdir(dirname)

    for idx, item_link in enumerate(item_links):
        # page = requests.get(item_link["href"])
        try:
            page = requests.get(item_link["href"])
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            title = soup.find('span', {"itemprop":"name"}).text
            product_id = soup.find('span', {'class':'grey'}).find_next_sibling().text
            price = soup.find('div', {'class': "ActualPrice"}).text
            image_url = soup.find('ul', {'id': "glasscase"}).find("li").find("img")["src"]
            image_path = os.path.join("HomeShopping", dirname, "Mobile Phones", product_id)
            image_response = requests.get(image_url, stream=True)
            with open(f'./{dirname}/{product_id}.png', 'wb') as out_file:
                shutil.copyfileobj(image_response.raw, out_file)
            del image_response
            categories = list(map(lambda x: x.text,
                        soup.find('div', {'class': "btn-group btn-breadcrumb hsbreadcumb"}).
                        findChildren(recursive=False)[2:]))
            categories = ", ".join(categories)
            image_name = product_id + '.png'
            item_dict[idx] = [product_id, title, price, image_name, image_url, image_path, categories]
            print(f"{title}")
        except Exception as e:
            print(e)
            continue

    df = pd.DataFrame.from_dict(item_dict, orient='index',
        columns=["Product ID", "Product Title", "Price", "Image Name", "Image Url", "Image Path", "Categories"])
    df.to_csv(f"./{dirname}/{dirname}.csv", index=False)


with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    executor.map(scrape, item_dict.keys(), item_dict.values())