from math import ceil, log

from config import CROMOS_POR_FUNDA, TOTAL_CROMOS


def fundas_adicionales(cromos_faltantes, cromos_por_funda=CROMOS_POR_FUNDA,
                       total_cromos=TOTAL_CROMOS, num_participantes=1,
                       probabilidad_objetivo=0.5):
    """Compra minima con refuerzo probabilistico para los ultimos cromos.

    Cuando quedan pocos cromos, comprar solo una funda puede atascar la
    simulacion durante muchas rondas. Para siete faltantes o menos se calcula
    cuantas fundas dan una probabilidad objetivo de encontrarlos dentro de la
    poblacion que todavia compra.
    """
    if cromos_faltantes <= 0:
        return 0
    minimo = ceil(cromos_faltantes / cromos_por_funda)
    if cromos_faltantes > 2 * cromos_por_funda:
        return minimo
    probabilidad_por_cromo = probabilidad_objetivo ** (1 / cromos_faltantes)
    extracciones = log(1 - probabilidad_por_cromo) / log(1 - 1 / total_cromos)
    refuerzo = ceil(extracciones / (cromos_por_funda * max(1, num_participantes)))
    return max(minimo, refuerzo)


def probabilidad_cromo_en_compras(num_fundas, total_cromos=TOTAL_CROMOS,
                                  cromos_por_funda=CROMOS_POR_FUNDA):
    extracciones = num_fundas * cromos_por_funda
    return 1 - ((total_cromos - 1) / total_cromos) ** extracciones


def probabilidad_completar_aproximada(cromos_faltantes, num_fundas,
                                      num_participantes=1,
                                      total_cromos=TOTAL_CROMOS,
                                      cromos_por_funda=CROMOS_POR_FUNDA):
    """Aproxima P(completar) tras compras e intercambio en poblacion cerrada.

    Supone independencia entre cromos faltantes. Para un participante aislado
    considera sus extracciones; con intercambio considera las extracciones de
    toda la poblacion como oportunidades de encontrar cada cromo faltante.
    """
    if cromos_faltantes <= 0:
        return 1.0
    oportunidades = max(1, num_participantes) * num_fundas * cromos_por_funda
    prob_cromo = 1 - ((total_cromos - 1) / total_cromos) ** oportunidades
    return prob_cromo ** cromos_faltantes


class ProbabilityCalculator:
    @staticmethod
    def prob_completar_ronda(cromos_faltantes, num_participantes,
                             num_fundas=None, total_cromos=TOTAL_CROMOS):
        if num_fundas is None:
            num_fundas = fundas_adicionales(
                cromos_faltantes,
                total_cromos=total_cromos,
                num_participantes=num_participantes,
            )
        return probabilidad_completar_aproximada(
            cromos_faltantes,
            num_fundas,
            num_participantes,
            total_cromos,
        )
