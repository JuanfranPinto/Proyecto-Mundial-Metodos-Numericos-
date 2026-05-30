from statistics import mean, pvariance


class Statistics:
    def __init__(self, resultados_simulaciones):
        self.resultados = resultados_simulaciones

    def calcular_promedio_fundas(self):
        return mean(r["fundas_totales"] for r in self.resultados)

    def calcular_varianza(self):
        valores = [r["fundas_totales"] for r in self.resultados]
        return pvariance(valores) if len(valores) > 1 else 0.0

    def calcular_minimo_fundas(self):
        completados = [r for r in self.resultados if r["completado"]]
        if not completados:
            return None
        return min(r["fundas_para_completar_poblacion"] for r in completados)

    def calcular_minimo_fundas_adicionales(self):
        completados = [r for r in self.resultados if r["completado"]]
        if not completados:
            return None
        return min(
            r["fundas_adicionales_para_completar_poblacion"]
            for r in completados
        )

    def prob_empirica(self):
        return mean(1.0 if r["completado"] else 0.0 for r in self.resultados)

    def prob_teorica(self):
        probabilidades = []
        for resultado in self.resultados:
            if resultado["historial"]:
                ultima = resultado["historial"][-1]["probabilidades_teoricas"]
                probabilidades.extend(ultima.values())
        return mean(probabilidades) if probabilidades else 1.0

    def rondas_promedio(self):
        return mean(r["rondas"] for r in self.resultados)

    def costo_promedio(self):
        return mean(r["costo_promedio"] for r in self.resultados)

    def resumen(self):
        return {
            "minimo_fundas": self.calcular_minimo_fundas(),
            "minimo_fundas_adicionales": self.calcular_minimo_fundas_adicionales(),
            "promedio_fundas": self.calcular_promedio_fundas(),
            "varianza": self.calcular_varianza(),
            "probabilidad_empirica": self.prob_empirica(),
            "probabilidad_teorica": self.prob_teorica(),
            "rondas_promedio": self.rondas_promedio(),
            "costo_promedio": self.costo_promedio(),
        }
