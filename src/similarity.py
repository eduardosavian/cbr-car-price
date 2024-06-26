import numpy as np
import pandas as pd
import zipfile

exterior_color_map = {
    "white"    : np.array([255, 255, 255], dtype=np.float32),
    "gray"     : np.array([128, 128, 128], dtype=np.float32),
    "black"    : np.array([0, 0, 0], dtype=np.float32),
    "red"      : np.array([255, 0, 0], dtype=np.float32),
    "silver"   : np.array([192, 192, 192], dtype=np.float32),
    "brown"    : np.array([165, 42, 42], dtype=np.float32),
    "beige"    : np.array([245, 245, 200], dtype=np.float32),
    "blue"     : np.array([0, 0, 255], dtype=np.float32),
    "purple"   : np.array([128, 128, 128], dtype=np.float32),
    "burgundy" : np.array([128, 0, 32], dtype=np.float32),
    "gold"     : np.array([255, 215, 0], dtype=np.float32),
    "yellow"   : np.array([255, 255, 0], dtype=np.float32),
    "green"    : np.array([0, 128, 0], dtype=np.float32),
    "charcoal" : np.array([54, 69, 79], dtype=np.float32),
    "orange"   : np.array([255, 165, 0], dtype=np.float32),
    "off-white": np.array([255, 255, 250], dtype=np.float32),
    "turquoise": np.array([64, 224, 208], dtype=np.float32),
    "pink"     : np.array([255, 192, 203], dtype=np.float32),
    "lime"     : np.array([0, 255, 0], dtype=np.float32),
}

