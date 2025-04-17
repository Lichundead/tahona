import tkinter as tk
from calculadora_dinero.gui import CalculadoraDineroCOP
import logging

def main():
    # Configuración global del logging
    logging.basicConfig(filename='app.log', level=logging.ERROR)
    
    # Creación de la ventana principal
    root = tk.Tk()
    app = CalculadoraDineroCOP(root)
    root.mainloop()

if __name__ == "__main__":
    main()
