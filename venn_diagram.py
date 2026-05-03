import matplotlib.pyplot as plt
from matplotlib_venn import venn2


def crear_venn_por_similitud(porcentaje, output_path="venn_diagram.png"):
    """crea diagrama de venn basado en el porcentaje de similitud"""

    # convertir porcentaje a valores proporcionales para venn2
    interseccion = porcentaje
    unico_cada_lado = 100 - porcentaje

    # tonos degradados de azul: claro para unico, medio para otro, oscuro para comun
    color_unico_1 = "#a8d5e2"
    color_unico_2 = "#6baed6"
    color_comun = "#2171b5"

    # crear figura mas pequena con fondo transparente
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    # venn diagram
    v = venn2(
        subsets=(unico_cada_lado, unico_cada_lado, interseccion),
        set_labels=("Documento 1", "Documento 2"),
        ax=ax
    )

    # aplicar colores degradados
    patch_10 = v.get_patch_by_id("10")
    patch_01 = v.get_patch_by_id("01")
    patch_11 = v.get_patch_by_id("11")

    if patch_10:
        patch_10.set_color(color_unico_1)
        patch_10.set_alpha(0.9)
    if patch_01:
        patch_01.set_color(color_unico_2)
        patch_01.set_alpha(0.9)
    if patch_11:
        patch_11.set_color(color_comun)
        patch_11.set_alpha(0.9)

    # labels con los valores
    label_10 = v.get_label_by_id("10")
    label_01 = v.get_label_by_id("01")
    label_11 = v.get_label_by_id("11")

    if label_10:
        label_10.set_text(f"{unico_cada_lado:.0f}%\nunico")
    if label_01:
        label_01.set_text(f"{unico_cada_lado:.0f}%\nunico")
    if label_11:
        label_11.set_text(f"{interseccion:.0f}%\ncomun")

    # titulo
    ax.set_title(
        f"Similitud: {porcentaje}%",
        fontsize=14,
        fontweight="bold"
    )

    # guardar con fondo transparente
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", transparent=True)
    plt.close()

    return output_path
