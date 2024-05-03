from menu import *
from tkinter import Tk
from sys import exit

def main():
    root = Tk()
    root.title("Car Recommendation System")
    app = CarRecommendationApp(root)
    app.main_menu()

    root.mainloop()

if __name__ == "__main__":
    main()
    exit()
