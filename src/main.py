from menu import *

def main():
    root = Tk()
    root.title("Car Recommendation System")

    # Initialize the GUI application
    app = CarRecommendationApp(root)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
    exit()
