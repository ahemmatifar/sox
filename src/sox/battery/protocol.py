from typing import Literal

import pybamm as pb


def append_steps(*experiments: pb.Experiment) -> list:
    return [exp.args[0][0] for exp in experiments]


def append_experiments(*experiments: pb.Experiment) -> pb.Experiment:
    return pb.Experiment(append_steps(*experiments), *experiments[0].args)


def cc_charge_cv_rest(
    c_rate: float = 1,
    max_voltage: float = 4.1,
    cv_hold_c_rate_limit: float = 0.05,
    rest_time_h: float = 0.5,
    period_s: float = 1,
) -> pb.Experiment:
    return pb.Experiment(
        [
            (
                f"Charge at {c_rate} C until {max_voltage} V",
                f"Hold at {max_voltage} V until {cv_hold_c_rate_limit} C",
                f"Rest for {rest_time_h} hour",
            )
        ],
        period=f"{period_s} seconds",
    )


def cc_discharge_rest(
    c_rate: float = 1,
    min_voltage: float = 3.3,
    rest_time_h: float = 0.5,
    period_s: float = 1,
) -> pb.Experiment:
    return pb.Experiment(
        [
            (
                f"Discharge at {c_rate} C until {min_voltage} V",
                f"Rest for {rest_time_h} hour",
            )
        ],
        period=f"{period_s} seconds",
    )


def charge_discharge_cycling(
    chg_c_rate: float = 1,
    max_chg_voltage: float = 4.1,
    chg_cv_hold_c_rate_limit: float = 0.05,
    chg_rest_time_h: float = 0.5,
    dchg_c_rate: float = 1,
    min_dchg_voltage: float = 3.3,
    dchg_rest_time_h: float = 0.5,
    direction: Literal["charge", "discharge"] = "discharge",
    number_of_cycles: int = 1,
    period_s: float = 1,
) -> pb.Experiment:
    charge = cc_charge_cv_rest(chg_c_rate, max_chg_voltage, chg_cv_hold_c_rate_limit, chg_rest_time_h, period_s)
    discharge = cc_discharge_rest(dchg_c_rate, min_dchg_voltage, dchg_rest_time_h, period_s)
    if direction == "charge":
        return pb.Experiment(append_steps(charge, discharge) * number_of_cycles, period=f"{period_s} seconds")
    elif direction == "discharge":
        return pb.Experiment(append_steps(discharge, charge) * number_of_cycles, period=f"{period_s} seconds")
    else:
        raise ValueError("direction must be 'charge' or 'discharge'")


def single_pulse(
    direction: Literal["charge", "discharge"] = "discharge",
    c_rate: float = 1,
    pulse_time_sec: float = 60,
    pulse_rest_time_sec: float = 600,
    period_s: float = 1,
) -> pb.Experiment:
    return pb.Experiment(
        [
            (
                f"{direction.capitalize()} at {c_rate} C for {pulse_time_sec} seconds",
                f"Rest for {pulse_rest_time_sec} seconds",
            )
        ],
        period=f"{period_s} seconds",
    )


def single_pulse_train(
    direction: Literal["charge", "discharge"] = "discharge",
    c_rate: float = 1,
    pulse_time_sec: float = 60,
    pulse_rest_time_sec: float = 600,
    number_of_pulses: int = 20,
    period_s: float = 1,
) -> pb.Experiment:
    pulse_steps = single_pulse(direction, c_rate, pulse_time_sec, pulse_rest_time_sec, period_s).args[0]
    return pb.Experiment(pulse_steps * number_of_pulses, period=f"{period_s} seconds")


def multi_pulse_train(
    direction=None,
    c_rate=None,
    pulse_time_sec=None,
    pulse_rest_time_sec=None,
    number_of_pulses=None,
    period_s: float = 1,
) -> pb.Experiment:
    pulse_steps = append_steps(
        *[
            single_pulse(
                direction[i],
                c_rate[i],
                pulse_time_sec[i],
                pulse_rest_time_sec[i],
                period_s,
            )
            for i in range(len(direction))
        ]
    )
    return pb.Experiment(pulse_steps * number_of_pulses, period=f"{period_s} seconds")
