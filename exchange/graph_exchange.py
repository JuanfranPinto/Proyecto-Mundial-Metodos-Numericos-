from collections import defaultdict


class GraphExchange:
    """Asignacion maxima dentro de una poblacion cerrada.

    Cada repetido conserva su origen y solo se entrega a un participante que lo
    necesita. La asignacion global permite materializar cadenas de intercambio.
    """

    def construir_grafo(self, participantes):
        necesidades = defaultdict(list)
        for participante in participantes:
            for sticker_id in range(participante.album.total_stickers):
                if participante.album.necesita(sticker_id):
                    necesidades[sticker_id].append(participante)
        return necesidades

    def ejecutar(self, participantes):
        necesidades = self.construir_grafo(participantes)
        intercambios = 0
        for propietario in participantes:
            for sticker_id, cantidad in list(propietario.cromos_intercambiar.items()):
                candidatos = necesidades.get(sticker_id, [])
                while cantidad and candidatos:
                    receptor = candidatos.pop()
                    if receptor is propietario:
                        continue
                    propietario.cromos_intercambiar[sticker_id] -= 1
                    receptor.album.agregar(sticker_id)
                    receptor.intercambios_recibidos += 1
                    cantidad -= 1
                    intercambios += 1
        return intercambios
