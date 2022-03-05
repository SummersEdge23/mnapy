## -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 07:22:25 2021

@author: Christian

"""
import pandas as pd

from mnapy.Engine import Engine

FILE_LOCATION = r"ACSourceInitial_nl.txt"

engine = Engine(time_start = 0, time_step=5e-6, time_end=25e-3)
engine.load_file(FILE_LOCATION)

VM0 = engine.InstanceOfVoltMeter(engine.IndexOfVoltMeter("VM0"))

Vout = []
Time = []

def logic(step):
    Vout.append(VM0.Get_Voltage())
    Time.append(engine.simulation_time)
    None

def output(step):
    None

def plot():
    df = pd.DataFrame(list(zip(Time, Vout)), columns=["Time", "Voltage"])
    df.plot("Time", ["Voltage"], grid=True)
    None

engine.simulation_loop(logic, output, plot)
