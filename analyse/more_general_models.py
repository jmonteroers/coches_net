import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import numpy as np
import pdb

regressor_type = 'random_forest'  # alternative is 'random_forest' (random forest)
selected_columns = ['kilometrage','kilometrage_year', 'year_old', 'VXL',
                     'VX', 'auto', 'warranty', 'type_petrol', 'office',
                     'range_rover_sport', 'tdv6', 'rr', 'land_cruiser_5p',
                     'grand_cherokee', 'overland']

cars = pd.read_csv('dataframes/cars_with_indicators.csv')
cars.type_petrol = cars.type_petrol.astype('category').cat.codes
y = cars.spot_price.values
X = cars[selected_columns].values
X = X.astype(float)
# remove nans
rows_with_nans = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
X = X[rows_with_nans]
y = y[rows_with_nans]
cars = cars[rows_with_nans]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.15)

def prepare_X(X, train=True, scaler=None):
    assert train or scaler is not None, 'For test set, you need to provide a scaler'
    if train:
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)
    return X_scaled, scaler

X_train_scaled, scaler = prepare_X(X_train)
X_test_scaled, _ = prepare_X(X_test, train=False, scaler=scaler)
if regressor_type == 'random_forest':
    reg = RandomForestRegressor(max_depth=6, n_estimators=100,
                                random_state=8)
elif regressor_type == 'neural_network':
    reg = MLPRegressor(hidden_layer_sizes=(1000, 100, 100, 30), max_iter=int(1e4), learning_rate='adaptive',
                       learning_rate_init=0.01,
                       verbose=True,
                       tol=int(1e-5))
reg.fit(X_train_scaled, y_train)
test_predictions = reg.predict(X_test_scaled)
print('R2 prediction score: {}'.format(r2_score(y_test, test_predictions)))

# add residuals to database
X_scaled, _ = prepare_X(X, False, scaler)
predictions = reg.predict(X_scaled)
print('R2 score: {}'.format(r2_score(y, predictions)))
cars['residuals'] = y - predictions
cars = cars[(cars.spot_price <=35000) & (cars.kilometrage <= 100000) & (cars.year >= 2013)
            & (cars.date >= '2020-08-28')]
cars.sort_values('residuals', inplace=True)
print(cars[['title', 'location', 'date', 'spot_price', 'residuals']].head(15))
print(cars[['title', 'location', 'date', 'spot_price', 'residuals']].head(30).tail(15))

pdb.set_trace()
