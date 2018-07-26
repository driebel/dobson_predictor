# dobson_predictor
This is the dobson observation program I wrote at pole


Instructions for Dobson Predictor Program

Author: David Riebel (riebel.d@gmail.com) Winterover 2017

This is a simple program which generates basic text calendars for performing lunar Dobson observations at the NOAA Atmospheric Research Observatory, South Pole, Antarctica.  Lunar Dobsons can only be performed when the moon is bright (> 50%), above the minimum observation altitude (10 degrees), and visible from the windows in the Dobson room of ARO (azimuth between grid 250 and 140 degrees).  The time when all of those conditions are met varies from month to month.  This program allows the observer to determine the schedule of observation windows for a given month or an entire winter season all at once.

Begin the program by double clicking on the dobson_predictor.exe file.  A GUI window will open, allowing you to customize what schedule you wish to see.

On the upper left side of the window, enter the year of the observations you would like to calculate.  This defaults to the current year.

Below the year entry field, a series of checkboxes allows you to select individual months, or to calculate an entire winter's schedule at once.

The right side of the window allows you to specify the format of the output.  Select whether you would like the results displayed in UTC or local station (NZ) time.  Yes, The program automatically handles daylight savings time if asking for results in station time.  Next choose whether you would like the results saved to a text file on the Desktop or simply displayed in the GUI window.  If you save the results to a file, it  will be called dobson_window_<month>_<year>.txt if only a single month is calculated, or dobson_window_winter_<year>.txt if more than one month is selected.

Once you have specified your query, click the "Go!" button to calculate the Dobson observation schedule for the chosen period.  The program takes about a second to generate a single month, and about 3-4 seconds to do an entire winter.

Many days have two observation windows, one in the morning and again at night, these are displayed from left to right.  All times are given in the 24-hour clock because we are not savages.  If a day only has one observation window, the columns for the second window are left blank.  The lunar phase is also displayed, so you can decide when to launch a balloon (near full moon) and when to perform a Brewer sighting (also near the full moon).  The program does *NOT* take the sun into account at all, so it will produce "valid" observation windows during times when it is too bright to observe the moon.  Ignore those, obviously.

You can run as many queries as you'd like while the window is open.  When you're done, either click the "Quit" button or just close the window.

The program is written in Python 3, and nerds can find the source code in dobson_predictor.py (hopefully kept in the same directory as these instructions).

Feel free to drop me a line and let me know how your season is going and if you've found this program useful or have questions!
