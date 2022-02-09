# Proyecto FAA

Para que funcione el proyecto, los dos archivos de datos `HT_Sensor_dataset.dat` y `HT_Sensor_metadata.dat` deben colocarse en el directorio `data/` (crearlo si no existe).

Librerías usadas:
- `pandas`
- `numpy`
- `argparse`
- `matplotlib`
- `logging`
- `sklearn`

## Comentarios
- No hay datos para el experimento 95 (no demasiado relevante puesto que según el metadata era simplemente background noise).
- A simple vista parece que el vino genera mucho más ruido que el plátano.
- No válidos:
    - R5 completamente (ej. 31!, 32!, 33!, etc. a partir del 31 basicamente).
    - Experimento 47 hay algún tipo de error (pico de 100 en R7 y R8).
    - Experimento 76 no hay datos entre los límites indicados.

- En principio la idea es seleccionar solo los datos entre los límites de estímulo. De esta forma el conjunto de datos estará mucho más equilibrado, a diferencia del original que una proporción muchísimo mayor de datos de background sin estímulo que con estímulo.
