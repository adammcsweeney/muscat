
# IMPORTS

from itertools import permutations


# INPUTS

SystemMargin = 0.3

PayloadMass = [300,200]

# DEFINITION OF FUNCTIONS

# find unique permutations (used for staging)
def unique_permutations(iterable, r=None):
    previous = tuple()
    for p in permutations(sorted(iterable), r):
        if p > previous:
            previous = p
            yield list(p)

# find unique staging permutations for given staging profile and delta-v budget
def OptionStageProfiles(Option):
    # number of stages of option
    NoStages = len(Option)
    # number of staging events of option
    NoStageEvents = NoStages - 1
    # initial staging profile for option
    InitProfile = [True]*NoStageEvents + [False]*(len(DeltaV) - NoStageEvents)
    # find unique staging permutations for option
    # create container
    StagingProfile = []
    # find unique permutations around InitProfile
    for staging_option in unique_permutations(InitProfile):
        StagingProfile.append(staging_option)
    # return list for unique staging options
    return StagingProfile


# DEFINITION OF DELTA-V BUDGET

DeltaV = [
    # E-M Cruise
    30.01,
    # MOI + TOA
    888.72,
    # Aerobraking
    240.16,
    # At Mars
    240.66,
    # TEI
    2072.20,
    # M-E Cruise
    29.01,
    # E Approach
    70.04
    ]

RCS_DeltaV = [
    # E-M Cruise
    0.0,
    # MOI + TOA
    0.0,
    # Aerobraking
    0.0,
    # At Mars
    66.42,
    # TEI
    2.06,
    # M-E Cruise
    0.0,
    # E Approach
    1.88]

# DEFINITION OF STAGES

# class definitions of different types of stage
# these stages are combined to form different mission staging options

# Mission Module (MM)
# The core stage, mandatory for any mission option

class MissionModule(object):

    def __init__(self):
        self.name = "Mission Module"
        self.payload = sum(PayloadMass)

        self.tank_mass = self.SizeTanks()

        self.eng_isp = 320
        self.rcs_isp = 300

        self.dry_mass = self.DryMass()
        self.propellant_mass = self.PropellantMass()
        self.wet_mass = self.WetMass()

    # EQUIPMENT SIZING

    def SizeTanks(self):
        TankSize = 10
        return TankSize

    # STAGE MASS TOTALS

    def DryMass(self):
        DryMass = 1000
        return DryMass

    def PropellantMass(self):
        PropellantMass = 1000
        return PropellantMass

    def WetMass(self):
        return self.dry_mass + self.propellant_mass


# Propulsion Module (PM)
# additional pure propulsion stage(s) added to the Mission Module

class PropulsionModule(object):

    def __init__(self, PM_index = 1):
        self.name = "Propulsion Module " + str(PM_index)
        self.payload = 0

        self.tank_mass = self.SizeTanks()

        self.eng_isp = 320
        self.rcs_isp = 300

        self.dry_mass = self.DryMass()
        self.propellant_mass = self.PropellantMass()
        self.wet_mass = self.WetMass()

        # EQUIPMENT SIZING

    def SizeTanks(self):
        TankSize = 10
        return TankSize

        # STAGE MASS TOTALS

    def DryMass(self):
        DryMass = 500
        return DryMass

    def PropellantMass(self):
        PropellantMass = 500
        return PropellantMass

    def WetMass(self):
        return self.dry_mass + self.propellant_mass


# Composite class

class Composite(object):

    def __init__(self, ModuleList):
        self.name = "Option ID"


# DEFINE MISSION CONFIGURATIONS OPTIONS

Option_1 = [MissionModule()]
Option_2 = [MissionModule(), PropulsionModule(PM_index=1)]
Option_3 = [MissionModule(), PropulsionModule(PM_index=2), PropulsionModule(PM_index=1)]

# collection of options

Options = [Option_1, Option_2, Option_3]


for option in Options:
    print(OptionStageProfiles(option))









