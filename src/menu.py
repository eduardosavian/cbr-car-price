from utils import *


def menu(zip_name, file_name):
    df = load_data(zip_name, file_name)
    df = clean_df(df)

    dic_weight = {
        "maker": 1,
        "model": 1,
        "body": 1,
        "transmission": 1,
        "condition": 1,
        "odometer": 1,
        "exterior_color": 1,
        "interior_color": 1,
        "year": 1,
    }

    dic_input = {
        "maker": "bmw",
        "model": "x5",
        "body": "suv",
        "transmission": "automatic",
        "exterior_color": "black",
        "interior_color": "black",
        "condition": 1000.0,
        "odometer": 100000,
        "year": 2019,
    }

    most_similar_car, max_similarity = find_most_similar_car(dic_input, df, dic_weight)
    print(most_similar_car)
    print(max_similarity)
