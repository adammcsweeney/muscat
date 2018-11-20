# module for assessing the relative geometry between the Sun, Earth, and a target planet for user defined time-frame
# outputs distances and conjunction periods

# TODO === fix treatment of dates to speed up script
# TODO === add conjunction finding function

import numpy as np
import pykep as pk
import matplotlib.pyplot as plt
import matplotlib.dates as dlt
import datetime as dt
import math as math

# 1. INPUTS

# target planet
target_pl = 'Mars'

# reference timeframe
initial_epoch = '2026-01-01'
final_epoch = '2036-01-01'


# 2. REFERENCE DATA

# planets
earth = pk.planet.jpl_lp('earth')
target = pk.planet.jpl_lp(target_pl)

# timeframe
timefix = " 00:00"
initial_epoch = pk.epoch_from_string(initial_epoch+timefix).mjd2000
final_epoch = pk.epoch_from_string(final_epoch+timefix).mjd2000


# 3. FUNCTIONS

# angle between vectors

def angle_find(v1, v2):

    A = np.cross(v1,v2)

    B = np.dot(v1,v2)

    ThetaInRadians = np.arctan2(np.linalg.norm(A), B)

    ThetaInDegrees = math.degrees(ThetaInRadians)

    return ThetaInDegrees

# generate data on angles for date range

# SET angle - Sun-Earth-Target angle

def SET_angle_data(screen_output=True, steps=1):

    # create data containers

    epochs = []
    dates = []
    STE_angles = []

    # first line of data report

    if screen_output:
        print(f"{'Epoch'}\t{'Sun-Earth-Target angle (deg)'}")

    # generate data

    for date in np.arange(initial_epoch, final_epoch, steps):

        # set current epoch
        epoch = pk.epoch(date)


        # get position vectors

        # (1) Sun - Earth
        r1 , __ = earth.eph(date)

        # (2) Earth - Target
        r , __ = target.eph(date)

        x2 = r1[0] - r[0]
        y2 = r1[1] - r[1]
        z2 = r1[2] - r[2]

        r2 = (x2, y2, z2)

        # find angle
        SunEarthTargAngle = angle_find(r1,r2)

        # get dates in correct format
        date = dlt.datestr2num(str(epoch))
        date = dlt.num2date(date)
        date = str(date)[:10]

        # collect data

        epochs.append(epoch)
        dates.append(date)
        STE_angles.append(SunEarthTargAngle)

        if screen_output:
            print(f"{epoch}\t{SunEarthTargAngle}")

    return epochs, dates, STE_angles

# SET angle - Sun-Target-Earth angle

def STE_angle_data(screen_output=True, steps=1):

    # create data containers

    epochs = []
    dates = []
    SET_angles = []

    # first line of data report

    if screen_output:
        print(f"{'Epoch'}\t{'Sun-Target-Earth angle (deg)'}")

    # generate data

    for date in np.arange(initial_epoch, final_epoch, steps):

        # set current epoch
        epoch = pk.epoch(date)

        # get position vectors

        # (1) Sun - Target
        r1, __ = target.eph(date)

        # (2) Earth - Target
        r, __ = earth.eph(date)

        x2 = r1[0] - r[0]
        y2 = r1[1] - r[1]
        z2 = r1[2] - r[2]

        r2 = (x2, y2, z2)

        # find angle
        SunTargEarthAngle = angle_find(r1, r2)

        # get dates in correct format
        date = dlt.datestr2num(str(epoch))
        date = dlt.num2date(date)
        date = str(date)[:10]

        # collect data

        epochs.append(epoch)
        dates.append(date)
        SET_angles.append(SunTargEarthAngle)

        if screen_output:
            print(f"{epoch}\t{SunTargEarthAngle}")

    return epochs, dates, SET_angles

def plot_angles():

    # generate and collect data

    epochs, dates, SET_angles = SET_angle_data()
    __, __, STE_angles = STE_angle_data()

    # format dates

    dates = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]

    # plot set-up

    plt.gca().xaxis.set_major_formatter(dlt.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(dlt.YearLocator())
    plt.plot(dates, SET_angles, linewidth=1.5, linestyle=':', label='Sun-Earth-'+target_pl, color='dodgerblue')
    plt.plot(dates, STE_angles, linewidth=1.5, linestyle='-', label='Sun-' + target_pl + '-Earth', color='orangered')
    plt.xticks(rotation=90)

    # tick parameters
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')

    # grid parameters
    plt.grid(color='lightgrey', linestyle=':', linewidth=0.5)

    # axis labels
    plt.ylabel('Angles (deg)')
    plt.xlabel('Date')

    plt.xlim(dates[0], dates[-1])
    plt.ylim(0, 180)
    # plt.gcf().autofmt_xdate()

    plt.legend(loc=0)

    plt.tight_layout()

    plt.show()

# 4. OUTPUTS

plot_angles()
