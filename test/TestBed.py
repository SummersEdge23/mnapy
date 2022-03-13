import pandas as pd

from mnapy.Engine import Engine

FILE_LOCATION = r"ACSourceInitial_nl.txt"

# integration_method = ["trapezoidal", "backward_euler"]
engine = Engine(time_start = 0, time_step=5e-6, time_end=25e-3, integration_method="trapezoidal")
engine.load_file(FILE_LOCATION)

VM0 = engine.VoltMeter("VM0")

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
