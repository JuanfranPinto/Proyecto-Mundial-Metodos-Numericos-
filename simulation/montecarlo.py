from config import SEMILLA, SIMULACIONES
from simulation.simulator import Simulator


class MonteCarloSimulation:
    def __init__(self, total_cromos=None, fundas_iniciales=None, semilla=SEMILLA):
        self.total_cromos = total_cromos
        self.fundas_iniciales = fundas_iniciales
        self.semilla = semilla

    def ejecutar(self, num_participantes, num_simulaciones=SIMULACIONES,
                 max_rondas=None):
        resultados = []
        for repeticion in range(num_simulaciones):
            opciones = {"semilla": self.semilla + repeticion}
            if self.total_cromos is not None:
                opciones["total_cromos"] = self.total_cromos
            if self.fundas_iniciales is not None:
                opciones["fundas_iniciales"] = self.fundas_iniciales
            simulator = Simulator(num_participantes, **opciones)
            if max_rondas is None:
                resultados.append(simulator.ejecutar_simulacion_completa())
            else:
                resultados.append(simulator.ejecutar_simulacion_completa(max_rondas))
        return resultados

    def simular_rondas(self, num_simulaciones, num_participantes=1):
        return self.ejecutar(num_participantes, num_simulaciones)
