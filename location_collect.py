import tkinter as tk
from tkinter import ttk
import tkintermapview
import csv 
from datetime import date, datetime
import os
#date_var = tk.StringVar(value=str(date.today()))

clicked_coords = []
current_marker = None        
#saved_data = []
csv_markers = []
csv_markers_visible = False


def add_location(coords):

    global current_marker
    lat, lon = coords
    today = str(date.today())
    now = datetime.now().strftime("%H:%M:%S")
 
    # Record
    clicked_coords.append((lat, lon, today, now)) # here
 
    # Update marker
    if current_marker:
        current_marker.delete()
    current_marker = map_widget.set_marker(
        lat, lon,
        text=f"{lat:.6f}, {lon:.6f}",
        marker_color_circle="#3b82f6",
        marker_color_outside="#1d4ed8",
    )
 
    # Update readout labels
    lat_var.set(f"{lat:.8f}")
    lon_var.set(f"{lon:.8f}")
    count_var.set(str(len(clicked_coords))) 
    date_var.set(today)
    time_var.set(now)
 
    # Append to the history list
    history_list.insert(0, f"{len(clicked_coords):>3}.  {lat:.6f},  {lon:.6f} {today} {now}") #add here
 
def save_to_csv():
    file = "locations.csv"
    start_count = 1

    # If file exists, read the last ID to continue counting from
    if os.path.exists(file):
        with open(file, "r", newline="") as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:  # more than just the header
                start_count = int(rows[-1][0]) + 1

    # Append new rows (or create file if it doesn't exist)
    write_header = not os.path.exists(file)
    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Count", "Latitude", "Longitude", "Date", "Time"])
        for i, (lat, lon, today, now) in enumerate(clicked_coords, start_count):
            writer.writerow([i, lat, lon, today, now])

    save_btn.config(text="Saved!")
    root.after(1500, lambda: save_btn.config(text="Add to CSV"))
    
def show_all_from_csv():
    global csv_markers_visible

    if csv_markers_visible:
        for m in csv_markers:
            m.delete()
        csv_markers.clear()
        show_all_btn.config(text="Show all location history")
        csv_markers_visible = False
        return

    file = "locations.csv"
    if not os.path.exists(file):
        return

    for m in csv_markers:
        m.delete()
    csv_markers.clear()

    with open(file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat, lon = float(row["Latitude"]), float(row["Longitude"])
            m = map_widget.set_marker(lat, lon,
                marker_color_circle="#22c55e",
                marker_color_outside="#15803d",
                text="")
            csv_markers.append(m)

    show_all_btn.config(text="Hide location history")
    csv_markers_visible = True

def clear_all(): 

    global current_marker
    if current_marker:
        current_marker.delete()
        current_marker = None
    clicked_coords.clear()
    lat_var.set("-")
    lon_var.set("-")
    count_var.set("0") 
    time_var.set("-")
    history_list.delete(0, tk.END)
 
def clear_selected():
    selected = history_list.curselection()
    if not selected:
        return
    
    for i in reversed(selected):
        history_list.delete(i)
        
        coord_index = len(clicked_coords) -1 -i
        del clicked_coords[coord_index]
    

root = tk.Tk()
root.title("Map Click Geocoordinates")
root.geometry("980x680")
root.minsize(700, 500)
root.configure(bg="#0f172a")
 

left = tk.Frame(root, bg="#1e293b", width=240)
left.pack(side=tk.LEFT, fill=tk.Y, padx=(12, 0), pady=12)
left.pack_propagate(False)
 
right = tk.Frame(root, bg="#0f172a")
right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)
 

tk.Label(left, text="RECORD DATA", font=("Courier", 13, "bold"),
         bg="#1e293b", fg="#3b82f6").pack(pady=(18, 2))
tk.Label(left, text="geocoordinate tool", font=("Courier", 9),
         bg="#1e293b", fg="#64748b").pack(pady=(0, 18))


ttk.Separator(left, orient="horizontal").pack(fill=tk.X, padx=16, pady=4)
 
