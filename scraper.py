import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.realmadrid.com/futbol'
NEWS_URL = 'https://www.realmadrid.com'
XPATH_LINK_TO_ARTICLE = '//article[@class="m_highlight "]/a/@href'
XPATH_TITLE = '//div[@class="nnt-cabecera_container"]/h1/text()'
XPATH_SUBTITLE = '//div[@class="nnt-noticia_module_text"]/h2/text()'
XPATH_BODY = '//div[@class="ck_editor_noticia"]/p/text()'


def parse_new(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            new = response.content
            parsed = html.fromstring(new)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                subtitle = parsed.xpath(XPATH_SUBTITLE)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(subtitle)
                f.write('\n\n')
                for p in body:
                    p += ' '
                f.write(p)
                f.write('\n\n')
                f.write(url)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            today = datetime.date.today().strftime('%Y-%m-%d')
            if not os.path.isdir(today):
                os.mkdir(today)

            for key, link in enumerate(links_to_news):
                filename = f'{today}/notice_{key}.txt'
                parse_new(f'{NEWS_URL}{link}', filename)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        pass


def run():
    parse_home()


if __name__ == '__main__':
    run()

