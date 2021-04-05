import math
from typing import List

from pysolver import ACCurrentLimits
from pysolver import Utils
from pysolver import Wire


class ACCurrent:
    def __init__(
        self,
        context,
        Phase,
        options,
        Frequency,
        tag,
        units,
        Current,
        options_units,
        option_limits,
        Offset,
    ):
        self.Phase = Phase
        self.options = options
        self.Frequency = Frequency
        self.tag = tag
        self.units = units
        self.Current = Current
        self.options_units = options_units
        self.option_limits = ACCurrentLimits.ACCurrentLimits(
            **Utils.Utils.FixDictionary(option_limits)
        )
        self.Offset = Offset
        self.Nodes = []
        self.Linkages = []
        self.Designator = ""
        self.Id = -1
        self.SimulationId = -1
        self.ElementType = -1
        self.WireReferences = []
        self.context = context

    def Set_Phase(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Phase[0])
            and abs(setter) <= abs(self.option_limits.Phase[1])
        ) or abs(setter) == 0:
            self.Phase = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Phase(self) -> float:
        None
        return self.Phase

    def Set_Frequency(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Frequency[0])
            and abs(setter) <= abs(self.option_limits.Frequency[1])
        ) or abs(setter) == 0:
            self.Frequency = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Frequency(self) -> float:
        None
        return self.Frequency

    def Set_Current(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Current[0])
            and abs(setter) <= abs(self.option_limits.Current[1])
        ) or abs(setter) == 0:
            self.Current = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Current(self) -> float:
        None
        return self.Current

    def Set_Offset(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Offset[0])
            and abs(setter) <= abs(self.option_limits.Offset[1])
        ) or abs(setter) == 0:
            self.Offset = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Offset(self) -> float:
        None
        return self.Offset

    def reset(self) -> None:
        None

    def update(self) -> None:
        None

    def stamp(self) -> None:
        None
        self.context.stamp_current(
            self.Nodes[0],
            self.Nodes[1],
            math.sin(
                2 * math.pi * self.Frequency * self.context.simulation_time
                + math.radians(self.Phase)
            )
            * self.Current
            + self.Offset,
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
