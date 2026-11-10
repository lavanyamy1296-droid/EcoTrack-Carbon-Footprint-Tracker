# Simplified illustrative factors for a student demonstration.
FACTORS = {
    "electricity_kwh": 0.70, "lpg_kg": 3.00, "car_km": 0.18,
    "two_wheeler_km": 0.07, "bus_passenger_km": 0.08,
    "train_passenger_km": 0.04, "waste_kg": 0.50
}
DIET_FACTORS = {"Mostly plant-based": 35.0, "Mixed diet": 65.0, "Meat-heavy": 100.0}

def calculate_footprint(activity):
    home = activity["electricity_kwh"] * FACTORS["electricity_kwh"] + activity["lpg_kg"] * FACTORS["lpg_kg"]
    transport = (activity["car_km"] * FACTORS["car_km"]
                 + activity["two_wheeler_km"] * FACTORS["two_wheeler_km"]
                 + activity["bus_passenger_km"] * FACTORS["bus_passenger_km"]
                 + activity["train_passenger_km"] * FACTORS["train_passenger_km"])
    food = DIET_FACTORS[activity["diet"]]
    waste = activity["waste_kg"] * FACTORS["waste_kg"]
    breakdown = {"Home energy": round(home, 2), "Transport": round(transport, 2),
                 "Food (diet proxy)": round(food, 2), "Waste": round(waste, 2)}
    total = round(sum(breakdown.values()), 2)
    return {"total_kg": total, "breakdown": breakdown, "largest_category": max(breakdown, key=breakdown.get), "diet": activity["diet"], "recycling": activity["recycling"]}

def get_recommendations(result):
    tips = []
    b = result["breakdown"]
    if b["Home energy"] >= 50:
        tips += ["Reduce avoidable electricity use: switch off idle devices, use efficient lighting, and set air-conditioning moderately.",
                 "Track monthly kWh on your electricity bill to see whether energy-saving changes help."]
    else:
        tips.append("Keep efficient habits: use daylight, switch off unused appliances, and choose efficient devices.")
    if b["Transport"] >= 50:
        tips.append("Combine errands, use public transport, carpool, or walk/cycle for short trips where practical.")
    else:
        tips.append("Maintain lower-emission travel habits and avoid unnecessary journeys.")
    diet = result.get("diet", "")
    if diet == "Meat-heavy":
        tips.append("Try adding a few plant-rich meals each week and avoid buying more food than you can use.")
    elif diet == "Mixed diet":
        tips.append("Consider more plant-based meals and plan portions to reduce food waste.")
    else:
        tips.append("Continue choosing plant-rich meals and store food carefully to avoid spoilage.")
    if b["Waste"] >= 10:
        tips.append("Separate recyclable and compostable waste where local facilities accept them; reduce single-use packaging.")
    if result.get("recycling") != "Yes":
        tips.append("Check local waste collection rules and start separating accepted recyclables.")
    return tips
