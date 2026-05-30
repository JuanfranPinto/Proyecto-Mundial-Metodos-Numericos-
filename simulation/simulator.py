from random import Random

from config import FUNDAS_INICIALES, MAX_RONDAS, PRECIO_FUNDA, TOTAL_CROMOS
from exchange.triangular_exchange import TriangularExchange
from models.participante import Participante
from simulation.probabilities import (
    fundas_adicionales,
    probabilidad_completar_aproximada,
)


class Simulator:
    def __init__(self, num_participantes, semilla=None,
                 total_cromos=TOTAL_CROMOS,
                 fundas_iniciales=FUNDAS_INICIALES,
                 exchange=None):
        if num_participantes < 1:
            raise ValueError("Debe existir al menos un participante")
        self.rng = Random(semilla)
        self.total_cromos = total_cromos
        self.fundas_iniciales = fundas_iniciales
        self.participantes = [
            Participante(
                index + 1,
                fundas_iniciales,
                Random(self.rng.randrange(2 ** 32)),
                total_cromos,
            )
            for index in range(num_participantes)
        ]
        self.exchange = exchange or TriangularExchange()
        self.ronda = 0
        self.historial = []

    def ejecutar_ronda(self):
        self.ronda += 1
        intercambios_antes = self.exchange.ejecutar(self.participantes)
        compras = {}
        probabilidades = {}

        activos = sum(not p.album.completado() for p in self.participantes)
        for participante in self.participantes:
            faltantes = participante.album.faltantes()
            cantidad = fundas_adicionales(
                faltantes,
                total_cromos=self.total_cromos,
                num_participantes=activos,
            )
            compras[participante.id] = cantidad
            probabilidades[participante.id] = probabilidad_completar_aproximada(
                faltantes,
                cantidad,
                activos,
                self.total_cromos,
            )
            participante.comprar_y_pegar(cantidad)

        intercambios_despues = self.exchange.ejecutar(self.participantes)
        completados = sum(p.album.completado() for p in self.participantes)
        registro = {
            "ronda": self.ronda,
            "compras": compras,
            "fundas_adicionales": sum(compras.values()),
            "intercambios": intercambios_antes + intercambios_despues,
            "faltantes": {p.id: p.album.faltantes() for p in self.participantes},
            "probabilidades_teoricas": probabilidades,
            "completados": completados,
            "probabilidad_experimental": completados / len(self.participantes),
        }
        self.historial.append(registro)
        return registro

    def ejecutar_simulacion_completa(self, max_rondas=MAX_RONDAS):
        while (not all(p.album.completado() for p in self.participantes)
               and self.ronda < max_rondas):
            self.ejecutar_ronda()

        fundas = [p.fundas_compradas for p in self.participantes]
        fundas_para_completar_poblacion = max(fundas)
        return {
            "num_participantes": len(self.participantes),
            "rondas": self.ronda,
            "completado": all(p.album.completado() for p in self.participantes),
            "participantes_completados": sum(p.album.completado() for p in self.participantes),
            "fundas_totales": sum(fundas) / len(fundas),
            "fundas_por_participante": fundas,
            "fundas_iniciales": self.fundas_iniciales,
            "fundas_para_completar_poblacion": fundas_para_completar_poblacion,
            "fundas_adicionales_para_completar_poblacion": (
                fundas_para_completar_poblacion - self.fundas_iniciales
            ),
            "costo_promedio": (sum(fundas) / len(fundas)) * PRECIO_FUNDA,
            "faltantes_finales": [p.album.faltantes() for p in self.participantes],
            "historial": self.historial,
        }

    def simular(self, num_rondas):
        for _ in range(num_rondas):
            if all(p.album.completado() for p in self.participantes):
                break
            self.ejecutar_ronda()
        return self.historial
