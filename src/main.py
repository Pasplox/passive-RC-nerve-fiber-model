import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
IMG_DIR = Path(__file__).parent.parent / "images"
IMG_DIR.mkdir(exist_ok=True)

def load_data():
    table1 = pd.read_csv(DATA_DIR / "table1_steady_state_transmembrane_potentials.csv")
    table2 = pd.read_csv(DATA_DIR / "table2_square_wave_transmembrane_potentials.csv")
    table3 = pd.read_csv(DATA_DIR / "table3_transient_response_measurements.csv")
    table3 = table3.dropna(subset=["Maximum Delta V (V)"])
    return {"table1": table1, "table2": table2, "table3": table3}

data = load_data()

# # check that tables are loading correctly
# for name, df in data.items():
#     print(f"\n=== {name} ({df.shape[0]} rows x {df.shape[1]} cols) ===")
#     print(df.to_string(index=False))

# ── Table 1 Analysis ─────────────────────────────────────────────────────────

def analyze_steady_state(df, img_path):
    # step 1: remap "Vin" to node 0 and cast Node Number to int
    t1 = df.copy()
    t1["Node Number"] = t1["Node Number"].replace("Vin", "0").astype(int)

    # step 2: extract node numbers and voltages as arrays
    x = t1["Node Number"].values
    y = t1["Voltage (V)"].values

    # step 3: linear regression on log(y) vs x to extract decay constant
    slope, intercept = np.polyfit(x, np.log(y), 1)
    y_fit = np.exp(intercept + slope * x)

    Lc = -1 / slope
    Rin = np.exp(intercept)  # voltage at node 0 from fit; actual Rin needs current
    Ri = Rin / Lc
    Rm = Rin * Lc

    print(f"Table 1 slope: {slope:.4f}, Lc: {Lc:.4f}")
    print(f"  Derived Ri: {Ri/1e3:.2f} kΩ, Rm: {Rm/1e3:.2f} kΩ")

    # step 4: create semi-log plot, annotate, and save
    fig, ax = plt.subplots()
    ax.semilogy(x, y, 'o', label="data")
    ax.semilogy(x, y_fit, '-', label="linear fit")
    ax.set_xlabel("Node Number")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Steady-State Transmembrane Potential vs Node Number")
    ax.legend()
    ax.grid(True, which="both")
    plt.tight_layout()
    fig.savefig(img_path, dpi=300)
    plt.close()

    return {"slope": slope, "Lc": Lc, "Ri": Ri, "Rm": Rm}

results_t1 = analyze_steady_state(data["table1"], IMG_DIR / "table_1_analysis.png")


# ── Table 2 Analysis ─────────────────────────────────────────────────────────


# ── Table 3 Analysis ─────────────────────────────────────────────────────────
