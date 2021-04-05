## -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 07:22:25 2021

@author: Christian

"""
from pysolver import pandas as pd

from pysolver import Global
from Engine import Engine

def setup():
    global engine, TIME_STEP, VM0, Vout, Time
    
    engine.time_step = TIME_STEP
    VM0 = engine.GetVoltMeter("VM0")

def logic(StepCounter: int):
    global engine, TIME_STEP, VM0, Vout, Time
    
    Vout.append(engine.VoltMeter(VM0).Get_Voltage())
    Time.append(engine.simulation_time)
    None

def output(StepCounter: int):
    None

def plot():
    global engine, TIME_STEP, VM0, Vout, Time

    df = pd.DataFrame(list(zip(Time, Vout)), columns=["Time", "Voltage"])
    df.plot("Time", ["Voltage"])
    None

# Required Variables.
FILE_LOCATION = r"/home/christian/Downloads/ACSourceInitial_nl.txt"
T_SPAN = 100e-3
TIME_STEP = 166.67e-6
SOLVER_STEPS = int(round(T_SPAN / TIME_STEP))
StepCounter = 0
Lock = True

# User Variables.
VM0 = -1
ID0 = -1
Vout = []
Time = []

# Setup.
engine = Engine()
engine.load_file(FILE_LOCATION)
engine.initialize()
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

    if not Global.SystemFlags.FlagSimulating:
        break
    None
None

# Plot Data.
plot()