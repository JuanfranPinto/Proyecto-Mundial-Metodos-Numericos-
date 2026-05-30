import unittest

from analytics.statistics import Statistics


class StatisticsTest(unittest.TestCase):
    def test_minimum_is_taken_only_from_completed_populations(self):
        resultados = [
            {
                "completado": True,
                "fundas_totales": 200,
                "fundas_para_completar_poblacion": 220,
                "fundas_adicionales_para_completar_poblacion": 80,
                "rondas": 4,
                "costo_promedio": 240,
                "historial": [],
            },
            {
                "completado": True,
                "fundas_totales": 190,
                "fundas_para_completar_poblacion": 205,
                "fundas_adicionales_para_completar_poblacion": 65,
                "rondas": 3,
                "costo_promedio": 228,
                "historial": [],
            },
            {
                "completado": False,
                "fundas_totales": 150,
                "fundas_para_completar_poblacion": 150,
                "fundas_adicionales_para_completar_poblacion": 10,
                "rondas": 1,
                "costo_promedio": 180,
                "historial": [],
            },
        ]
        statistics = Statistics(resultados)
        self.assertEqual(statistics.calcular_minimo_fundas(), 205)
        self.assertEqual(statistics.calcular_minimo_fundas_adicionales(), 65)


if __name__ == "__main__":
    unittest.main()
