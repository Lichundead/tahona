import unittest
from calculadora_dinero import logica

class TestCalculadora(unittest.TestCase):
    def test_calcular_total(self):
        entradas = {
            "m50": (50, "2"),     # 50 * 2 = 100
            "m100": (100, "1"),    # 100 * 1 = 100
            "m200": (200, "0"),    # 200 * 0 = 0
        }
        total = logica.calcular_total(entradas)
        self.assertEqual(total, 200)  # 100 + 100 + 0 = 200

if __name__ == '__main__':
    unittest.main()
