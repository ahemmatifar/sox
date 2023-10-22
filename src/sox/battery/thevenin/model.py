import pybamm as pb

from sox.battery.thevenin.parameters import Inputs, Outputs


class Thevenin:
    def __init__(self, inputs: Inputs):
        self.inputs = inputs
        self.model = self.build_default_model()
        self.variable_names = self.model.variable_names()
        self._inputs = self.process_inputs()

    def build_default_model(self):
        # builds a default PyBaMM model
        return pb.equivalent_circuit.Thevenin(
            options={
                "number of rc elements": self.inputs.rc_pairs,
                "calculate discharge energy": "true",
            }
        )

    def process_inputs(self):
        # sets the parameters
        params = self.model.default_parameter_values
        params.update(
            {
                "Initial temperature [K]": self.inputs.initial_temperature + 273.15,
                "Upper voltage cut-off [V]": self.inputs.voltage_high_cut,
                "Cell-jig heat transfer coefficient [W/K]": self.inputs.k_cell_jig,
                "Cell thermal mass [J/K]": self.inputs.cth_cell,
                "Jig thermal mass [J/K]": self.inputs.cth_jig,
                "Jig-air heat transfer coefficient [W/K]": self.inputs.k_jig_air,
                "Cell capacity [A.h]": self.inputs.capacity,
                "Nominal cell capacity [A.h]": self.inputs.capacity,
                "Initial SoC": self.inputs.initial_soc,
                "Lower voltage cut-off [V]": self.inputs.voltage_low_cut,
                "Open-circuit voltage [V]": self.inputs.open_circuit_voltage,
                "Ambient temperature [K]": self.inputs.ambient_temperature + 273.15,
                "R0 [Ohm]": self.inputs.series_resistance,
                "Current function [A]": 0.0,
                "Entropic change [V/K]": self.inputs.entropic_change,
            }
        )
        for i in range(1, self.inputs.rc_pairs + 1):  # 1, 2, ..., n_rc_pairs
            params.update(
                {
                    f"Element-{i} initial overpotential [V]": self.inputs.initial_rc_voltage[i - 1],
                    f"R{i} [Ohm]": self.inputs.rc_resistance[i - 1],
                    f"C{i} [F]": self.inputs.rc_capacitance[i - 1],
                }
            )
        return params

    def solve(self, experiment: pb.Experiment):
        # solves the model
        simulation = pb.Simulation(model=self.model, experiment=experiment, parameter_values=self._inputs)
        simulation.solve()
        solution = simulation.solution
        return Outputs(
            time=solution.t,
            voltage=solution["Voltage [V]"].data,
            rc_voltage=[solution[f"Element-{i} overpotential [V]"].data for i in range(1, self.inputs.rc_pairs + 1)],
            ocv=solution["Open-circuit voltage [V]"].data,
            current=solution["Current [A]"].data,
            power=solution["Power [W]"].data,
            resistance=solution["Resistance [Ohm]"].data,
            series_resistance=solution["R0 [Ohm]"].data,
            rc_resistance=[solution[f"R{i} [Ohm]"].data for i in range(1, self.inputs.rc_pairs + 1)],
            rc_capacitance=[solution[f"C{i} [F]"].data for i in range(1, self.inputs.rc_pairs + 1)],
            soc=solution["SoC"].data,
            ambient_temperature=solution["Ambient temperature [degC]"].data,
            cell_temperature=solution["Cell temperature [degC]"].data,
            jig_temperature=solution["Jig temperature [degC]"].data,
        )
