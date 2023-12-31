from typing import Literal

import pybamm


class Experiment(pybamm.Experiment):
    """Utility for PyBaMM Experiment object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def append_steps(*experiments: Experiment) -> list:
    """Appends the steps of multiple experiments into a single list of steps"""
    return [exp.args[0][0] for exp in experiments]


def append_experiments(*experiments: Experiment) -> Experiment:
    """Appends multiple experiments into a single experiment"""
    return Experiment(append_steps(*experiments), *experiments[0].args)


def cc_charge_cv_rest(
    c_rate: float = 1,
    max_voltage: float = 4.1,
    cv_hold_c_rate_limit: float = 0.05,
    rest_time_h: float = 0.5,
    sampling_time_s: float = 1,
) -> Experiment:
    """Constant current charge, constant voltage hold, rest cycling protocol

    Args:
        c_rate (float): Charge rate (C).
        max_voltage (float): Maximum voltage (V).
        cv_hold_c_rate_limit (float): C-rate limit for CV hold (C).
        rest_time_h (float): Rest time (h).
        sampling_time_s (float): Sampling time (s).

    Returns:
        Experiment: PyBaMM experiment object.
    """
    return Experiment(
        [
            (
                f"Charge at {c_rate} C until {max_voltage} V",
                f"Hold at {max_voltage} V until {cv_hold_c_rate_limit} C",
                f"Rest for {rest_time_h} hour",
            )
        ],
        period=f"{sampling_time_s} seconds",
    )


def cc_discharge_rest(
    c_rate: float = 1,
    min_voltage: float = 3.3,
    rest_time_h: float = 0.5,
    sampling_time_s: float = 1,
) -> Experiment:
    """Constant current discharge, rest cycling protocol

    Args:
        c_rate (float): Discharge rate (C).
        min_voltage (float): Minimum voltage (V).
        rest_time_h (float): Rest time (h).
        sampling_time_s (float): Sampling time (s).
    """
    return Experiment(
        [
            (
                f"Discharge at {c_rate} C until {min_voltage} V",
                f"Rest for {rest_time_h} hour",
            )
        ],
        period=f"{sampling_time_s} seconds",
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
    sampling_time_s: float = 1,
) -> Experiment:
    """Charge and discharge cycling protocol

    Args:
        chg_c_rate (float): Charge rate (C).
        max_chg_voltage (float): Maximum voltage (V).
        chg_cv_hold_c_rate_limit (float): C-rate limit for CV hold (C).
        chg_rest_time_h (float): Rest time (h).
        dchg_c_rate (float): Discharge rate (C).
        min_dchg_voltage (float): Minimum voltage (V).
        dchg_rest_time_h (float): Rest time (h).
        direction (str): Direction of cycling, either 'charge' or 'discharge'. Defaults to 'discharge'.
        number_of_cycles (int): Number of cycles.
        sampling_time_s (float): Sampling time (s).
    """
    charge = cc_charge_cv_rest(chg_c_rate, max_chg_voltage, chg_cv_hold_c_rate_limit, chg_rest_time_h, sampling_time_s)
    discharge = cc_discharge_rest(dchg_c_rate, min_dchg_voltage, dchg_rest_time_h, sampling_time_s)
    if direction == "charge":
        return Experiment(append_steps(charge, discharge) * number_of_cycles, period=f"{sampling_time_s} seconds")
    elif direction == "discharge":
        return Experiment(append_steps(discharge, charge) * number_of_cycles, period=f"{sampling_time_s} seconds")
    else:
        raise ValueError("direction must be 'charge' or 'discharge'")


def single_pulse(
    direction: Literal["charge", "discharge"] = "discharge",
    c_rate: float = 1,
    pulse_time_sec: float = 60,
    pulse_rest_time_sec: float = 600,
    sampling_time_s: float = 1,
) -> Experiment:
    """Single pulse then rest protocol

    Args:
        direction (str): Direction of pulse, either 'charge' or 'discharge'. Defaults to 'discharge'.
        c_rate (float): C-rate of pulse (C).
        pulse_time_sec (float): Pulse time (s).
        pulse_rest_time_sec (float): Rest time (s).
        sampling_time_s (float): Sampling time (s).
    """
    return Experiment(
        [
            (
                f"{direction.capitalize()} at {c_rate} C for {pulse_time_sec} seconds",
                f"Rest for {pulse_rest_time_sec} seconds",
            )
        ],
        period=f"{sampling_time_s} seconds",
    )


def single_pulse_train(
    direction: Literal["charge", "discharge"] = "discharge",
    c_rate: float = 1,
    pulse_time_sec: float = 60,
    pulse_rest_time_sec: float = 600,
    number_of_pulses: int = 20,
    sampling_time_s: float = 1,
) -> Experiment:
    """Single pulse train protocol

    Args:
        direction (str): Direction of pulse, either 'charge' or 'discharge'. Defaults to 'discharge'.
        c_rate (float): C-rate of pulse (C).
        pulse_time_sec (float): Pulse time (s).
        pulse_rest_time_sec (float): Rest time (s).
        number_of_pulses (int): Number of pulses.
        sampling_time_s (float): Sampling time (s).
    """
    pulse_steps = single_pulse(direction, c_rate, pulse_time_sec, pulse_rest_time_sec, sampling_time_s).args[0]
    return Experiment(pulse_steps * number_of_pulses, period=f"{sampling_time_s} seconds")


def multi_pulse_train(
    direction=None,
    c_rate=None,
    pulse_time_sec=None,
    pulse_rest_time_sec=None,
    number_of_pulses: int = 1,
    sampling_time_s: float = 1,
) -> Experiment:
    """Multi pulse train protocol

    Args:
        direction (list): List of directions of pulses, either 'charge' or 'discharge'. Defaults to 'discharge'.
        c_rate (list): List of C-rates of pulses (C).
        pulse_time_sec (list): List of pulse times (s).
        pulse_rest_time_sec (list): List of rest times (s).
        number_of_pulses (int): Number of pulses.
        sampling_time_s (float): Sampling time (s).
    """
    pulse_steps = append_steps(
        *[
            single_pulse(
                direction[i],
                c_rate[i],
                pulse_time_sec[i],
                pulse_rest_time_sec[i],
                sampling_time_s,
            )
            for i in range(len(direction))
        ]
    )
    return Experiment(pulse_steps * number_of_pulses, period=f"{sampling_time_s} seconds")


def dst_schedule(
    peak_power: float,
    number_of_cycles: int = 1,
    sampling_time_s: float = 1,
):
    """Dynamically stress test schedule from USABC manual

    Args:
        peak_power (float): Peak power (W).
        number_of_cycles (int): Number of cycles.
        sampling_time_s (float): Sampling time (s).

    References:
        Electric Vehicle Battery Test Procedures Manual Revision 2.0
        https://avt.inl.gov/sites/default/files/pdf/battery/usabc_manual_rev2.pdf
    """
    table = [
        (16, 0),  # (time in sec, power_level in % of peak_power)
        (28, -12.5),
        (12, -25),
        (8, 12.5),
        (16, 0),
        (24, -12.5),
        (12, -25),
        (8, 12.5),
        (16, 0),
        (24, -12.5),
        (12, -25),
        (8, 12.5),
        (16, 0),
        (36, -12.5),
        (8, -100),
        (24, -62.5),
        (8, 25),
        (32, -25),
        (8, 50),
        (44, 0),
    ]
    steps = []
    for time, power_level in table:
        if power_level < 0:
            steps.append(f"Discharge at {-power_level/100*peak_power} W for {time} seconds")
        elif power_level > 0:
            steps.append(f"Charge at {power_level/100*peak_power} W for {time} seconds")
        else:
            steps.append(f"Rest for {time} seconds")

    return Experiment(
        steps * number_of_cycles,
        period=f"{sampling_time_s} seconds",
    )
