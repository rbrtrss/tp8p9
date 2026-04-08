import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

MU0 = 4 * np.pi * 1e-7
LABELS = ["a", "b", "c"]
COLORES = {"a": "tab:blue", "b": "tab:orange", "c": "tab:green"}


def fuerza_por_longitud(i1, i2, r):
    """Magnitud de la fuerza por unidad de longitud entre dos alambres paralelos."""
    return MU0 * abs(i1 * i2) / (2 * np.pi * r)


def fuerza_x_entre_alambres(i_objetivo, i_fuente, x_objetivo, x_fuente):
    """Componente horizontal de la fuerza por unidad de longitud sobre un alambre."""
    distancia = abs(x_fuente - x_objetivo)
    magnitud = fuerza_por_longitud(i_objetivo, i_fuente, distancia)
    misma_direccion = np.sign(i_objetivo) == np.sign(i_fuente)
    direccion_hacia_fuente = np.sign(x_fuente - x_objetivo)
    return magnitud * direccion_hacia_fuente if misma_direccion else -magnitud * direccion_hacia_fuente


def campo_z_entre_alambres(i_fuente, x_objetivo, x_fuente):
    """Componente z del campo magnético creado por un alambre sobre otro punto del eje x."""
    return -MU0 * i_fuente / (2 * np.pi * (x_objetivo - x_fuente))


def describir_sentido(valor):
    return "+j" if valor >= 0 else "-j"


def describir_direccion_fuerza(fuerza_x):
    if np.isclose(fuerza_x, 0.0):
        return "0 i"
    return "+i" if fuerza_x > 0 else "-i"


def describir_direccion_campo(campo_z):
    if np.isclose(campo_z, 0.0):
        return "0 k"
    return "+k" if campo_z > 0 else "-k"


def solicitar_float(mensaje, minimo=None, permitir_cero=False, default=None):
    while True:
        bruto = input(mensaje).strip()
        if not bruto and default is not None:
            return default

        try:
            valor = float(bruto)
        except ValueError:
            print("Ingresá un número válido.")
            continue

        if minimo is not None and valor < minimo:
            print(f"El valor debe ser mayor o igual que {minimo}.")
            continue

        if not permitir_cero and np.isclose(valor, 0.0):
            print("El valor no puede ser cero.")
            continue

        return valor


def solicitar_alambre_objetivo():
    while True:
        objetivo = input("Mostrar la resultante sobre qué alambre? [a/b/c, Enter=b]: ").strip().lower()
        if objetivo == "":
            return "b"
        if objetivo in LABELS:
            return objetivo
        print("Elegí 'a', 'b' o 'c'.")


def recolectar_parametros_interactivos():
    print("Simulación de tres alambres paralelos")
    print("Ingresá cada corriente con signo: positiva hacia +j, negativa hacia -j.\n")

    d = solicitar_float("Separación base d en metros [Enter=1.0]: ", minimo=1e-12, default=1.0)

    corrientes = []
    for label, default in zip(LABELS, [3.0, 3.0, 3.0]):
        corriente = solicitar_float(
            f"Corriente I_{label} en amperes [Enter={default}]: ",
            permitir_cero=True,
            default=default,
        )
        corrientes.append(corriente)

    objetivo = solicitar_alambre_objetivo()
    return corrientes[0], corrientes[1], corrientes[2], d, objetivo


def calcular_fuerzas(Ia, Ib, Ic, d, objetivo):
    corrientes = {"a": Ia, "b": Ib, "c": Ic}
    posiciones = {"a": 0.0, "b": d, "c": 3 * d}

    contribuciones = []
    campos = []
    for fuente in LABELS:
        if fuente == objetivo:
            continue
        fuerza_x = fuerza_x_entre_alambres(
            corrientes[objetivo],
            corrientes[fuente],
            posiciones[objetivo],
            posiciones[fuente],
        )
        contribuciones.append((fuente, fuerza_x))
        campo_z = campo_z_entre_alambres(corrientes[fuente], posiciones[objetivo], posiciones[fuente])
        campos.append((fuente, campo_z))

    resultante = sum(fuerza for _, fuerza in contribuciones)
    campo_resultante = sum(campo for _, campo in campos)
    return corrientes, posiciones, contribuciones, resultante, campos, campo_resultante


