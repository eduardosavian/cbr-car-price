import numpy as np
import pandas as pd
import zipfile
from openpyxl import Workbook  # Import Workbook from openpyxl


exterior_color_map = {
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "silver": (192, 192, 192),
    "brown": (165, 42, 42),
    "beige": (245, 245, 200),
    "blue": (0, 0, 255),
    "purple": (128, 128, 128),
    "burgundy": (128, 0, 32),
    "gold": (255, 215, 0),
    "yellow": (255, 255, 0),
    "green": (0, 128, 0),
    "charcoal": (54, 69, 79),
    "orange": (255, 165, 0),
    "off-white": (255, 255, 250),
    "turquoise": (64, 224, 208),
    "pink": (255, 192, 203),
    "lime": (0, 255, 0),
}

interior_color_map = {
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "silver": (192, 192, 192),
    "brown": (165, 42, 42),
    "beige": (245, 245, 200),
    "blue": (0, 0, 255),
    "purple": (128, 128, 128),
    "burgundy": (128, 0, 32),
    "gold": (255, 215, 0),
    "yellow": (255, 255, 0),
    "green": (0, 128, 0),
    "orange": (255, 165, 0),
    "off-white": (255, 255, 250),
    "tan": (210, 180, 140),
}

color_map = {}
color_map.update(exterior_color_map)
color_map.update(interior_color_map)


def load_data(zip_name, file_name):
    archive = zipfile.ZipFile(zip_name)
    df = pd.read_csv(archive.open(file_name))

    return df

def clean_body_types(body_type):
    if isinstance(body_type, str):  # Check if the value is a string
        body_type = body_type.strip().lower()  # Convert to lowercase and remove extra spaces
        if body_type in ['suv', 'sport utility vehicle']:
            return 'suv'
        elif body_type in ['sedan', 'saloon', 'hatchback', 'wagon', 'estate', 'g sedan']:
            return 'sedan'
        elif body_type in ['convertible', 'coupe', 'g coupe', 'Elantra Coupe', 'cts-v coupe', 'g37 coupe', 'g37 convertible', 'q60 coupe', 'q60 convertible', 'koup']:
            return 'convertible'
        elif body_type in ['van', 'minivan', 'e-series van', 'ram van', 'transit van', 'promaster cargo van']:
            return 'van'
        elif body_type in [
            'crew cab', 'double cab', 'extended cab', 'regular cab', 'supercrew', 'crewmax cab',
            'access cab', 'king cab', 'quad cab', 'super cab', 'club cab', 'mega cab', 'xtracab',
            'cab plus 4', 'cab plus', 'SuperCab'
        ]:
            return 'cab'  # Example category for various cab types
        else:
            return 'other'  # Assign 'other' category for unknown types or unique categories
    else:
        return 'other'  # Handle NaN values by assigning to 'other' category



def clean_df(df):
    drop_list = ["trim", "vin", "state", "saledate", "seller", "mmr"]

    df = df.drop(columns=drop_list, axis=1)

    columns_rename = {
        "make": "maker",
        "sellingprice": "price",
        "color": "exterior_color",
        "interior": "interior_color",
    }
    df = df.rename(columns=columns_rename)

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

    numeric_columns = ["odometer", "condition", "year", "price"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].astype(float)

    df = df.dropna(how="any")

    df['body'] = df['body'].apply(clean_body_types)

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.lower()

    filter_columns = ["exterior_color", "interior_color"]
    invalid_value = "—"

    for col in filter_columns:
        df = df[~df[col].str.contains(invalid_value)]

    filter_columns = ["body"]
    invalid_value = "other"

    for col in filter_columns:
        df = df[~df[col].str.contains(invalid_value)]

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
    return np.abs(float(condition1) - float(condition2)) / float(condition2)


def similarity_odometer(odometer1, odometer2):
    return np.abs(float(odometer1) - float(odometer2)) / float(odometer2)


def similarity_color(color1, color2):
    r1, g1, b1 = color_map[color1]
    r2, g2, b2 = color_map[color2]
    return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2


def similarity_year(year1, year2):
    return (float(year1) - float(year2)) ** 2


def calculate_car_similarity(car_input, df, weights):
    weights = np.array(list(weights.values()))
    cars = df.to_numpy()
    cars = np.concatenate((cars, np.zeros((cars.shape[0], 1))), axis=1)
    car_input = np.array(list(car_input.values()))

    for car in cars:
        sim = np.sum(
            weights
            * np.array(
                [
                    similarity_maker(car[0], car_input[0]),
                    similarity_model(car[1], car_input[1]),
                    similarity_body(car[2], car_input[2]),
                    similarity_transmission(car[3], car_input[3]),
                    similarity_color(car[4], car_input[4]),
                    similarity_color(car[5], car_input[5]),
                    similarity_odometer(car[6], car_input[6]),
                    similarity_condition(car[7], car_input[7]),
                    similarity_year(car[8], car_input[8]),
                ]
            )
        )

        car[-1] = sim

    cars = pd.DataFrame(cars, columns=list(df.columns) + ["similarity"])
    cars = cars.sort_values(by="similarity")

    return cars
