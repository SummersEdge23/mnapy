from typing import List

from mnapy import TransformerLimits
from mnapy import Utils
from mnapy import Wire


class Transformer:
    def __init__(
        self, context, options, tag, units, options_units, Turns_Ratio, option_limits
    ):
        self.options = options
        self.tag = tag
        self.units = units
        self.options_units = options_units
        self.Turns_Ratio = Turns_Ratio
        self.option_limits = TransformerLimits.TransformerLimits(
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

    def Set_Turns_Ratio(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Turns_Ratio[0])
            and abs(setter) <= abs(self.option_limits.Turns_Ratio[1])
        ) or abs(setter) == 0:
            self.Turns_Ratio = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Turns_Ratio(self) -> float:
        None
        return self.Turns_Ratio

    def reset(self) -> None:
        None

    def update(self) -> None:
        None

    def stamp(self) -> None:
        None
        self.context.stamp_transformer(
            self.Nodes[0],
            self.Nodes[1],
            self.Nodes[2],
            self.Nodes[3],
            self.Turns_Ratio,
            self.context.ELEMENT_TRAN_OFFSET + self.SimulationId,
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