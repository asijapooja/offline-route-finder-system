import tkinter as tk
from tkinter import messagebox, ttk

# ================= BACKEND - GRAPH + DIJKSTRA ================= #
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, city1, city2, distance):
        if city1 not in self.graph:
            self.graph[city1] = {}
        if city2 not in self.graph:
            self.graph[city2] = {}
        self.graph[city1][city2] = distance
        self.graph[city2][city1] = distance  # undirected graph

    def dijkstra(self, start, end):
        import heapq
        queue = [(0, start, [])]
        seen = set()

        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node in seen:
                continue
            path = path + [node]
            seen.add(node)

            if node == end:
                return (cost, path)

            for adj, weight in self.graph.get(node, {}).items():
                if adj not in seen:
                    heapq.heappush(queue, (cost + weight, adj, path))

        return float("inf"), []

# ================= FRONTEND - TKINTER UI ================= #
class RouteFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Route Finder")
        self.root.geometry("600x500")
        self.root.config(bg="#E8F0F2")

        self.graph = Graph()

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Offline Route Finder", font=("Arial", 18, "bold"), bg="#E8F0F2", fg="#0B3D91")
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#E8F0F2")
        frame.pack(pady=10)

        # Input for city and distance
        tk.Label(frame, text="City 1:", bg="#E8F0F2").grid(row=0, column=0, padx=5, pady=5)
        self.city1_entry = tk.Entry(frame)
        self.city1_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="City 2:", bg="#E8F0F2").grid(row=1, column=0, padx=5, pady=5)
        self.city2_entry = tk.Entry(frame)
        self.city2_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Distance (km):", bg="#E8F0F2").grid(row=2, column=0, padx=5, pady=5)
        self.distance_entry = tk.Entry(frame)
        self.distance_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Route", command=self.add_route, bg="#0B3D91", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)

        # Route finding section
        find_frame = tk.Frame(self.root, bg="#E8F0F2")
        find_frame.pack(pady=10)

        tk.Label(find_frame, text="Start City:", bg="#E8F0F2").grid(row=0, column=0, padx=5, pady=5)
        self.start_entry = tk.Entry(find_frame)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(find_frame, text="Destination City:", bg="#E8F0F2").grid(row=1, column=0, padx=5, pady=5)
        self.end_entry = tk.Entry(find_frame)
        self.end_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(find_frame, text="Find Shortest Route", command=self.find_route, bg="#1A73E8", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

        # Output display
        self.output_text = tk.Text(self.root, height=8, width=60, bg="white", fg="black", wrap="word")
        self.output_text.pack(pady=10)

    def add_route(self):
        city1 = self.city1_entry.get().strip().capitalize()
        city2 = self.city2_entry.get().strip().capitalize()
        distance = self.distance_entry.get().strip()

        if not city1 or not city2 or not distance.isdigit():
            messagebox.showerror("Error", "Please enter valid city names and numeric distance.")
            return

        distance = int(distance)
        self.graph.add_edge(city1, city2, distance)
        messagebox.showinfo("Success", f"Route added: {city1} ↔ {city2} ({distance} km)")
        self.city1_entry.delete(0, tk.END)
        self.city2_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)

    def find_route(self):
        start = self.start_entry.get().strip().capitalize()
        end = self.end_entry.get().strip().capitalize()

        if start not in self.graph.graph or end not in self.graph.graph:
            messagebox.showerror("Error", "Both cities must be added before finding a route.")
            return

        distance, path = self.graph.dijkstra(start, end)
        if path:
            result = f"Shortest route from {start} to {end}:\n{' → '.join(path)}\n\nTotal Distance: {distance} km"
        else:
            result = f"No route found between {start} and {end}."

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)

# ================= MAIN ================= #
if __name__ == "__main__":
    root = tk.Tk()
    app = RouteFinderApp(root)
    root.mainloop()

