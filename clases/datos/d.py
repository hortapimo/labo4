import tkinter as tk
from tkinter import messagebox
import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class SerialPlotterApp:
    def __init__(self, master):
        self.master = master
        master.title("Plotter de Ingeniería - Miguel")
        
        # Configuración Serial
        self.puerto = "/dev/ttyUSB1" # Ajustar si es necesario
        self.baudios = 115200
        self.corriendo = False
        self.datos_s1, self.datos_s2, self.datos_s3 = [], [], []
        
        # Interfaz
        self.btn_start = tk.Button(master, text="INICIAR CAPTURA", command=self.start, bg="green", fg="white")
        self.btn_start.pack(pady=10)
        
        self.btn_stop = tk.Button(master, text="DETENER Y GUARDAR", command=self.stop, bg="red", fg="white", state=tk.DISABLED)
        self.btn_stop.pack(pady=10)

        # Gráfico
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.line1, = self.ax.plot([], [], label="S1")
        self.line2, = self.ax.plot([], [], label="S2")
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack()

    def read_serial(self):
        try:
            with serial.Serial(self.puerto, self.baudios, timeout=1) as ser, \
                 open("datos_experimento.csv", "w") as f:
                writer = csv.writer(f)
                while self.corriendo:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            val1, val2 = float(parts[0]), float(parts[1])
                            self.datos_s1.append(val1)
                            self.datos_s2.append(val2)
                            writer.writerow([val1, val2])
                            
                            # Actualizar gráfico cada 10 puntos para no tildarse
                            if len(self.datos_s1) % 10 == 0:
                                self.line1.set_data(range(len(self.datos_s1)), self.datos_s1)
                                self.line2.set_data(range(len(self.datos_s2)), self.datos_s2)
                                self.ax.relim(); self.ax.autoscale_view()
                                self.canvas.draw()
        except Exception as e:
            self.corriendo = False
            messagebox.showerror("Error", f"No se pudo abrir el puerto: {e}")

    def start(self):
        self.corriendo = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        threading.Thread(target=self.read_serial, daemon=True).start()

    def stop(self):
        self.corriendo = False
        messagebox.showinfo("Éxito", "Datos guardados en datos_experimento.csv")
        self.master.quit()

root = tk.Tk()
app = SerialPlotterApp(root)
root.mainloop()
