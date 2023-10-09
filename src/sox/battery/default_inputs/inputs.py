import os

import pybamm as pb

from sox.battery.parameters import Inputs

path = os.path.join(os.path.dirname(__file__), "")

ocv_data = pb.parameters.process_1D_data("ecm_example_ocv.csv", path=path)
r0_data = pb.parameters.process_3D_data_csv("ecm_example_r0.csv", path=path)
r1_data = pb.parameters.process_3D_data_csv("ecm_example_r1.csv", path=path)
c1_data = pb.parameters.process_3D_data_csv("ecm_example_c1.csv", path=path)
dOCVdT_data = pb.parameters.process_2D_data_csv("ecm_example_docvdt.csv", path=path)


def open_circuit_voltage(soc):
    name, (x, y) = ocv_data
    return pb.Interpolant(x, y, soc, name)


def r0(temperature, current, soc):
    name, (x, y) = r0_data
    return pb.Interpolant(x, y, [temperature, current, soc], name)


def r1(temperature, current, soc):
    name, (x, y) = r1_data
    return pb.Interpolant(x, y, [temperature, current, soc], name)


def c1(temperature, current, soc):
    name, (x, y) = c1_data
    return pb.Interpolant(x, y, [temperature, current, soc], name)


def entropic_change(ocv, temperature):
    name, (x, y) = dOCVdT_data
    return pb.Interpolant(x, y, [ocv, temperature], name)


inputs = Inputs(
    # electrical properties
    rc_pairs=1,
    initial_rc_voltage=[0.0],
    voltage_high_cut=4.5,
    voltage_low_cut=2.5,
    capacity=10,
    initial_soc=0.5,
    open_circuit_voltage=open_circuit_voltage,
    entropic_change=entropic_change,
    series_resistance=r0,
    rc_resistance=[r1],
    rc_capacitance=[c1],
    # thermal properties
    initial_temperature=300.0,
    ambient_temperature=300.0,
    cth_cell=1000.0,
    cth_jig=500.0,
    k_cell_jig=10.0,
    k_jig_air=10.0,
)
