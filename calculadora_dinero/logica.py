def calcular_total(entradas):
    """
    Calcula el total de dinero a partir de las entradas.

    Parámetros:
      entradas (dict): Diccionario donde la clave es el identificador y el valor es una tupla (valor, cantidad_str)

    Retorna:
      int: Total calculado.
    """
    total = 0
    for identificador, (valor, cantidad_str) in entradas.items():
        try:
            cantidad = int(cantidad_str.strip()) if cantidad_str.strip() else 0
        except ValueError:
            cantidad = 0
        total += valor * cantidad
    return total
