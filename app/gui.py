# app/gui.py
import tkinter as tk
from tkinter import messagebox
import requests
from datetime import date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Import from modules
from app.auth import register_user, login_user, logout_user
from app.calculator import calculate_savings
from app.input_handler import validate_numeric, save_user_input
from app.solar_api import get_solar_data
from app.report_generator import save_report
from app.stats import get_aggregated_stats
from app.design import StyledLabel, StyledEntry, StyledButton, StyledFrame, COLORS, StyledRadiobutton


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Solar Energy Tracker")
        self.root.geometry("450x600")
        self.root.configure(bg=COLORS["background"])
        self.current_user = None
        self.create_login_screen()

    # Inside App class
    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container frame (for centering)
        main_frame = tk.Frame(self.root, bg=COLORS["background"])
        main_frame.pack(fill="both", expand=True)

        # Simulated shadow effect using nested frames
        outer_frame = tk.Frame(main_frame, bg="#bbb", bd=0)
        outer_frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=460)

        inner_frame = tk.Frame(outer_frame, bg=COLORS["background"], padx=20, pady=20)
        inner_frame.pack(fill="both", expand=True)

        StyledLabel(inner_frame,text="Smart Solar Savings",font=("Segoe UI", 20, "bold"),fg=COLORS["success"], anchor="center").pack(pady=(15, 15), fill="x")

        StyledLabel(inner_frame, text="Username").pack(anchor="w")
        self.username_entry = StyledEntry(inner_frame)
        self.username_entry.pack(pady=10, ipadx=45, ipady=4)

        StyledLabel(inner_frame, text="Password").pack(anchor="w")
        self.password_entry = StyledEntry(inner_frame, show="*")
        self.password_entry.pack(pady=10, ipadx=45, ipady=4)

        StyledButton(inner_frame, text="Login", command=self.handle_login).pack(pady=10, fill="x")
        StyledButton(inner_frame, text="Register", command=self.create_register_screen).pack(pady=10, fill="x")

    def create_register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg=COLORS["background"])
        main_frame.pack(fill="both", expand=True)

        outer_frame = tk.Frame(main_frame, bg="#bbb", bd=0)
        outer_frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=420)

        inner_frame = tk.Frame(outer_frame, bg=COLORS["background"], padx=20, pady=20)
        inner_frame.pack(fill="both", expand=True)

        StyledLabel(inner_frame, text="Register", font=("Segoe UI", 18, "bold"),fg=COLORS["success"]).pack(pady=(0, 10))

        StyledLabel(inner_frame, text="Username").pack(anchor="w")
        self.reg_username = StyledEntry(inner_frame)
        self.reg_username.pack(pady=1, ipadx=45, ipady=4)

        StyledLabel(inner_frame, text="Password").pack(anchor="w")
        self.reg_password = StyledEntry(inner_frame, show="*")
        self.reg_password.pack(pady=1, ipadx=45, ipady=4)

        StyledLabel(inner_frame, text="User Type").pack(anchor="w")

        self.user_type = tk.StringVar(value="Non-solar")
        StyledRadiobutton(inner_frame, text="Solar", variable=self.user_type, value="Solar").pack(anchor="w")
        StyledRadiobutton(inner_frame, text="Non-solar", variable=self.user_type, value="Non-solar").pack(anchor="w")

        StyledButton(inner_frame, text="Register", command=self.handle_register).pack(pady=10, fill="x")
        StyledButton(inner_frame, text="Back to Login", command=self.create_login_screen).pack(pady=10, fill="x")

    def create_dashboard(self, user_type):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = StyledFrame(self.root)
        StyledLabel(frame, text=f"Dashboard - {user_type} User", font=("Segoe UI", 16, "bold")).pack(pady=20)
        StyledButton(frame, text="Enter Energy Usage", command=lambda: self.show_input_form(user_type)).pack(pady=10)
        StyledButton(frame, text="View Community Stats", command=self.show_stats_screen).pack(pady=10)
        StyledButton(frame, text="Logout", command=self.handle_logout).pack(pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = login_user(username, password)

        if user:
            self.current_user = user
            if user["type"] == "Solar":
                self.show_input_form("Solar")
            else:
                self.show_input_form("Non-solar")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def handle_register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        user_type = self.user_type.get()

        if register_user(username, password, user_type):
            messagebox.showinfo("Success", "Registration successful!")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists.")

    def handle_logout(self):
        if self.current_user:
            logout_user(self.current_user['username'])
            self.current_user = None
        self.create_login_screen()

    def show_input_form(self, user_type):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top Back Button (Fixed)
        top_frame = tk.Frame(self.root, bg=COLORS["background"])
        top_frame.pack(side="top", fill="x", padx=10, pady=5)
        StyledButton(top_frame, text="← Back to Dashboard",
                    command=lambda: self.create_dashboard(user_type)).pack(anchor="w")

        # Main Scrollable Frame
        main_frame = tk.Frame(self.root, bg=COLORS["background"])
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame, bg=COLORS["background"], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["background"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Input Form Inside Scrollable Frame
        frame = StyledFrame(scrollable_frame)
        frame.pack(padx=700, pady=10, fill="x")

        StyledLabel(frame, text="Energy Usage Input", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))

        entries = {}

        # Common Fields
        StyledLabel(frame, text="Location (City)").pack(anchor="w")
        entries['location'] = StyledEntry(frame)
        entries['location'].pack(pady=5, fill="x")

        StyledLabel(frame, text="Monthly Electricity Bill (Currency)").pack(anchor="w")
        entries['bill'] = StyledEntry(frame)
        entries['bill'].pack(pady=5, fill="x")

        if user_type == "Solar":
            StyledLabel(frame, text="Daily Solar Energy Production (kWh)").pack(anchor="w")
            entries['daily_solar'] = StyledEntry(frame)
            entries['daily_solar'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Solar Panel Wattage (Wp)").pack(anchor="w")
            entries['panel_wattage'] = StyledEntry(frame)
            entries['panel_wattage'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Panel Quantity").pack(anchor="w")
            entries['panel_quantity'] = StyledEntry(frame)
            entries['panel_quantity'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Charge Controller Voltage (V)").pack(anchor="w")
            entries['cc_voltage'] = StyledEntry(frame)
            entries['cc_voltage'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Charge Controller Current (A)").pack(anchor="w")
            entries['cc_current'] = StyledEntry(frame)
            entries['cc_current'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Battery Capacity (Ah)").pack(anchor="w")
            entries['battery_capacity'] = StyledEntry(frame)
            entries['battery_capacity'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Inverter Rating (VA)").pack(anchor="w")
            entries['inverter_rating'] = StyledEntry(frame)
            entries['inverter_rating'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Daily Energy Generated (Wh)").pack(anchor="w")
            entries['daily_energy_wh'] = StyledEntry(frame)
            entries['daily_energy_wh'].pack(pady=5, fill="x")

            def fetch_and_show_solar_data():
                location = entries['location'].get().strip()
                if not location:
                    messagebox.showwarning("Input Required", "Please enter a location first.")
                    return

                solar_data, error = get_solar_data(location)
                if error:
                    messagebox.showerror("API Error", error)
                    return

                self.show_solar_result_screen(solar_data)

            StyledButton(frame, text="Fetch Solar Data", command=fetch_and_show_solar_data).pack(pady=10, fill="x")

        else:
            StyledLabel(frame, text="Total Power Consumption of Devices (W)").pack(anchor="w")
            entries['total_power'] = StyledEntry(frame)
            entries['total_power'].pack(pady=5, fill="x")

            StyledLabel(frame, text="Average Daily Operational Time (hrs)").pack(anchor="w")
            entries['daily_hours'] = StyledEntry(frame)
            entries['daily_hours'].pack(pady=5, fill="x")

        def handle_proceed():
            try:
                data = {
                    'location': entries['location'].get().strip(),
                    'monthly_bill': validate_numeric(entries['bill'].get(), "Monthly Bill"),
                }

                if user_type == "Solar":
                    data.update({
                        'daily_solar_kwh': validate_numeric(entries['daily_solar'].get(), "Daily Solar"),
                        'panel_wattage': validate_numeric(entries['panel_wattage'].get(), "Solar Panel Wattage"),
                        'panel_quantity': int(validate_numeric(entries['panel_quantity'].get(), "Panel Quantity")),
                        'cc_voltage': validate_numeric(entries['cc_voltage'].get(), "CC Voltage"),
                        'cc_current': validate_numeric(entries['cc_current'].get(), "CC Current"),
                        'battery_capacity': validate_numeric(entries['battery_capacity'].get(), "Battery Capacity"),
                        'inverter_rating': validate_numeric(entries['inverter_rating'].get(), "Inverter Rating"),
                        'daily_energy_wh': validate_numeric(entries['daily_energy_wh'].get(), "Daily Energy WH")
                    })

                    daily_solar_kwh = data['daily_solar_kwh'] or (data['daily_energy_wh'] / 1000)
                    result = calculate_savings(daily_solar_kwh)
                    result.update({
                        "location": data['location'],
                        "monthly_bill": data['monthly_bill'],
                        "daily_solar_kwh": data['daily_solar_kwh']
                    })
                    full_save_data = {**data, **result}
                    if save_user_input(full_save_data, user_id=self.current_user['id']):
                        pass

                    self.show_result_screen(user_type, result)

                else:
                    data.update({
                        'total_power': validate_numeric(entries['total_power'].get(), "Total Power"),
                        'daily_hours': validate_numeric(entries['daily_hours'].get(), "Daily Hours")
                    })

                    total_power = data['total_power']
                    daily_hours = data['daily_hours']

                    GRID_ELECTRICITY_RATE_KWH = 5
                    CO2_PER_KWH_GRID = 0.5

                    daily_energy_consumption_kwh = (total_power / 1000) * daily_hours
                    monthly_saving_if_solar = daily_energy_consumption_kwh * 30 * GRID_ELECTRICITY_RATE_KWH
                    yearly_saving_if_solar = monthly_saving_if_solar * 12
                    co2_saved_yearly = daily_energy_consumption_kwh * CO2_PER_KWH_GRID * 30 * 12
                    trees_saved = round(co2_saved_yearly / 21.76, 2)

                    result = {
                        "daily_saving": daily_energy_consumption_kwh * GRID_ELECTRICITY_RATE_KWH,
                        "monthly_saving": monthly_saving_if_solar,
                        "yearly_saving": yearly_saving_if_solar,

                        "co2_daily": daily_energy_consumption_kwh * CO2_PER_KWH_GRID,
                        "co2_monthly": daily_energy_consumption_kwh * CO2_PER_KWH_GRID * 30,
                        "co2_yearly": co2_saved_yearly,

                        "trees_saved": trees_saved,
                        "badge": "None"
                    }

                    result.update({
                        "location": data['location'],
                        "monthly_bill": data['monthly_bill'],
                        "daily_solar_kwh": daily_energy_consumption_kwh
                    })

                    full_save_data = {**data, **result}
                    if save_user_input(full_save_data, user_id=self.current_user['id']):
                        pass

                    self.show_result_screen(user_type, result)

            except ValueError as e:
                messagebox.showerror("Input Error", str(e))

      
       

        StyledButton(frame, text="Proceed", command=handle_proceed).pack(pady=10, fill="x")
        

    def show_result_screen(self, user_type, result_data):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = StyledFrame(self.root)
        StyledLabel(frame, text="Savings Summary", font=("Segoe UI", 16, "bold")).pack(pady=10)

        if user_type == "Solar" and result_data:
            StyledLabel(frame, text=f"Estimated Daily Saving: ₹{result_data['daily_saving']:.2f}").pack()
            StyledLabel(frame, text=f"Estimated Monthly Saving: ₹{result_data['monthly_saving']:.2f}").pack()
            StyledLabel(frame, text=f"Estimated Yearly Saving: ₹{result_data['yearly_saving']:.2f}").pack()

            StyledLabel(frame, text="", font=("Arial", 12)).pack()

            StyledLabel(frame, text=f"CO₂ Saved Daily: {result_data['co2_daily']:.2f} kg").pack()
            StyledLabel(frame, text=f"CO₂ Saved Monthly: {result_data['co2_monthly']:.2f} kg").pack()
            StyledLabel(frame, text=f"CO₂ Saved Yearly: {result_data['co2_yearly']:.2f} kg").pack()

            StyledLabel(frame, text="", font=("Arial", 12)).pack()
            StyledLabel(frame, text="🌿 Environmental Impact", font=("Segoe UI", 14, "bold")).pack()
            StyledLabel(frame, text=f"Trees Equivalent Saved: {result_data['trees_saved']:.2f} trees/year").pack()

            recommended_usage = round(result_data['daily_saving'] / 5, 2)
            StyledLabel(frame, text=f"Recommended Daily Usage: {recommended_usage} kWh").pack()

            StyledLabel(frame, text="", font=("Arial", 12)).pack()
            StyledLabel(frame, text="💡 Recommendation:", font=("Segoe UI", 12, "bold")).pack()
            StyledLabel(frame, text="Use high-power appliances between 10 AM – 4 PM for maximum efficiency.").pack()

            if result_data["badge"] != "None":
                StyledLabel(frame, text="", font=("Arial", 12)).pack()
                StyledLabel(frame, text="🏆 Your Badge:", font=("Segoe UI", 14, "bold")).pack()
                StyledLabel(frame, text=result_data["badge"], font=("Segoe UI", 14, "bold"), fg="green").pack()

            def on_format_selected(format_choice):
                full_report_data = {
                    "location": result_data.get("location", "Unknown"),
                    "monthly_bill": result_data["monthly_bill"],
                    "daily_solar_kwh": result_data["daily_solar_kwh"],
                    "daily_saving": result_data["daily_saving"],
                    "monthly_saving": result_data["monthly_saving"],
                    "yearly_saving": result_data["yearly_saving"],
                    "co2_yearly": result_data["co2_yearly"],
                    "trees_saved": result_data["trees_saved"],
                    "badge": result_data.get("badge", "None")
                }
                file_path, error = save_report(full_report_data, format_choice)
                if error:
                    messagebox.showerror("Report Error", error)
                else:
                    messagebox.showinfo("Success", f"{format_choice.upper()} report saved:\n{file_path}")

            button_frame = tk.Frame(self.root, bg=COLORS["background"])
            button_frame.pack(pady=10)
            StyledButton(button_frame, text="Save as PDF", width=12, command=lambda: on_format_selected("pdf")).pack(side=tk.LEFT, padx=5)
            StyledButton(button_frame, text="Save as TXT", width=12, command=lambda: on_format_selected("txt")).pack(side=tk.LEFT, padx=5)

        else:
            StyledLabel(frame, text="You're not using solar energy yet.", font=("Segoe UI", 12, "bold")).pack()
            StyledLabel(frame, text="Here's what you could save:", font=("Segoe UI", 12)).pack(pady=(0, 10))

            StyledLabel(frame, text=f"Monthly Electricity Cost: ₹{result_data['monthly_bill']:.2f}").pack()
            StyledLabel(frame, text=f"Potential Daily Saving: ₹{result_data['daily_saving']:.2f}").pack()
            StyledLabel(frame, text=f"Potential Monthly Saving: ₹{result_data['monthly_saving']:.2f}").pack()
            StyledLabel(frame, text=f"Potential Yearly Saving: ₹{result_data['yearly_saving']:.2f}").pack()

            StyledLabel(frame, text="", font=("Arial", 12)).pack()
            StyledLabel(frame, text=f"CO₂ Reduction Potential (Yearly): {result_data['co2_yearly']:.2f} kg").pack()
            StyledLabel(frame, text=f"Trees Equivalent Saved: {result_data['trees_saved']:.2f} trees/year").pack()

            StyledLabel(frame, text="", font=("Arial", 12)).pack()
            StyledLabel(frame, text="🌱 Motivation:", font=("Segoe UI", 12, "bold")).pack()
            StyledLabel(frame, text="Switching to solar can help reduce costs and protect the environment.",
                        font=("Segoe UI", 12)).pack()
            StyledLabel(frame, text="Consider going green today!", font=("Segoe UI", 12)).pack()

            def on_format_selected(format_choice):
                full_report_data = {
                    "location": result_data.get("location", "Unknown"),
                    "monthly_bill": result_data["monthly_bill"],
                    "daily_solar_kwh": result_data["daily_solar_kwh"],
                    "daily_saving": result_data["daily_saving"],
                    "monthly_saving": result_data["monthly_saving"],
                    "yearly_saving": result_data["yearly_saving"],
                    "co2_yearly": result_data["co2_yearly"],
                    "trees_saved": result_data["trees_saved"],
                    "badge": "None"
                }
                file_path, error = save_report(full_report_data, format_choice)
                if error:
                    messagebox.showerror("Report Error", error)
                else:
                    messagebox.showinfo("Success", f"{format_choice.upper()} report saved successfully:\n{file_path}")

            button_frame = tk.Frame(self.root, bg=COLORS["background"])
            button_frame.pack(pady=10)
            StyledButton(button_frame, text="Save as PDF", width=12, command=lambda: on_format_selected("pdf")).pack(
                side=tk.LEFT, padx=5)
            StyledButton(button_frame, text="Save as TXT", width=12, command=lambda: on_format_selected("txt")).pack(
                side=tk.LEFT, padx=5)

        StyledButton(self.root, text="Back to Dashboard",
                     command=lambda: self.create_dashboard(user_type)).pack(pady=10)

    def show_solar_result_screen(self, solar_data):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = StyledFrame(self.root)
        StyledLabel(frame, text="Solar Energy Info", font=("Segoe UI", 16, "bold")).pack(pady=10)
        StyledLabel(frame, text=f"Location: {solar_data['location']}").pack()
        StyledLabel(frame, text=f"Daily Solar Energy Potential: {solar_data['daily_solar_kwh']} kWh/m²/day").pack()
        StyledLabel(frame, text=f"Recommended Daily Usage: {solar_data['recommended_usage_kwh']} kWh").pack()
        StyledButton(self.root, text="Back to Input Form", command=lambda: self.show_input_form("Solar")).pack(pady=10)

    def show_stats_screen(self):
        stats = get_aggregated_stats()

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = StyledFrame(self.root)
        StyledLabel(frame, text="📊 Comparative Statistics", font=("Segoe UI", 16, "bold")).pack(pady=10)

        fig, axes = plt.subplots(1, 3, figsize=(8, 4), dpi=75)

        labels = ['Solar', 'Non-Solar']
        monthly_savings = [stats["Solar"]["avg_monthly_saving"], stats["Non-solar"].get("avg_monthly_saving", 0)]
        co2_savings = [stats["Solar"]["avg_co2_saved"], stats["Non-solar"].get("avg_co2_saved", 0)]
        trees_saved = [stats["Solar"]["avg_trees_saved"], stats["Non-solar"].get("avg_trees_saved", 0)]

        axes[0].bar(labels, monthly_savings,
                    color=['green' if monthly_savings[0] > monthly_savings[1] else 'gray', 'orange'])
        axes[0].set_title("Avg Monthly Savings (₹)")
        axes[0].set_ylabel("₹")

        axes[1].bar(labels, co2_savings,
                    color=['green' if co2_savings[0] > 0 else 'gray', 'gray'])
        axes[1].set_title("CO₂ Saved Yearly (kg)")

        axes[2].bar(labels, trees_saved,
                    color=['green' if trees_saved[0] > 0 else 'gray', 'gray'])
        axes[2].set_title("Trees Equivalent Saved")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        summary_text = (
            f"Based on community data:\n\n"
            f"Solar users save an average of ₹{stats['Solar']['avg_monthly_saving']:.2f}/month.\n"
            f"They also reduce {stats['Solar']['avg_co2_saved']:.2f} kg CO₂/year,\n"
            f"which equals planting {stats['Solar']['avg_trees_saved']:.2f} trees!\n\n"
            f"Non-solar users could save ₹{stats['Non-solar'].get('avg_monthly_saving', 0):.2f}/month.\n"
            f"Switching to solar helps both your wallet and the planet."
        )

        tk.Label(self.root, text=summary_text, justify=tk.LEFT, bg=COLORS["background"], fg=COLORS["text"]).pack(pady=10)

        StyledButton(self.root, text="Back to Dashboard", command=lambda: self.create_dashboard("Solar")).pack(pady=10)

    def run(self):
        self.root.mainloop()