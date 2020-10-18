from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta


def get_list_from_html(html, class_):
    list_html = html.find_all(class_=class_)
    return [el.get_text().strip() for el in list_html]


def get_prices_from_html(html):
    '''
    First price is spot price, second is financed (if available)
    '''
    prices_html = html.find_all(class_="mt-AdPrice-amount")
    prices = tuple(price_tag.strong.get_text() for price_tag in prices_html)
    return prices


def transform_car(title, date, prices, attributes, warranty, office):
    '''
    transform input to a dictionary representing a car
    args(title, date, prices, attributes, warranty, office) ->
    Car(title, date, spot_price, financed_price, location, type_petrol, year,
    mileage, warranty, office)
    '''
    fields = ['title', 'date', 'spot_price', 'financed_price',
              'location', 'type_petrol', 'year', 'kilometrage',
              'warranty', 'office']
    car = {field:None for field in fields}
    try:
        car['title'] = title
        car['date'] = date[0]
        car['spot_price'] = prices[0]
        car['financed_price'] = prices[1] if len(prices) > 1 else None
        car['location'] = attributes[0]
        car['type_petrol'] = attributes[1]
        car['year'] = attributes[2]
        car['kilometrage'] = attributes[3]
        car['warranty'] = warranty[0] if warranty else None
        car['office'] = office[0] if office else None
    except IndexError as e:
        print(e)
    return car


# borrowed from stackoverflow, idea by Kyle Barron
def vec_dt_replace(series, year=None, month=None, day=None):
    return pd.to_datetime(
        {'year': series.dt.year if year is None else year,
         'month': series.dt.month if month is None else month,
         'day': series.dt.day if day is None else day})


def clean_numeric(series, measure=' €'):
    series = series.str.replace('.', '')
    series = series.str.replace(measure, '')
    series[~series.isnull() & series.str.contains('N/D')] = None
    return series.astype(float)


def clean_cars_df(cars, date_download=None):
    if cars.shape[0] == 0:
        return None
    # clean date
    date_download = date_download or datetime.today()
    yesterday = (date_download - timedelta(1)).strftime('%d/%m %H:%M')
    date_download = date_download.strftime('%d/%m %H:%M')
    cars.date = cars.date.str.replace('Ahora.*', date_download, case=False)
    cars.date = cars.date.str.replace('Hoy.*', date_download, case=False)
    cars.date = cars.date.str.replace('Hace.*', date_download, case=False)
    cars.date = cars.date.str.replace('Ayer.*', yesterday, case=False)
    cars.date = pd.to_datetime(cars.date, format='%d/%m %H:%M')
    cars.date = vec_dt_replace(cars.date, year=2020)
    # clean numeric columns
    cars.spot_price = clean_numeric(cars.spot_price)
    cars.financed_price = clean_numeric(cars.financed_price)
    cars.kilometrage = clean_numeric(cars.kilometrage, measure=' km')
    # convert year
    cars.year = cars.year.astype(float)
    # convert warranty
    cars.warranty = cars.warranty.str.extract('(\d+)').astype(float)
    cars.warranty[cars.warranty.isnull()] = 0
    cars.warranty = cars.warranty.astype(int)
    # convert office
    cars.office = cars.office == "Gerencia"
    return cars


def read_html(content):
    '''
    Returns list, where each element has all the info about an add in
    a dictionary
    '''

    soup = BeautifulSoup(content)
    # get title
    titles = get_list_from_html(soup, class_='mt-CardAd-titleHiglight')
    # get attributes
    attributes = get_list_from_html(soup, 'mt-CardAd-attribute')
    # get cars by getting body
    ads_html = soup.find_all(class_='mt-CardAd')
    cars = []
    for ad in ads_html:
        title = get_list_from_html(ad, 'mt-CardAd-titleHiglight')
        assert len(title) == 1, 'cannot find more than one title'
        title = title[0]
        attributes = get_list_from_html(ad, 'mt-CardAd-attribute')
        warranty = get_list_from_html(ad, "mt-AdPrice-warranty u-c--green")
        prices = get_prices_from_html(ad)
        date = get_list_from_html(ad, "mt-CardAd-date")
        office = get_list_from_html(ad, "mt-CardAd-extra")
        cars.append(transform_car(title, date, prices, attributes, warranty, office))
    return cars


def from_html_to_df(content, date_download=None):
    cars = read_html(content)
    cars = pd.DataFrame(cars)
    cars = clean_cars_df(cars, date_download=date_download)
    return cars


if __name__ == '__main__':
    import pdb
    cars = read_html('land_cruiser_demo.html')
    cars = pd.DataFrame(cars)
    cars = clean_cars_df(cars)
    cars.to_pickle('dataframes/sample_cars.pkl')
    pdb.set_trace()
    import matplotlib.pyplot as plt
    cars.plot.scatter('kilometrage', 'spot_price')
    plt.show()
