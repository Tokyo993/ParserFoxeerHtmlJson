from parser_links.foxeer.foxeer_parser import FoxeerParser

class FrameParser(FoxeerParser):
    URL = 'https://www.foxeer.com/frame-t-71'

    def __init__(self):
        super().__init__(self.URL)

    def parse_page(self):
        Frames = self.soup.find_all('li', class_='product-item col col-md-4 col-6')
        page_data = []

        for Frame in Frames:
            link = Frame.find('a')['href']
            product_soup = self.get_soup(link)
            images = self.get_product_images(product_soup)
            name = Frame.find('h3', class_='product-name product_title')

            # Получить детали из таблицы на странице товара
            product_details = self.get_product_details(link)

            # Получить теги из страницы товара
            tags = self.get_product_tags(link)

            price = self.get_product_price(link)

            page_data.append({
                'name': name,
                'link': link,
                'price': price,
                'type': 'Frame',
                'details': product_details,
                'tags': tags,
            })

        return page_data

    def parse(self):
        return self.parse_all_pages(self.parse_page)