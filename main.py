import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, messagebox
from interpolator import Interpolator


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.x_interp = None
        self.y_interp = None
        self.canvas = None
        self.ax = None
        self.fig = None
        self.method_var = None
        self.title("UInterpolation")
        self.geometry("800x600")

        # Create and set up the main container frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create and set up the menu bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Create and set up the "File" menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.browse)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Create and set up the "Help" menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # Create and set up the "Interpolation Method" menu
        self.interpolation_method_menu = tk.Menu(self.menubar, tearoff=0)
        self.interpolation_method_menu.add_command(label="Linear", command=self.set_interpolation_method_linear)
        self.interpolation_method_menu.add_command(label="Lagrange", command=self.set_interpolation_method_lagrange)
        self.interpolation_method_menu.add_command(label="Akima spline",
                                                   command=self.set_interpolation_method_akima_spline)
        self.interpolation_method_menu.add_command(label="Cubic spline", command=self.set_interpolation_method_spline)
        self.interpolation_method_menu.add_command(label="PCHIP",
                                                   command=self.set_interpolation_method_pchip)
        self.menubar.add_cascade(label="Interpolation Method", menu=self.interpolation_method_menu)

        # Create and set up the new input frame
        self.input_frame = tk.Frame(self, width=200)
        self.input_frame.pack(fill=tk.X, side=tk.TOP, padx=10)

        # Create and set up the input hints container
        self.input_hints_container = tk.Frame(self.input_frame)
        self.input_hints_container.pack(fill=tk.X, side=tk.LEFT, padx=10)

        # Create and set up the "Browse" button
        self.browse_button = tk.Button(self.input_hints_container, text="Browse", command=self.browse)
        self.browse_button.pack(side=tk.BOTTOM)

        # Create and set up the input hint label
        self.input_hint = tk.Label(self.input_hints_container,
                                   text="Enter data in the format: x,y\n(one point per line)\n\n\n...or import data from file\n")
        self.input_hint.pack(side=tk.TOP)

        # Create and set up the container for items on the right side
        self.right_container = tk.Frame(self.input_frame)
        self.right_container.pack(fill=tk.Y, side=tk.RIGHT, padx=10, ipady=20)

        # Create and set up the input text widget
        self.input_text = tk.Text(self.input_frame, width=20, height=10)
        self.input_text.pack(side=tk.LEFT, padx=10)

        # Create and set up the interpolation method selection widgets
        self.method_label = tk.Label(self.right_container, text="Select interpolation method:")
        self.method_label.pack(side=tk.TOP)
        self.method_var = tk.StringVar()
        self.method_var.set("Linear")
        self.method_dropdown = tk.OptionMenu(self.right_container, self.method_var, "Linear", "Lagrange",
                                             "Akima spline", "Cubic spline",
                                             "PCHIP")
        self.method_dropdown.pack(side=tk.TOP)

        # Create and set up the "Plot" button
        self.plot_button = tk.Button(self.right_container, text="Plot", command=self.plot)
        self.plot_button.pack(side=tk.BOTTOM, pady=20, padx=10)

        # Create a container frame for the plot
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def set_interpolation_method_linear(self):
        self.method_var.set("Linear")

    def set_interpolation_method_lagrange(self):
        self.method_var.set("Lagrange")

    def set_interpolation_method_akima_spline(self):
        self.method_var.set("Akima spline")

    def set_interpolation_method_spline(self):
        self.method_var.set("Cubic spline")

    def set_interpolation_method_pchip(self):
        self.method_var.set("PCHIP")

    def browse(self):
        # Open a file dialog to allow the user to select a file
        filepath = filedialog.askopenfilename()

        # Read the data from the file and display it in the input field
        with open(filepath, "r") as f:
            data = f.read()
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", data)

    def save(self):
        # Open a file dialog to allow the user to select a file
        filepath = filedialog.asksaveasfilename()

        # Write the plot to the file
        if filepath:
            # Save the figure to the selected filepath
            self.fig.savefig(filepath, bbox_inches='tight')

    def about(self):
        # Open a message box with information about the application
        tk.messagebox.showinfo("About", "This is an application for visualization of interpolation methods.")

    def plot(self):
        # Parse the input data and create x and y lists
        data = self.input_text.get("1.0", tk.END).strip().split("\n")
        x = [float(point.split(",")[0]) for point in data]
        y = [float(point.split(",")[1]) for point in data]

        # Create a new figure and axis
        self.fig, self.ax = plt.subplots()

        # Perform the interpolation using the selected method
        if self.method_var.get() == "Linear":
            self.x_interp = x
            self.y_interp = y
        elif self.method_var.get() == "Lagrange":
            self.x_interp = np.linspace(min(x), max(x), num=100)
            self.y_interp = Interpolator.lagrange_interpolation(x, y, self.x_interp)
        elif self.method_var.get() == "Akima spline":
            self.x_interp = np.linspace(min(x), max(x), num=100)
            self.y_interp = Interpolator.akima_spline_interpolation(x, y, self.x_interp)
            pass
        elif self.method_var.get() == "Cubic spline":
            self.x_interp = np.linspace(min(x), max(x), num=100)
            self.y_interp = Interpolator.cubic_spline_interpolation(x, y, self.x_interp)
        elif self.method_var.get() == "PCHIP":
            self.x_interp = np.linspace(min(x), max(x), num=100)
            self.y_interp = Interpolator.pchip_spline_interpolation(x, y, self.x_interp)

        if self.y_interp is not None:
            # Plot the data points
            self.ax.scatter(self.x_interp, self.y_interp)

            # Plot the interpolation curve
            self.ax.plot(self.x_interp, self.y_interp)

        # Plot the data points
        self.ax.scatter(x, y)

        # Add labels and title
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("Interpolation Result")

        # Create a Tkinter-compatible canvas for the plot
        if self.canvas is not None:
            self.plot_frame.destroy()
            self.plot_frame = tk.Frame(self)
            self.plot_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
