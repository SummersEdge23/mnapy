## -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 07:22:25 2021

@author: Christian

"""
import pandas as pd

from mnapy.Engine import Engine
import matplotlib.pyplot as plt
import numpy as np

plt.close("all")

# Required Variables.
#FILE_LOCATION = r"/home/christian/Downloads/ACSource_nl.txt"
FILE_LOCATION = r"ACSourceInitial2_nl.txt"

lte_estimation_step = 0
time_stash = []
half_step = False
ts_retry_max = 50
ts_iter = 0
eps = 0
time_step = 1
initial_time_step = 1e-9
delta = 5e-3
first_solution = True
logic_lock = True

time_end = 500e-3

# User Variables.
VM0 = -1
DC0 = -1
DC1 = -1
Vout = []
Time = []

# Setup.
engine = Engine()
engine.load_file(FILE_LOCATION)
engine.initialize()

VM0 = engine.IndexOfVoltMeter("VM0")
#DC0 = engine.IndexOfDCSource("DC0")
#DC1 = engine.IndexOfDCSource("DC1")

def setup():
    engine.simulation_time = 0
    engine.time_step = initial_time_step
    engine.setup()
#    engine.InstanceOfDCSource(DC0).Set_Voltage(5)
#    engine.InstanceOfDCSource(DC1).Set_Voltage(5)
    
def logic():
    Vout.append(engine.InstanceOfVoltMeter(VM0).Get_Voltage())
    Time.append(engine.simulation_time)
    None

def output():
    None

def plot():
    dt = [0]
    for i in range(1, len(Time)):
        dt.append(Time[i] - Time[i-1])
        
    df = pd.DataFrame(list(zip(Time, Vout, dt)), columns=["Time", "Voltage", "dt"])
#    df.plot("Time", ["Voltage"], grid=True, style=".-")
#    df.plot("Time", ["dt"], grid=True, style=".-")
    df.plot("Time", ["Voltage"], grid=True)
    df.plot("Time", ["dt"], grid=True)
    None


setup()

# Engine Loop.
while engine.simulation_time < time_end:
    if not logic_lock:
        logic()
        logic_lock = True
    None
    
    engine.simulate()

    if engine.ready():      
        if (first_solution):            
            first_solution = False
            half_step = False
        else:
            if (lte_estimation_step == 0):
                time_stash.append(engine.save_state())
                
                if (half_step):
                    engine.simulation_time -= engine.time_step
                    engine.time_step = (0.9 * delta * engine.time_step ** 2) / eps
                    engine.time_step = max(engine.time_step, initial_time_step * 1.02)
                    engine.setup()
                    ts_iter += 1
                    
                    if (ts_iter >= ts_retry_max):
                        raise RuntimeError("Optiminal Timestep Search Failed.")
                
                lte_estimation_step += 1
                
            elif (lte_estimation_step == 1):
                lte_estimation_step += 1
            elif (lte_estimation_step == 2):                
                time_stash.append(engine.save_state())

                t1 = time_stash[-2]["matrix_x"]
                t2 = time_stash[-1]["matrix_x"]
                
                abs_t1 = np.array([abs(i) for i in t1])
                abs_t2 = np.array([abs(i) for i in t2])
                
                eps = float(abs(max(abs_t1 - abs_t2)))
                eps = max(eps, float(abs(max(abs_t2-abs_t1))))
                eps = abs(eps)

                if (eps != 0):
                    eps /= 12
                                    
                if (eps < delta):
                    output()
                    
                    engine.time_step *= 1.02
                    engine.time_step = min(engine.time_step, time_step)
                    engine.setup()
                    logic_lock = False
                    half_step = False                    
                    time_stash.clear()
                    ts_iter = 0
                else:
                    engine.apply_state(time_stash[-2])
                    engine.setup()
                    half_step = True
                    time_stash.clear()

                lte_estimation_step = 0
    None

    if not engine.Params.SystemFlags.FlagSimulating:
        break
    None
None

# Plot Data.
plot()
