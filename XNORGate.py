import math
from typing import List

from pysolver import Global
from pysolver import Utils
from pysolver import Wire
from pysolver import XNORGateLimits


class XNORGate:
    def __init__(
        self,
        context,
        Input_Voltage2,
        options,
        Input_Voltage1,
        tag,
        units,
        High_Voltage,
        Output_Voltage,
        options_units,
        option_limits,
    ):
        self.Input_Voltage2 = Input_Voltage2
        self.options = options
        self.Input_Voltage1 = Input_Voltage1
        self.tag = tag
        self.units = units
        self.High_Voltage = High_Voltage
        self.Output_Voltage = Output_Voltage
        self.options_units = options_units
        self.option_limits = XNORGateLimits.XNORGateLimits(
            **Utils.Utils.FixDictionary(option_limits)
        )
        self.Nodes = []
        self.Linkages = []
        self.Designator = ""
        self.Id = -1
        self.SimulationId = -1
        self.ElementType = -1
        self.WireReferences = []
        self.context = context

    def Set_High_Voltage(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.High_Voltage[0])
            and abs(setter) <= abs(self.option_limits.High_Voltage[1])
        ) or abs(setter) == 0:
            self.High_Voltage = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_High_Voltage(self) -> float:
        None
        return self.High_Voltage

    def reset(self) -> None:
        None
        self.Output_Voltage = 0

    def update(self) -> None:
        None
        if Global.SystemFlags.FlagSimulating and self.context.solutions_ready:
            self.Input_Voltage1 = math.tanh(
                10
                * (
                    self.context.get_voltage(self.Nodes[0], -1) / self.High_Voltage
                    - 0.5
                )
            )
            self.Input_Voltage2 = math.tanh(
                10
                * (
                    self.context.get_voltage(self.Nodes[1], -1) / self.High_Voltage
                    - 0.5
                )
            )
            self.Output_Voltage = self.High_Voltage * (
                0.5 * (1 + self.Input_Voltage1 * self.Input_Voltage2)
            )

    def stamp(self) -> None:
        None
        self.context.stamp_voltage(
            self.Nodes[2],
            -1,
            self.Output_Voltage,
            self.context.ELEMENT_XNOR_OFFSET + self.SimulationId,
        )

    def SetId(self, Id: str) -> None:
        None
        self.Id = int(Id)

    def SetNodes(self, Nodes: List[int]) -> None:
        None
        self.Nodes = Nodes

    def SetLinkages(self, Linkages: List[int]) -> None:
        None
        self.Linkages = Linkages

    def SetDesignator(self, Designator: str) -> None:
        None
        self.Designator = Designator

    def GetDesignator(self) -> str:
        None
        return self.Designator

    def SetSimulationId(self, Id: int) -> None:
        None
        self.SimulationId = Id

    def SetWireReferences(self, wires: List[Wire.Wire]) -> None:
        None
        self.WireReferences.clear()
        for i in range(0, len(wires)):
            self.WireReferences.append(wires[i])

    def GetNode(self, i: int) -> int:
        None
        if i < len(self.Nodes):
            return self.Nodes[i]
        else:
            return -1

    def GetElementType(self) -> int:
        None
        return self.ElementType

    def SetElementType(self, setter: int) -> None:
        None
        self.ElementType = setter
