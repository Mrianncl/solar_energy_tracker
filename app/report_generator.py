# app/report_generator.py
from datetime import time
import os
from fpdf import FPDF
from pathlib import Path

REPORTS_DIR = Path("reports")  # platform-independent

def format_report_lines(data, ascii_safe=False):
    return [
        "Solar Energy Savings Report",
        "=" * 30,
        f"Location: {data['location']}",
        f"Monthly Bill: {'$' if ascii_safe else '$'}{data['monthly_bill']}",
        f"Daily Solar kWh: {data['daily_solar_kwh']} kWh",
        f"Estimated Daily Saving: {'$' if ascii_safe else '$'}{data['daily_saving']:.2f}",
        f"Estimated Monthly Saving: {'$' if ascii_safe else '$'}{data['monthly_saving']:.2f}",
        f"{'CO2' if ascii_safe else 'CO₂'} Saved Yearly: {data['co2_yearly']:.2f} kg",
        f"Trees Equivalent Saved: {data['trees_saved']:.2f} trees/year",
        "",
        "Recommendation:",
        "Use high-power appliances during peak sunlight hours (10 AM - 4 PM)"  # dash made ASCII-safe
    ]

def generate_txt_report(data, file_path):
    lines = format_report_lines(data, ascii_safe=False)  # UTF-8 supports Unicode
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        return f"Error writing TXT report: {e}"

def generate_pdf_report(data, file_path):
    lines = format_report_lines(data, ascii_safe=True)  # avoid Unicode for FPDF
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for i, line in enumerate(lines):
            if line == "":
                pdf.ln(5)
            elif i == 0:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, line, ln=True, align='C')
                pdf.set_font("Arial", size=12)
            elif line.startswith("Recommendation:") or "Use high-power" in line:
                pdf.set_font("Arial", style="I", size=12)
                pdf.multi_cell(0, 10, line)
                pdf.set_font("Arial", size=12)
            else:
                pdf.cell(0, 10, line, ln=True)

        pdf.output(file_path)
    except Exception as e:
        return f"Error writing PDF report: {e}"

def save_report(data, format_choice="txt"):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    base_filename = f"solar_report_{data['location'].lower().replace(' ', '_')}"
   
    filename = f"{base_filename}.{format_choice}"
    file_path = REPORTS_DIR / filename

    if format_choice == "txt":
        err = generate_txt_report(data, file_path)
    elif format_choice == "pdf":
        err = generate_pdf_report(data, file_path)
    else:
        return None, "Unsupported format"

    if err:
        return None, err

    return str(file_path), None
