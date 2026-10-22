import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

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

# step 1: remap "Vin" to node 0 and cast Node Number to int
t1 = data["table1"].copy()
t1["Node Number"] = t1["Node Number"].replace("Vin", "0").astype(int)

# step 2: extract node numbers and voltages as arrays
x = t1["Node Number"].values
y = t1["Voltage (V)"].values

# step 3: create semi-log plot (linear x, log y)

# step 4: annotate axes, title, and grid

# step 5: save figure and/or show


# ── Table 2 Analysis ─────────────────────────────────────────────────────────


# ── Table 3 Analysis ─────────────────────────────────────────────────────────
