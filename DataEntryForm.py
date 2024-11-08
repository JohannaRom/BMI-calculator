import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

data_file = 'bmi_data.txt'

categories = ["Underweight", "Normal", "Overweight", "Obese"]

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        age = int(age_entry.get().strip())
        height = float(height_entry.get().strip())
        weight = float(weight_entry.get().strip())

        if not name:
            raise ValueError("Please enter a valid name.")
        if age <= 0:
            raise ValueError("Please enter a valid age.")
        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be positive values.")

        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(text=f"{name}, your BMI is {bmi:.2f}. Category: {category}")

        with open(data_file, 'a') as f:
            f.write(f"{name},{age},{height},{weight},{bmi},{category}\n")

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

def show_graph():
    counts = {cat: 0 for cat in categories}
    try:
        with open(data_file, 'r') as f:
            for line in f:
                _, _, _, _, _, category = line.strip().split(',')
                if category in counts:
                    counts[category] += 1
    except FileNotFoundError:
        messagebox.showerror("File Error", "No data file found. Please calculate a BMI first.")
        return

    values = [counts[cat] for cat in categories]
    if sum(values) == 0:
        messagebox.showinfo("No Data", "No BMI records available to display.")
        return

    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().grid(row=8, column=0, columnspan=2, pady=10)
    canvas.draw()

window = tk.Tk()
window.title("BMI Calculator")

tk.Label(window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = ttk.Entry(window)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(window, text="Age:").grid(row=1, column=0, padx=10, pady=5)
age_entry = ttk.Entry(window)
age_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(window, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
height_entry = ttk.Entry(window)
height_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(window, text="Weight (kg):").grid(row=3, column=0, padx=10, pady=5)
weight_entry = ttk.Entry(window)
weight_entry.grid(row=3, column=1, padx=10, pady=5)

calculate_button = ttk.Button(window, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

result_label = tk.Label(window, text="")
result_label.grid(row=5, column=0, columnspan=2, pady=5)

show_graph_button = ttk.Button(window, text="Show Graph", command=show_graph)
show_graph_button.grid(row=6, column=0, columnspan=2, pady=10)

window.mainloop()
