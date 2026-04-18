# Hybrid Solar System Optimization (Uganda) 🇺🇬☀️

A simple tool for designing practical, cost-effective hybrid solar systems for homes and small businesses in Uganda.

---

## Why I Built This

In Uganda, power cuts are normal. So people turn to solar, which is logical because the country's solar potential is high.

But from what I've seen, most systems end up either too expensive because they're overdesigned, or unreliable because they're undersized or poorly put together. A big part of the problem is how systems get sized in the first place.

The common assumption is: *the battery must power everything.* That looks fine on paper, but in practice it leads to very large battery banks, high upfront costs, and people settling for cheap batteries that don't last. On the other end, some installations skip proper design entirely — just trial and error — and those usually work for a while before quietly falling apart.

I wanted to try something more grounded.

---

## The Idea

Instead of designing for everything, this tool focuses on:

- using solar output directly during the day, and
- sizing the battery only for what actually needs backup

Put simply: **don't spend money storing energy you don't need to store.**

---

## What the Tool Does

This is a Python simulator that takes a realistic load profile (your appliances and when you use them), pulls in real solar irradiance data, and simulates energy flow hour by hour. From that it gives you:

- recommended PV size (kW)
- recommended battery size (kWh)
- graphs showing how solar output and load interact across the day

---

## Two System Types

### 1. Full Load System
Solar and battery cover everything — no grid required. Good for off-grid setups or high-budget installs where you want complete independence.

### 2. Critical Load System *(main focus)*
The battery only covers essential appliances. Heavy loads either run on solar during the day or stay on the grid.

| Critical (battery-backed) | Non-critical (grid / daytime solar) |
|---------------------------|-------------------------------------|
| Lights                    | Electric cooker                     |
| Wi-Fi router              | Flat iron                           |
| Phone & laptop charging   | Water heater                        |
| TV                        | Washing machine                     |

This cuts battery size significantly without losing reliability where it actually matters.

**Why leave heavy loads off the battery?** An iron or water heater might only run for 20–30 minutes a day, but at 1000–3000W, designing a battery around them means paying for capacity that sits idle almost all the time. It's cheaper and smarter to let them run when solar is strong, or leave them on the grid.

---

## How It Works

1. You define your appliances, their ratings, and when you use them
2. The tool builds an hourly energy profile across 24 hours
3. It processes solar data from the [NASA POWER dataset](https://power.larc.nasa.gov/) for your location
4. It simulates solar production, load demand, and battery charge/discharge hour by hour

For the critical-load case, a binary search finds the **minimum solar size** that keeps the system stable — no oversizing, no guesswork. Battery size is derived from the actual energy swing during simulation, not a rule-of-thumb multiplier.

---

## Results (Typical Ugandan Home)

|              | Full Load System | Critical Load System     |
|--------------|------------------|--------------------------|
| Battery size | Large            | Much smaller             |
| Cost         | High             | More affordable          |
| Grid needed? | No               | For heavy loads only     |
| Best for     | Off-grid         | Urban / peri-urban homes |

You still get backup during outages and usable solar during the day — just without overpaying for it.

---

## Who This Is For

- Households that want reliable backup without going fully off-grid
- Small businesses — shops, salons, stationery, offices
- Solar technicians looking for a more principled way to size systems
- Engineers and students working on energy access problems

---

## Tech Stack

- Python 3
- Pandas
- Matplotlib
- Solar irradiance data from [NASA POWER](https://power.larc.nasa.gov/)

---

## How to Use

```bash
# Install dependencies
pip install -r requirements.txt

# Edit your load profile
# Open data/load_profile.csv and fill in your appliances average usage for the time zones

# Run the simulation
python src/main.py

# Results and graphs go to outputs/figures/
```

You can use solar data for any location — just download the hourly irradiance CSV from NASA POWER for your coordinates and point the script at it.

---

## Project Structure

```
uganda-hybrid-solar-design/
│
├── data/
│   ├── load_profile.csv
│   └── solar_irradiance/
│       └── kampala_bwaise_irr_2025.csv
│
├── outputs/
│   └── figures/
│
├── src/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## What's Coming Next

- [ ] Cost estimates based on current Ugandan market prices
- [ ] Payback period calculation against UMEME tariffs
- [ ] Smarter load scheduling — run heavy appliances when solar is strongest
- [ ] Better handling of consecutive cloudy days
- [ ] Simple web interface for non-technical users

---

## About

Built by **Timothy Mukhooli** — Electrical Engineer with a background in solar systems, FPGA design, and embedded systems. This started as a personal project to address something I kept seeing go wrong in local solar installations. Still a work in progress.

---

## License

MIT — use it, modify it, build on it.