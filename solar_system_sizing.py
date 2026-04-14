import pandas as pd
import matplotlib.pyplot as plt

# Load profile
file_path = "load_profile.csv"
full_load_profile = pd.read_csv(file_path)

# LOAD PROFILE PROCESSING
# Define time blocks and their durations
time_blocks = [
    ("Usage hrs (0 to 4)", 0, 4),   # 4 hours
    ("Usage hrs (4 to 7)", 4, 7),   # 3 hours
    ("Usage hrs (7 to 10)", 7, 10),
    ("Usage hrs (10 to 13)", 10, 13),
    ("Usage hrs (13 to 16)", 13, 16),
    ("Usage hrs (16 to 19)", 16, 19),
    ("Usage hrs (19 to 22)", 19, 22),
    ("Usage hrs (22 to 0)", 22, 24) # 2 hours
]

# Initialize hourly load (0–23)
hourly_load_kwh = [0] * 24

# Loop through each appliance
for _, row in full_load_profile.iterrows():
    power_kw = (row["Quantity"] * row["Rating (W)"]) / 1000  # convert to kW

    for col, start, end in time_blocks:
        total_usage_hours = row[col]

        duration = end - start
        if duration <= 0:
            continue

        # distribute evenly per hour
        usage_per_hour = total_usage_hours / duration

        for hr in range(start, end):
            energy = power_kw * usage_per_hour  # kWh for that hour
            hourly_load_kwh[hr % 24] += energy

# Convert to pandas Series for convenience
hourly_load_profile = pd.Series(hourly_load_kwh, index=range(24))

print("\nHourly Load Profile (kWh):")
print(hourly_load_profile)

# Load iiradiance CSV (skip header rows)
file_path = "Solar_irradiance_Hourly_20250101_20251230_000d35N_032d56E_UTC.csv"
hourly_solar_irradiance = pd.read_csv(file_path, skiprows=9)

# Rename for clarity
hourly_solar_irradiance.rename(columns={
    "ALLSKY_SFC_SW_DWN": "irradiance"
}, inplace=True)

# Remove invalid values (-999)
hourly_solar_irradiance = hourly_solar_irradiance[hourly_solar_irradiance["irradiance"] >= 0]

# Yearly average irradiance
yearly_avg = hourly_solar_irradiance["irradiance"].mean()
print(f"Yearly average irradiance: {yearly_avg:.2f} Wh/m²")

# Average per hour (0–23)
hourly_avg = hourly_solar_irradiance.groupby("HR")["irradiance"].mean()

print("\nAverage irradiance per hour:")
print(hourly_avg)

# Plot irradiance
# plt.figure()
# plt.plot(hourly_avg.index, hourly_avg.values)
# plt.xlabel("Hour of Day (0-23)")
# plt.ylabel("Average Irradiance (Wh/m²)")
# plt.title("Average Solar Irradiance Profile (Kampala, 2025)")
# plt.grid()

# plt.show()

# -----------------------------
# CASE 1: FULL LOAD SOLAR SYSTEM
# -----------------------------

# 1. Total daily load (kWh)
daily_load_kwh = hourly_load_profile.sum()
print(f"\nTotal Daily Load: {daily_load_kwh:.2f} kWh")

# 2. Peak Sun Hours (PSH)
daily_irradiance = hourly_avg.sum()  # Wh/m² per day
psh = daily_irradiance / 1000        # kWh/m²/day
print(f"Peak Sun Hours (PSH): {psh:.2f} hours")

# 3. Required solar system size (kW)
pv_size_fl_kwh = daily_load_kwh / psh
print(f"Required Solar Size: {pv_size_fl_kwh:.2f} kW")

# -----------------------------
# 4. Hourly solar output (kWh)
# -----------------------------
solar_output_kwh = (pv_size_fl_kwh * hourly_avg) / 1000  # convert Wh → kWh

# -----------------------------
# 5. Compare load vs solar
# -----------------------------
net_energy = hourly_load_profile - solar_output_kwh

# -----------------------------
# 6. Battery sizing
# -----------------------------
battery_energy = 0

for val in net_energy:
    if val > 0:   # deficit only
        battery_energy += val

# Apply efficiency (85%)
battery_size_fl_kwh = battery_energy / 0.85

print(f"Required Battery Size: {battery_size_fl_kwh:.2f} kWh")

# -----------------------------
# 7. Plot solar vs load
# -----------------------------
plt.figure()

plt.plot(hourly_load_profile.index, hourly_load_profile.values, label="Load (kWh)")
plt.plot(hourly_avg.index, solar_output_kwh.values, label="Solar Output (kWh)")

plt.xlabel("Hour of Day (0-23)")
plt.ylabel("Energy (kWh)")
plt.title("Load vs Solar Output (Full System)")
plt.legend()
plt.grid()

