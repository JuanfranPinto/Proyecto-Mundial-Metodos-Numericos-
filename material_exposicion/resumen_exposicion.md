# Resumen para la exposicion

## 1. Problema planteado

El album del Mundial 2026 tiene `980` cromos. Cada funda contiene `7` cromos y
cuesta `$1.20`. En el caso ideal, sin cromos repetidos, una persona necesitaria:

```text
980 cromos / 7 cromos por funda = 140 fundas
140 fundas * $1.20 = $168
```

Sin embargo, en una compra real aparecen cromos repetidos. El objetivo del
programa es estudiar como los intercambios entre participantes reducen la
cantidad de fundas adicionales necesarias.

## 2. Supuestos del modelo

- Todos los cromos tienen la misma probabilidad de aparecer.
- Cada participante inicia comprando `140` fundas.
- Los intercambios solo ocurren dentro de una poblacion cerrada.
- Se permiten cadenas de intercambio entre varios participantes.
- Cada participante pega sus cromos nuevos y conserva sus repetidos para
  intercambiarlos.

## 3. Estructura del programa

El proyecto esta dividido en modulos:

- `models/`: representa cromos, fundas, albumes y participantes.
- `exchange/`: administra intercambios directos y cadenas de intercambio.
- `simulation/`: ejecuta rondas, calcula fundas adicionales y realiza Monte Carlo.
- `analytics/`: obtiene minimos, promedios, probabilidades y estadisticas.
- `ui/`: contiene la interfaz grafica con tematica azul del Mundial.

## 4. Proceso de una simulacion

1. El usuario ingresa entre `1` y `50` participantes.
2. Presiona `Nueva simulacion`.
3. Cada participante compra `140` fundas iniciales.
4. Los cromos nuevos se pegan en el album.
5. Los cromos repetidos se guardan para intercambiarlos.
6. El sistema identifica que cromos necesita cada participante.
7. Los repetidos se entregan a participantes que todavia los necesitan.
8. Se contabilizan los intercambios recibidos por cada participante.
9. Se calculan las fundas adicionales segun los cromos faltantes.
10. Se compran nuevas fundas y se repite el proceso.
11. La simulacion termina cuando todos completan el album.

## 5. Algoritmo de intercambio

El intercambio se representa como un grafo:

- Cada cromo faltante se relaciona con los participantes que lo necesitan.
- Cada participante ofrece sus cromos repetidos.
- El sistema asigna cada repetido a otro participante que lo requiera.
- La asignacion global permite intercambios directos y cadenas de tres o mas
  participantes.

No se crean cromos artificialmente: todos los cromos intercambiados provienen
de repetidos existentes dentro de la poblacion.

## 6. Fundas adicionales

La formula minima inicial es:

```text
fundas adicionales = techo(cromos faltantes / 7)
```

Cuando quedan pocos cromos, el programa agrega un refuerzo probabilistico. Esto
evita que la simulacion se estanque durante demasiadas rondas esperando un solo
cromo dificil de obtener.

## 7. Resultados mostrados en la interfaz

La pestana `Proceso de intercambio` muestra por participante:

- Cromos pegados.
- Cromos faltantes.
- Fundas totales compradas.
- Fundas adicionales.
- Intercambios recibidos.
- Estado del album.

Al finalizar se muestran tres datos diferentes:

- `Minimo individual`: menor cantidad comprada por un participante.
- `Promedio`: promedio de fundas compradas por la poblacion.
- `Requeridas para que todos completen`: cantidad del participante que necesito
  mas fundas.

## 8. Analisis por poblacion

La pestana `Analisis por poblacion` ejecuta simulaciones Monte Carlo para
comparar poblaciones de distintos tamanos.

La interfaz presenta:

- Minimo de fundas necesarias.
- Minimo de fundas adicionales.
- Promedio como referencia.
- Rondas promedio.
- Porcentaje de simulaciones completadas.
- Grafica de fundas adicionales minimas segun el numero de participantes.

## 9. Conclusion para presentar

El programa permite observar que los intercambios reducen la necesidad de
comprar nuevas fundas. Mientras mas participantes existen en la poblacion
cerrada, mayor es la disponibilidad de cromos repetidos utiles para otras
personas.

La simulacion demuestra de forma visual y experimental que organizar
intercambios mejora la eficiencia para completar el album y reduce el gasto
adicional.

## 10. Guion breve para explicar en clase

> Nuestro proyecto simula la completacion del album del Mundial 2026. Aunque el
> minimo ideal es de 140 fundas, en la realidad aparecen cromos repetidos. Cada
> participante compra inicialmente esas 140 fundas, pega sus cromos nuevos y
> guarda los repetidos. El programa busca que repetidos sirven para completar
> los albumes de otros participantes y realiza intercambios dentro de una
> poblacion cerrada. Despues de cada ronda calcula cuantas fundas adicionales
> deben comprarse y repite el proceso hasta que todos terminan. Finalmente,
> comparamos diferentes cantidades de participantes mediante simulaciones
> Monte Carlo y una grafica. Esto nos permite analizar como una poblacion mayor
> facilita los intercambios y reduce las compras adicionales.
