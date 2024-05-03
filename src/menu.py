import tkinter as tk
from tkinter import ttk
from similarity import load_data, clean_df, calculate_car_similarity

class CarRecommendationApp:
    KNOWLEDGE_DB = 'car_prices_mini'
    def __init__(self, master):
        self.master_frame = master
        self.recc_frame = None
        self.master_frame.title("Car Recommendation System")

        self.df = None
        self.dic_input = {
            "maker": tk.StringVar(value="bmw"),
            "model": tk.StringVar(value="x5"),
            "body": tk.StringVar(value="suv"),
            "transmission": tk.StringVar(value="automatic"),
            "exterior_color": tk.StringVar(value="black"),
            "interior_color": tk.StringVar(value="black"),
            "odometer": tk.DoubleVar(value=37),
            "condition": tk.DoubleVar(value=5),
            "year": tk.IntVar(value=2015),
        }
        self.dic_weight = {
            "maker": tk.DoubleVar(value=1),
            "model": tk.DoubleVar(value=1),
            "body": tk.DoubleVar(value=1),
            "transmission": tk.DoubleVar(value=1),
            "exterior_color": tk.DoubleVar(value=1),
            "interior_color": tk.DoubleVar(value=1),
            "odometer": tk.DoubleVar(value=1),
            "condition": tk.DoubleVar(value=1),
            "year": tk.DoubleVar(value=1),
        }

        self.dic_tolerance_windows = {
            "odometer": tk.DoubleVar(value=0),
            "condition": tk.DoubleVar(value=0),
            "year": tk.DoubleVar(value=0),
        }


    def create_widgets(self):
        frm = ttk.Frame(self.master_frame, padding=10)
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
                if key in ("odometer", "year", "condition"):
                    ttk.Label(frm, text="Tolerance window (use 0 for default)").grid(
                        column=2, row=row, pady=5)
                    ttk.Entry(frm, textvariable=self.dic_tolerance_windows[key]).grid(
                        column=3, row=row, pady=5, padx=3)

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
        self.df = load_data(f"data/{self.KNOWLEDGE_DB}.zip", f"{self.KNOWLEDGE_DB}.csv")
        self.df = clean_df(self.df)

        # Transform user input into a more usable format.
        user_input = {}
        for key, var in self.dic_input.items():
            val = var.get()
            try:
                user_input[key.lower()] = float(val)
            except ValueError:
                user_input[key.lower()] = val.lower()

        tolerance_windows = {}
        for key, var in self.dic_tolerance_windows.items():
            val = var.get()
            if val > 0:
                tolerance_windows[key] = val

        user_weights = {key.lower(): var.get() for key, var in self.dic_weight.items()}

        # Calculate car similarity based on user input and weights
        self.df = calculate_car_similarity(user_input, self.df, user_weights, tolerance_windows)

        # Clear existing widgets in the master window
        # for widget in self.master_frame.winfo_children():
        #     widget.destroy()

        self.recc_frame = tk.Toplevel(self.master_frame)
        frm = ttk.Frame(self.recc_frame, padding=10)
        frm.grid()

        # Display user input and weights
        ttk.Label(frm, text="User Input:", font=("Helvetica", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        for idx, (k, value) in enumerate(user_input.items()):
            ttk.Label(frm, text=f"{k.capitalize()}: {value}").grid(
                row=idx + 1, column=0, sticky="w", padx=10, pady=5
            )
            ttk.Label(frm, text=f"Weight: {user_weights[k]}").grid(
                row=idx + 1, column=1, sticky="w", padx=10, pady=5
            )

        result_text = tk.Text(frm, height=20, width=120)
        result_text.grid(row=len(user_input) + len(user_weights) + 4, column=0, columnspan=2, padx=10, pady=10)
        result_text.insert(tk.END, self.df.head(10).to_string())
        result_text.configure(state="disabled") # Lock textbox so the user can't mess it up

        # Display top recommended cars
        # NOTE: iterrows() has some weird behavior here, I don't like this enumerate() hack.
        # i = 0
        # for i, (_, row) in enumerate(self.df.head(10).iterrows()):
        #     for col_idx, header in enumerate(headers):
        #         fmt_text = ""
        #         if header == 'similarity':
        #             fmt_text = f"{100 * row[header]:.2f}"
        #         else:
        #             fmt_text = f"{row[header]}"
        #
        #         ttk.Label(frm, text=fmt_text).grid(
        #             row=len(user_input) + len(user_weights) + i + 5,
        #             column=col_idx,
        #             padx=10,
        #             pady=5,
        #         )

        # Button to close the window
        ttk.Button(frm, text="Close", command=self.recc_frame.destroy).grid(
            row=len(user_input) + len(user_weights) + 5, column=0, columnspan=2, pady=10
        )


