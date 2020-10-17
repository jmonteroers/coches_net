import os
import pandas as pd
from read_page import from_html_to_df
import shutil
import pdb


def add_new_pages(filename, date_download=None):
    assert filename in ['all_cars', 'small_cars'], 'filename must be either all_cars or small_cars'
    dir = 'files/'
    if filename == 'all_cars':
        dir = 'files/'
    elif filename == 'small_cars':
        dir = 'files/small_cars/'
    source_dir = dir + 'new_pages/'
    dest_dir = dir + 'used_pages/'
    cars = pd.read_pickle(f'dataframes/{filename}.pkl')
    n_initial = cars.shape[0]
    for file in os.listdir(source_dir):
        if file.endswith('.html'):
            with open(os.path.join(source_dir, file), 'r') as f:
                content = f.read()
            new_cars = from_html_to_df(content,
                                       date_download=date_download)
            if new_cars is None:
                continue
            new_cars['page'] = file
            cars = pd.concat([cars, new_cars])
            # move to used_pages
            shutil.move(os.path.join(source_dir, file), dest_dir)
    columns_for_duplicates = [column for column in cars.columns if column != 'page']
    cars.drop_duplicates(columns_for_duplicates, keep='first', inplace=True)
    cars.to_pickle(f'dataframes/{filename}.pkl')
    cars.to_csv(f'dataframes/{filename}.csv', index=False)
    n_final = cars.shape[0]
    print(f'Se han añadido {n_final - n_initial} coches nuevos')
    pdb.set_trace()


if __name__ == '__main__':
    add_new_pages('all_cars')