def field(parent, label, var):
    row = tk.Frame(parent, bg="#1e293b")
    row.pack(fill=tk.X, padx=16, pady=4)
    tk.Label(row, text=label, font=("Courier", 9), bg="#1e293b",
             fg="#94a3b8", anchor="w").pack(fill=tk.X)
    tk.Label(row, textvariable=var, font=("Courier", 12, "bold"),
             bg="#0f172a", fg="#e2e8f0", anchor="w",
             relief="flat", padx=8, pady=4).pack(fill=tk.X)

lat_var   = tk.StringVar(value="-")
lon_var   = tk.StringVar(value="-")
count_var = tk.StringVar(value="0") 
date_var = tk.StringVar(value="-")
time_var = tk.StringVar(value="-")
 
field(left, "LATITUDE",  lat_var)
field(left, "LONGITUDE", lon_var)
#field(left, "ID",    count_var) #
field(left, "DATE",      date_var)
field(left, "TIME", time_var)
#field(left, "DATE", date_var)
 
ttk.Separator(left, orient="horizontal").pack(fill=tk.X, padx=16, pady=12)
 
# Buttons
btn_style = {"font": ("Courier", 10, "bold"), "relief": "flat",
             "cursor": "hand2", "pady": 7}
 
save_btn = tk.Button(left, text="Save CSV", bg="#16a34a", fg="white",
                     activebackground="#15803d", activeforeground="white",
                     command=save_to_csv, **btn_style)
save_btn.pack(fill=tk.X, padx=16, pady=(0, 6))


tk.Button(left, text="Clear all", bg="#334155", fg="#cbd5e1",
          activebackground="#475569", activeforeground="white",
          command=clear_all, **btn_style).pack(fill=tk.X, padx=16)

tk.Button(left, text="Clear selected", bg="#7f1d1d", fg="#fca5a5",
          activebackground="#991b1b", activeforeground="white",
          command=clear_selected, **btn_style).pack(fill=tk.X, padx=16, pady=(6, 0))

 
ttk.Separator(left, orient="horizontal").pack(fill=tk.X, padx=16, pady=12)
 
tk.Label(left, text="INPUTS", font=("Courier", 9), bg="#1e293b",
         fg="#64748b", anchor="w").pack(fill=tk.X, padx=16)
 
history_frame = tk.Frame(left, bg="#1e293b")
history_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(4, 16))
 
scrollbar = tk.Scrollbar(history_frame, bg="#334155")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
 
history_list = tk.Listbox(history_frame, font=("Courier", 8),
                           bg="#0f172a", fg="#94a3b8",
                           selectbackground="#3b82f6", selectforeground="white",
                           relief="flat", bd=0,
                           yscrollcommand=scrollbar.set)
history_list.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=history_list.yview)
 

tk.Label(right, text="Click anywhere on the map",
         font=("Courier", 9), bg="#0f172a", fg="#475569").pack(anchor="w")
 
map_widget = tkintermapview.TkinterMapView(right, corner_radius=8)
map_widget.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
 
# Map view
map_widget.set_position(-27.475919124999148, 153.0096159909169) # Edit location here
map_widget.set_zoom(15)

map_widget.add_left_click_map_command(add_location)

show_all_btn = tk.Button(right, text="Show all location history", bg="#14532d", fg="#86efac",
          activebackground="#15803d", activeforeground="white",
          font=("Courier", 10, "bold"), relief="flat", cursor="hand2",
          command=show_all_from_csv)
show_all_btn.pack(fill=tk.X, pady=(6, 0))

root.mainloop()
 
# Print session summary after window closes
if clicked_coords:
    print("\n Session coordinates ")
    for i, (lat, lon, today, now) in enumerate(clicked_coords, 1): #add here
        print(f"  {i:>3}.  lat={lat:.8f}   lon={lon:.8f}   date={today} {now}")
    print(f"\n  Total points: {len(clicked_coords)}")
    
