import tkinter as tk
from tkinter import ttk
from functools import partial
import tkinter.messagebox as messagebox
import logging

from calculadora_dinero import logica

class CalculadoraDineroCOP:
    """
    Clase que representa la interfaz gráfica de la Calculadora de Dinero en COP.
    """
    def __init__(self, root):
        self.root = root
        self._job = None
        self.root.title("Calculadora de Dinero")
        self.root.geometry("400x600")
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        # Configuración de fuentes
        self.fuente_general = ('Arial', 12)
        self.fuente_titulo = ('Arial', 14, 'bold')
        self.fuente_resultado = ('Arial', 18, 'bold')
        
        # Denominaciones con identificador único: (valor, descripción, identificador)
        self.denominaciones = [
            (50, "Moneda de $50", "m50"),
            (100, "Moneda de $100", "m100"),
            (200, "Moneda de $200", "m200"),
            (500, "Moneda de $500", "m500"),
            (1000, "Billete/Moneda de $1.000", "b1k"),
            (2000, "Billete de $2.000", "b2k"),
            (5000, "Billete de $5.000", "b5k"),
            (10000, "Billete de $10.000", "b10k"),
            (20000, "Billete de $20.000", "b20k"),
            (50000, "Billete de $50.000", "b50k"),
            (100000, "Billete de $100.000", "b100k")
        ]
        
        self.entries = {}  # Diccionario para almacenar cada entrada (widget) asociado a su denominación.
        self.crear_interfaz()
        self.root.after(100, self.verificar_estado)  # Inicia el watchdog.

    def crear_interfaz(self):
        """Crea y posiciona los widgets en la interfaz."""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Encabezados de las columnas
        ttk.Label(main_frame, text="Denominación", font=self.fuente_titulo).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(main_frame, text="Cantidad", font=self.fuente_titulo).grid(row=0, column=1, padx=10, pady=5)
        
        # Creación dinámica de los renglones para cada denominación.
        for i, (valor, nombre, identificador) in enumerate(self.denominaciones, start=1):
            ttk.Label(main_frame, text=nombre, font=self.fuente_general).grid(row=i, column=0, sticky="w", padx=10, pady=8)
            
            entry = ttk.Entry(main_frame, width=12, font=self.fuente_general)
            entry.insert(0, "")  # Inicialmente vacía.
            entry.grid(row=i, column=1, padx=10, pady=8)
            
            # Asociamos el evento de teclado con un debounce para actualizar el total.
            entry.bind('<KeyRelease>', partial(self.actualizacion_segura, identificador))
            self.entries[identificador] = (valor, entry)
        
        # Etiqueta para mostrar el total calculado.
        self.resultado = ttk.Label(main_frame, 
                                   text="Total: $0 COP", 
                                   font=self.fuente_resultado,
                                   foreground="dark green")
        self.resultado.grid(row=len(self.denominaciones)+1, columnspan=2, pady=15)
    
    def actualizacion_segura(self, identificador, event=None):
        """
        Implementa un debounce para evitar cálculos excesivos.
        """
        try:
            if self._job is not None:
                self.root.after_cancel(self._job)
            self._job = self.root.after(300, self.actualizar_total)
        except Exception as e:
            logging.error("Error en actualizacion_segura: %s", e)

    def actualizar_total(self):
        """
        Extrae los datos de las entradas y utiliza la lógica para calcular el total.
        """
        try:
            # Se construye un diccionario con los valores actuales.
            entradas = {}
            for identificador, (valor, entry) in self.entries.items():
                entradas[identificador] = (valor, entry.get())
            total = logica.calcular_total(entradas)
            total_formateado = f"${total:,.0f} COP".replace(',', '.')
            self.resultado.config(text=f"TOTAL: {total_formateado}")
        except Exception as e:
            logging.error("Error en actualizar_total: %s", e)
            messagebox.showerror("Error", "Ocurrió un error al calcular el total.")
            self.resultado.config(text="Error en cálculo", foreground="red")
    
    def verificar_estado(self):
        """Sistema de watchdog para prevenir bloqueos."""
        try:
            if self.root.winfo_exists():
                self.root.after(1000, self.verificar_estado)
        except Exception:
            import sys
            sys.exit(1)

    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        self.root.destroy()
