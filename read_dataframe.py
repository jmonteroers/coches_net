import pandas as pd
import pdb

toyotas = pd.read_pickle('dataframes/all_toyotas.pkl')
selection = toyotas[(toyotas.spot_price <= 35000) & (toyotas.kilometrage <= 125000)]  # 21 cars
auto_selection = selection[selection.title.str.contains('AUTO')]  # 3 cars
sorted_selection = selection.sort_values('date', ascending=False)
pdb.set_trace()
