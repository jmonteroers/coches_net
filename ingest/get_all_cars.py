import os.path
import pandas as pd
from datetime import datetime, timedelta
from read_page import from_html_to_df
import shutil
import pdb

# an ad-hoc exception to raise if some of the ad pages have not been processed
class AdNotProcessedException(Exception):
    def __init__():
        exception_msg = \
        ('A problem has ocurred when extracting one of the'
         'dataframes. stopping execution')
        super().__init__(exception_msg)

def get_all_cars(source_dir: str, *, filename=None: str,
                 dest_dir: str=None,
                 date_download: datetime.datetime=None,
                 save_dir: str=None,
                 save_mode: 'either "pkl" or "csv"'=None,
                 check_all_pages: bool=False) -> None:
    '''
    Processes all html files in `source_dir` with ads from coches.net,
    and concatenates them into a pandas DataFrame, which is either returned or
    saved in  `saved_dir` with the name `filename`. Resulting DataFrame can be
    returned (default) or saved by specifying save_mode.

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
    if None, do not save dataframe, return it instead
    - check_all_pages, whether execution should be stopped if one of the pages
    cannot be processed. if False, print a warning to the screen.
    '''
    # create pattern to fill with all files
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
                continue
            # add name of the file as a variable to DataFrame
            new_cars['page'] = file
            # update cars
            cars = pd.concat([cars, new_cars]) if cars else new_cars
            # either move or copy file
            if dest_dir is not None:
                shutil.move(os.path.join(source_dir, file),
                            os.path.join(dest_dir, file))
            else:
                shutil.copy(os.path.join(source_dir, file),
                            os.path.join(dest_dir, file))
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
            cars.to_csv(f'dataframes/{filename}.csv', index=False)
        return
    return cars

if __name__ == '__main__':
    # to-do: fill with example
    pass
