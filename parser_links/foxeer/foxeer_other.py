from parser_links.foxeer.foxeer_parser import FoxeerParser

class OtherParser(FoxeerParser):
    URL = 'https://www.foxeer.com/others-t-82'

    def __init__(self):
        super().__init__(self.URL)
    def parse_page(self):
        product_type = self.soup.find('h1', class_='page-title').text.strip()
        Others = self.soup.find_all('li', class_='product-item col col-md-4 col-6')
        page_data = []

        for Other in Others:
            name = Other.find('h3', class_='product-name product_title')
            link = Other.find('a')['href']

            # Получить детали из таблицы на странице товара
            product_details = self.get_product_details(link)

            price = self.get_product_price(link)

            page_data.append({
                'name': name,
                'link': link,
                'price': price,
                'type': product_type,
                'details': product_details
            })

        return page_data

    def parse(self):
        return self.parse_all_pages(self.parse_page)
