from bs4 import BeautifulSoup
import requests
import time
import csv


def assemble_news(tickers):
    # Parameters
    # tickers = ['AAPL', 'TSLA', 'AMZN', 'EPC', 'ADS', 'AMD', 'WMT', 'BDN', 'KSS', 'DBX']

    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    for ticker in tickers:
        print("Retrieving news headlines about", ticker, "...")
        url = finviz_url + ticker
        # headers used to avoid being detected as a web crawler.
        resp = requests.session().get(url, headers={'user-agent': 'my-app/0.0.1'})
        html = BeautifulSoup(resp.content, features="lxml")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
        time.sleep(1)
    return news_tables


def create_news_csv(news_tables, filename):
    parsed_news = []
    rows = []
    # Write headlines to csv file using bs4
    # Repeated headlines modify to only hyave it show up once.
    with open(filename, 'w', newline="") as news_file:
        news_writer = csv.writer(news_file)
        news_writer.writerow(['Company', 'date', 'time', 'headline'])
        for file_name, news_table in news_tables.items():
            date_ = None
            for data in news_table.findAll('tr'):
                # Data contains everything about the newsheadline
                # data.a grabs the "a" html tag or url line.
                text = data.a.get_text()
                # same as data.a but instead of "a", gets "td" html tag
                date_scrape = data.td.text.split()

                if len(date_scrape) == 1:
                    time_ = date_scrape[0]

                else:
                    date_ = date_scrape[0]
                    time_ = date_scrape[1]

                ticker = file_name.split('_')[0]
                rows.append([ticker, date_, time_, text])

                parsed_news.append([ticker, date_, time_, text])
        news_writer.writerows(rows)


def run(tickers, filename):
    news_tables = assemble_news(tickers)
    create_news_csv(news_tables, filename)
