import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import numpy as np


def remove_nas(*args: 'arrays of 2 dims',
               return_boolean_mask=False) -> list:
    '''
    Returns all arrays in args without the rows with NaNs
    All arrays passed must have the same number of rows and
    be two-dimensional.
    '''
    arrays = list(args)
    complete_array = np.hstack(arrays)
    boolean_mask = ~np.isnan(complete_array).any(axis=1)
    for idx, ar in enumerate(arrays):
        arrays[idx] = ar[boolean_mask]
    return arrays, boolean_mask if return_mask else arrays


def prepare_X(X, train=True, scaler=None):
    scaler = scaler or MinMaxScaler()
    X_scaled = scaler.fit_transform(X) if train else scaler.transform(X)
    return X_scaled, scaler


def prepare_for_sklearn(data_location: str,
                        dep_var: 'either "spot_price" or "financed_price"',
                        indep_vars: list,
                        test_size):
    indep_vars = indep_vars or ['kilometrage','kilometrage_per_year', 'hp',
                                'year_old', 'auto', 'warranty', 'type_petrol',
                                'office']
    cars = pd.read_csv(data_location)
    # create dummy variables from type_petrol column
    if 'type_petrol' in indep_vars:
        cars = pd.get_dummies(cars, columns=['type_petrol'])
        indep_vars.remove('type_petrol')
        indep_vars += cars.type_petrol.unique().tolist()
    # convert pandas columns to numpy arrays
    y = cars[dep_var].values.reshape(-1, 1)
    X = cars[indep_vars].values
    # transform integers to floats
    X = X.astype(float)
    # remove nans
    [X, y], boolean_mask = remove_nas(X, y, return_boolean_mask=True)
    cars = cars[boolean_mask]
    # apply train/test split
    X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=test_size)
    # scale regressors
    X_train_scaled, scaler = prepare_X(X_train, train=True)
    X_test_scaled, _ = prepare_X(X_test, train=False, scaler=scaler)

    return cars, (X_train_scaled, X_test_scaled, y_train, y_test)


def find_discounts(data_location: str,
                   n_discounts: int=20,*,
                   output_columns: list=None,
                   dep_var: 'either "spot_price" or "financed_price"'
                   ='spot_price', model_type: str='random_forest',
                   indep_vars: list=None,
                   filter: 'function' = None,
                   test_size=.15,
                   return_r2=False,
                   **kwargs):
    '''
    Note.
    Last values for neural network,
    # hidden_layer_sizes=(1000, 100, 100, 30), max_iter=int(1e4),
    # learning_rate='adaptive',learning_rate_init=0.01,
    # verbose=True, tol=int(1e-5)
    Last values for random_forest,
    # max_depth=6, n_estimators=100, random_state=8
    '''
    ### prepare default variables
    output_columns = output_columns or ['title', 'location', 'date',
                                        'spot_price', 'residuals']
    if model_type == 'random_forest':
        model = RandomForestRegressor(**kwargs)
    elif model_type == 'neural_network':
        model = MLPRegressor(**kwargs)

    ### prepare data
    cars, (X_train_scaled, X_test_scaled, y_train, y_test) = \
    prepare_for_sklearn(data_location,
                        dep_var=dep_var, indep_vars=indep_vars,
                        test_size=test_size)

    ### fit model, obtain residuals
    model.fit(X_train_scaled, y_train)
    # obtain predictions
    test_predictions = model.predict(X_test_scaled)
    train_predictions = model.predict(X_train_scaled)
    predictions = np.concatenate([train_predictions, test_predictions])
    # add residuals to database
    cars['residuals'] = y - predictions

    ### get r2 score if requested
    if return_r2:
        r2_train = r2_score(y_train, train_predictions)
        r2_test = r2_score(y_test, test_predictions)
        r2 = (r2_train, r2_test)

    ### find and clean best discounts
    # apply user-defined filter function
    cars = filter(cars) if filter else cars
    cars.sort_values('residuals', inplace=True)
    cars = cars[output_columns]
    cars.drop_duplicates(inplace=True)
    cars = cars.head(n_discounts)
    return cars, r2 if return_r2 else cars
