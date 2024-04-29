from tkinter import *
from tkinter import ttk
from utils import load_data, clean_df, calculate_car_similarity

class CarRecommendationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Recommendation System")

        # Initialize data structures
        self.df = None
        self.dic_input = {
            "maker": StringVar(value="Toyota"),
            "model": StringVar(value="Corolla"),
            "body": StringVar(value="Sedan"),
            "transmission": StringVar(value="automatic"),
            "exterior_color": StringVar(value="black"),
            "interior_color": StringVar(value="black"),
            "condition": StringVar(value="50"),
            "odometer": StringVar(value="100000"),
            "year": StringVar(value="2018")
        }
        self.dic_weight = {
            "maker": DoubleVar(value=25),
            "model": DoubleVar(value=5),
            "body": DoubleVar(value=20),
            "transmission": DoubleVar(value=10),
            "exterior_color": DoubleVar(value=2),
            "interior_color": DoubleVar(value=2),
            "condition": DoubleVar(value=15),
            "odometer": DoubleVar(value=16),
            "year": DoubleVar(value=6)
        }

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.grid()

        # Labels and Entry Widgets for user input
        row = 0
        for key in self.dic_input:
            ttk.Label(frm, text=f"{key.capitalize()}:").grid(column=0, row=row, sticky='e')

            if key == "exterior_color":
                colors = [
                    "White", "Gray", "Black", "Red", "Silver", "Brown", "Beige", "Blue",
                    "Purple", "Burgundy", "Gold", "Yellow", "Green", "Charcoal", "Orange",
                    "Off-White", "Turquoise", "Pink", "Lime"
                ]
                # Dropdown menu for exterior color selection
                color_combo = ttk.Combobox(frm, textvariable=self.dic_input[key], values=colors)
                color_combo.grid(column=1, row=row, pady=5)
                color_combo.current(2)  # Set default to "Black"

            elif key == "interior_color":
                colors = [
                    "White", "Gray", "Black", "Red", "Silver", "Brown", "Beige", "Blue",
                    "Purple", "Burgundy", "Gold", "Yellow", "Green", "Orange", "Off-White",
                    "Tan"
                ]
                # Dropdown menu for interior color selection
                color_combo = ttk.Combobox(frm, textvariable=self.dic_input[key], values=colors)
                color_combo.grid(column=1, row=row, pady=5)
                color_combo.current(2)  # Set default to "Black"

            else:
                # Normal Entry widget for other attributes
                ttk.Entry(frm, textvariable=self.dic_input[key]).grid(column=1, row=row, pady=5)

            row += 1


            row += 1

        # Labels and Entry Widgets for weights
        row += 1
        ttk.Label(frm, text="Enter Weights:").grid(column=0, row=row, columnspan=2, pady=10)

        row += 1
        for key in self.dic_weight:
            ttk.Label(frm, text=f"{key.capitalize()} Weight:").grid(column=0, row=row, sticky='e')
            ttk.Entry(frm, textvariable=self.dic_weight[key]).grid(column=1, row=row, pady=5)
            row += 1

        # Button to calculate and display recommendations
        ttk.Button(frm, text="Get Recommendations", command=self.get_recommendations).grid(column=0, row=row, columnspan=2, pady=10)

    def get_recommendations(self):
        # Load and process data
        self.df = load_data("data/car_prices_data.zip", "car_prices.csv")
        self.df = clean_df(self.df)

        # Prepare input and weights
        user_input = {key: var.get().lower() for key, var in self.dic_input.items()}
        user_weights = {key: var.get() for key, var in self.dic_weight.items()}

        # Calculate recommendations
        self.df = calculate_car_similarity(user_input, self.df, user_weights)

        # Display recommendations (for demonstration, you can customize this)
        top_recommendations = self.df.head(3)
        print(top_recommendations)  # For now, just printing to console

