# TP8P9

Simulación de tres alambres paralelos infinitos con cálculo de fuerza magnética y campo magnético resultante por unidad de longitud.

## Qué hace

El script [simulacion_tres_alambres.py](/home/roberto/tp8p9/simulacion_tres_alambres.py) permite:

- ingresar `I_a`, `I_b` e `I_c` con signo;
- elegir sobre qué alambre (`a`, `b` o `c`) calcular la resultante;
- mostrar un resumen numérico en consola;
- dibujar una representación cartesiana con corrientes, fuerzas parciales, fuerza resultante y campo magnético resultante.

## Convenciones

- `I > 0` representa corriente en dirección `+j`.
- `I < 0` representa corriente en dirección `-j`.
- Las fuerzas sobre los alambres se reportan sobre el eje `x` usando `+i` o `-i`.
- El campo magnético perpendicular al plano se reporta usando `+k` o `-k`.
- En el gráfico, `⊙` representa `+k` y `⊗` representa `-k`.

## Geometría del problema

- Los alambres son rectas paralelas al eje `y`.
- Sus posiciones están sobre el eje `x`.
- Las ubicaciones son:
  `a` en `x = 0`, `b` en `x = d`, `c` en `x = 3d`.
- La separación entre `a` y `b` es `d`.
- La separación entre `b` y `c` es `2d`.

## Visualización

- Cada alambre tiene un color distinto.
- La flecha de cada corriente usa el color de su alambre.
- Cada componente de fuerza usa el color del alambre que la genera.
- La fuerza resultante se dibuja en rojo.
- El campo magnético resultante sobre el alambre objetivo se muestra junto al símbolo `⊙` o `⊗` con el color del alambre objetivo.

## Requisitos

- `uv`
- Python `>= 3.13`

Las dependencias están declaradas en [pyproject.toml](/home/roberto/tp8p9/pyproject.toml).

## Instalación

```bash
uv sync
```

## Uso

Ejecutá:

```bash
uv run python simulacion_tres_alambres.py
```

El programa pide:

1. la separación base `d` en metros;
2. las corrientes `I_a`, `I_b`, `I_c` en amperes;
3. el alambre objetivo (`a`, `b` o `c`).

Los valores por defecto para las corrientes son:

```text
I_a = 3.0 A
I_b = 3.0 A
I_c = 3.0 A
```

## Ejemplo de entrada

```text
Separación base d en metros [Enter=1.0]:
Corriente I_a en amperes [Enter=3.0]: 4
Corriente I_b en amperes [Enter=3.0]: -2
Corriente I_c en amperes [Enter=3.0]: 1
Mostrar la resultante sobre qué alambre? [a/b/c, Enter=b]: a
```

## Ejemplo de salida

```text
Corrientes configuradas:
I_a = 4.000 A (+j)
I_b = -2.000 A (-j)
I_c = 1.000 A (+j)

Fuerzas sobre el alambre a:
F_ab/L = 1.600000e-06 N/m (-i)
F_ac/L = 2.666667e-07 N/m (+i)
F_a/L = -1.333333e-06 N/m (-i)

Campo magnético sobre el alambre a:
B_ab = 4.000000e-07 T (-k)
B_ac = 6.666667e-08 T (+k)
B_a = -3.333333e-07 T (-k)
```

## Modelo físico

La magnitud de la fuerza por unidad de longitud entre dos alambres paralelos es:

```text
F/L = mu0 * |I1 * I2| / (2 * pi * r)
```

donde `r` es la distancia entre alambres.

## Nota sobre Matplotlib

Si el entorno no permite escribir en la configuración de Matplotlib, usá:

```bash
MPLCONFIGDIR=.matplotlib uv run python simulacion_tres_alambres.py
```
