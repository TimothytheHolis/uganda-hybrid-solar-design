# Hybrid Solar System Optimization for Ugandan Homes & Small Businesses 🇺🇬☀️

A data-driven approach to designing **right-sized hybrid solar systems** that maximize reliability while minimizing cost — built specifically for the Ugandan context.

---

## 🌍 The Problem

Grid power in Uganda is unreliable. Load shedding is common, and many households and small businesses need backup power. Solar is the obvious answer — but the way most systems are currently sized leads to two common failure modes:

1. **Oversized batteries** — Traditional solar design formulas assume the battery must store *all* the solar energy generated and supply *all* the load during outages. For homes with heavy appliances (water heaters, electric cookers, flat irons), this results in very large, expensive battery banks. Many households resort to cheap, unreliable batteries — which get damaged quickly, especially when connected directly to loads without proper charge management.

2. **Undersized solar** — To keep costs down, installers sometimes cut the PV array, but without properly accounting for realistic load curves, the system underperforms.

The result: expensive systems that still fail, or cheap systems that damage equipment and batteries.

> **This project proposes a better approach: simulate the real energy balance hour by hour, use solar output directly during the day, and size the battery only for the deficit — not the whole load.**

---

## ⚡ Project Overview

This Python-based tool models a home or small business energy system with hourly resolution, using real solar irradiance data and a realistic load profile. It outputs:

- Recommended solar PV size (kW)
- Recommended battery size (kWh)
- Visual comparison of load vs solar output across the day

The system is designed around **two operating modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| **Full Load System** | Solar + battery powers all appliances | Fully off-grid, high-budget |
| **Critical Load System** | Solar + battery powers only essential devices; heavy loads use grid | Hybrid grid-tied, cost-optimized |

The **Critical Load approach is the main innovation** — it makes solar accessible and reliable for the middle-income Ugandan household.

---

## 🧠 How It Works

### 1. Load Profile Modeling

Appliances are entered with their rated wattage, quantity, and usage hours across eight time blocks (0–4, 4–7, 7–10, ... 22–24). The tool computes an hourly energy consumption profile in kWh.

Each appliance is tagged as **critical** (must have power during outages) or **non-critical** (can rely on grid).

Typical critical loads: lights, router, phone charging, fan, small TV, fridge  
Typical non-critical: electric cooker, flat iron, water heater (paccolator), washing machine

> **Why exclude heavy loads from the battery?** A flat iron or water heater may only run for 30 minutes a day, but its instantaneous power draw (1000–3000W) is enormous. Storing that energy in a battery means paying for large capacity that sits idle most of the time. Let the grid handle those peak loads.

### 2. Solar Irradiance Data

The tool uses real hourly irradiance data from the **NASA POWER dataset** for Kampala (0.35°N, 32.56°E), averaged over a full year to produce a representative daily solar profile.

Peak Sun Hours (PSH) are derived from this data — a more accurate approach than using a fixed number from a lookup table.

### 3. Energy Flow Simulation

The simulator runs hour by hour:

```
For each hour:
  if solar_output >= load:
      surplus → charge battery (× efficiency)
  else:
      deficit from critical load → discharge battery (÷ efficiency)
```

A 5-day warm-up period stabilizes battery state before final sizing is determined. Charge/discharge efficiency defaults to 85% (representative of lithium iron phosphate or AGM batteries).

### 4. Optimization via Binary Search

For the critical load case, the minimum viable PV size is found using **binary search** between 0 and the full-load PV requirement. At each step, the simulator checks whether the battery state of charge ever drops below zero. The smallest PV size that keeps the battery non-negative is selected.

This avoids the common over-engineering trap of simply adding more panels.

### 5. Battery Sizing

Battery capacity is set equal to the **maximum swing in stored energy** during the simulation — the difference between the peak charge and the point of deepest discharge. This directly represents the real energy buffer needed, rather than a rule-of-thumb multiplier.

---

## 📊 Key Results (Example — Typical Ugandan Home)

| Parameter      | Full Load System| Critical Load System    |
|----------------|-----------------|-------------------------|
| PV Size        | Larger          | Reduced                 |
| Battery Size   | Large           | Significantly smaller   |
| Grid Dependency| None            | Handles heavy loads only|
| Reliability    | High (off-grid) | High (hybrid)           |
| Cost           | High            | Moderate                |

> **The critical load approach can reduce battery requirements substantially, directly cutting system cost and improving long-term reliability.**

---

## 🚀 Who Is This For?

- **Middle-income households** in Uganda and similar markets who want reliable backup power without spending on an off-grid system
- **Small businesses** — shops, stationery, salons — needing daytime power continuity
- **Rural businesses** with agricultural or water pumping needs (irrigation, boreholes)
- **Solar installers and engineers** wanting a quick simulation tool for client proposals
- **Researchers and students** studying energy access in sub-Saharan Africa

---

## 🛠️ Technologies Used

- **Python 3**
- **Pandas** — data processing and time-series manipulation
- **Matplotlib** — visualization
- **NASA POWER API data** — real irradiance inputs

---

## 📁 Repository Structure

```
├── main.py                         # Main simulation script
├── load_profile.csv                # Appliance list (edit for your home)
├── Solar_irradiance_Hourly_*.csv   # NASA POWER irradiance data (Kampala)
└── README.md
```

---

## 🔧 How to Use

1. **Edit `load_profile.csv`** with your appliances, ratings, quantities, usage hours, and critical status.
2. **Run `main.py`** — it will output PV and battery sizing for both full-load and critical-load cases, and show plots.
3. Optionally download fresh irradiance data from [NASA POWER](https://power.larc.nasa.gov/data-access-viewer/) for your location.

---

## 🗺️ Roadmap

The following extensions are planned:

- [ ] **Cost analysis** — PV panel, battery, inverter, and installation cost estimates for the Ugandan market
- [ ] **Payback period calculation** — based on current UMEME tariffs and fuel/generator costs
- [ ] **Load scheduling** — recommend shifting flexible loads (fridge, water pump, washing machine) to solar hours
- [ ] **Flexible/deferrable load handling** — model loads that can be shifted to match solar availability
- [ ] **Multi-day battery simulation** — account for consecutive cloudy days
- [ ] **Web interface** — allow non-technical users to input their load and get a system recommendation
- [ ] **Grid tariff integration** — optimize import/export decisions for grid-connected systems

---

## 🤝 Author

**Timothy Mukhooli**  
Electrical Engineer | Solar Systems Design | Embedded Systems (FPGA, MCU, C)

*Open to collaboration, consulting, and remote work opportunities in energy systems, embedded systems, and engineering tools.*

---

## 📄 License

MIT License — free to use, adapt, and build upon.
