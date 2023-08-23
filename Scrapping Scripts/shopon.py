""" Scrapping Shopon """
import os
import shutil
import requests
import bs4
import pandas as pd

dirname = "Kids Fashion"

i = 1
item_links = []
item_dict = {}
while True:
    url = f"https://shopon.pk/kids-fashion/page-{i}/"
    page = requests.get(url)
    if not page.ok:
        break
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    number_of_links = len(soup.find_all('div', {'class': "ty-column3"}))
    for link in soup.find_all("a", {'class': "product-title"}, limit=number_of_links, href=True):
        item_links.append(link)
    i += 1

with open(f'{dirname}.txt', "w", encoding="utf-8") as f:
    for item_link in item_links:
        f.write(str(item_link['href']))
        f.write("\n")

print(f"{len(item_links)} links found")

if(not os.path.exists(dirname)):
    os.mkdir(dirname)

for idx, item_link in enumerate(item_links):
    try:
        page = requests.get(item_link['href'])
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        title = soup.find('h1', {'class': "ut2-pb__title"}).find('bdi').text
        product_id = soup.find('span', {'class':'ty-control-group__item'}).text
        price = soup.find('span', {'class': "ty-price"}).find('bdi').findChildren()
        price = price[0].text.strip('.') + " " + price[1].text
        image_url = soup.find('a', {'class': "cm-image-previewer cm-previewer ty-previewer"})["href"]
        image_path = os.path.join("Shopon", dirname, "Body Care", product_id)
        image_response = requests.get(image_url, stream=True)
        with open(f'./{dirname}/{product_id}.png', 'wb') as out_file:
            shutil.copyfileobj(image_response.raw, out_file)
        del image_response
        categories = list(map(lambda x: x.text,
                    soup.findAll('span', {'itemprop': "itemListElement"})[1:]))
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
