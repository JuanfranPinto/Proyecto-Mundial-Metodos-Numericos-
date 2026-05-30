import tkinter as tk


class LineChart(tk.Canvas):
    """Grafica lineal liviana para no depender de matplotlib en la interfaz."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            background="white",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            **kwargs,
        )
        self.datos = []
        self.titulo = ""
        self.bind("<Configure>", lambda _event: self.redibujar())

    def establecer_datos(self, datos, titulo):
        self.datos = sorted(datos)
        self.titulo = titulo
        self.redibujar()

    def redibujar(self):
        self.delete("all")
        ancho = max(self.winfo_width(), 360)
        alto = max(self.winfo_height(), 220)
        margen_izq, margen_der, margen_sup, margen_inf = 64, 24, 38, 48
        self.create_text(ancho / 2, 18, text=self.titulo, font=("Segoe UI", 11, "bold"))
        self.create_line(margen_izq, margen_sup, margen_izq, alto - margen_inf, fill="#475569")
        self.create_line(
            margen_izq,
            alto - margen_inf,
            ancho - margen_der,
            alto - margen_inf,
            fill="#475569",
        )
        if not self.datos:
            self.create_text(
                ancho / 2,
                alto / 2,
                text="Ejecute el analisis para generar la grafica.",
                fill="#64748b",
            )
            return

        xs = [dato[0] for dato in self.datos]
        ys = [dato[1] for dato in self.datos]
        max_x = max(xs) or 1
        max_y = max(ys) or 1

        def x_px(valor):
            return margen_izq + (valor / max_x) * (ancho - margen_izq - margen_der)

        def y_px(valor):
            return alto - margen_inf - (valor / max_y) * (alto - margen_sup - margen_inf)

        for paso in range(5):
            valor = round(max_y * paso / 4)
            y = y_px(valor)
            self.create_line(margen_izq, y, ancho - margen_der, y, fill="#e2e8f0")
            self.create_text(margen_izq - 8, y, text=str(valor), anchor="e", fill="#475569")

        puntos = []
        for x, y in self.datos:
            puntos.extend([x_px(x), y_px(y)])
        if len(puntos) >= 4:
            self.create_line(*puntos, fill="#2563eb", width=2)
        for x, y in self.datos:
            px, py = x_px(x), y_px(y)
            self.create_oval(px - 3, py - 3, px + 3, py + 3, fill="#2563eb", outline="")
            self.create_text(px, alto - margen_inf + 16, text=str(x), fill="#475569")

        self.create_text(ancho / 2, alto - 10, text="Numero de participantes", fill="#334155")
        self.create_text(
            14,
            alto / 2,
            text="Fundas adicionales minimas",
            angle=90,
            fill="#334155",
        )
