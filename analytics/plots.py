class Plotter:
    def _matplotlib(self):
        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:
            raise RuntimeError(
                "Instale matplotlib para generar graficos: py -m pip install matplotlib"
            ) from exc
        return plt

    def grafico_fundas_vs_participantes(self, datos, mostrar=True, ruta=None):
        plt = self._matplotlib()
        participantes = sorted(datos)
        valores = [datos[n]["minimo_fundas_adicionales"] for n in participantes]
        plt.figure()
        plt.plot(participantes, valores, marker="o")
        plt.xlabel("Numero de participantes")
        plt.ylabel("Fundas adicionales minimas")
        plt.title("Impacto del intercambio en las fundas adicionales minimas")
        plt.grid(True, alpha=0.3)
        if ruta:
            plt.savefig(ruta, bbox_inches="tight")
        if mostrar:
            plt.show()
        return plt.gca()

    def grafico_comparacion_probabilidades(self, datos, mostrar=True, ruta=None):
        plt = self._matplotlib()
        participantes = sorted(datos)
        empiricas = [datos[n]["probabilidad_empirica"] for n in participantes]
        teoricas = [datos[n]["probabilidad_teorica"] for n in participantes]
        plt.figure()
        plt.plot(participantes, empiricas, marker="o", label="Experimental")
        plt.plot(participantes, teoricas, marker="s", label="Analitica aproximada")
        plt.xlabel("Numero de participantes")
        plt.ylabel("Probabilidad de completar")
        plt.title("Probabilidad de completar el album")
        plt.ylim(0, 1.05)
        plt.legend()
        plt.grid(True, alpha=0.3)
        if ruta:
            plt.savefig(ruta, bbox_inches="tight")
        if mostrar:
            plt.show()
        return plt.gca()

    def grafico_probabilidad(self, datos, mostrar=True, ruta=None):
        return self.grafico_comparacion_probabilidades(datos, mostrar, ruta)
