from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def metric_conversion(m):
    out = {k: str(Q_(m[k]).to('inch').round(2)) for (k, v) in m.items()}
    return {k: v.replace('inch', 'Inches') for (k, v) in out.items()}
