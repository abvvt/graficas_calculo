import csv
from collections import Counter
import datetime

# Ruta del archivo CSV del SSN
RUTA_ARCHIVO = "C:/Users/abiga/OneDrive/regresion_sismos/SSNMX_catalogo_19000101_20251125_m55_99.csv"

# -----------------------------------------------------------
# 1. Leer archivo CSV y omitir las primeras líneas basura
# -----------------------------------------------------------

def abrir_csv_ssn(ruta):
    """Carga el CSV del SSN, saltando las líneas antes del encabezado real."""
    with open(ruta, encoding="utf-8") as f:
        lineas = f.readlines()

    # Buscar dónde empieza el encabezado real
    indice_header = None
    for i, linea in enumerate(lineas):
        if linea.startswith("Fecha,"):
            indice_header = i
            break

    if indice_header is None:
        raise ValueError("❌ No se encontró una línea de encabezado válida (que empiece con 'Fecha,').")

    # Mantener solo desde el encabezado detectado
    contenido_limpio = lineas[indice_header:]

    reader = csv.DictReader(contenido_limpio)
    return list(reader)

try:
    datos = abrir_csv_ssn(RUTA_ARCHIVO)
except Exception as e:
    print("❌ Error al leer CSV:", e)
    exit()

print("Columnas detectadas:", list(datos[0].keys()))

# -----------------------------------------------------------
# 2. Extraer años desde columna "Fecha"
# -----------------------------------------------------------

años = []
COLUMNA_FECHA = "Fecha"

formatos_fecha = [
    "%Y-%m-%d",               # común
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%m/%d/%Y"
]

for fila in datos:
    fecha_str = fila[COLUMNA_FECHA].strip()

    fecha = None
    for formato in formatos_fecha:
        try:
            fecha = datetime.datetime.strptime(fecha_str, formato)
            break
        except ValueError:
            continue

    if fecha:
        años.append(fecha.year)
    else:
        print(f"⚠️ Fecha no reconocida: {fecha_str}")

# -----------------------------------------------------------
# 3. Contar sismos por año
# -----------------------------------------------------------

conteo_años = Counter(años)

print("\nSismos por año:")
for año in sorted(conteo_años):
    print(f"{año}: {conteo_años[año]}")

X = sorted(conteo_años.keys())
Y = [conteo_años[a] for a in X]

print("\nAños distintos encontrados:", X)
print("Cantidad:", len(X))

# -----------------------------------------------------------
# 4. Validar regresión lineal
# -----------------------------------------------------------

if len(X) < 2:
    print("❌ No hay suficientes años distintos para regresión lineal.")
    exit()

# -----------------------------------------------------------
# 5. Cálculos de regresión lineal
# -----------------------------------------------------------

n = len(X)
sum_x = sum(X)
sum_y = sum(Y)
sum_xy = sum(X[i] * Y[i] for i in range(n))
sum_x2 = sum(x ** 2 for x in X)

denominador = n * sum_x2 - (sum_x ** 2)
if denominador == 0:
    print("❌ Error: denominador de regresión es 0.")
    exit()

a = (n * sum_xy - sum_x * sum_y) / denominador
b = (sum_y - a * sum_x) / n

print("\nPendiente (a):", round(a, 4))
print("Intercepto (b):", round(b, 4))

# -----------------------------------------------------------
# 6. Predicciones
# -----------------------------------------------------------

Y_pred = [a * x + b for x in X]

print("\nPredicciones (primeros 10 valores):")
for i in range(min(10, len(X))):
    print(f"Año {X[i]} → estimado: {round(Y_pred[i], 2)} sismos")

print("\nValores Y reales:", Y)




