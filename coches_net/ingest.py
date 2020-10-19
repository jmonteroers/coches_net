import pandas as pd
import os.path
from .read_page import from_html_to_df
import shutil


# an ad-hoc exception to raise if some of the ad pages have not been processed
class AdNotProcessedException(Exception):
    def __init__():
        exception_msg = \
        ('A problem has ocurred when extracting one of the'
         'dataframes. stopping execution')
        super().__init__(exception_msg)

def get_all_cars(source_dir: str, *, filename: str=None,
                 dest_dir: str=None,
                 date_download: 'datetime.datetime'=None,
                 save_dir: str=None,
                 save_mode: 'either "pkl" or "csv"'='pkl',
                 check_all_pages: bool=False) -> None:
    '''
    Processes all html files in `source_dir` with ads from coches.net,
    and concatenates them into a pandas DataFrame, which is always returned.
    Resulting DataFrame can be saved by specifying `save_dir` and `filename`.

    Original html files can be either preserved (default option, dest_dir None)
    or moved to the `dest_dir` folder. If check_all_cars is True, method checks
    that all pages have been processed.

    Values:
    - source_dir, folder from which to process all html files. does not
    process subfolders
    - save_dir, folder to save resulting DataFrame
    - filename, a string with the name of the file to be saved
    - dest_dir, directory to move original html files to. If None, do not move
    original files
    - date_download, date when html pages were obtained, to add it to dataframe.
    if None, uses today as date_download
    - save_mode, None, "pkl" or "csv". format with which to save resulting dataframe.
    if None, do not save dataframe
    - check_all_pages, whether execution should be stopped if one of the pages
    cannot be processed. if False, print a warning to the screen.
    '''
    # get cars from all files in source_dir
    cars = None
    for file in os.listdir(source_dir):
        if file.endswith('.html'):
            with open(source_dir + file, 'r') as f:
                content = f.read()
            new_cars = from_html_to_df(content,
                                       date_download=date_download)
            # if there is a problem when processing the page, new_cars will be
            # None
            if new_cars is None:
                if check_all_cars:
                    raise(AdNotProcessedException())
                else:
                    print(f'Warning! {file} could not be processed')
                continue
            # add name of the file as a variable to DataFrame
            new_cars['page'] = file
            # update cars
            cars = (pd.concat([cars, new_cars])
                    if cars is not None else new_cars)
            # either move or copy file
            if dest_dir is not None:
                shutil.copy(os.path.join(source_dir, file),
                            os.path.join(dest_dir, file))
    # check that we have processed any of the pages
    if cars is None:
        return
    # drop duplicates without considering page column
    columns_for_duplicates = [column for column in cars.columns
                              if column != 'page']
    cars.drop_duplicates(columns_for_duplicates, keep='first', inplace=True)
    # save or return
    if save_dir is not None and filename:
        assert save_mode in ['pkl', 'csv'], 'save_mode must be either "pkl" or "csv"'
        if save_mode == 'pkl':
            cars.to_pickle(os.path.join(save_dir, f'{filename}.pkl'))
        elif save_mode == 'csv':
            cars.to_csv(os.path.join(save_dir, f'{filename}.pkl'), index=False)
    return cars


def add_new_pages(source_dir: str,
                  datafile: str, *,
                  date_download: 'datetime.datetime'=None,
                  dest_dir: str=None,
                  check_all_pages: bool=False,
                  save=False):
    '''
    Processes all html files in `source_dir` with ads from coches.net,
    and concatenates them into the existing dataframe in datafile. It always
    returns the resulting dataframe. Optionally, it can rewrite the existing
    dataframe by setting save to True.

    Values:
    - source_dir, folder from which to process all html files. does not
    process subfolders
    - datafile, relative/absolute path to location where existing dataframe exists
    - dest_dir, directory to move original html files to. If None, do not move
    original files
    - date_download, date when html pages were obtained, to add it to dataframe.
    if None, uses today as date_download
    - check_all_pages, whether execution should be stopped if one of the pages
    cannot be processed. if False, print a warning to the screen.
    - save, should the original dataframe with the new observations
    be saved (True) or returned (False)?
    '''
    if datafile.endswith('.pkl'):
        df = pd.read_pickle(datafile)
    elif datafile.endswith('.csv'):
        df = pd.read_csv(datafile)
    else:
        print('datafile must be either a csv or a pickle file')
        return None
    n_initial_obs = df.shape[0]
    new_car_ads = get_all_cars(source_dir, date_download=date_download,
                               dest_dir=dest_dir,
                               check_all_pages=check_all_pages)
    # need to check that new_car_ads is not None
    if new_car_ads:
        df = pd.concat([df, new_car_ads])
    n_final_obs = df.shape[0]
    print(f'{n_final_obs - n_initial_obs} new cars have been added.')
    if save and datafile.endswith('.pkl'):
        df.to_pickle(datafile)
    elif save and datafile.endswith('.csv'):
        df.to_csv(datafile)
    return df
