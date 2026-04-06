"""
This file contains the simple code to set an alarm on the system

It uses Python's Tkinter and time modules to create GUIs and update current time.

This module along with the clock module constitute the alarm clock project. This
module doesn't use the pygame library due to build errors
"""
import datetime
import time
import threading
import tkinter as tk

def thread():
    global t1
    t1 = threading.Thread(target=alarm)
    t1.start()


def alarm():
    # alarm set to an infinite loop
    global hour
    global minute
    global second

    while True:
        # alarm set
        set_alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
        time.sleep(1)

        # get current time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time, set_alarm_time)

        # condition to check if set time is equal to current time
        if current_time == set_alarm_time:
            print("Wake Up now!")


def stop_alarm():
    global t1
    print("Stop Alarm")
    del t1


def main():
    # create Windows and other variables
    window = tk.Tk()
    window.geometry("500x250")
    t1 = "thread_var"

    tk.Label(window, text="Alarm Clock", font=("Helvetica 20 bold"),
             fg="red").pack(pady=10)
    tk.Label(window, text="Set Time", font=("Helvetica 15 bold")).pack()

    frame = tk.Frame(window)
    frame.pack()

    hour = tk.StringVar(window)
    hours = ("0" + str(_hour) if _hour < 10 else str(_hour) for _hour in
             range(0, 25))
    hour.set(hours[0])

    hrs = tk.OptionMenu(frame, hour, *hours)
    hrs.pack(side=tk.LEFT)

    minute = tk.StringVar(window)
    minutes = (
        "0" + str(_minute) if _minute < 10 else str(_minute) for _minute in
    range(0, 61)
    )
    minute.set(minutes[0])

    mins = tk.OptionMenu(frame, minute, *minutes)
    mins.pack(side=tk.LEFT)

    second = tk.StringVar(window)
    seconds = (
        "0" + str(_second) if _second < 10 else str(_second) for _second in
    range(0, 61)
    )
    second.set(seconds[0])

    secs = tk.OptionMenu(frame, second, *seconds)
    secs.pack(side=tk.LEFT)

    tk.Button(window, text="Set Alarm", font=("Helvetica 15"),
              command=thread).pack(pady=20)

    tk.Button(
        window, text="Stop Alarm", bg="red", fg="white", command=stop_alarm
    ).pack(pady=30)

    window.mainloop()

if __name__ == "__main__":
    main()