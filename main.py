import argparse

from analytics.plots import Plotter
from analytics.statistics import Statistics
from simulation.montecarlo import MonteCarloSimulation


def analizar_poblaciones(poblaciones, repeticiones, max_rondas):
    montecarlo = MonteCarloSimulation()
    resultados_globales = {}
    for num_participantes in poblaciones:
        print(f"Simulando con {num_participantes} participante(s)...")
        simulaciones = montecarlo.ejecutar(
            num_participantes,
            repeticiones,
            max_rondas,
        )
        resultados_globales[num_participantes] = Statistics(simulaciones).resumen()
    return resultados_globales


def imprimir_resumen(resultados):
    print("\nParticipantes | Min. fundas | Min. adicionales | Rondas | P. experimental")
    print("-" * 76)
    for participantes, resumen in sorted(resultados.items()):
        print(
            f"{participantes:>13} | "
            f"{str(resumen['minimo_fundas']):>11} | "
            f"{str(resumen['minimo_fundas_adicionales']):>16} | "
            f"{resumen['rondas_promedio']:>6.2f} | "
            f"{resumen['probabilidad_empirica']:>15.2%}"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulacion del album del Mundial 2026 con intercambios.",
    )
    parser.add_argument(
        "--participantes",
        nargs="+",
        type=int,
        default=[1, 5, 10, 20, 30, 40, 50],
        help="Cantidades de participantes a comparar.",
    )
    parser.add_argument("--repeticiones", type=int, default=5)
    parser.add_argument("--max-rondas", type=int, default=60)
    parser.add_argument("--graficos", action="store_true")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Ejecutar en consola. Sin esta opcion se abre la interfaz grafica.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.cli:
        from ui.app import ejecutar_app
        ejecutar_app()
        return

    resultados = analizar_poblaciones(
        args.participantes,
        args.repeticiones,
        args.max_rondas,
    )
    imprimir_resumen(resultados)
    if args.graficos:
        plotter = Plotter()
        plotter.grafico_fundas_vs_participantes(resultados)
        plotter.grafico_comparacion_probabilidades(resultados)


if __name__ == "__main__":
    main()
