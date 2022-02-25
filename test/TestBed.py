## -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 07:22:25 2021

@author: Christian

"""
import pandas as pd

from mnapy.Engine import Engine

# Required Variables.
FILE_LOCATION = r"ACSourceInitial_nl.txt"
T_SPAN = 100e-3
TIME_STEP = 166.67e-6
SOLVER_STEPS = int(round(T_SPAN / TIME_STEP))
StepCounter = 0
Lock = True

# User Variables.
VM0 = -1
Vout = []
Time = []

# Setup.
engine = Engine()
engine.load_file(FILE_LOCATION)
engine.initialize()

VM0 = engine.IndexOfVoltMeter("VM0")

def setup():
    engine.time_step = TIME_STEP
    engine.setup()

def logic(StepCounter: int):
    Vout.append(engine.InstanceOfVoltMeter(VM0).Get_Voltage())
    Time.append(engine.simulation_time)
    None

def output(StepCounter: int):
    None

def plot():
    df = pd.DataFrame(list(zip(Time, Vout)), columns=["Time", "Voltage"])
    df.plot("Time", ["Voltage"])
    None

setup()

# Engine Loop.
while StepCounter < SOLVER_STEPS:
    if not Lock:
        logic(StepCounter)
        Lock = True
    None

    engine.simulate()

    if engine.ready():
        Lock = False
        output(StepCounter)
        StepCounter += 1
    None

    if not engine.Params.SystemFlags.FlagSimulating:
        break
    None
None

# Plot Data.
plot()
