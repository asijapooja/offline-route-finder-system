# route_finder.py
import heapq

# Graph data (you can expand this easily)
graph = {
    "A": {"B": 5, "C": 2},
    "B": {"A": 5, "C": 1, "D": 3},
    "C": {"A": 2, "B": 1, "D": 7, "E": 4},
    "D": {"B": 3, "C": 7, "E": 2},
    "E": {"C": 4, "D": 2}
}

def shortest_path(start, end):
    """Find the shortest path using Dijkstra's algorithm."""
    if start not in graph or end not in graph:
        return None, float('inf')
    
    pq = [(0, start, [])]
    visited = set()

    while pq:
        (cost, node, path) = heapq.heappop(pq)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        if node == end:
            return path, cost
        for adj, weight in graph[node].items():
            if adj not in visited:
                heapq.heappush(pq, (cost + weight, adj, path))

    return None, float('inf')
# app.py
import tkinter as tk
from tkinter import messagebox
import route_finder  # backend logic

def find_route():
    start = entry_start.get().strip().upper()
    end = entry_end.get().strip().upper()

    if not start or not end:
        messagebox.showerror("Error", "Please enter both start and end points.")
        return

    path, cost = route_finder.shortest_path(start, end)

    if path is None:
        label_result.config(text="Route not found.")
    else:
        label_result.config(text=f"Path: {' → '.join(path)}\nTotal Distance: {cost} km")

def create_window():
    window = tk.Tk()
    window.title("Offline Route Finder")
    window.geometry("400x300")
    window.config(bg="#e6f2ff")

    tk.Label(window, text="Offline Route Finder", font=("Arial", 16, "bold"), bg="#e6f2ff").pack(pady=10)

    frame = tk.Frame(window, bg="#e6f2ff")
    frame.pack(pady=10)

    tk.Label(frame, text="Start:", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5)
    global entry_start
    entry_start = tk.Entry(frame)
    entry_start.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="End:", bg="#e6f2ff").grid(row=1, column=0, padx=5, pady=5)
    global entry_end
    entry_end = tk.Entry(frame)
    entry_end.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(window, text="Find Route", command=find_route, bg="#007acc", fg="white").pack(pady=10)

    global label_result
    label_result = tk.Label(window, text="", bg="#e6f2ff", font=("Arial", 12))
    label_result.pack(pady=10)

    window.mainloop()
