from tkinter import *
from tkinter import ttk
from utils import load_data, clean_df, calculate_car_similarity


class CarRecommendationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Recommendation System")

        self.df = None
        self.dic_input = {
            "maker": StringVar(value="bmw"),
            "model": StringVar(value="x5"),
            "body": StringVar(value="suv"),
            "transmission": StringVar(value="automatic"),
            "exterior_color": StringVar(value="black"),
            "interior_color": StringVar(value="black"),
            "odometer": StringVar(value="37"),
            "condition": StringVar(value="5"),
            "year": StringVar(value="2015"),
        }
        self.dic_weight = {
            "maker": DoubleVar(value=1),
            "model": DoubleVar(value=1),
            "body": DoubleVar(value=1),
            "transmission": DoubleVar(value=1),
            "exterior_color": DoubleVar(value=1),
            "interior_color": DoubleVar(value=1),
            "odometer": DoubleVar(value=1),
            "condition": DoubleVar(value=1),
            "year": DoubleVar(value=1),
        }

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.grid()

        row = 0
        for key in self.dic_input:
            ttk.Label(frm, text=f"{key.capitalize()}:").grid(
                column=0, row=row, sticky="e"
            )

            if key == "exterior_color":
                colors = [
                    "White",
                    "Gray",
                    "Black",
                    "Red",
                    "Silver",
                    "Brown",
                    "Beige",
                    "Blue",
                    "Purple",
                    "Burgundy",
                    "Gold",
                    "Yellow",
                    "Green",
                    "Charcoal",
                    "Orange",
                    "Off-White",
                    "Turquoise",
                    "Pink",
                    "Lime",
                ]

                color_combo = ttk.Combobox(
                    frm, textvariable=self.dic_input[key], values=colors
                )
                color_combo.grid(column=1, row=row, pady=5)
                color_combo.current(2)

            elif key == "interior_color":
                colors = [
                    "White",
                    "Gray",
                    "Black",
                    "Red",
                    "Silver",
                    "Brown",
                    "Beige",
                    "Blue",
                    "Purple",
                    "Burgundy",
                    "Gold",
                    "Yellow",
                    "Green",
                    "Orange",
                    "Off-White",
                    "Tan",
                ]

                color_combo = ttk.Combobox(
                    frm, textvariable=self.dic_input[key], values=colors
                )
                color_combo.grid(column=1, row=row, pady=5)
                color_combo.current(2)

            elif key == "body":
                cars_body = ["suv", "sedan", "van", "cab", "convertible"]
                body_combo = ttk.Combobox(
                    frm, textvariable=self.dic_input[key], values=cars_body
                )
                body_combo.grid(column=1, row=row, pady=5)
                body_combo.current(0)

            else:
                ttk.Entry(frm, textvariable=self.dic_input[key]).grid(
                    column=1, row=row, pady=5
                )

            row += 1

        # Labels and Entry Widgets for weights
        row += 1
        ttk.Label(frm, text="Enter Weights:").grid(
            column=0, row=row, columnspan=2, pady=10
        )

        row += 1
        for key in self.dic_weight:
            ttk.Label(frm, text=f"{key.capitalize()} Weight:").grid(
                column=0, row=row, sticky="e"
            )
            ttk.Entry(frm, textvariable=self.dic_weight[key]).grid(
                column=1, row=row, pady=5
            )
            row += 1

        # Button to calculate and display recommendations
        ttk.Button(
            frm, text="Get Recommendations", command=self.get_recommendations
        ).grid(column=0, row=row, columnspan=2, pady=10)

    def get_recommendations(self):
        # Load and clean the car data
        self.df = load_data("data/car_prices.zip", "car_prices.csv")
        self.df = clean_df(self.df)

        # Get user input and weights
        user_input = {key: var.get().lower() for key, var in self.dic_input.items()}
        user_weights = {key: var.get() for key, var in self.dic_weight.items()}

        # Calculate car similarity based on user input and weights
        self.df = calculate_car_similarity(user_input, self.df, user_weights)

        # Clear existing widgets in the master window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Create a new frame for displaying recommendations
        frm = ttk.Frame(self.master, padding=10)
        frm.grid()

        # Display user input and weights
        ttk.Label(frm, text="User Input:", font=("Helvetica", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )
        for idx, (key, value) in enumerate(user_input.items()):
            ttk.Label(frm, text=f"{key.capitalize()}: {value}").grid(
                row=idx + 1, column=0, sticky="w", padx=10, pady=5
            )
            ttk.Label(frm, text=f"Weight: {user_weights[key]}").grid(
                row=idx + 1, column=1, sticky="w", padx=10, pady=5
            )

        # Display recommendation headers
        headers = self.df.columns
        for col_idx, header in enumerate(headers):
            ttk.Label(
                frm, text=f"{header.capitalize()}", font=("Helvetica", 12, "bold")
            ).grid(
                row=len(user_input) + len(user_weights) + 4,
                column=col_idx,
                padx=10,
                pady=5,
            )

        # Display top recommended cars
        for i, (index, row) in enumerate(self.df.head(10).iterrows()):
            for col_idx, header in enumerate(headers):
                ttk.Label(frm, text=f"{row[header]:.2}").grid(
                    row=len(user_input) + len(user_weights) + i + 5,
                    column=col_idx,
                    padx=10,
                    pady=5,
                )

        # Button to close the window
        ttk.Button(frm, text="Close", command=self.master.destroy).grid(
            row=len(user_input) + len(user_weights) + i + 6,
            column=0,
            columnspan=len(headers),
            pady=10,
        )