interior_color_map = {
    "white"    : np.array([255, 255, 255], dtype=np.float32),
    "gray"     : np.array([128, 128, 128], dtype=np.float32),
    "black"    : np.array([0, 0, 0], dtype=np.float32),
    "red"      : np.array([255, 0, 0], dtype=np.float32),
    "silver"   : np.array([192, 192, 192], dtype=np.float32),
    "brown"    : np.array([165, 42, 42], dtype=np.float32),
    "beige"    : np.array([245, 245, 200], dtype=np.float32),
    "blue"     : np.array([0, 0, 255], dtype=np.float32),
    "purple"   : np.array([128, 128, 128], dtype=np.float32),
    "burgundy" : np.array([128, 0, 32], dtype=np.float32),
    "gold"     : np.array([255, 215, 0], dtype=np.float32),
    "yellow"   : np.array([255, 255, 0], dtype=np.float32),
    "green"    : np.array([0, 128, 0], dtype=np.float32),
    "orange"   : np.array([255, 165, 0], dtype=np.float32),
    "off-white": np.array([255, 255, 250], dtype=np.float32),
    "tan"      : np.array([210, 180, 140], dtype=np.float32),
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
        body_type = (
            body_type.strip().lower()
        )  # Convert to lowercase and remove extra spaces
        if body_type in ["suv", "sport utility vehicle"]:
            return "suv"
        elif body_type in [
            "sedan",
            "saloon",
            "hatchback",
            "wagon",
            "estate",
            "g sedan",
        ]:
            return "sedan"
        elif body_type in [
            "convertible",
            "coupe",
            "g coupe",
            "Elantra Coupe",
            "cts-v coupe",
            "g37 coupe",
            "g37 convertible",
            "q60 coupe",
            "q60 convertible",
            "koup",
        ]:
            return "convertible"
        elif body_type in [
            "van",
            "minivan",
            "e-series van",
            "ram van",
            "transit van",
            "promaster cargo van",
        ]:
            return "van"
        elif body_type in [
            "crew cab",
            "double cab",
            "extended cab",
            "regular cab",
            "supercrew",
            "crewmax cab",
            "access cab",
            "king cab",
            "quad cab",
            "super cab",
            "club cab",
            "mega cab",
            "xtracab",
            "cab plus 4",
            "cab plus",
            "SuperCab",
        ]:
            return "cab"
        else:
            return "other"
    else:
        return "other"


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

    df["body"] = df["body"].apply(clean_body_types)

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


body_similarity_matrix = {
    "suv": {
        "suv": 1.0,
        "sedan": 0.3,
        "convertible": 0.1,
        "van": 0.2,
        "cab": 0.6,
        "other": 0.2,
    },
    "sedan": {
        "suv": 0.3,
        "sedan": 1.0,
        "convertible": 0.6,
        "van": 0.2,
        "cab": 0.2,
        "other": 0.4,
    },
    "convertible": {
        "suv": 0.1,
        "sedan": 0.6,
        "convertible": 1.0,
        "van": 0.2,
        "cab": 0.2,
        "other": 0.3,
    },
    "van": {
        "suv": 0.2,
        "sedan": 0.2,
        "convertible": 0.2,
        "van": 1.0,
        "cab": 0.4,
        "other": 0.3,
    },
    "cab": {
        "suv": 0.6,
        "sedan": 0.2,
        "convertible": 0.2,
        "van": 0.4,
        "cab": 1.0,
        "other": 0.5,
    },
    "other": {
        "suv": 0.2,
        "sedan": 0.2,
        "convertible": 0.2,
        "van": 0.2,
        "cab": 0.2,
        "other": 1.0,
    },
}


def similarity_body(body1, body2):
    return body_similarity_matrix[body1][body2]


def similarity_symbols(symbol1, symbol2):
    return 1 if symbol1 == symbol2 else 0

def numeric_similarity(a, b, lo, hi):
    return 1 - np.abs((a - b) / (hi - lo))

def similarity_color(color1, color2):
    r1, g1, b1 = color_map[color1]
    r2, g2, b2 = color_map[color2]
    return 1 - np.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def calculate_car_similarity(car_input, df, weights, tolerance_windows: dict):
    weights = np.array(list(weights.values()))
    cars = df.to_numpy()
    cars = np.concatenate((cars, np.zeros((cars.shape[0], 1))), axis=1)
    car_input = np.array(list(car_input.values()))

    odometer_hi, odometer_lo = 0, 0
    condition_hi, condition_lo = 0, 0
    year_hi, year_lo = 0, 0

    if "odometer" in tolerance_windows:
        odometer_hi = tolerance_windows["odometer"]
        odometer_lo = - tolerance_windows["odometer"]
    else:
        odometer_hi = df["odometer"].max()
        odometer_lo = df["odometer"].min()

    if "year" in tolerance_windows:
        year_hi = tolerance_windows["year"]
        year_lo = - tolerance_windows["year"]
    else:
        year_hi = df["year"].max()
        year_lo = df["year"].min()

    if "condition" in tolerance_windows:
        condition_hi = tolerance_windows["condition"]
        condition_lo = - tolerance_windows["condition"]
    else:
        condition_hi = df["condition"].max()
        condition_lo = df["condition"].min()

    weights /= np.sum(weights)

    for car in cars:
        sim = np.sum(
            weights * np.array(
                [
                    similarity_symbols(car_input[0], car[0]),
                    similarity_symbols(car_input[1], car[1]),
                    similarity_body(car_input[2],    car[2]),
                    similarity_symbols(car_input[3], car[3]),
                    similarity_color(car_input[4],   car[4]),
                    similarity_color(car_input[5],   car[5]),
                    numeric_similarity(float(car_input[6]), float(car[6]), odometer_lo,  odometer_hi),
                    numeric_similarity(float(car_input[7]), float(car[7]), condition_lo, condition_hi),
                    numeric_similarity(float(car_input[8]), float(car[8]), year_lo,      year_hi),
                ]
            )
        )

        car[-1] = sim

    cars = pd.DataFrame(cars, columns=list(df.columns) + ["similarity"])
    cars = cars.sort_values(by="similarity", ascending=False)

    return cars
