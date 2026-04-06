"""
This file contains the simple code to display current time and stage of the
day in a separate window.

It uses Python's Tkinter and time modules to create GUIs and update current time.

This module along with the alarm module constitute the alarm clock project.
"""

import time
import tkinter as tk


# Function to determine the time of day
def get_time_of_day(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"


def main():
    # Create App Window
    window = tk.Tk()
    window.title("Dynamic Clock")
    window.resizable(width=0, height=0)

    clock_time = tk.Label(
        window, font=("courier new", 40), background="black", foreground="white"
    )

    clock_time.pack(anchor="center")

    ##################################### START UPDATE_TIME() ##################
    # Define update time in scope of the tools rather than pass the UI elements
    # all the time
    def update_time():
        current_time = time.strftime("%H:%M:%S %p")
        hour = int(time.strftime("%H"))
        time_of_day = get_time_of_day(hour)

        # Update the text of the clockTime Label with the current time and time of day
        clock_time.config(text=current_time + f"\nGood {time_of_day}!")

        # Dynamically change the background color based on time of day
        color = (
            "lightblue"
            if time_of_day == "Morning"
            else "lightyellow" if time_of_day == "Afternoon" else "lightcoral"
        )
    ##################################### END UPDATE_TIME() ###################

        window.configure(background=color)

        # Schedule the update_time function to be called again after 1000
        # milliseconds (1 second)
        clock_time.after(1000, update_time)

    update_time()

    window.mainloop()


if __name__ == "__main__":
    main()
