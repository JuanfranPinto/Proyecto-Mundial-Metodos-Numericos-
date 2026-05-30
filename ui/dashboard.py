import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from analytics.statistics import Statistics
from simulation.montecarlo import MonteCarloSimulation
from simulation.simulator import Simulator
from ui.widgets import LineChart


class Dashboard:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Album Mundial 2026 - Simulacion de intercambios")
        self.ventana.geometry("1080x720")
        self.ventana.minsize(900, 620)
        self.simulator = None
        self.automatico = False
        self.cola = queue.Queue()
        self.resultados_analisis = {}
        self.crear_widgets()

    def crear_widgets(self):
        encabezado = ttk.Frame(self.ventana, padding=(14, 12))
        encabezado.pack(fill="x")
        ttk.Label(
            encabezado,
            text="Album Mundial 2026",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            encabezado,
            text="Simulacion de compras, intercambios y completacion del album.",
        ).pack(anchor="w")

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tab_proceso = ttk.Frame(self.pestanas, padding=10)
        self.tab_analisis = ttk.Frame(self.pestanas, padding=10)
        self.pestanas.add(self.tab_proceso, text="Proceso de intercambio")
        self.pestanas.add(self.tab_analisis, text="Analisis por poblacion")
        self._crear_tab_proceso()
        self._crear_tab_analisis()

    def _crear_tab_proceso(self):
        controles = ttk.Frame(self.tab_proceso)
        controles.pack(fill="x")
        ttk.Label(controles, text="Participantes:").pack(side="left")
        self.valor_participantes = tk.StringVar()
        self.valor_participantes.trace_add("write", self._al_cambiar_participantes)
        validar_participantes = (self.ventana.register(self._validar_entrada_participantes), "%P")
        self.entrada_participantes = ttk.Entry(
            controles,
            width=7,
            textvariable=self.valor_participantes,
            validate="key",
            validatecommand=validar_participantes,
        )
        self.entrada_participantes.pack(side="left", padx=6)
        ttk.Button(controles, text="Nueva simulacion", command=self.iniciar).pack(side="left")
        self.boton_ejecutar_ronda = ttk.Button(
            controles,
            text="Ejecutar una ronda",
            command=self.ejecutar_ronda,
            state="disabled",
        )
        self.boton_ejecutar_ronda.pack(
            side="left", padx=6
        )
        self.boton_simular_completo = ttk.Button(
            controles,
            text="Simular hasta completar",
            command=self.simular_hasta_completar,
            state="disabled",
        )
        self.boton_simular_completo.pack(side="left")

        self.estado = tk.StringVar(value="Configure una poblacion para iniciar.")
        ttk.Label(self.tab_proceso, textvariable=self.estado, padding=(0, 10)).pack(fill="x")
        self.tabla = ttk.Treeview(
            self.tab_proceso,
            columns=(
                "participante",
                "pegados",
                "faltantes",
                "fundas",
                "adicionales",
                "intercambios",
                "estado",
            ),
            show="headings",
            height=16,
        )
        for columna, titulo, ancho in [
            ("participante", "Participante", 100),
            ("pegados", "Cromos pegados", 120),
            ("faltantes", "Cromos faltantes", 120),
            ("fundas", "Fundas totales", 110),
            ("adicionales", "Fundas adicionales", 130),
            ("intercambios", "Intercambios recibidos", 145),
            ("estado", "Estado", 110),
        ]:
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor="center")
        self.tabla.pack(fill="both", expand=True)

        self.resumen_proceso = tk.StringVar(value="")
        ttk.Label(
            self.tab_proceso,
            textvariable=self.resumen_proceso,
            padding=(0, 10),
            font=("Segoe UI", 10, "bold"),
        ).pack(fill="x")

    def _validar_entrada_participantes(self, valor):
        return valor == "" or (valor.isdigit() and int(valor) <= 50)

    def _al_cambiar_participantes(self, *_args):
        self.simulator = None
        self.automatico = False
        if hasattr(self, "boton_ejecutar_ronda"):
            self._establecer_botones_proceso("disabled")
            self.estado.set("Presione Nueva simulacion para aplicar el numero de participantes.")
            self.resumen_proceso.set("")
            for item in self.tabla.get_children():
                self.tabla.delete(item)

    def _establecer_botones_proceso(self, estado):
        self.boton_ejecutar_ronda.config(state=estado)
        self.boton_simular_completo.config(state=estado)

    def _crear_tab_analisis(self):
        controles = ttk.Frame(self.tab_analisis)
        controles.pack(fill="x")
        ttk.Label(controles, text="Comparar poblaciones desde 1 hasta:").pack(side="left")
        self.entrada_max_participantes = ttk.Entry(controles, width=7)
        self.entrada_max_participantes.insert(0, "50")
        self.entrada_max_participantes.pack(side="left", padx=6)
        ttk.Label(controles, text="Repeticiones:").pack(side="left")
        self.entrada_repeticiones = ttk.Entry(controles, width=7)
        self.entrada_repeticiones.insert(0, "5")
        self.entrada_repeticiones.pack(side="left", padx=6)
        self.boton_analizar = ttk.Button(
            controles,
            text="Ejecutar analisis",
            command=self.iniciar_analisis,
        )
        self.boton_analizar.pack(side="left")

        self.estado_analisis = tk.StringVar(
            value="La grafica mostrara el minimo de fundas adicionales necesario para completar."
        )
        ttk.Label(self.tab_analisis, textvariable=self.estado_analisis, padding=(0, 10)).pack(
            fill="x"
        )

        cuerpo = ttk.Panedwindow(self.tab_analisis, orient="vertical")
        cuerpo.pack(fill="both", expand=True)
        marco_tabla = ttk.Frame(cuerpo)
        marco_grafica = ttk.Frame(cuerpo)
        cuerpo.add(marco_tabla, weight=2)
        cuerpo.add(marco_grafica, weight=3)

        self.tabla_analisis = ttk.Treeview(
            marco_tabla,
            columns=("participantes", "minimo", "adicionales", "promedio", "rondas", "exito"),
            show="headings",
            height=9,
        )
        for columna, titulo, ancho in [
            ("participantes", "Participantes", 90),
            ("minimo", "Fundas minimas", 110),
            ("adicionales", "Adicionales minimas", 125),
            ("promedio", "Promedio (referencia)", 140),
            ("rondas", "Rondas promedio", 110),
            ("exito", "Simulaciones completas", 145),
        ]:
            self.tabla_analisis.heading(columna, text=titulo)
            self.tabla_analisis.column(columna, width=ancho, anchor="center")
        self.tabla_analisis.pack(fill="both", expand=True)

        self.grafica = LineChart(marco_grafica, height=280)
        self.grafica.pack(fill="both", expand=True, pady=(8, 0))
        self.grafica.establecer_datos([], "Minimo de fundas adicionales por poblacion")
        self.resumen_analisis = tk.StringVar(value="")
        ttk.Label(
            self.tab_analisis,
            textvariable=self.resumen_analisis,
            padding=(0, 8),
            font=("Segoe UI", 10, "bold"),
        ).pack(fill="x")

    def iniciar(self):
        try:
            participantes = int(self.entrada_participantes.get())
            if not 1 <= participantes <= 50:
                raise ValueError("Ingrese un numero de participantes entre 1 y 50.")
            self.simulator = Simulator(participantes)
        except ValueError as exc:
            self.simulator = None
            self._establecer_botones_proceso("disabled")
            messagebox.showerror("Dato invalido", str(exc))
            return
        self.automatico = False
        self._establecer_botones_proceso("normal")
        self.estado.set("Simulacion iniciada con 140 fundas por participante.")
        self.actualizar_tabla()

    def ejecutar_ronda(self):
        if self.simulator is None:
            self.iniciar()
        if self.simulator is None:
            return
        if all(p.album.completado() for p in self.simulator.participantes):
            self._mostrar_final_proceso()
            return
        registro = self.simulator.ejecutar_ronda()
        self.estado.set(
            f"Ronda {registro['ronda']} | "
            f"Fundas adicionales compradas: {registro['fundas_adicionales']} | "
            f"Albums completos: {registro['completados']}"
        )
        self.actualizar_tabla()
        if all(p.album.completado() for p in self.simulator.participantes):
            self._mostrar_final_proceso()

    def simular_hasta_completar(self):
        if self.simulator is None:
            self.iniciar()
        if self.simulator is None:
            return
        self.automatico = True
        self._ejecutar_automaticamente()

    def _ejecutar_automaticamente(self):
        if not self.automatico or self.simulator is None:
            return
        if all(p.album.completado() for p in self.simulator.participantes):
            self.automatico = False
            self._mostrar_final_proceso()
            return
        self.ejecutar_ronda()
        self.ventana.after(30, self._ejecutar_automaticamente)

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for participante in self.simulator.participantes:
            faltantes = participante.album.faltantes()
            self.tabla.insert(
                "",
                "end",
                values=(
                    participante.id,
                    participante.album.total_stickers - faltantes,
                    faltantes,
                    participante.fundas_compradas,
                    participante.fundas_compradas - self.simulator.fundas_iniciales,
                    participante.intercambios_recibidos,
                    "Completo" if participante.album.completado() else "En proceso",
                ),
            )
        fundas = [p.fundas_compradas for p in self.simulator.participantes]
        minimo = min(fundas)
        promedio = sum(fundas) / len(fundas)
        requerido_poblacion = max(fundas)
        self.resumen_proceso.set(
            f"Fundas minimas: {minimo} | "
            f"Promedio: {promedio:.2f} | "
            f"Requeridas para que todos completen: {requerido_poblacion}"
        )

    def _mostrar_final_proceso(self):
        fundas = [p.fundas_compradas for p in self.simulator.participantes]
        minimo = min(fundas)
        promedio = sum(fundas) / len(fundas)
        requerido_poblacion = max(fundas)
        self.estado.set(
            f"Todos completaron el album en {self.simulator.ronda} rondas. "
            f"Minimo individual: {minimo} fundas "
            f"({minimo - self.simulator.fundas_iniciales} adicionales) | "
            f"Promedio: {promedio:.2f} fundas | "
            f"Requeridas para que todos completen: {requerido_poblacion} fundas "
            f"({requerido_poblacion - self.simulator.fundas_iniciales} adicionales)."
        )

    def iniciar_analisis(self):
        try:
            max_participantes = int(self.entrada_max_participantes.get())
            repeticiones = int(self.entrada_repeticiones.get())
            if not 1 <= max_participantes <= 50 or repeticiones < 1:
                raise ValueError("Use entre 1 y 50 participantes y al menos una repeticion.")
        except ValueError as exc:
            messagebox.showerror("Datos invalidos", str(exc))
            return
        self.resultados_analisis = {}
        for item in self.tabla_analisis.get_children():
            self.tabla_analisis.delete(item)
        self.grafica.establecer_datos([], "Minimo de fundas adicionales por poblacion")
        self.resumen_analisis.set("")
        self.boton_analizar.config(state="disabled")
        self.estado_analisis.set("Iniciando analisis...")
        threading.Thread(
            target=self._analizar_poblaciones,
            args=(max_participantes, repeticiones),
            daemon=True,
        ).start()
        self.ventana.after(80, self._procesar_cola)

    def _analizar_poblaciones(self, max_participantes, repeticiones):
        montecarlo = MonteCarloSimulation()
        for participantes in range(1, max_participantes + 1):
            simulaciones = montecarlo.ejecutar(participantes, repeticiones)
            self.cola.put(("resultado", participantes, Statistics(simulaciones).resumen()))
        self.cola.put(("fin", max_participantes, repeticiones))

    def _procesar_cola(self):
        try:
            while True:
                mensaje = self.cola.get_nowait()
                if mensaje[0] == "resultado":
                    self._agregar_resultado(mensaje[1], mensaje[2])
                elif mensaje[0] == "fin":
                    self._finalizar_analisis(mensaje[1], mensaje[2])
                    return
        except queue.Empty:
            self.ventana.after(80, self._procesar_cola)

    def _agregar_resultado(self, participantes, resumen):
        self.resultados_analisis[participantes] = resumen
        minimo = resumen["minimo_fundas"]
        adicionales = resumen["minimo_fundas_adicionales"]
        self.tabla_analisis.insert(
            "",
            "end",
            values=(
                participantes,
                minimo if minimo is not None else "Sin completar",
                adicionales if adicionales is not None else "-",
                f"{resumen['promedio_fundas']:.2f}",
                f"{resumen['rondas_promedio']:.2f}",
                f"{resumen['probabilidad_empirica']:.0%}",
            ),
        )
        datos = [
            (cantidad, datos["minimo_fundas_adicionales"])
            for cantidad, datos in self.resultados_analisis.items()
            if datos["minimo_fundas_adicionales"] is not None
        ]
        self.grafica.establecer_datos(datos, "Minimo de fundas adicionales por poblacion")
        self.estado_analisis.set(f"Analizando poblacion de {participantes} participante(s)...")

    def _finalizar_analisis(self, max_participantes, repeticiones):
        self.boton_analizar.config(state="normal")
        self.estado_analisis.set(
            f"Analisis terminado: poblaciones de 1 a {max_participantes}, "
            f"{repeticiones} repeticion(es) por poblacion."
        )
        validos = [
            (cantidad, datos["minimo_fundas_adicionales"])
            for cantidad, datos in self.resultados_analisis.items()
            if datos["minimo_fundas_adicionales"] is not None
        ]
        if validos:
            mejor = min(validos, key=lambda item: item[1])
            self.resumen_analisis.set(
                f"Mejor resultado observado: {mejor[1]} fundas adicionales con "
                f"{mejor[0]} participante(s). La tabla conserva el promedio solo como referencia."
            )

    def ejecutar(self):
        self.ventana.mainloop()
