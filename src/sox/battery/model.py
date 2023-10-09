import pybamm as pb

from sox.battery.parameters import Inputs, Outputs


class TheveninModel:
    def __init__(self, parameters: Inputs):
        self.parameters = parameters
        self.model = self.build_default_model()
        self.variable_names = self.model.variable_names()
        self._parameters = self.process_parameters()

    def build_default_model(self):
        # builds a default PyBaMM model
        return pb.equivalent_circuit.Thevenin(
            options={
                "number of rc elements": self.parameters.rc_pairs,
                "calculate discharge energy": "true",
            }
        )

    def process_parameters(self):
        # sets the parameters
        params = self.model.default_parameter_values
        params.update(
            {
                "Initial temperature [K]": self.parameters.initial_temperature,
                "Upper voltage cut-off [V]": self.parameters.voltage_high_cut,
                "Cell-jig heat transfer coefficient [W/K]": self.parameters.k_cell_jig,
                "Cell thermal mass [J/K]": self.parameters.cth_cell,
                "Jig thermal mass [J/K]": self.parameters.cth_jig,
                "Jig-air heat transfer coefficient [W/K]": self.parameters.k_jig_air,
                "Cell capacity [A.h]": self.parameters.capacity,
                "Nominal cell capacity [A.h]": self.parameters.capacity,
                "Initial SoC": self.parameters.initial_soc,
                "Lower voltage cut-off [V]": self.parameters.voltage_low_cut,
                "Open-circuit voltage [V]": self.parameters.open_circuit_voltage,
                "Ambient temperature [K]": self.parameters.ambient_temperature,
                "R0 [Ohm]": self.parameters.series_resistance,
                "Current function [A]": 0.0,
                "Entropic change [V/K]": self.parameters.entropic_change,
            }
        )
        for i in range(1, self.parameters.rc_pairs + 1):  # 1, 2, ..., n_rc_pairs
            params.update(
                {
                    f"Element-{i} initial overpotential [V]": self.parameters.initial_rc_voltage[i - 1],
                    f"R{i} [Ohm]": self.parameters.rc_resistance[i - 1],
                    f"C{i} [F]": self.parameters.rc_capacitance[i - 1],
                },
                check_already_exists=False,
            )
        return params

    def solve(self, experiment: pb.Experiment):
        # solves the model
        simulation = pb.Simulation(model=self.model, experiment=experiment, parameter_values=self._parameters)
        simulation.solve()
        solution = simulation.solution
        return Outputs(
            time=solution.t,
            voltage=solution["Voltage [V]"].data,
            rc_voltage=[
                solution[f"Element-{i} overpotential [V]"].data for i in range(1, self.parameters.rc_pairs + 1)
            ],
            ocv=solution["Open-circuit voltage [V]"].data,
            current=solution["Current [A]"].data,
            power=solution["Power [W]"].data,
            resistance=solution["Resistance [Ohm]"].data,
            series_resistance=solution["R0 [Ohm]"].data,
            rc_resistance=[solution[f"R{i} [Ohm]"].data for i in range(1, self.parameters.rc_pairs + 1)],
            rc_capacitance=[solution[f"C{i} [F]"].data for i in range(1, self.parameters.rc_pairs + 1)],
            soc=solution["SoC"].data,
            ambient_temperature=solution["Ambient temperature [degC]"].data,
            cell_temperature=solution["Cell temperature [degC]"].data,
            jig_temperature=solution["Jig temperature [degC]"].data,
        )
