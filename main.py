import tkinter as tk
import logging
import os 

try:
    from calculadora_dinero.gui import CalculadoraDineroCOP
except ImportError as e:
    print(f"Error: No se pudo importar CalculadoraDineroCOP desde calculadora_dinero.gui: {e}")
    print("Asegúrate de que la estructura del proyecto es correcta y que estás ejecutando desde la raíz.")
    exit(1) 

LOG_FILE = 'app.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
LOG_LEVEL = logging.INFO 

def setup_logging():
    try:
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(
            filename=LOG_FILE,
            level=LOG_LEVEL,
            format=LOG_FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S' 
        )
        logging.info("Logging configurado exitosamente.")
    except Exception as e:
        print(f"Error configurando el logging: {e}")

def main():
    """Función principal que configura y ejecuta la aplicación."""

    setup_logging()
    logging.info("Iniciando la aplicación Calculadora de Dinero COP.")

    try:
        root = tk.Tk()
    except tk.TclError as e:
        logging.critical(f"No se pudo inicializar Tkinter (¿Falta display?): {e}")
        print(f"Error crítico: No se pudo inicializar Tkinter. ¿Estás en un entorno sin GUI? Detalles: {e}")
        exit(1)

    try:
        app = CalculadoraDineroCOP(root)
        logging.debug("Instancia de CalculadoraDineroCOP creada.")
    except Exception as e:
        logging.critical(f"No se pudo crear la instancia de la aplicación: {e}", exc_info=True)
        print(f"Error crítico al crear la aplicación: {e}")
        try:
            root.destroy() 
        except:
            pass
        exit(1)

    logging.info("Iniciando el bucle principal de Tkinter (mainloop).")
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Aplicación interrumpida por el usuario (Ctrl+C).")
        try:
            if root.winfo_exists():
                root.destroy()
        except:
            pass
    except Exception as e:
        logging.critical(f"Error inesperado en el mainloop: {e}", exc_info=True)
        try:
            if root.winfo_exists():
                root.destroy()
        except:
            pass
        exit(1)

    logging.info("La aplicación ha finalizado.")

if __name__ == "__main__":
    main()
