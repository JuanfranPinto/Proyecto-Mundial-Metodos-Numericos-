import unittest
from random import Random

from exchange.graph_exchange import GraphExchange
from models.pack import Pack
from models.participante import Participante


class ModelsTest(unittest.TestCase):
    def test_pack_has_valid_stickers(self):
        pack = Pack(Random(1), num_stickers=7, total_stickers=10)
        self.assertEqual(len(pack.stickers), 7)
        self.assertTrue(all(0 <= sticker.id < 10 for sticker in pack.stickers))

    def test_participant_tracks_purchased_packs(self):
        participant = Participante(1, 0, Random(1), total_stickers=10)
        participant.comprar_y_pegar(3)
        self.assertEqual(participant.fundas_compradas, 3)

    def test_exchange_moves_existing_duplicate(self):
        first = Participante(1, 0, Random(1), total_stickers=3)
        second = Participante(2, 0, Random(2), total_stickers=3)
        first.album.agregar(0)
        first.album.agregar(0)
        second.album.agregar(1)

        intercambios = GraphExchange().ejecutar([first, second])

        self.assertEqual(intercambios, 1)
        self.assertFalse(second.album.necesita(0))
        self.assertEqual(first.cromos_intercambiar[0], 0)


if __name__ == "__main__":
    unittest.main()
