import numpy as np
import pandas as pd
import zipfile


def load_data(zip_name, file_name):
    archive = zipfile.ZipFile(zip_name)
    df = pd.read_csv(archive.open(file_name))

    return df


def clean_df(df):
    drop_list = ["trim", "vin", "state", "saledate", "seller", "mmr"]

    df = df.drop(columns=drop_list, axis=1)

    df = df.dropna(how="any")

    columns_rename = {
        "make": "maker",
        "sellingprice": "price",
        "color": "exterior_color",
        "interior": "interior_color",
    }
    df = df.rename(columns=columns_rename)

    df.drop(df[df["exterior_color"].str.contains("—")].index, inplace=True)
    df.drop(df[df["interior_color"].str.contains("—")].index, inplace=True)

    cols = [
        "maker",
        "model",
        "body",
        "transmission",
        "interior_color",
        "exterior_color",
        "odometer",
        "condition",
        "year",
        "price",
    ]
    df = df[cols]

    return df


def similarity_maker(maker1, maker2):
    return 0 if maker1 == maker2 else 1


def similarity_model(model1, model2):
    return 0 if model1 == model2 else 1


def similarity_body(body1, body2):
    return 0 if body1 == body2 else 1


def similarity_transmission(transmission1, transmission2):
    return 0 if transmission1 == transmission2 else 1


def similarity_condition(condition1, condition2):
    return 0 if condition1 == condition2 else 1


def similarity_odometer(odometer1, odometer2):
    return (odometer1 - odometer2) ** 2


def similarity_color(color1, color2):

    # r1, g1, b1 = color_map[color1]
    # r2, g2, b2 = color_map[color2]
    # return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
    return 1


def similarity_year(year1, year2):
    return (year1 - year2) ** 2

def find_most_similar(car_input, df, weights):
    weights = np.array(list(weights.values()))
    cars = df.to_numpy()
    # add a column in the end
    cars = np.concatenate((cars, np.zeros((cars.shape[0], 1))), axis=1)

    car_input = np.array(list(car_input.values()))
    print(type(car_input), type(cars), type(weights))

    max_similarity = float("inf")
    most_similar_car = None

    for car in cars:
        #print(car)
        #print(car_input)
        #print(weights)
        sim = 0
        sim = np.sum(weights * np.array([
            similarity_maker(car[0], car_input[0]),
            similarity_model(car[1], car_input[1]),
            similarity_body(car[2], car_input[2]),
            similarity_transmission(car[3], car_input[3]),
            similarity_color(car[4], car_input[4]),
            similarity_color(car[5], car_input[5]),
            similarity_odometer(car[6], car_input[6]),
            similarity_condition(car[7], car_input[7]),
            similarity_year(car[8], car_input[8])
        ]))

        if sim < max_similarity:
            max_similarity = sim
            most_similar_car = car
    return most_similar_car, max_similarity