import requests
from bs4 import BeautifulSoup
from itertools import product

class FoxeerParser:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(url)

    def get_soup(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def get_product_details(self, product_url):
        response = requests.get(product_url)
        response.raise_for_status()
        product_soup = BeautifulSoup(response.text, 'html.parser')
        details_table = product_soup.find('table', class_='table table-bordered')
        details = {}
        if details_table:
            for row in details_table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0]
                    value = cells[1]
                    details[key] = value

        download_links = []
        download_section = product_soup.find('div', id='nav-n6')
        if download_section:
            download_lists = download_section.find_all('div', class_='download-list')
            for dl in download_lists:
                link = dl.find('a')['href']
                text = dl.find('a')
                download_links.append({'text': text, 'link': link})
        details['download_links'] = download_links

        video_link = None
        video_section = product_soup.find('div', id='nav-n5')
        if video_section:
            iframe = video_section.find('iframe')
            if iframe:
                video_link = iframe['src']
        details['video_link'] = video_link

        images = self.get_product_images(product_soup)

        return {'details': details, 'details_table': details_table, 'images': images}

    def get_product_tags(self, product_url):
        response = requests.get(product_url)
        response.raise_for_status()
        product_soup = BeautifulSoup(response.text, 'html.parser')
        spec_info = product_soup.find('div', id='spec_info')
        if not spec_info:
            return []

        categories = spec_info.find_all('div', class_='spec_goods_price_div')
        all_tags = []

        for category in categories:
            key_element = category.find('li', class_='jaj')
            key = key_element.text.strip().replace(':', '')
            options = category.find_all('a')
            values = [option.text.strip() for option in options if option.get('enable') == '1']
            all_tags.append({key: values})

        tag_keys = [list(tag.keys())[0] for tag in all_tags]
        tag_values = [list(tag.values())[0] for tag in all_tags]

        tag_combinations = []
        for combination in product(*tag_values):
            tag_combination = ', '.join(f"{tag_keys[i]}: {combination[i]}" for i in range(len(combination)))
            tag_combinations.append(tag_combination)

        return {'tag_combinations': tag_combinations, 'spec_info': spec_info}

    def get_product_price(self, product_url):
        response = requests.get(product_url)
        response.raise_for_status()
        product_soup = BeautifulSoup(response.text, 'html.parser')
        price_div = product_soup.find('div', class_='price price-detail')
        if price_div:
            price = price_div
        else:
            price = 'Price not available'
        return {'price': price, 'price_div': price_div}

    def get_product_images(self, product_soup):
        images = []
        image_block = product_soup.find('div', class_='product-img')
        if image_block:
            img_tags = image_block.find_all('img')
            for img in img_tags:
                images.append(img['src'])
        return {'images': images, 'image_block': image_block}

    def parse_all_pages(self, parse_page_callback):
        all_data = []
        current_url = self.url

        while current_url:
            self.soup = self.get_soup(current_url)
            page_data = parse_page_callback()
            all_data.extend(page_data)

            next_page = self.soup.find('a', class_='next')
            if next_page:
                current_url = next_page['href']
            else:
                current_url = None

        return all_data

    def parse(self):
        raise NotImplementedError('Этот метод должен быть реализован в подклассе')