from typing import List

from pysolver import Global
from pysolver import Utils
from pysolver import VoltageControlledCapacitorLimits
from pysolver import Wire


class VoltageControlledCapacitor:
    def __init__(
        self,
        context,
        Transient_Resistance,
        Initial_Voltage,
        Output_Capacitance,
        Elm1,
        Input_Voltage,
        Elm0,
        units,
        High_Voltage,
        Elm3,
        Transient_Current,
        Elm2,
        options_units,
        Low_Voltage,
        option_limits,
        Interpolate,
        options,
        tag,
        Transient_Voltage,
        Equivalent_Current,
    ):
        self.Transient_Resistance = Transient_Resistance
        self.Initial_Voltage = Initial_Voltage
        self.Output_Capacitance = Output_Capacitance
        self.Elm1 = Elm1
        self.Input_Voltage = Input_Voltage
        self.Elm0 = Elm0
        self.units = units
        self.High_Voltage = High_Voltage
        self.Elm3 = Elm3
        self.Transient_Current = Transient_Current
        self.Elm2 = Elm2
        self.options_units = options_units
        self.Low_Voltage = Low_Voltage
        self.option_limits = (
            VoltageControlledCapacitorLimits.VoltageControlledCapacitorLimits(
                **Utils.Utils.FixDictionary(option_limits)
            )
        )
        self.Interpolate = Interpolate
        self.options = options
        self.tag = tag
        self.Transient_Voltage = Transient_Voltage
        self.Equivalent_Current = Equivalent_Current
        self.Nodes = []
        self.Linkages = []
        self.Designator = ""
        self.Id = -1
        self.SimulationId = -1
        self.ElementType = -1
        self.WireReferences = []
        self.context = context

    def Set_Interpolate(self, setter: str) -> None:
        None
        if setter == (Global.SystemConstants.ON) or setter == (
            Global.SystemConstants.OFF
        ):
            self.Interpolate = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Interpolate(self) -> str:
        None
        return self.Interpolate

    def Set_Initial_Voltage(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Initial_Voltage[0])
            and abs(setter) <= abs(self.option_limits.Initial_Voltage[1])
        ) or abs(setter) == 0:
            self.Initial_Voltage = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Initial_Voltage(self) -> float:
        None
        return self.Initial_Voltage

    def Set_Elm1(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Elm1[0])
            and abs(setter) <= abs(self.option_limits.Elm1[1])
        ) or abs(setter) == 0:
            self.Elm1 = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Elm1(self) -> float:
        None
        return self.Elm1

    def Set_Elm0(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Elm0[0])
            and abs(setter) <= abs(self.option_limits.Elm0[1])
        ) or abs(setter) == 0:
            self.Elm0 = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Elm0(self) -> float:
        None
        return self.Elm0

    def Set_Elm3(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Elm3[0])
            and abs(setter) <= abs(self.option_limits.Elm3[1])
        ) or abs(setter) == 0:
            self.Elm3 = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Elm3(self) -> float:
        None
        return self.Elm3

    def Set_Elm2(self, setter: float) -> None:
        None
        if (
            abs(setter) >= abs(self.option_limits.Elm2[0])
            and abs(setter) <= abs(self.option_limits.Elm2[1])
        ) or abs(setter) == 0:
            self.Elm2 = setter
        else:
            print(self.Designator + " -> Value is outside of limits.")

    def Get_Elm2(self) -> float:
        None
        return self.Elm2

    def reset(self) -> None:
        None
        self.Transient_Resistance = self.context.time_step / (
            2 * self.Output_Capacitance
        )
        self.Transient_Voltage = self.Initial_Voltage
        self.Transient_Current = 0
        self.Equivalent_Current = (
            -self.Transient_Voltage / self.Transient_Resistance - self.Transient_Current
        )

    def update(self) -> None:
        None
        if (
            Global.SystemFlags.FlagSimulating
            and self.context.solutions_ready
            and self.context.simulation_step != 0
        ):
            self.Input_Voltage = Utils.Utils.limit(
                self.context.get_voltage(self.Nodes[1], -1),
                self.Low_Voltage,
                self.High_Voltage,
            )
            if self.Interpolate == (Global.SystemConstants.ON):
                self.Output_Capacitance = Utils.Utils.linterp(
                    [
                        self.High_Voltage * 0,
                        self.High_Voltage * 0.33,
                        self.High_Voltage * 0.66,
                        self.High_Voltage * 1.0,
                    ],
                    [self.Elm0, self.Elm1, self.Elm2, self.Elm3],
                    self.Input_Voltage,
                )
            elif self.Interpolate == (Global.SystemConstants.OFF):
                index: int = 0
                if (
                    self.Input_Voltage >= self.High_Voltage * 0
                    and self.Input_Voltage <= self.High_Voltage * 0.25
                ):
                    index = 0
                elif (
                    self.Input_Voltage >= self.High_Voltage * 0.25
                    and self.Input_Voltage <= self.High_Voltage * 0.5
                ):
                    index = 1
                elif (
                    self.Input_Voltage >= self.High_Voltage * 0.5
                    and self.Input_Voltage <= self.High_Voltage * 0.75
                ):
                    index = 2
                elif (
                    self.Input_Voltage >= self.High_Voltage * 0.75
                    and self.Input_Voltage <= self.High_Voltage * 1.0
                ):
                    index = 3

                self.Output_Capacitance = [
                    self.Elm0, self.Elm1, self.Elm2, self.Elm3
                ][index]

    def stamp(self) -> None:
        None
        self.context.stamp_capacitor(
            self.Nodes[0],
            self.Nodes[2],
            self.Transient_Resistance,
            self.Equivalent_Current,
        )
        self.context.stamp_node(self.Nodes[1], Global.SystemSettings.R_MAX)

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

    def update_vcca(self) -> None:
        None
        if self.context.solutions_ready:
            self.conserve_energy()
            voltage: float = self.context.get_voltage(self.Nodes[0], self.Nodes[2])
            self.Transient_Voltage = voltage
            self.Transient_Current = (
                voltage / self.Transient_Resistance + self.Equivalent_Current
            )
            self.Equivalent_Current = (
                -self.Transient_Voltage / self.Transient_Resistance
                - self.Transient_Current
            )

    def conserve_energy(self) -> None:
        None
        self.Transient_Resistance = self.context.time_step / (
            2 * self.Output_Capacitance
        )
        self.Equivalent_Current = (
            -self.Transient_Voltage / self.Transient_Resistance - self.Transient_Current
        )

    def GetElementType(self) -> int:
        None
        return self.ElementType

    def SetElementType(self, setter: int) -> None:
        None
        self.ElementType = setter
