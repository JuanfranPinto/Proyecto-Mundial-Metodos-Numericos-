from random import Random

from config import CROMOS_POR_FUNDA, TOTAL_CROMOS
from models.sticker import Sticker


class Pack:
    def __init__(self, rng=None, num_stickers=CROMOS_POR_FUNDA, total_stickers=TOTAL_CROMOS):
        self.rng = rng or Random()
        self.total_stickers = total_stickers
        self.stickers = [self.generar_cromo() for _ in range(num_stickers)]

    def generar_cromo(self):
        sticker_id = self.rng.randrange(self.total_stickers)
        return Sticker(sticker_id)
