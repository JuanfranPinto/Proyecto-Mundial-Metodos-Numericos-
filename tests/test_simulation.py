import unittest

from simulation.probabilities import fundas_adicionales
from simulation.simulator import Simulator


class SimulationTest(unittest.TestCase):
    def test_additional_packs_policy(self):
        self.assertEqual(fundas_adicionales(0), 0)
        self.assertGreater(fundas_adicionales(1), 1)
        self.assertGreater(fundas_adicionales(10), 2)
        self.assertEqual(fundas_adicionales(15), 3)

    def test_small_simulation_completes(self):
        simulator = Simulator(
            num_participantes=3,
            semilla=7,
            total_cromos=12,
            fundas_iniciales=2,
        )
        result = simulator.ejecutar_simulacion_completa(max_rondas=100)
        self.assertTrue(result["completado"])
        self.assertGreaterEqual(result["fundas_totales"], 2)
        self.assertTrue(result["historial"])


if __name__ == "__main__":
    unittest.main()