def imprimir_resumen(corrientes, contribuciones, objetivo, resultante, campos, campo_resultante):
    print("\nCorrientes configuradas:")
    for label in LABELS:
        print(f"I_{label} = {corrientes[label]:.3f} A ({describir_sentido(corrientes[label])})")

    print(f"\nFuerzas sobre el alambre {objetivo}:")
    for fuente, fuerza_x in contribuciones:
        print(
            f"F_{objetivo}{fuente}/L = {abs(fuerza_x):.6e} N/m "
            f"({describir_direccion_fuerza(fuerza_x)})"
        )

    print(
        f"F_{objetivo}/L = {resultante:.6e} N/m "
        f"({describir_direccion_fuerza(resultante)})"
    )

    print(f"\nCampo magnético sobre el alambre {objetivo}:")
    for fuente, campo_z in campos:
        print(
            f"B_{objetivo}{fuente} = {abs(campo_z):.6e} T "
            f"({describir_direccion_campo(campo_z)})"
        )

    print(
        f"B_{objetivo} = {campo_resultante:.6e} T "
        f"({describir_direccion_campo(campo_resultante)})"
    )


def dibujar_alambres(ax, posiciones, corrientes):
    offsets_texto = {"a": 0.12, "b": 0.18, "c": -0.7}

    for label in LABELS:
        x = posiciones[label]
        corriente = corrientes[label]
        color = COLORES[label]
        ax.plot([x, x], [-1.2, 1.2], linewidth=3, color=color)

        if corriente >= 0:
            xy, xytext = (x, 1.05), (x, 0.2)
        else:
            xy, xytext = (x, 0.2), (x, 1.05)

        ax.annotate(
            "",
            xy=xy,
            xytext=xytext,
            arrowprops=dict(arrowstyle="->", lw=3.4, mutation_scale=20, color=color),
        )
        ax.text(
            x + offsets_texto[label],
            1.05,
            rf"$I_{{{label}}}={corriente:.1f}\,\mathrm{{A}}$",
            va="bottom",
            fontsize=11,
            color=color,
            ha="left" if offsets_texto[label] >= 0 else "right",
        )
        ax.text(x, -1.32, rf"${label}$", ha="center", fontsize=13, color=color)


def dibujar_distancias(ax, d):
    ax.annotate(
        "",
        xy=(0, -0.35),
        xytext=(d, -0.35),
        arrowprops=dict(arrowstyle="<->", lw=1.5, linestyle="--"),
    )
    ax.text(d / 2, -0.24, r"$d$", ha="center", fontsize=12)

    ax.annotate(
        "",
        xy=(d, -0.62),
        xytext=(3 * d, -0.62),
        arrowprops=dict(arrowstyle="<->", lw=1.5, linestyle="--"),
    )
    ax.text(2 * d, -0.51, r"$2d$", ha="center", fontsize=12)


def configurar_plano(ax, posiciones):
    margen_x = max(0.5, 0.2 * posiciones["c"])
    ax.set_xlim(-margen_x, posiciones["c"] + margen_x)
    ax.set_ylim(-1.5, 1.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0.0))
    ax.spines["left"].set_position(("data", 0.0))
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y")
    ax.xaxis.set_label_coords(1.02, 0.52)
    ax.yaxis.set_label_coords(0.52, 1.02)
    ax.set_yticks([-1.0, -0.5, 0.5, 1.0])
    ax.set_xticks([posiciones[label] for label in LABELS])
    ax.grid(True, linestyle=":", linewidth=0.8, alpha=0.7)


