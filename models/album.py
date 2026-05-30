from collections import Counter

from config import TOTAL_CROMOS


class Album:
    def __init__(self, total_stickers=TOTAL_CROMOS):
        self.stickers_pegados = set()
        self.stickers_repetidos = Counter()
        self.total_stickers = total_stickers

    def agregar(self, sticker):
        sticker_id = sticker.id if hasattr(sticker, "id") else int(sticker)
        if sticker_id in self.stickers_pegados:
            self.stickers_repetidos[sticker_id] += 1
            return False
        self.stickers_pegados.add(sticker_id)
        return True

    def necesita(self, sticker_id):
        return sticker_id not in self.stickers_pegados

    def faltantes(self):
        return self.total_stickers - len(self.stickers_pegados)

    def completado(self):
        return self.faltantes() == 0
