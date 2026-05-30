from random import Random

from config import FUNDAS_INICIALES, TOTAL_CROMOS
from models.album import Album
from models.pack import Pack


class Participante:
    def __init__(self, id_participante, num_fundas_iniciales=FUNDAS_INICIALES,
                 rng=None, total_stickers=TOTAL_CROMOS):
        self.id = id_participante
        self.rng = rng or Random()
        self.album = Album(total_stickers)
        self.fundas_compradas = 0
        self.intercambios_recibidos = 0
        if num_fundas_iniciales:
            self.comprar_y_pegar(num_fundas_iniciales)

    @property
    def cromos_intercambiar(self):
        return self.album.stickers_repetidos

    def comprar_y_pegar(self, num_fundas):
        num_fundas = max(0, int(num_fundas))
        for _ in range(num_fundas):
            pack = Pack(self.rng, total_stickers=self.album.total_stickers)
            for sticker in pack.stickers:
                self.album.agregar(sticker)
        self.fundas_compradas += num_fundas
        return num_fundas