def dibujar_fuerzas(ax, objetivo, posiciones, contribuciones, resultante):
    x_objetivo = posiciones[objetivo]
    magnitudes = [abs(fuerza_x) for _, fuerza_x in contribuciones] + [abs(resultante)]
    max_fuerza = max([valor for valor in magnitudes if valor > 0], default=1.0)
    escala = max(0.25, posiciones["b"] * 0.85) / max_fuerza
    desplazamiento_texto = max(0.06, 0.04 * posiciones["c"])

    niveles = [0.22, -0.22]
    for (fuente, fuerza_x), y in zip(contribuciones, niveles):
        if np.isclose(fuerza_x, 0.0):
            continue
        fin_x = x_objetivo + fuerza_x * escala
        color_fuente = COLORES[fuente]
        ax.add_patch(
            FancyArrowPatch(
                (x_objetivo, y),
                (fin_x, y),
                arrowstyle="-|>",
                mutation_scale=18,
                lw=2,
                color=color_fuente,
            )
        )
        ax.text(
            fin_x + np.sign(fuerza_x) * desplazamiento_texto,
            y + 0.1,
            rf"$\frac{{F_{{{objetivo}{fuente}}}}}{{L}}$",
            ha="left" if fuerza_x > 0 else "right",
            fontsize=11,
            color=color_fuente,
        )

    if not np.isclose(resultante, 0.0):
        fin_x = x_objetivo + resultante * escala
        ax.add_patch(
            FancyArrowPatch(
                (x_objetivo, 0.5),
                (fin_x, 0.5),
                arrowstyle="-|>",
                mutation_scale=20,
                lw=2.5,
                color="tab:red",
            )
        )
        ax.text(
            fin_x + np.sign(resultante) * desplazamiento_texto,
            0.62,
            rf"$\frac{{F_{{{objetivo}}}}}{{L}} = {resultante:.2e}\,\mathrm{{N/m}}$",
            ha="left" if resultante > 0 else "right",
            fontsize=11,
            color="tab:red",
        )
    else:
        ax.text(
            x_objetivo,
            0.58,
            rf"$\frac{{F_{{{objetivo}}}}}{{L}} = 0$",
            ha="center",
            fontsize=11,
            color="tab:red",
        )


def dibujar_campo_resultante(ax, objetivo, posiciones, campo_resultante):
    x_objetivo = posiciones[objetivo]
    color = COLORES[objetivo]
    desplazamiento = max(0.22, 0.16 * posiciones["c"])
    x_texto = x_objetivo + desplazamiento
    ha = "left"

    if np.isclose(campo_resultante, 0.0):
        ax.text(x_texto, 0.95, r"$B=0$", ha=ha, fontsize=12, color=color)
        return

    simbolo = r"$\odot$" if campo_resultante > 0 else r"$\otimes$"
    texto = f"{simbolo} " + rf"$B_{{{objetivo}}}={abs(campo_resultante):.2e}\,\mathrm{{T}}$"
    ax.text(x_texto, 0.95, texto, ha=ha, fontsize=12, color=color)


def graficar(corrientes, posiciones, contribuciones, resultante, objetivo, campo_resultante):
    fig, ax = plt.subplots(figsize=(9, 5.2))
    configurar_plano(ax, posiciones)
    dibujar_alambres(ax, posiciones, corrientes)
    dibujar_distancias(ax, posiciones["b"])
    dibujar_fuerzas(ax, objetivo, posiciones, contribuciones, resultante)
    dibujar_campo_resultante(ax, objetivo, posiciones, campo_resultante)
    ax.set_title(f"Resultante sobre el alambre {objetivo}")
    plt.tight_layout()
    plt.show()


def simulacion(Ia=3.0, Ib=3.0, Ic=3.0, d=1.0, objetivo="b"):
    objetivo = objetivo.lower()
    if objetivo not in LABELS:
        raise ValueError("El alambre objetivo debe ser 'a', 'b' o 'c'.")
    if d <= 0:
        raise ValueError("La distancia d debe ser positiva.")

    corrientes, posiciones, contribuciones, resultante, campos, campo_resultante = calcular_fuerzas(
        Ia, Ib, Ic, d, objetivo
    )
    imprimir_resumen(corrientes, contribuciones, objetivo, resultante, campos, campo_resultante)
    graficar(corrientes, posiciones, contribuciones, resultante, objetivo, campo_resultante)


def main():
    Ia, Ib, Ic, d, objetivo = recolectar_parametros_interactivos()
    simulacion(Ia=Ia, Ib=Ib, Ic=Ic, d=d, objetivo=objetivo)


if __name__ == "__main__":
    main()
