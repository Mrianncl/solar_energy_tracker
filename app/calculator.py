# app/calculator.py

from app.environment import calculate_environmental_impact


ELECTRICITY_RATE_KWH = 5   # Local currency per kWh
CO2_PER_KWH_GRID = 0.5    # kg of CO2 emitted per kWh from grid
CO2_PER_TREE_YEAR = 21.76  # kg of CO2 absorbed per tree per year

def calculate_savings(daily_solar_kwh):
    daily_saving_currency = daily_solar_kwh * ELECTRICITY_RATE_KWH
    monthly_saving = daily_saving_currency * 30
    yearly_saving = monthly_saving * 12

    co2_saved_daily = daily_solar_kwh * CO2_PER_KWH_GRID
    co2_saved_monthly = co2_saved_daily * 30
    co2_saved_yearly = co2_saved_monthly * 12

    env_data = calculate_environmental_impact(co2_saved_yearly)

    badge = "None"
    if co2_saved_monthly > 300:
        badge = "🥇 Gold"
    elif co2_saved_monthly > 150:
        badge = "🥈 Silver"
    elif co2_saved_monthly > 50:
        badge = "🥉 Bronze"

    return {
        "daily_saving": daily_saving_currency,
        "monthly_saving": monthly_saving,
        "yearly_saving": yearly_saving,

        "co2_daily": co2_saved_daily,
        "co2_monthly": co2_saved_monthly,
        "co2_yearly": co2_saved_yearly,

        "trees_saved": env_data["trees_saved"],  # Use environmental impact function
        "badge": badge
    }