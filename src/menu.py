from utils import *


def test_weight():
    dic_weight = {
        "maker": 25,
        "model": 5,
        "body": 20,
        "transmission": 10,
        "exterior_color": 2,
        "interior_color": 2,
        "condition": 15,
        "odometer": 16,
        "year": 6,
    }

    return dic_weight

def test_input():
    dic_input = {
        "maker": "Toyota",
        "model": "Corolla",
        "body": "Sedan",
        "transmission": "automatic",
        "exterior_color": "black",
        "interior_color": "black",
        "condition": "50",
        "odometer": "100000",
        "year": "2018",
    }

    return dic_input

def get_input(dic_input):
    print("Please enter the following information:")
    for key, value in dic_input.items():
        dic_input[key] = input(f"{key}: ").lower()
    return dic_input

def get_weight(dic_weight):
    print("Please enter the following weights:")
    for key, value in dic_weight.items():
        dic_weight[key] = float(input(f"{key}: "))
    return dic_weight

def show_all_cars(df):
    print(df)

def menu(zip_name, file_name):
    df = load_data(zip_name, file_name)
    df = clean_df(df)

    dic_input = test_input()
    dic_weight = test_weight()

    #dic_input = get_input(dic_input)
    #dic_weight = get_weight(dic_weight)

    for key, value in dic_input.items():
        if isinstance(value, str):
            dic_input[key] = value.lower()

    df = calculate_car_similarity(dic_input, df, dic_weight)
    print(dic_input.values())
    print(df.head(3))