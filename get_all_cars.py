import os
import pandas as pd
from datetime import datetime, timedelta
from read_page import from_html_to_df
import shutil
import pdb

def get_all_cars(filename, date_download=None):
    assert filename == 'all_cars' or filename == 'small_cars', 'wrong filename inserted'
    if filename == 'all_cars':
        dir = 'files/'
    elif filename == 'small_cars':
        dir = 'files/small_cars/'
    source_dir = dir + 'new_pages/'
    dest_dir = dir + 'used_pages/'
    # create pattern to fill with all files
    cars = pd.read_pickle('dataframes/sample_cars.pkl')
    cars = pd.DataFrame(columns=list(cars.columns) + ['page'])
    for file in os.listdir(source_dir):
        if file.endswith('.html'):
            with open(source_dir + file, 'r') as f:
                content = f.read()
            new_cars = from_html_to_df(content,
                                       date_download=date_download)
            if new_cars is None:
                continue
            new_cars['page'] = file
            cars = pd.concat([cars, new_cars])
            shutil.move(source_dir + file, dest_dir + file)
    # to drop duplicates, don't consider page column
    columns_for_duplicates = [column for column in cars.columns if column != 'page']
    cars.drop_duplicates(columns_for_duplicates, keep='first', inplace=True)
    if cars.shape[0] > 0:
        cars.to_pickle(f'dataframes/{filename}.pkl')
        cars.to_csv(f'dataframes/{filename}.csv', index=False)
    else:
        print('Warning! Trying to create new dataframe from nothing')
    pdb.set_trace()

if __name__ == '__main__':
    get_all_cars('small_cars', date_download = None)
