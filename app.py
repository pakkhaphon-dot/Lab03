"""Lab 03 — BJT DC Bias web app (Flask + Jinja)."""

import math

from flask import Flask, render_template, request

import dc_bias

app = Flask(__name__)

# Field order matters: it must match each calculator's argument order.
MODE_FIELDS = {
    "divider": ("r1", "r2", "re"),
    "fixed": ("rb",),
    "emitter": ("rb", "re"),
}

CALCULATORS = {
    "divider": dc_bias.voltage_divider_bias,
    "fixed": dc_bias.fixed_bias,
    "emitter": dc_bias.emitter_bias,
}

# Convert the units shown on the form into ohms (beta stays dimensionless).
SCALE_TO_OHMS = {
    "vcc": 1.0,
    "rc": 1_000.0,       # kΩ -> Ω
    "beta": 1.0,
    "vbe": 1.0,
    "rb": 1_000_000.0,   # MΩ -> Ω
    "re": 1_000.0,       # kΩ -> Ω
    "r1": 1_000.0,       # kΩ -> Ω
    "r2": 1_000.0,       # kΩ -> Ω
}

DEFAULTS = {
    "vcc": "12",
    "rc": "2.2",
    "beta": "100",
    "vbe": "0.70",
    "r1": "100",
    "r2": "22",
    "re": "1",
    "rb": "1",
}


def _parse_positive(form, name):
    """Read one required field; reject missing, non-numeric, non-finite, <= 0."""
    raw = form.get(name, "").strip()
    if not raw:
        raise ValueError(f"กรอก {name} ด้วย")
    try:
        value = float(raw)
    except ValueError:
        raise ValueError(f"{name} ต้องเป็นตัวเลข") from None
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} ต้องเป็นจำนวนจำกัดที่มากกว่า 0")
    return value


@app.route("/", methods=["GET", "POST"])
def index():
    mode = (
        request.form.get("mode", "divider")
        if request.method == "POST"
        else request.args.get("mode", "divider")
    )
    error = None
    result = None

    if request.method == "POST":
        if mode not in MODE_FIELDS:
            error = f"ไม่รู้จักโหมด {mode!r} กรุณาเลือกวงจรใหม่"
        else:
            try:
                names = ("vcc", "rc", "beta", "vbe", *MODE_FIELDS[mode])
                values = {
                    name: _parse_positive(request.form, name) * SCALE_TO_OHMS[name]
                    for name in names
                }
                result = CALCULATORS[mode](
                    values["vcc"],
                    values["rc"],
                    values["beta"],
                    values["vbe"],
                    *(values[name] for name in MODE_FIELDS[mode]),
                )
            except ValueError as exc:
                error = str(exc)
            except ZeroDivisionError:
                error = "ตัวหารเป็นศูนย์ กรุณาตรวจค่าที่กรอก"

    return render_template(
        "index.html",
        mode=mode,
        modes=MODE_FIELDS,
        error=error,
        result=result,
        form=request.form,
        defaults=DEFAULTS,
    )


if __name__ == "__main__":
    app.run(debug=True)