plt.show()

# -----------------------------
# CRITICAL LOAD PROFILE
# -----------------------------

# Clean 'critical' column (avoid issues with spaces/case)
full_load_profile["critical"] = full_load_profile["critical"].str.strip().str.lower()

# Filter only critical loads
critical_load_df = full_load_profile[full_load_profile["critical"] == "yes"]

# Initialize hourly critical load
hourly_critical_kwh = [0] * 24

# Loop through critical appliances
for _, row in critical_load_df.iterrows():
    power_kw = (row["Quantity"] * row["Rating (W)"]) / 1000

    for col, start, end in time_blocks:
        total_usage_hours = row[col]
        duration = end - start

        if duration <= 0:
            continue

        usage_per_hour = total_usage_hours / duration

        for hr in range(start, end):
            energy = power_kw * usage_per_hour
            hourly_critical_kwh[hr] += energy

# Convert to pandas Series
hourly_critical_profile = pd.Series(hourly_critical_kwh, index=range(24))

print("\nHourly Critical Load Profile (kWh):")
print(hourly_critical_profile)

plt.figure()

plt.plot(hourly_load_profile.index, hourly_load_profile.values, label="Total Load")
plt.plot(hourly_critical_profile.index, hourly_critical_profile.values, linestyle='--', label="Critical Load")

plt.xlabel("Hour of Day (0-23)")
plt.ylabel("Energy (kWh)")
plt.title("Total Load vs Critical Load")
plt.legend()
plt.grid()

plt.show()

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate_system(pv_size_cl_kwh, irradiance_profile, load_profile, critical_profile, efficiency=0.85):
    battery_init = 0
    min_battery = 0
    max_battery = 0


    for day in range(5):  # simulate 5 days to stabilize
        for hr in range(24):
            # Solar production (kWh)
            solar_kwh = (pv_size_cl_kwh * irradiance_profile[hr]) / 1000
    
            load_kwh = load_profile[hr]
            critical_kwh = critical_profile[hr]
    
            if solar_kwh >= load_kwh:
                # Excess energy → charge battery
                surplus = solar_kwh - load_kwh
                battery_init += surplus * efficiency
            else:
                # Deficit → only critical load must be met
                deficit = max(0, critical_kwh - solar_kwh)
                battery_init -= deficit / efficiency

    battery = battery_init

    for hr in range(24):
        # Solar production (kWh)
        solar_kwh = (pv_size_cl_kwh * irradiance_profile[hr]) / 1000

        load_kwh = load_profile[hr]
        critical_kwh = critical_profile[hr]

        if solar_kwh >= load_kwh:
            # Excess energy → charge battery
            surplus = solar_kwh - load_kwh
            battery += surplus * efficiency
        else:
            # Deficit → only critical load must be met
            deficit = max(0, critical_kwh - solar_kwh)
            battery -= deficit / efficiency

        # Track limits
        min_battery = min(min_battery, battery)
        max_battery = max(max_battery, battery)

    system_works = (min_battery >= 0)

    return system_works, min_battery, max_battery

# -----------------------------
# BINARY SEARCH
# -----------------------------
low = 0
high = pv_size_fl_kwh  # from full-load case

tolerance = 0.01  # kW precision (~10W)

while (high - low) > tolerance:
    pv_size_cl_kwh = (low + high) / 2

    works, min_batt, max_batt = simulate_system(
        pv_size_cl_kwh,
        hourly_avg,
        hourly_load_profile,
        hourly_critical_profile
    )

    if works:
        high = pv_size_cl_kwh
    else:
        low = pv_size_cl_kwh

# Final optimal size
optimal_pv_size_cl_kwh = high

print(f"\nOptimal PV Size (Critical Load): {optimal_pv_size_cl_kwh:.2f} kW")

works, min_batt, max_batt = simulate_system(
    optimal_pv_size_cl_kwh,
    hourly_avg,
    hourly_load_profile,
    hourly_critical_profile
)

battery_size_kwh = max_batt

print(f"Required Battery Size: {battery_size_kwh:.2f} kWh")

# Solar output for optimal system
solar_output_kwh = (optimal_pv_size_cl_kwh * hourly_avg) / 1000

plt.figure()

plt.plot(hourly_load_profile.index, hourly_load_profile.values, label="Total Load")
plt.plot(hourly_critical_profile.index, hourly_critical_profile.values, linestyle='--', label="Critical Load")
plt.plot(hourly_avg.index, solar_output_kwh.values, label="Solar Output")

plt.xlabel("Hour of Day (0-23)")
plt.ylabel("Energy (kWh)")
plt.title("Optimized System (Critical Load Case)")
plt.legend()
plt.grid()

plt.show()