import pandas as pd
import networkx as nx
def calculate_distance_matrix(file_path):
    df = pd.read_csv(file_path)
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row['id_start'], row['id_end'], weight=row['distance'])
    distance_matrix = nx.floyd_warshall_numpy(G, weight='weight', nodelist=sorted(G.nodes()))
    distance_matrix = (distance_matrix + distance_matrix.T) / 2
    for i in range(distance_matrix.shape[0]):
        distance_matrix[i, i] = 0
        result_df = pd.DataFrame(distance_matrix, index=sorted(G.nodes()), columns=sorted(G.nodes()))
    return result_df
result_distance_matrix = calculate_distance_matrix('dataset-3.csv')
print(result_distance_matrix.iloc[:5,:5])


def unroll_distance_matrix(distance_matrix_df):
    locations = distance_matrix_df.index
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
    for start_loc in locations:
        for end_loc in locations:
            if start_loc != end_loc:
                distance = distance_matrix_df.loc[start_loc, end_loc]
                unrolled_df = unrolled_df.append({'id_start': start_loc, 'id_end': end_loc, 'distance': distance}, ignore_index=True)
    return unrolled_df
result_unrolled_distance = unroll_distance_matrix(result_distance_matrix)
print(result_unrolled_distance)


import pandas as pd

def find_ids_within_ten_percentage_threshold(distance_df, reference_value):

    reference_rows = distance_df[distance_df['id_start'] == reference_value]

    reference_avg_distance = reference_rows['distance'].mean()

    lower_threshold = reference_avg_distance - (reference_avg_distance * 0.1)
    upper_threshold = reference_avg_distance + (reference_avg_distance * 0.1)

    within_threshold_rows = distance_df[(distance_df['distance'] >= lower_threshold) & (distance_df['distance'] <= upper_threshold)]

    result_ids = sorted(within_threshold_rows['id_start'].unique())

    return result_ids


reference_value = 123
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_distance, reference_value)

print(result_within_threshold)


def calculate_toll_rate(distance_df):
    result_df = distance_df.copy()
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        result_df[vehicle_type] = result_df['distance'] * rate_coefficient
    return result_df
result_with_toll_rates = calculate_toll_rate(result_unrolled_distance)
print(result_with_toll_rates.iloc[:5,:5])



import pandas as pd
import datetime

def calculate_time_based_toll_rates(input_df):
    weekday_discount_factors = {
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0)): 0.8,
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0)): 1.2,
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59)): 0.8,
    }
    weekend_discount_factor = 0.7

    input_df['start_day'] = input_df['Date'].dt.strftime('%A')
    input_df['start_time'] = input_df['Date'].dt.time
    input_df['end_day'] = input_df['start_day']
    input_df['end_time'] = input_df['start_time']

    for idx, row in input_df.iterrows():
        start_time = row['start_time']
        end_time = row['end_time']
        is_weekend = row['start_day'] in ['Saturday', 'Sunday']

        if is_weekend:
            input_df.at[idx, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount_factor
        else:
            for time_range, discount_factor in weekday_discount_factors.items():
                if start_time >= time_range[0] and end_time <= time_range[1]:
                    input_df.at[idx, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor
                    break

    return input_df

result_df_with_time_based_toll = calculate_time_based_toll_rates(result_df_with_toll)

print(result_df_with_time_based_toll.head())

