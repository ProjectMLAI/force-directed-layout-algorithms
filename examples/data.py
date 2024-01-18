import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from poker_utils import load_poker, poker_distance, annotate_poker
import forcelayout as fl
import time
from codecarbon import EmissionsTracker
import tracemalloc
from ttkthemes import ThemedTk
import numpy as np

dataset_sizes = ['5', '10', '100', '200', '500', '1000', '2000', '3000', '5000', '10000', '20000', '50000', '100000', '200000', '250000', '500000', '1000000', '2500000']

algorithms = {
    'brute': fl.SpringForce,
    'chalmers96': fl.NeighbourSampling,
    'hybrid': fl.Hybrid,
    'pivot': fl.Pivot,
}

# Global variables for labels
global time_status_label, emissions_status_label, average_force_label, layout_stress_label, memory_usage_status_label

def run_visualization():
    tracemalloc.start()
    tracker = EmissionsTracker()
    tracker.start()

    try:
        # selected dataset size and algorithm
        selected_size = dataset_size_combobox.get()
        selected_algorithm = algorithm_combobox.get().lower()

        data_set_size = int(selected_size)  # Convert string to int to use the selected size
        
        poker_hands = load_poker(data_set_size)
        algorithm = algorithms[selected_algorithm]

        start = time.time()
        # Perform layout calculations without plotting
        spring_layout = fl.draw_spring_layout(
            dataset=poker_hands,
            distance=poker_distance,
            algorithm=algorithm,
            alpha=0.7,
            color_by=lambda d: d[10],
            annotate=annotate_poker,
            algorithm_highlights=True
        )
        total = time.time() - start

        # Update the status labels
        time_status_label.config(text=f'Layout time: {"%.2f" % total}s ({"%.1f" % (total / 60)} mins)')
        # Assuming your layout algorithm has these attributes
        average_force = np.mean(getattr(spring_layout, '_average_speeds', []))
        layout_stress = getattr(spring_layout, 'get_stress', lambda: 0)()
        average_force_label.config(text=f'Average Force: {average_force:.4f}')
        layout_stress_label.config(text=f'Layout Stress: {layout_stress:.4f}')
        
    except ValueError:
        status_label.config(text="Please enter a valid dataset size.")
    except KeyError:
        status_label.config(text="Please select a valid algorithm.")
    finally:
        emissions_data = tracker.stop()
        emissions = emissions_data if isinstance(emissions_data, float) else "Unknown"
        emissions_status_label.config(text=f'Total Emissions: {emissions:.4f} kg')

        tracemalloc.stop()
        current, peak = tracemalloc.get_traced_memory()
        memory_usage_status_label.config(text=f'Peak memory usage: {peak / 10**6:.2f} MB')

def setup_ui():
    global window, dataset_size_combobox, algorithm_combobox
    global time_status_label, emissions_status_label, average_force_label
    global layout_stress_label, memory_usage_status_label

    window = ThemedTk(theme="equilux")  # Make sure the 'equilux' theme is installed, or choose another dark theme
    window.title("Poker Hands Layout Visualization")
    window.geometry("800x600")

    # Load and set the background image
    bg_image = Image.open("plex.jpg")  # Ensure 'plex.jpg' is in the same directory as your script
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(window, width=800, height=600)
    canvas.grid(row=0, column=0, columnspan=3, rowspan=5, sticky='nsew')

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)


    canvas.create_image(0, 0, image=bg_photo, anchor="nw")


    style = ttk.Style(window)
    style.configure('TLabel', font=('Helvetica', 12), background='black', foreground='white')
    style.configure('TButton', font=('Helvetica', 12, 'bold'), background='black', foreground='white')
    style.configure('TCombobox', font=('Helvetica', 12), background='black', foreground='white')

  
    eco_metrics_heading = ttk.Label(window, text="EcoMetrics Pro", font=('Helvetica', 16, 'bold'), background='black', foreground='white')
    canvas.create_window(400, 25, window=eco_metrics_heading)


    dataset_size_label = ttk.Label(window, text="Select Dataset Size:", background='black', foreground='white')
    dataset_size_combobox = ttk.Combobox(window, values=dataset_sizes, width=20, state='readonly', font=('Helvetica', 12), background='black')
    canvas.create_window(400, 100, window=dataset_size_label)
    canvas.create_window(400, 130, window=dataset_size_combobox)

    algorithm_label = ttk.Label(window, text="Select Algorithm:", background='black', foreground='white')
    algorithm_combobox = ttk.Combobox(window, values=list(algorithms.keys()), width=20, state='readonly', font=('Helvetica', 12), background='black')
    canvas.create_window(400, 170, window=algorithm_label)
    canvas.create_window(400, 200, window=algorithm_combobox)

    run_button = ttk.Button(window, text="Run Visualization", command=run_visualization)
    canvas.create_window(400, 250, window=run_button)

    time_status_label = ttk.Label(window, text="Layout time: N/A", style='TLabel')
    emissions_status_label = ttk.Label(window, text="Emissions: N/A", style='TLabel')
    average_force_label = ttk.Label(window, text="Average Force: N/A", style='TLabel')
    layout_stress_label = ttk.Label(window, text="Layout Stress: N/A", style='TLabel')
    memory_usage_status_label = ttk.Label(window, text="Memory Usage: N/A", style='TLabel')

    
    label_width = 200  
    label_height = 25
    canvas.create_window(400, 450, window=time_status_label, width=label_width, height=label_height)
    canvas.create_window(400, 480, window=emissions_status_label, width=label_width, height=label_height)
    canvas.create_window(400, 510, window=average_force_label, width=label_width, height=label_height)
    canvas.create_window(400, 540, window=layout_stress_label, width=label_width, height=label_height)
    canvas.create_window(400, 570, window=memory_usage_status_label, width=label_width, height=label_height)

    
    canvas.bg_photo = bg_photo

    window.mainloop()


#setup_ui()
