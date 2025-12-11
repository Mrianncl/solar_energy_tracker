# app/environment.py

# Constants
CO2_PER_TREE_YEAR = 21.76  # kg of CO2 absorbed per tree per year
CO2_SAVINGS_PER_KWH = 0.5  # kg of CO2 avoided per kWh from solar

def calculate_environmental_impact(co2_saved_yearly):
    """
    Returns:
        dict: trees_saved, co2_saved
    """
    trees_saved = round(co2_saved_yearly / CO2_PER_TREE_YEAR, 2)
    return {
        "trees_saved": trees_saved,
        "co2_saved_yearly": co2_saved_yearly,
        "co2_per_tree_year": CO2_PER_TREE_YEAR
    }