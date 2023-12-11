import pandas as pd

import pandas as pd
def generate_car_matrix(file_path):
    df = pd.read_csv(file_path)
    result_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    result_df.values[[range(result_df.shape[0])]*2]
    return result_df
result_dataframe = generate_car_matrix('dataset-1.csv')
print(result_dataframe.iloc[:5,:5])


import numpy as np
def get_type_count(file_path):
    df = pd.read_csv(file_path)
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(np.select(conditions, choices, default='Unknown'), dtype='category')
    type_count = df['car_type'].value_counts().to_dict()
    type_count = dict(sorted(type_count.items()))
    return type_count
result_type_count = get_type_count('dataset-1.csv')
print(result_type_count)


def get_bus_indexes(file_path):
    df = pd.read_csv(file_path)
    mean_bus_value = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()
    bus_indexes.sort()
    return bus_indexes
result_bus_indexes = get_bus_indexes('dataset-1.csv')
print(result_bus_indexes)

def filter_routes(file_path):
    df = pd.read_csv(file_path)
    selected_routes = df.groupby('route')['truck'].mean()
    selected_routes = selected_routes[selected_routes > 7].index.tolist()
    selected_routes.sort()
    return selected_routes
result_filtered_routes = filter_routes('dataset-1.csv')
print(result_filtered_routes)




def multiply_matrix(input_dataframe):
    modified_df = input_dataframe.copy()
    modified_df[modified_df > 20] *= 0.75
    modified_df[modified_df <= 20] *= 1.25
    modified_df = modified_df.round(1)
    return modified_df
result_dataframe_modified = multiply_matrix(result_dataframe)
print(result_dataframe_modified.iloc[:5,:5])




import pandas as pd

def verify_time_completeness(df):
    problematic_rows = []

    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')

    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

    for index, row in df.iterrows():
        try:
            check_completeness(row)
        except pd.errors.OutOfBoundsDatetime as e:
            problematic_rows.append(index)
            print(f"Problematic row at index {index}: {e}")

    completeness_series = df.groupby(['id', 'id_2']).apply(lambda group: check_completeness_group(group)).reset_index(drop=True)

    if problematic_rows:
        print("\nProblematic rows:")
        print(df.loc[problematic_rows])

    return completeness_series

def check_completeness(row):

    if not pd.isna(row['start_datetime']) and not pd.isna(row['end_datetime']):
        full_day_coverage = (row['start_datetime'].time() == pd.Timestamp('00:00:00').time()) and (row['end_datetime'].time() == pd.Timestamp('23:59:59').time())
        days_of_week_coverage = row['start_datetime'].dayofweek == 0 and row['end_datetime'].dayofweek == 6
        return full_day_coverage and days_of_week_coverage
    return False

def check_completeness_group(group):

    min_datetime = group['start_datetime'].min()
    max_datetime = group['end_datetime'].max()


    if not pd.isna(min_datetime) and not pd.isna(max_datetime):
        full_day_coverage = (min_datetime.time() == pd.Timestamp('00:00:00').time()) and (max_datetime.time() == pd.Timestamp('23:59:59').time())
        days_of_week_coverage = min_datetime.dayofweek == 0 and max_datetime.dayofweek == 6
        return full_day_coverage and days_of_week_coverage
    return False


dataset_2_df = pd.read_csv('dataset-2.csv')


verification_result = verify_time_completeness(dataset_2_df)
print(verification_result)









