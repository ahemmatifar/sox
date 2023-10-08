import pybamm as pb

from sox.battery.parameters import Parameters


class TheveninModel:
    def __init__(self, parameters: Parameters):
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
                "Upper voltage cut-off [V]": self.parameters.toc_voltage_cut_off,
                "Cell-jig heat transfer coefficient [W/K]": self.parameters.h_jig,
                "Cell thermal mass [J/K]": self.parameters.cp_cell,
                "Jig thermal mass [J/K]": self.parameters.cp_jig,
                "Jig-air heat transfer coefficient [W/K]": self.parameters.h_air,
                "Cell capacity [A.h]": self.parameters.capacity,
                "Nominal cell capacity [A.h]": self.parameters.capacity,
                "Initial SoC": self.parameters.initial_soc,
                "Lower voltage cut-off [V]": self.parameters.bod_voltage_cut_off,
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
        return simulation
