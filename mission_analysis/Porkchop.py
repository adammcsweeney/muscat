# create porkchop plots for interplanetary mission analysis
# note: currently finds lowest C3 type 2 trajectory
# credit to DarioIzzo: https://gist.github.com/darioizzo/10643082

# TODO ==== create separate porkchop utilities
# 1. Mission independent (C3 departure
# 2. Mission dependent (considering LV, capture orbit, Isp, Mass fractions etc.)


# import statement
import numpy as np
from scipy import array
import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import pykep as pk

# plt.xkcd()

# Mission independent porkchop plot

class Porkchop(object):

    def __init__(self,
                 Planet_i = pk.planet.jpl_lp('earth'),
                 Planet_f = pk.planet.jpl_lp('mars'),
                 Epoch_i = 9700,
                 Epoch_f = 9900,
                 ToF_min = 1,
                 ToF_max = 600,
                 ShowPork = False):

        # planets
        self.Planet_i = Planet_i
        self.Planet_f = Planet_f

        # epochs
        self.Epoch_i = Epoch_i
        self.Epoch_f = Epoch_f

        # ToF
        self.ToF_min = ToF_min
        self.ToF_max = ToF_max

        # show pork colour scheme?
        self.ShowPork = ShowPork

    def get_data(self):

        # range of departure epochs
        start_epochs = np.arange(self.Epoch_i, self.Epoch_f, 1.)

        # range of transfer durations
        duration = np.arange(self.ToF_min, self.ToF_max + 1, 1.)

        # data container list
        data = list()

        # TODO ==== check and delete
        data_tof = list()

        # loop through each departure epoch in range
        for start in start_epochs:

            # create an empty list for each row
            row = list()

            # TODO ==== check and delete
            row_tof = list()

            # loop through each transfer duration
            for T in duration:
                # get ephemeris data for departure and arrival epoch, starting from given departure epoch
                r1, v1 = self.Planet_i.eph(pk.epoch(start))
                r2, v2 = self.Planet_f.eph(pk.epoch(start + T))

                # solve Lambert's Problem for given departure / arrival ephemeris
                LambertSolutions = pk.lambert_problem(r1, r2, T * 60 * 60 * 24, self.Planet_i.mu_central_body)

                # find the norm of the difference between Planet_i velocity and Lambert Solution v1
                # i.e. this is the magnitude of departure velocity wrt to Planet_i
                DV1 = np.linalg.norm(array(v1) - array(LambertSolutions.get_v1()[0]))

                # find the norm of the difference between Planet_f velocity and Lambert Solution v2
                # i.e. this is the magnitude of the arrival velocity wrt to Planet_f
                DV2 = np.linalg.norm(array(v2) - array(LambertSolutions.get_v2()[0]))

                # Evaluate maximum positive DV1, subtracting 4000
                # 4000 assumed as launch vehicle Vinf  (set to 0
                DV1 = max([0, DV1])

                # convert to C3 (in km^2/sec^2)
                DV1 = (DV1 / 1000) ** 2

                # Total DV
                DV = DV1

                # add DV value to row list
                row.append(DV)

                # TODO ==== check and delete
                row_tof.append(T)

            # add row of DV values for given ToF values to data container list
            data.append(row)

            # TODO ==== check and delete
            data_tof.append(row_tof)

        # Next, extract the best solution found and the relative epochs

        # create list with minimum value for each row in data list
        # i.e. the lowest DV in each row, the lowest DV for each departure epoch in defined range
        # note: minrows is the length of the number of individual epochs considered in input range
        minrows = [min(row) for row in data]

        # return the index number of the minimum DV value from minrows list
        # i.e. the lowest DV solution
        i_idx = np.argmin(minrows)

        # get the index of the row containing the lowest DV solution
        # i.e. for the departure of the lowest DV solution, as each row corresponds to a given departure epoch
        j_idx = np.argmin(data[i_idx])

        # extract the best solution from data grid (i.e. for evaluating the DV, ToF, and departure Epoch
        best = data[i_idx][j_idx]

        return start_epochs, duration, data, best, i_idx, j_idx, data_tof

    def report(self, data):

        # print data outputs

        starts = data[0]
        ToFs = data[1]
        best = data[3]
        i = data[4]
        j = data[5]

        print(f"{'Best C3 (km^2/sec^2): '}\t{best}")
        print(f"{'Transfer Type: '}\t{'II (TBC)'}")
        print(f"{'Launch epoch: '}\t{pk.epoch(starts[i])}")
        print(f"{'Launch epoch (MJD2000): '}\t{starts[i]}")
        print(f"{'Time of flight (days): '}\t{ToFs[j]}")
        print(f"{'Arrival epoch: '}\t{pk.epoch(starts[i]+ToFs[j])}")
        print(f"{'Arrival epoch (MJD2000): '}\t{str(starts[i]+ToFs[j])}")

    def get_plot(self, start_epochs, duration, data, data_tof):

        # Data collection for Plots

        # line to convert epoch into correct format for plotting on x-axis
        # hacky fix; add 730120 to make compatible with matplotlib date treatment
        # TODO ==== makes this better
        departure_epochs = [x + 730120 for x in start_epochs]

        # create new list of ToFs
        durations = [ToF + 0 for ToF in duration]

        # create grid for ToF and departure epoch data

        durations_pl, start_epochs_pl = np.meshgrid(durations, departure_epochs)

        # durations_pl, start_epochs_pl = np.meshgrid(durations, new_test)

        # create array for arrival epochs
        end_epochs_pl = [ToF + start for ToF, start in zip(durations_pl, departure_epochs)]

        # print(pk.epoch(start_epochs_pl[0][0]))

        # add x and y axis labels
        plt.xlabel("Launch epoch")
        plt.ylabel("Arrival epoch")

        # tick parameters
        plt.minorticks_on()
        plt.tick_params(direction='in', which='both', labelsize = 'small')

        # grid parameters
        plt.grid(color='lightgrey', linestyle=':', linewidth=0.5)

        # plot axis limits
        plt.xlim()
        # hacky fix; add 730120 to make compatible with matplotlib date treatment
        # TODO === make this better
        plt.ylim(self.Epoch_i + 250 + 730120, self.Epoch_f + self.ToF_max + 730120)

        # set axis to date format
        # x axis
        # note: edit this line to adjust date format
        plt.gca().xaxis.set_major_formatter(mdt.DateFormatter('%Y-%b-%d'))
        # plt.gca().xaxis.set_major_formatter(mdt.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdt.AutoDateLocator())
        # y axis
        # note: edit this line to adjust date format
        plt.gca().yaxis.set_major_formatter(mdt.DateFormatter('%Y-%b-%d'))
        # plt.gca().yaxis.set_major_formatter(mdt.DateFormatter('%Y'))
        plt.gca().yaxis.set_major_locator(mdt.AutoDateLocator())


        # TODO ==== add color bar!

        # filled contour plot
        if self.ShowPork:
            fig = plt.contourf(
                start_epochs_pl,
                end_epochs_pl,
                array(data),
                levels=list(np.linspace(0, 50, 11)),
                cmap='jet',
            )
            # line contour plot
            fig = plt.contour(
                start_epochs_pl,
                end_epochs_pl,
                array(data),
                levels=list(np.linspace(0, 50, 11)),
                colors='k',
                # cmap='jet',
                linewidths=.9,
                linestyles='-'
            )
            # labels on contour lines
            plt.clabel(fig,
                       colors='black',
                       fontsize=4,
                       inline=True,
                       inline_spacing=1,
                       fmt='%1.1f')
        else:
            # line contour plot
            fig = plt.contour(
                start_epochs_pl,
                end_epochs_pl,
                array(data),
                levels=list(np.linspace(0, 30, 21)),
                # colors='k',
                cmap='jet',
                linewidths=.5,
                linestyles=':'
            )
            # labels on contour lines
            plt.clabel(fig,
                       colors='black',
                       fontsize=4,
                       inline=True,
                       inline_spacing=1,
                       fmt='%1.1f')

        # add lines of constant ToF
        fig = plt.contour(
            start_epochs_pl,
            end_epochs_pl,
            array(data_tof),
            levels=list(np.linspace(0, 1000, 21)),
            colors='k',
            # cmap='jet',
            linewidths=.5,
            linestyles=':'
        )

        # labels on contour lines
        clabels = plt.clabel(fig,
                   colors='k',
                   fontsize=4,
                   inline=True,
                   inline_spacing=3,
                   fmt='%1.0f')



        plt.tight_layout()

        plt.gcf().autofmt_xdate()


        plt.show()

# # test run
#
# # 1. create porkchop data from inputs
#
# # call porkchop class
# porkchop = Porkchop()
#
# # data generation
# data = porkchop.get_data()
#
# # 2. Report on porkchop data
# porkchop.report(data)
#
# # 3. Produce porkchop plot
# # print(len(data[0]))
# # print(len(data[1]))
# porkchop.get_plot(data[0], data[1], data[2], data[6])