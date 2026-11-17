"""DC operating-point equations for NPN common-emitter bias circuits.

All resistances are in ohms and currents in amperes inside these functions.
The web layer converts input units before calling them.
"""


def _finish(vcc, rc, beta, vbe, ib, re_ohms):
    """Build the shared result dict from base current."""
    ic_a = beta * ib
    ie_a = (beta + 1) * ib
    ve = ie_a * re_ohms
    vb = ve + vbe
    vc = vcc - ic_a * rc
    vce = vc - ve

    result = {
        "vb_v": vb,
        "ve_v": ve,
        "vc_v": vc,
        "vce_v": vce,
        "ic_ma": ic_a * 1e3,
    }
    if ib <= 0 or vce <= 0.2:
        result["warning"] = (
            "แบบจำลอง Forward Active อาจใช้ไม่ได้ "
            "(I_B ≤ 0 หรือ V_CE ≤ 0.2 V)"
        )
    return result


def fixed_bias(vcc, rc, beta, vbe, rb):
    """Fixed bias: RB from VCC to base, emitter tied directly to ground."""
    ib = (vcc - vbe) / rb
    return _finish(vcc, rc, beta, vbe, ib, 0.0)


def emitter_bias(vcc, rc, beta, vbe, rb, re):
    """Emitter bias with a single supply: RB to base, RE from emitter to ground."""
    ib = (vcc - vbe) / (rb + (beta + 1) * re)
    return _finish(vcc, rc, beta, vbe, ib, re)


def voltage_divider_bias(vcc, rc, beta, vbe, r1, r2, re):
    """Voltage-divider bias (the Lab 2 circuit, unchanged)."""
    vth = vcc * r2 / (r1 + r2)
    rth = r1 * r2 / (r1 + r2)
    ib = (vth - vbe) / (rth + (beta + 1) * re)
    return _finish(vcc, rc, beta, vbe, ib, re)
