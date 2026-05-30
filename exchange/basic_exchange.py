class BasicExchange:
    """Intercambio directo de cromos repetidos entre pares."""

    def ejecutar(self, participantes):
        intercambios = 0
        for index, participante in enumerate(participantes):
            for otro in participantes[index + 1:]:
                intercambios += self.intercambiar_pares(participante, otro)
        return intercambios

    def intercambiar_pares(self, primero, segundo):
        entregables_primero = [
            sticker_id for sticker_id, cantidad in primero.cromos_intercambiar.items()
            if cantidad and segundo.album.necesita(sticker_id)
        ]
        entregables_segundo = [
            sticker_id for sticker_id, cantidad in segundo.cromos_intercambiar.items()
            if cantidad and primero.album.necesita(sticker_id)
        ]
        cantidad = min(len(entregables_primero), len(entregables_segundo))
        for sticker_primero, sticker_segundo in zip(
                entregables_primero[:cantidad], entregables_segundo[:cantidad]):
            primero.cromos_intercambiar[sticker_primero] -= 1
            segundo.cromos_intercambiar[sticker_segundo] -= 1
            segundo.album.agregar(sticker_primero)
            primero.album.agregar(sticker_segundo)
            segundo.intercambios_recibidos += 1
            primero.intercambios_recibidos += 1
        return cantidad
