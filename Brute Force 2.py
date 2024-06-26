import tkinter as tk
from tkinter import messagebox
from itertools import combinations
import time

# Define distances and travel_times matrices globally
distances = [
    [0, 6.7, 20.6, 15.4, 26.9, 27.4, 27.2, 24.3, 25.0, 24.7],
    [6.7, 0, 26.3, 10.2, 27.7, 28.1, 27.3, 25.5, 30.8, 27.3],
    [20.6, 26.3, 0, 28.2, 35.5, 35.9, 37.7, 33.3, 34.2, 37.7],
    [15.4, 10.2, 28.2, 0, 32.0, 32.5, 31.7, 29.9, 32.4, 31.7],
    [26.9, 27.7, 35.5, 32.0, 0, 0.45, 4.0, 7.2, 2.8, 2.4],
    [27.4, 28.1, 35.9, 32.5, 0.45, 0, 3.3, 6.8, 3.5, 3.1],
    [27.2, 27.3, 37.7, 31.7, 4.0, 3.3, 0, 10.7, 1.0, 0.021],
    [24.3, 25.5, 33.3, 29.9, 7.2, 6.8, 10.7, 0, 11.5, 10.9],
    [25.0, 30.8, 34.2, 32.4, 2.8, 3.5, 1.0, 11.5, 0, 2.3],
    [24.7, 27.3, 37.7, 31.7, 2.4, 3.1, 21, 10.9, 2.3, 0]
]

travel_times = [
    [0, 9, 24, 19, 28, 30, 32, 30, 24, 24],
    [9, 0, 27, 15, 29, 31, 31, 29, 31, 31],
    [24, 27, 0, 36, 38, 39, 40, 38, 39, 39],
    [19, 15, 36, 0, 32, 33, 30, 31, 32, 30],
    [28, 29, 38, 32, 0, 1, 8, 11, 7, 6],
    [30, 31, 39, 33, 1, 0, 7, 10, 9, 12],
    [32, 31, 40, 30, 8, 7, 0, 13, 2, 1],
    [30, 29, 38, 31, 11, 10, 13, 0, 12, 12],
    [24, 31, 39, 32, 7, 9, 2, 12, 0, 6],
    [24, 31, 39, 30, 6, 12, 1, 12, 6, 0]
]

def is_valid_combination(activities, budget, time_limit, distance_limit, min_rating):
    total_cost = 0
    total_time = 0
    total_distance = 0
    total_rating = 0
    n = len(activities)

    for i in range(n):
        activity = activities[i]
        total_cost += activity[5]
        total_time += activity[2]
        total_rating += activity[4]
        if i > 0:
            prev_activity = activities[i-1]
            total_time += travel_times[prev_activity[0]][activity[0]]
            total_distance += distances[prev_activity[0]][activity[0]]

    return (total_cost <= budget and total_time <= time_limit and
            total_distance <= distance_limit and
            total_rating / n >= min_rating)

def brute_force(activities, budget, time_limit, distance_limit, min_rating):
    best_combination = []
    best_rating = 0

    for r in range(1, len(activities) + 1):
        for combination in combinations(activities, r):
            if is_valid_combination(combination, budget, time_limit, distance_limit, min_rating):
                total_rating = sum(activity[4] for activity in combination)
                if total_rating > best_rating:
                    best_combination = combination
                    best_rating = total_rating

    total_cost = sum(activity[5] for activity in best_combination)
    total_time = 0
    total_distance = 0

    for i, activity in enumerate(best_combination):
        if i == 0:
            total_time += activity[2]
            total_distance += activity[3]
        else:
            prev_activity = best_combination[i - 1]
            total_time += travel_times[prev_activity[0]][activity[0]]
            total_distance += distances[prev_activity[0]][activity[0]]

    avg_rating = sum(activity[4] for activity in best_combination) / len(best_combination) if best_combination else 0

    return best_combination, avg_rating, total_cost, total_time, total_distance

def run_brute_force():
    try:
        budget = float(budget_entry.get())
        time_limit = float(time_entry.get()) * 60  # Convert hours to minutes
        distance_limit = float(distance_entry.get())
        min_rating = float(rating_entry.get())

        activities = [
            (0, "District 21, IOI City Mall", 9, 4.9, 4.2, 60),
            (1, "Taman Saujana Hijau Putrajaya", 12, 9.7, 4.7, 0),
            (2, "Bangi Wonderland", 25, 21.8, 4.1, 55),
            (3, "Taman Tasik Cyberjaya Lake Gardens", 22, 20, 4.5, 30),
            (4, "Berjaya Time Square Theme Park", 26, 24.4, 4.3, 57),
            (5, "Partybox360, Lalaport BBCC", 28, 23.1, 4.9, 38),
            (6, "VAR Live MyTown", 27, 23.2, 4.8, 104),
            (7, "Supreme Bowl, Midvalley", 26, 22.3, 3.4, 60),
            (8, "Xction Xtreme Park, Sunway Velocity", 26, 23.3, 3.5, 65),
            (9, "EnerG X Park, MyTown", 28, 23.3, 4.1, 63)
        ]

        start_time = time.time()
        best_activities, avg_rating, total_cost, total_time, total_distance = brute_force(activities, budget, time_limit, distance_limit, min_rating)
        end_time = time.time()

        if not best_activities:
            result = "No valid itinerary found. Please adjust your constraints."
        else:
            result = "Optimal Itinerary:\n\n"
            for i, activity in enumerate(best_activities):
                result += f"{activity[1]}\n"
                result += f"Duration: {activity[2]} min, Rating: {activity[4]}, Cost: ${activity[5]}\n"
                if i == 0:
                    result += f"Distance: {activity[3]:.2f} km\n"
                if i > 0:
                    prev_activity = best_activities[i-1]
                    travel_distance = distances[prev_activity[0]][activity[0]]
                    travel_time = travel_times[prev_activity[0]][activity[0]]
                    result += f"Travel from previous: Distance: {travel_distance:.2f} km, Time: {travel_time} min\n"
                result += "\n"

            result += f"\nTotal Cost: ${total_cost:.2f}"
            result += f"\nTotal Travel Time: {total_time} minutes"
            result += f"\nTotal Travelling Distance: {total_distance:.2f} km"
            result += f"\nAverage Rating: {avg_rating:.2f}"
            result += f"\nRuntime: {end_time - start_time:.4f} seconds"

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for all fields.")

window = tk.Tk()
window.title("Post Final Trip Planner")

tk.Label(window, text="Budget ($):").grid(row=0, column=0, sticky="e")
budget_entry = tk.Entry(window)
budget_entry.grid(row=0, column=1)

tk.Label(window, text="Time Limit (hours):").grid(row=1, column=0, sticky="e")
time_entry = tk.Entry(window)
time_entry.grid(row=1, column=1)

tk.Label(window, text="Distance Limit (km):").grid(row=2, column=0, sticky="e")
distance_entry = tk.Entry(window)
distance_entry.grid(row=2, column=1)

tk.Label(window, text="Minimum Rating:").grid(row=3, column=0, sticky="e")
rating_entry = tk.Entry(window)
rating_entry.grid(row=3, column=1)

run_button = tk.Button(window, text="Plan Trip", command=run_brute_force)
run_button.grid(row=4, column=0, columnspan=2)

result_text = tk.Text(window, height=25, width=70)
result_text.grid(row=5, column=0, columnspan=2)

window.mainloop()
