from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def metric_conversion(m: dict) -> dict:
    """Converts dimensions from metric to imperial units

    Parameters
    ----------
    m : dict
        A dictionary containing dimension measurements in the metric system

    Returns
    -------
    dict
        A dictionary containing dimension measurements in the imperial system
    """
    out: dict = {k: str(Q_(m[k]).to('inch').round(2)) for (k, v) in m.items()}
    return {k: v.replace('inch', 'Inches') for (k, v) in out.items()}
