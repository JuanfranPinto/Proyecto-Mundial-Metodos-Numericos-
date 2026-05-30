# Diagrama de flujo del simulador del album Mundial 2026

```mermaid
flowchart TD
    A["Inicio del programa"] --> B{"Modo de ejecucion"}
    B -->|"Interfaz grafica por defecto"| C["Abrir ventana principal"]
    B -->|"Consola opcional --cli"| Z["Ejecutar analisis automatico y mostrar resumen"]

    C --> D{"Seleccionar pestana"}

    D -->|"Proceso de intercambio"| E["Ingresar entre 1 y 50 participantes"]
    E --> F["Presionar Nueva simulacion"]
    F --> G["Crear participantes con album vacio"]
    G --> H["Cada participante compra 140 fundas iniciales"]
    H --> I["Pegar cromos nuevos y guardar repetidos"]

    I --> J{"Accion seleccionada"}
    J -->|"Ejecutar una ronda"| K["Iniciar nueva ronda"]
    J -->|"Simular hasta completar"| K

    K --> L["Intercambiar cromos repetidos disponibles"]
    L --> M["Construir grafo: cromo faltante -> participantes que lo necesitan"]
    M --> N["Entregar repetidos dentro de la poblacion cerrada"]
    N --> O["Contabilizar intercambios recibidos por participante"]

    O --> P["Calcular cromos faltantes de cada participante"]
    P --> Q["Calcular fundas adicionales necesarias"]
    Q --> R["Comprar nuevas fundas y pegar cromos nuevos"]
    R --> S["Realizar una segunda ronda de intercambios"]
    S --> T["Actualizar tabla: pegados, faltantes, fundas e intercambios"]
    T --> U{"Todos completaron el album?"}
    U -->|"No"| J
    U -->|"Si"| V["Mostrar minimo individual, promedio y fundas requeridas para que todos completen"]

    D -->|"Analisis por poblacion"| W["Elegir maximo de participantes y repeticiones"]
    W --> X["Ejecutar simulaciones Monte Carlo para poblaciones de 1 hasta N"]
    X --> Y["Calcular minimo de fundas adicionales, promedio, rondas y probabilidad experimental"]
    Y --> AA["Mostrar tabla comparativa y grafica en la interfaz"]
```

## Lectura rapida del diagrama

- La aplicacion abre una interfaz grafica por defecto.
- Cada participante inicia con `140` fundas de `7` cromos.
- Los cromos nuevos se pegan en el album y los repetidos quedan disponibles.
- En cada ronda se intercambian repetidos dentro de la poblacion cerrada.
- Luego se calculan y compran fundas adicionales segun los cromos faltantes.
- El proceso se repite hasta completar los albumes.
- La segunda pestana compara distintas poblaciones mediante simulaciones Monte Carlo.
