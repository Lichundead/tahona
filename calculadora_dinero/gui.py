import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
import logging

try:
    from . import logica
except ImportError:
    import logica

class CalculadoraDineroCOP:

    DEBOUNCE_MS = 300  
    WATCHDOG_INTERVAL_MS = 1000 

    # Fuentes
    FUENTE_GENERAL = ('Arial', 12)
    FUENTE_TITULO = ('Arial', 14, 'bold')
    FUENTE_RESULTADO = ('Arial', 18, 'bold')

    # Colores
    COLOR_RESULTADO_OK = "dark green"
    COLOR_RESULTADO_ERROR = "red"

    # Textos
    TEXTO_TOTAL_FORMAT = "TOTAL: ${:,.0f} COP" 
    TEXTO_TOTAL_DEFAULT = "TOTAL: $0 COP"
    TEXTO_TOTAL_ERROR = "Error en cálculo"

    DENOMINACIONES = [
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

    def __init__(self, root):
        self.root = root
        self._job_id_debounce = None 
        self.root.title("Calculadora de Dinero COP")
        self.root.geometry("400x600") 
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing) 

        self.entries = {}  

        self._validate_cmd = self.root.register(self._validate_input)

        self.crear_interfaz()
        self.root.after(self.WATCHDOG_INTERVAL_MS, self.verificar_estado)

    def _validate_input(self, P):
        return P == "" or P.isdigit()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(len(self.DENOMINACIONES) + 1, weight=1) 
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)


        ttk.Label(main_frame, text="Denominación", font=self.FUENTE_TITULO).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(main_frame, text="Cantidad", font=self.FUENTE_TITULO).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        for i, (valor, nombre, identificador) in enumerate(self.DENOMINACIONES, start=1):
            ttk.Label(main_frame, text=nombre, font=self.FUENTE_GENERAL).grid(row=i, column=0, sticky="w", padx=10, pady=8)

            entry = ttk.Entry(
                main_frame,
                width=12,
                font=self.FUENTE_GENERAL,
                validate='key', 
                validatecommand=(self._validate_cmd, '%P') 
            )
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew") 

            entry.bind('<KeyRelease>', partial(self.programar_actualizacion, identificador))

            self.entries[identificador] = (valor, entry)

        self.resultado_label = ttk.Label(
            main_frame,
            text=self.TEXTO_TOTAL_DEFAULT,
            font=self.FUENTE_RESULTADO,
            foreground=self.COLOR_RESULTADO_OK
        )
        self.resultado_label.grid(
            row=len(self.DENOMINACIONES) + 1,
            column=0,
            columnspan=2, 
            pady=20 
        )

    def programar_actualizacion(self, identificador_origen, event=None):
        try:
            if self._job_id_debounce is not None:
                self.root.after_cancel(self._job_id_debounce)

            self._job_id_debounce = self.root.after(self.DEBOUNCE_MS, self.actualizar_total)
        except Exception as e:
            logging.error("Error en programar_actualizacion: %s", e)

    def actualizar_total(self):
        self._job_id_debounce = None 
        try:
            entradas_actuales = {}
            for identificador, (valor, entry_widget) in self.entries.items():
                entradas_actuales[identificador] = (valor, entry_widget.get())


            total = logica.calcular_total(entradas_actuales)


            total_formateado = self.TEXTO_TOTAL_FORMAT.format(total).replace(',', '.')


            self.resultado_label.config(text=total_formateado, foreground=self.COLOR_RESULTADO_OK)

        except Exception as e:
            logging.error("Error en actualizar_total: %s", e)
            messagebox.showerror("Error de Cálculo", f"Ocurrió un error al calcular el total:\n{e}")
            self.resultado_label.config(text=self.TEXTO_TOTAL_ERROR, foreground=self.COLOR_RESULTADO_ERROR)

    def verificar_estado(self):
        try:
            if self.root.winfo_exists():
                self.root.after(self.WATCHDOG_INTERVAL_MS, self.verificar_estado)
        except Exception as e:
            logging.critical(f"Error fatal en watchdog, saliendo: {e}")
            import sys
            sys.exit(1) 

    def on_closing(self):
        logging.info("Cerrando la aplicación.")
        if self._job_id_debounce is not None:
             try:
                 self.root.after_cancel(self._job_id_debounce)
             except Exception:
                 pass 
        self.root.destroy()

