import logging

def calcular_total(entradas):
    total = 0
    try:
        for identificador, (valor, cantidad_str) in entradas.items():
            try:
                cantidad = int(cantidad_str.strip()) if cantidad_str and cantidad_str.strip() else 0
                if cantidad < 0:
                    logging.warning(f"Cantidad negativa '{cantidad}' recibida para {identificador}. Tratada como 0.")
                    cantidad = 0
            except ValueError:
                logging.warning(f"Entrada inválida '{cantidad_str}' para {identificador}. Tratada como 0.")
                cantidad = 0
            except Exception as e:
                 logging.error(f"Error inesperado procesando cantidad para {identificador}: {e}")
                 cantidad = 0
            try:
                subtotal = valor * cantidad
                total += subtotal
            except TypeError as e:
                logging.error(f"Error de tipo al calcular subtotal para {identificador} (valor={valor}, cantidad={cantidad}): {e}")

    except AttributeError as e:
        logging.error(f"Error procesando el diccionario de entradas: {e}. Asegúrese que el formato es correcto.")
        raise TypeError("Formato de diccionario de entradas inválido.") from e
    except Exception as e:
        logging.error(f"Error inesperado en calcular_total: {e}")

    return total

