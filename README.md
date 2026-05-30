# Album del Mundial 2026 - Metodos Numericos

Simulacion del numero de fundas necesarias para completar un album de 980
cromos dentro de una poblacion cerrada. Los cromos repetidos se intercambian
entre participantes despues de cada ronda de compra.

## Interfaz grafica

```powershell
py main.py
```

La interfaz incluye dos pestanas:

- `Proceso de intercambio`: permite ejecutar rondas y visualizar el progreso,
  cromos faltantes y fundas adicionales de cada participante.
- `Analisis por poblacion`: compara poblaciones de 1 a 50 participantes,
  muestra estadisticas en una tabla y grafica el minimo de fundas adicionales.

No se genera un archivo CSV de forma automatica. Los resultados se muestran
directamente en la interfaz.

## Consola opcional

Para ejecutar un analisis rapido sin abrir la interfaz:

```powershell
py main.py --cli --participantes 1 10 20 30 40 50 --repeticiones 30
```

## Modelo

- Cada cromo tiene la misma probabilidad de aparecer.
- Cada funda contiene 7 cromos.
- Cada participante inicia con 140 fundas.
- En cada ronda compra como minimo `ceil(cromos_faltantes / 7)` fundas
  adicionales. Para los ultimos catorce cromos se aplica un refuerzo calculado
  con una probabilidad objetivo de 50%, evitando rondas estancadas.
- El intercambio global usa exclusivamente repetidos de la poblacion cerrada
  y permite cadenas de dos, tres o mas participantes.
- La probabilidad analitica es una aproximacion por independencia entre cromos;
  el resultado experimental proviene de Monte Carlo.
- Para cada poblacion, el valor principal es el minimo observado de fundas
  necesario para que todos sus participantes completen el album. El promedio
  se conserva unicamente como estadistica de referencia.
