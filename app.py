
import base64
import datetime
import io
import os
import time

import matplotlib
matplotlib.use("Agg")  # headless: no display needed to render plots
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request

from algorithms import ALGORITHMS

app = Flask(__name__)

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Safety cap: some algorithms here are O(n^2) or worse. With a small step size and large n_max, the number of data points can explode.
MAX_DATA_POINTS = 200


def _parse_int(raw, field_name):

    try:
        return int(str(raw).replace(",", "").strip()), None
    except (TypeError, ValueError):
        return None, f"'{field_name}' must be an integer, got: {raw!r}"


@app.route("/analyze", methods=["GET"])
def analyze():
    algo_param = request.args.get("algo")
    step_param = request.args.get("step")
    n_max_param = request.args.get("n_max")

    if not algo_param:
        return jsonify({"error": "Missing required query parameter: algo"}), 400
    if not step_param:
        return jsonify({"error": "Missing required query parameter: step"}), 400
    if not n_max_param:
        return jsonify({"error": "Missing required query parameter: n_max"}), 400

    # Allow one algo or a comma-separated list, and tolerate stray quotes/brackets
    algo_names = [
        a.strip().strip("'\"[]")
        for a in algo_param.split(",")
        if a.strip().strip("'\"[]")
    ]

    step, err = _parse_int(step_param, "step")
    if err:
        return jsonify({"error": err}), 400
    n_max, err = _parse_int(n_max_param, "n_max")
    if err:
        return jsonify({"error": err}), 400

    if step <= 0:
        return jsonify({"error": "'step' must be a positive integer"}), 400
    if n_max <= 0:
        return jsonify({"error": "'n_max' must be a positive integer"}), 400

    unknown = [a for a in algo_names if a not in ALGORITHMS]
    if unknown:
        return jsonify({
            "error": f"Unknown algorithm(s): {', '.join(unknown)}",
            "supported_algorithms": sorted(ALGORITHMS.keys())
        }), 400

    n_values = list(range(0, n_max + 1, step))
    if len(n_values) > MAX_DATA_POINTS:
        return jsonify({
            "error": (
                f"Too many data points ({len(n_values)}) for n_max={n_max} "
                f"and step={step}. Increase step or lower n_max so that "
                f"n_max // step <= {MAX_DATA_POINTS}."
            )
        }), 400

    # Run each algorithm across every n and record wall-clock time
    timings = {}
    for name in algo_names:
        func = ALGORITHMS[name]["func"]
        series = []
        for n in n_values:
            start = time.perf_counter()
            func(n)
            series.append(time.perf_counter() - start)
        timings[name] = series

    # Build the plot
    plt.figure(figsize=(8, 5))
    for name, series in timings.items():
        label = f"{name} ({ALGORITHMS[name]['complexity']})"
        plt.plot(n_values, series, marker="o", markersize=3, label=label)
    plt.xlabel("n (number of elements)")
    plt.ylabel("Time (seconds)")
    plt.title("Time Complexity Visualizer")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{'_'.join(algo_names)}_{timestamp}.png"
    filepath = os.path.join(PLOTS_DIR, filename)
    plt.savefig(filepath, dpi=120)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=120)
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return jsonify({
        "algorithms": algo_names,
        "step": step,
        "n_max": n_max,
        "n_values": n_values,
        "timings": timings,
        "image_path": filepath,
        "image_base64": image_base64,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
