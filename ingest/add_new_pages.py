import pandas as pd
from read_page import from_html_to_df
from get_all_cars import get_all_cars
import shutil

def add_new_pages(source_dir: str,
                  datafile: str, *,
                  date_download: datetime.datetime=None,
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


if __name__ == '__main__':
    # to-do: add an example of usage
    pass
