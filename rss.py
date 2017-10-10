import feedparser
import time
import os
from newspaper import Article
from pprint import pprint as pp

NEWSURLS = {
    'apnews':           'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a76b4ad082fe88aa0db04909',
    'googlenews':       'http://news.google.com/?output=rss',
    'yahoonews':        'http://news.yahoo.com/rss/',
    'busineswire':      'http://www.businesswire.com/portal/site/home/rss/',
    'BBC business':     'feeds.bbci.co.uk/news/business/rss.xml',
    'NYTimesbusiness': 'http://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
    'Ruetersbusiness': 'http://feeds.reuters.com/reuters/businessNews',

    'TheEconomist':     'http://www.economist.com/sections/business-finance/rss.xml',#economist'
    'TheEconomist':     'http://www.economist.com/sections/science-technology/rss.xml'

    'Marketwatch':      'http://feeds.marketwatch.com/marketwatch/topstories/' #marketwatch
    'MWmarketpulse':    'http://feeds.marketwatch.com/marketwatch/marketpulse/',
    'MWstockstowatch':  'http://feeds.marketwatch.com/marketwatch/StockstoWatch/',
    'MWinterenet':      'http://feeds.marketwatch.com/marketwatch/internet/',
    'MWsoftware':       'http://feeds.marketwatch.com/marketwatch/software/',
    'MWresearch':       'http://feeds.marketwatch.com/marketwatch/newslettersandresearch/',

    'CNNmoney':         'http://rss.cnn.com/rss/money_latest.rss', #CNN
    'CNNmoneytopstories': 'http://rss.cnn.com/rss/money_topstories.rss',
    'CNNcompanies':     'http://rss.cnn.com/rss/money_news_companies.rss',
    'CNNinternational': 'http://rss.cnn.com/rss/money_news_international.rss',
    'CNNmarket':        'http://rss.cnn.com/rss/money_markets.rss',
    'CNNtechnology':    'http://rss.cnn.com/rss/money_technology.rss',
    'CNNautos':         'http://rss.cnn.com/rss/money_autos.rss',

    'NASDAQ':           'http://articlefeeds.nasdaq.com/nasdaq/categories?category=Basics',#NASDAQ
    'NASDAQcommodities':'http://articlefeeds.nasdaq.com/nasdaq/categories?category=Commodities',
    'NASDAQinternational':'http://articlefeeds.nasdaq.com/nasdaq/categories?category=International',
    'NASDAQbusiness':   'http://articlefeeds.nasdaq.com/nasdaq/categories?category=Business',
    'NASDAQtechnology': 'http://articlefeeds.nasdaq.com/nasdaq/categories?category=Technology',
    'NASDAQusmarket':   'http://articlefeeds.nasdaq.com/nasdaq/categories?category=US+Markets',




}

RSS = True #change True/False for extraction.
GOOGLE = False
KEYWORD = input('Input keyword (all lowercase, please!): ')


def exist(direc):
    if not os.path.exists(direc):
        os.mkdir(direc)


def set_times():
    '''
    Sets day distance for articles for 7 and 30 days. Does not take into account leap years.

    th_day - thirtieth day

    sv_day - seventh day

    day - actaul day of the month
    '''

    ctime = time.strftime('%d,%m,%Y')
    month = int(ctime.split(',')[1])
    day = int(ctime.split(',')[0])
    subth = day - 30
    subsv = day - 7
    if subsv < 0:
        sv_month = month - 1
    else:
        sv_month = month
    if subth < 0:
        th_month = month - 1
    else:
        th_month = month


    th_one = [1, 3, 5, 7, 8, 10, 12]
    th = [4, 6, 9, 11]
    if month in th_one:
        th_day = 31 + subth
        sv_day = 31 + subsv
    elif th_one in th:
        th_day = 30 + subth
        sv_day = 30 + subsv
    else:
        th_day = 28 + subth #fix leap later
        sv_day = 28 + subsv
    return (th_day, sv_day, day, th_month, sv_month, month)


def rss_feeds():
    rss_arts = []
    for key, url in NEWSURLS.items():
        feed = feedparser.parse( url ) 
        for newsitem in feed['items']:
            art_url = newsitem['links'][0]['href']
            dates = newsitem["published_parsed"]
            rss_arts.append((art_url, dates))
    return rss_arts 


def extr_info(art_url):
    try:
        print(art_url)
        article = Article(art_url)
        article.download()
        article.parse()
        article.nlp()
        text = article.text
        title = article.title
        kws = article.keywords
        return kws, text, title

    except:
        return False, False, False #write in different way



def extr_news(th_day, sv_day, day, th_month, sv_month, month, arts, typ):
    '''
    Extracts news articles from given search source if it meets date requirements, and writes them to necessary directory.
    '''

    doc_count = 0
    th_count = 0
    sv_count = 0

    for art_url, dates in arts:
        kws, text, title = extr_info(art_url)

        if kws:
            doc_count += 1

            if KEYWORD in kws:
                pub_year = dates[0]
                pub_month = dates[1]
                pub_day = dates[2]
                if pub_year == 2017:
                    if pub_month == month and pub_day <= day: # if publication month is in current month and day is less than current day
                        sv_count += 1
                        th_count += 1
                    elif pub_month == sv_month and pub_day >= sv_day: # if publication month is same as seventh day month and the publication day is greater than seventh day
                        sv_count += 1
                        th_count += 1
                    elif pub_month == th_month and pub_day >= th_day: # if publication month is same as thirtieth day month and the publication day is greater than thirtieth day
                        th_count += 1
                exist('texts')
                exist('texts/{0}'.format(KEYWORD))
                exist('texts/{0}/{1}'.format(KEYWORD, typ))
                with open('texts/{0}/{1}/{2}'.format(typ, KEYWORD, title), 'w') as file:
                    file.write(text)
                print('ARTICLE FOUND!!!')
            else:
                print('Article unrelated.')
        else:
            print('Article unrelated.')
        time.sleep(2) #sleepy time

    print('{0}'.format(typ))
    print('Docs Queried: {0}'.format(doc_count))
    print('7 Days: {0}'.format(sv_count))
    print('30 Days: {0}'.format(th_count))






th_day, sv_day, day, th_month, sv_month, month = set_times()

if RSS:
    rss_arts = rss_feeds()
    extr_news(th_day, sv_day, day, th_month, sv_month, month, rss_arts, 'RSS')

if GOOGLE:
    google_arts = google()
    extr_news(th_day, sv_day, day, th_month, sv_month, month, rss_arts, 'RSS')