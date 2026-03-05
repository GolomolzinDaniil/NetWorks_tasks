from playwright.sync_api import sync_playwright


def parse(num_page, url):

    data = []

    with sync_playwright() as p:

        browser = p.chromium.launch(channel='msedge')
        main_page = browser.new_page()
        main_page.goto(url)


        for _ in range(num_page):
            
            elements = main_page.query_selector_all('article.product_pod')

            for el in elements:

                tag = el.query_selector('h3 a')

                if tag:
                    name = tag.get_attribute('title')

                    price_el = el.query_selector('p.price_color')
                    price = price_el.inner_text() if price_el else 'N/A'

                    stock_el = el.query_selector('p.instock.availability')
                    stock = stock_el.inner_text().strip() if stock_el else 'N/A'
                    
                    # ссылка на личную страницу книги
                    book_url = tag.get_attribute('href')

                    if book_url:
                        book_url = f'{url}{'' if book_url.startswith('catalogue/') else 'catalogue/'}{book_url}'
                    else: book_url = 'N/A'

                    data.append(
                        {
                            'name': name,
                            'price': price,
                            'availability': stock,
                            'url': book_url
                        }
                    )
                
            next_page = main_page.query_selector('li.next a')
            if next_page:
                next_page.click()
                main_page.wait_for_load_state('networkidle')

    return data