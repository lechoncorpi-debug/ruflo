import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "actividad3-inventarios")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

# ---------------- Chart 1: ABC Pareto ----------------
names = [
    "Smartphone 5G", "Laptop 14\"", "TV OLED 55\"", "Tablet 10\"",
    "Audífonos ANC", "Smartwatch", "Cámara seg.", "Cargadores GaN",
    "Bocina BT", "Cables y kits",
]
values = [11.268, 4.515, 2.310, 1.650, 1.080, 0.935, 0.510, 0.504, 0.324, 0.280]  # $M
classes = ["A", "A", "B", "B", "B", "C", "C", "C", "C", "C"]
total = sum(values)
cum = np.cumsum(values) / total * 100

colors = ["#C0392B" if c == "A" else ("#E67E22" if c == "B" else "#2471A3") for c in classes]

fig, ax1 = plt.subplots(figsize=(9, 4.4))
bars = ax1.bar(range(len(names)), values, color=colors, width=0.68, zorder=3)
ax1.set_ylabel("Valor anual de consumo (millones USD)")
ax1.set_xticks(range(len(names)))
ax1.set_xticklabels(names, rotation=30, ha="right", fontsize=9)
ax1.set_ylim(0, max(values) * 1.2)
ax1.tick_params(axis="y", labelcolor="#333333")

ax2 = ax1.twinx()
ax2.plot(range(len(names)), cum, marker="o", color="#17202A", linewidth=2, zorder=4)
ax2.set_ylabel("Porcentaje acumulado (%)", color="#17202A")
ax2.set_ylim(0, 105)
ax2.axhline(70, color="#C0392B", linestyle="--", linewidth=1, alpha=0.7)
ax2.axhline(90, color="#E67E22", linestyle="--", linewidth=1, alpha=0.7)
ax2.text(9.1, 72, "A = 70%", color="#C0392B", fontsize=8)
ax2.text(9.1, 88, "B = 90%", color="#E67E22", fontsize=8)
ax2.tick_params(axis="y", labelcolor="#17202A")

for i, (v, c) in enumerate(zip(values, cum)):
    ax1.text(i, v + 0.15, f"{v:.2f}", ha="center", fontsize=8, color="#1a1a1a")
    ax2.text(i, c + 2.5, f"{c:.0f}%", ha="center", fontsize=7.5, color="#17202A")

ax1.set_title("Análisis ABC (Pareto) del portafolio de XYZ — valor anual de consumo", fontsize=11, weight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_pareto.png"), dpi=200)
plt.close(fig)

# ---------------- Chart 2: Demand forecast ----------------
months = np.arange(1, 19)

sku1 = {"hist": [1850, 1780, 1920, 1950, 2010, 2050, 1980, 2100, 2150, 2200, 2450, 2600],
        "a": 1690.30, "b": 60.98, "name": "Flagship 5G Smartphone", "mape": 3.44}
sku2 = {"hist": [420, 390, 410, 430, 460, 480, 520, 560, 510, 540, 620, 680],
        "a": 352.12, "b": 23.01, "name": "Ultra-Slim Business Laptop 14\"", "mape": 4.62}

fig, axes = plt.subplots(2, 1, figsize=(9, 7.2))
for ax, s in zip(axes, [sku1, sku2]):
    trend = [s["a"] + s["b"] * m for m in months]
    ax.plot(months[:12], s["hist"], marker="o", color="#2471A3", linewidth=2, label="Demanda histórica")
    ax.plot(months, trend, color="#E67E22", linewidth=2, linestyle="-", label="Línea de tendencia (ajuste)")
    ax.plot(months[12:], trend[12:], marker="s", color="#C0392B", linewidth=0, ms=6, linestyle="--", label="Pronóstico (meses 13–18)")
    ax.plot(months[11:13], trend[11:13], color="#C0392B", linewidth=2, linestyle="--")
    ax.axvline(12.5, color="#7F8C8D", linestyle=":", linewidth=1.3)
    ax.text(12.6, ax.get_ylim()[0], "  → Pronóstico", color="#C0392B", fontsize=8, va="bottom")
    ax.set_title(s["name"] + f"  (MAPE del ajuste: {s['mape']:.1f}%)", fontsize=10.5, weight="bold")
    ax.set_ylabel("Unidades / mes")
    ax.set_xticks(months)
    ax.set_xlabel("Mes")
    ax.legend(fontsize=8.5, loc="upper left")

fig.suptitle("Pronóstico de demanda con regresión lineal de tendencia (histórico 12 meses + 6 meses proyectados)", fontsize=12, weight="bold", y=0.995)
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(os.path.join(OUT, "fig_forecast.png"), dpi=200)
plt.close(fig)

print("Charts written to", OUT)
print(os.listdir(OUT))
