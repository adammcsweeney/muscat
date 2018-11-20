# module for assessing the relative geometry between the Sun, Earth, and a target planet for user defined time-frame
# outputs distances and conjunction periods

# TODO === fix treatment of dates to speed up script

import numpy as np
import pykep as pk
import matplotlib.pyplot as plt
import matplotlib.dates as dlt
import datetime as dt

# INPUTS

# target planet
target_pl = 'Mars'

# reference timeframe
initial_epoch = '2018-01-01'
final_epoch = '2035-01-01'


# REFERENCE DATA

# planets
earth = pk.planet.jpl_lp('earth')
target = pk.planet.jpl_lp(target_pl)

# timeframe
timefix = " 00:00"
initial_epoch = pk.epoch_from_string(initial_epoch+timefix).mjd2000
final_epoch = pk.epoch_from_string(final_epoch+timefix).mjd2000


# FUNCTIONS

# RANGE

def range_data(screen_output=False, steps=1):

    if screen_output:
        print(f"{'Epoch'}\t{'Solar Distance (AU)'}\t{'Earth Distance (AU)'}")

    dates = []
    epochs = []
    solar_dists =[]
    earth_dists = []

    for date in np.arange(initial_epoch,final_epoch,steps):
        epoch = pk.epoch(date)

        # Solar distance
        r,v = target.eph(date)
        solar_dist = np.linalg.norm(r)
        solar_dist /= pk.AU

        # Earth-target distance
        rE, vE = earth.eph(date)

        xd = r[0]-rE[0]
        yd = r[1] - rE[1]
        zd = r[2] - rE[2]

        earth_dist = (xd ** 2 + yd ** 2 + zd ** 2) ** 0.5

        earth_dist = np.linalg.norm(earth_dist)
        earth_dist /= pk.AU

        # get dates in correct format
        date = dlt.datestr2num(str(epoch))
        date = dlt.num2date(date)
        date = str(date)[:10]
        # print(str(date)[:10])


        dates.append(date)
        epochs.append(epoch)
        solar_dists.append(solar_dist)
        earth_dists.append(earth_dist)

        if screen_output:
            print(f"{epoch}\t{solar_dist}\t{earth_dist}")


    # TODO ==== fix means to plot dates on x axis
    # print(dates)


    # print(dates)

    return dates, epochs, solar_dists, earth_dists



def plot_range():


    x , epochs, y1, y2 = range_data(False)

    x = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in x]

    print(x)

    plt.gca().xaxis.set_major_formatter(dlt.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(dlt.YearLocator())
    plt.plot(x, y2, linewidth = 2.5,linestyle='-', label = target_pl+'-Earth distance')
    plt.plot(x, y1, linewidth=2.5,linestyle='-', label = 'Sun-'+target_pl+' distance')
    plt.xticks(rotation = 90)

    # tick parameters
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')

    # grid parameters
    plt.grid(color='lightgrey', linestyle=':', linewidth=0.5)

    # axis labels
    plt.ylabel('Distance (AU)')
    plt.xlabel('Epoch (AU)')

    plt.xlim(x[0],x[-1])
    plt.ylim(0)
    # plt.gcf().autofmt_xdate()

    plt.legend(loc = 0)

    plt.tight_layout()

    plt.show()

# range_data(False)
plot_range()









