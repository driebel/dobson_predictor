#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 21:15:04 2017

@author: David Riebel, Winterover 2017.
Drop me a line!  Let me know how your season is going
and if you love/hate this program

riebel.d@gmail.com
"""

from tkinter import *
import ephem
import datetime as dt
import pandas as pd
from math import pi
import os
import pytz
import sys

all_months = ['junk', 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September']
# Add junk so that index matches actual month number

old_stdout = sys.stdout  # Need this to restore stdout
aro = ephem.Observer()  # Define aro as an observer
aro.lat = '-89.99'  # ARO's latitude
aro.lon = '0.0'  # use 0 to align our north with 0 latitude.
# Thus azimuth is already on the grid system.
aro.elevation = 2864  # good value for ARO's elevation, taken from SkySonde
aro.temp = -60  # Eh, -60 seems like a good typical winter temp
aro.pressure = 680  # 680 mb is a good typical pressure

moon = ephem.Moon()  # initialize moon ephemeris object
min_obs_alt = 10.0 * pi/180  # 10 degrees in radians
right_edge = 250.0 * pi/180  # Approx max view angle out right side window
left_edge = 140.0 * pi/180  # Approx max view angle out left side window
utc_tz = pytz.timezone('UTC')
station_tz = pytz.timezone('Pacific/Auckland')
day_fmt = '%d %b'
time_fmt = '%H:%M'
resolution = 5*60  # Set resolution to 5 minutes in seconds


# Define a way to redirect the output of print to the tkinter text box
class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)


def display_month(month, year, file_name, display_tz, save_output=False):
    outdir = os.path.join(os.path.expanduser('~'), 'Desktop')
    out_file = os.path.join(outdir, file_name)
    month_name = all_months[month]
    time_test = dt.datetime(year, month, 1)  # First of the month
    time_test = display_tz.localize(time_test)
    # Define time_test in display TZ, so the entire month is covered
    if display_tz == station_tz:
        chosen_tz = 'Station Time'
    else:
        chosen_tz = 'UTC'
    # Loop over the entire month in five minute steps, calculate the alt az
    # at each time and see if it meets our observation criteria.
    # alt must be greater than 10 degrees, azimuth must be in the windows
    # All interior calculations done in UTC
    obs_window = []  # This will be a list of all valid observation times
    while time_test.month == month:
        aro.date = time_test.astimezone(utc_tz)  # ephem requires UTC always
        moon.compute(aro)
        if (moon.alt >= min_obs_alt and moon.az <= right_edge and
          moon.az >= left_edge and moon.phase >= 50):
            obs_window.append(time_test)
        time_test += dt.timedelta(0, resolution)  # test at 5min intervals

    index = [i.day for i in obs_window]
    obs_window = pd.Series(obs_window, index=index)
    index = pd.Series(index)  # Covert the index to a series to use unique
    days_of_observations = index.unique()
    col1 = 'Date'
    col2 = "Window Starts"
    col3 = "Window Ends"
    col4 = "Phase (%)"
    if save_output:
        output = open(out_file, 'a')
    else:
        output = sys.stdout
    print("Dobson Observation Window for {} {}"
          .format(month_name, year), file=output)
    print("All times in {}".format(chosen_tz), file=output)
    print("{:8}  {:^15}  {:^15}    {:^15} {:^15} {:^9}".format(
            col1, col2, col3, col2, col3, col4), file=output)
    for i in days_of_observations:
        if type(obs_window.loc[i]) == pd.tslib.Timestamp:
            pass
# if there is only one time stamp in a day, the min/max functions fail.
# This is rare, but kills the program. Just skip those days.
        else:
            window_start_1 = min(obs_window.loc[i])
            window_close_2 = max(obs_window.loc[i])
            window_start_2 = 0
            window_close_1 = 0
            one_day = obs_window.loc[i]  # Extract one day of moon locations
            for j in range(0, len(one_day) - 1):
                if (one_day.iloc[j+1] - one_day.iloc[j] >
                      dt.timedelta(0, resolution)):
                    window_close_1 = one_day.iloc[j]
                    window_start_2 = one_day.iloc[j+1]
            day = dt.datetime(year=year, month=month, day=i)
            day = display_tz.localize(day)
            aro.date = window_start_1
            moon.compute(aro)

            if window_start_2 != 0:
                print('{:8}  {:^15}  {:^15}   {:^15}  {:^15}  {:^9}'.format(
                    day.astimezone(display_tz).strftime(day_fmt),
                    window_start_1.astimezone(display_tz).strftime(time_fmt),
                    window_close_1.astimezone(display_tz).strftime(time_fmt),
                    window_start_2.astimezone(display_tz).strftime(time_fmt),
                    window_close_2.astimezone(display_tz).strftime(time_fmt),
                    int(moon.phase)), file=output)
            else:
                gap = ' '
                print('{:8}  {:^15}  {:^15}   {:^15}  {:^15}  {:^9}'.format(
                    day.astimezone(display_tz).strftime(day_fmt),
                    window_start_1.astimezone(display_tz).strftime(time_fmt),
                    window_close_2.astimezone(display_tz).strftime(time_fmt),
                    gap, gap, int(moon.phase)), file=output)

    print('\n\n', file=output)
    if save_output:
        output.close()
# End display_month function


# Define the Tkinter Window which sets all parameters
main_window = Tk()
main_window.title('Dobson Observation Window Predictor')

year_frame = Frame(main_window, relief=GROOVE, borderwidth=2)
year_frame.pack(side=LEFT)

month_frame = Frame(year_frame, relief=GROOVE, borderwidth=2)
month_frame.pack(side=BOTTOM)

# msg = 'For what month shall I calculate the Dobson window?'
# Label(main_window, text=msg).pack(expand=YES, fill=BOTH)

Label(year_frame, text='Year').pack(side='top')
string_year = StringVar(main_window)
string_year.set(str(dt.date.today().year))
Entry(year_frame, textvariable=string_year).pack(expand=YES)


mar_var = IntVar()
mar = Checkbutton(month_frame, text='March', onvalue=3, offvalue=0,
                     variable=mar_var)

apr_var = IntVar()
apr = Checkbutton(month_frame, text='April', onvalue=4, offvalue=0,
                     variable=apr_var)

may_var = IntVar()
may = Checkbutton(month_frame, text='May', onvalue=5, offvalue=0,
                     variable=may_var)

jun_var = IntVar()
jun = Checkbutton(month_frame, text='June', onvalue=6, offvalue=0,
                     variable=jun_var)

jul_var = IntVar()
jul = Checkbutton(month_frame, text='July', onvalue=7, offvalue=0,
                     variable=jul_var)

aug_var = IntVar()
aug = Checkbutton(month_frame, text='August', onvalue=8, offvalue=0,
                     variable=aug_var)

sep_var = IntVar()
sep = Checkbutton(month_frame, text='September', onvalue=9, offvalue=0,
                     variable=sep_var)

month_checkboxes = [mar, apr, may, jun, jul, aug, sep]

for check in month_checkboxes:
    check.pack(anchor=W)


def use_all_months():
    if int(all_var.get()) == 99:
        for i in month_checkboxes:
            i.config(state=DISABLED)
    else:
        for i in month_checkboxes:
            i.config(state=NORMAL)


all_var = IntVar()
all_month_check = Checkbutton(year_frame, text='Entire Winter', onvalue=99,
                                 offvalue=0, command=use_all_months,
                                 variable=all_var, font='bold')
all_month_check.pack(expand=YES, fill=BOTH, side=BOTTOM)

tz_choice = StringVar(main_window)
tz_choice.set('UTC')

msg = 'What Time Zone would you like the results displayed in?'
Label(main_window, text=msg).pack(expand=YES, fill=BOTH)
u = Radiobutton(main_window, variable=tz_choice, value='UTC', text='UTC')
u.pack(expand=YES, fill=BOTH)

z = Radiobutton(main_window, variable=tz_choice, value='NZ', text='Station Time')
z.pack(expand=YES, fill=BOTH)

save_choice = StringVar(main_window)
save_choice.set('no')

msg = 'Would you like the results saved to a text file on the Desktop?'
Label(main_window, text=msg).pack(expand=YES, fill=BOTH)

no_sav = Radiobutton(main_window, variable=save_choice, value='no', text='No')
no_sav.pack(expand=YES, fill=BOTH)

sav = Radiobutton(main_window, variable=save_choice, value='yes', text='Yes')
sav.pack(expand=YES, fill=BOTH)


def begin_calc():
    year = int(string_year.get())
    if tz_choice.get() == 'NZ':
        display_tz = station_tz
    else:
        display_tz = utc_tz
    if save_choice.get() == 'yes':
        save_output = True
    else:
        save_output = False
        sys.stdout = StdRedirector(text)
    if all_var.get() == 99:
        month_number = [3, 4, 5, 6, 7, 8, 9]
    else:
        month_number = [mar_var.get(), apr_var.get(), may_var.get(),
                        jun_var.get(), jul_var.get(), aug_var.get(),
                        sep_var.get()]
        for i in range(month_number.count(0)):
            month_number.remove(0)
    if len(month_number) == 1:
        month_number = month_number[0]
        month_name = all_months[month_number]
        file_name = "dobson_window_{}_{}.txt".format(month_name, year)
        display_month(month_number, year, file_name, display_tz, save_output)
    else:
        file_name = "dobson_window_winter_{}.txt".format(year)
        for month in month_number:
            display_month(month, year, file_name, display_tz, save_output)


button_frame = Frame(main_window)
button_frame.pack(expand=YES, side=BOTTOM)
execute_button = Button(button_frame, text='Go!', command=begin_calc)
execute_button.pack(expand=YES, side=LEFT, padx=10)

text = Text(main_window, relief=SUNKEN)
sbar = Scrollbar(main_window)
sbar.config(command=text.yview)
text.config(yscrollcommand=sbar.set)
sbar.pack(side=RIGHT, fill=Y)
text.pack(side=BOTTOM, expand=YES, fill=BOTH)


def quit_action():
    sys.stdout = old_stdout
    main_window.destroy()


quit_button = Button(button_frame, text='Quit', command=quit_action)
quit_button.pack(expand=YES, side=RIGHT)

main_window.protocol('WM_DELETE_WINDOW', lambda: quit_action())
# Assign the close button to close gracefully by running the
# quit_action function

main_window.update_idletasks()  # Makes window choose its dimensions
# w = main_window.winfo_width()  # Width of the main window
w = 850  # Make main window 850 pixels wide
h = main_window.winfo_height()  # Height of the main window
ws = main_window.winfo_screenwidth()  # width of the screen
hs = main_window.winfo_screenheight()  # height of the screen
# calculate x and y coordinates for the Tk root window to be centered.
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
main_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

main_window.mainloop()
