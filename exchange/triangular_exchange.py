from exchange.graph_exchange import GraphExchange


class TriangularExchange(GraphExchange):
    """Intercambio por cadenas de dos o mas participantes.

    La asignacion global del grafo incluye los ciclos triangulares como caso
    particular y encuentra tambien cadenas mas largas.
    """
