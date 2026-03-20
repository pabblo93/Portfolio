"""
==============================================================================
 CONVERSOR CURVA HORARIA → CUARTOHORARIA
 Según Anexo 11 de la PO 10.5 (BOE-A-2025-6693)
 
 Método: Interpolación cúbica (spline) con conservación de energía horaria.
==============================================================================
"""

import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from pathlib import Path
from datetime import timedelta
import sys
import os


# ============================================================================
# 1. ENTRADA INTERACTIVA
# ============================================================================

def solicitar_datos():
    """Solicita al usuario los datos necesarios por consola."""
    
    print("=" * 70)
    print(" CONVERSOR HORARIA → CUARTOHORARIA (Anexo 11 PO 10.5)")
    print("=" * 70)
    print()
    
    # --- Fichero de entrada ---
    while True:
        fichero = input("📂 Ruta del fichero de curva horaria (.xls/.xlsx/.csv): ").strip()
        fichero = fichero.strip('"').strip("'")
        
        if os.path.isfile(fichero):
            print(f"   ✅ Fichero encontrado: {fichero}")
            break
        else:
            print(f"   ❌ No se encuentra el fichero. Verifica la ruta.")
    
    # --- Valor frontera: última hora mes anterior ---
    print()
    print("─" * 70)
    print("📌 VALOR FRONTERA: Última hora del mes ANTERIOR")
    print("   (Energía kWh de la última hora del mes previo al fichero)")
    print("   Si no lo tienes, pulsa ENTER y se usará la primera hora del mes.")
    print("─" * 70)
    
    while True:
        valor_anterior_str = input("   Valor (kWh) o ENTER para omitir: ").strip()
        
        if valor_anterior_str == "":
            energia_anterior = None
            print("   ℹ️  Se usará la primera hora del mes como aproximación.")
            break
        else:
            try:
                energia_anterior = float(valor_anterior_str.replace(",", "."))
                print(f"   ✅ Valor registrado: {energia_anterior:.4f} kWh")
                break
            except ValueError:
                print("   ❌ Introduce un número válido (ej: 125.3) o pulsa ENTER.")
    
    # --- Valor frontera: primera hora mes siguiente ---
    print()
    print("─" * 70)
    print("📌 VALOR FRONTERA: Primera hora del mes SIGUIENTE")
    print("   (Energía kWh de la primera hora del mes posterior al fichero)")
    print("   Si no lo tienes (lo habitual en consumos futuros), pulsa ENTER")
    print("   y se usará la última hora del mes.")
    print("─" * 70)
    
    while True:
        valor_siguiente_str = input("   Valor (kWh) o ENTER para omitir: ").strip()
        
        if valor_siguiente_str == "":
            energia_siguiente = None
            print("   ℹ️  Se usará la última hora del mes como aproximación.")
            break
        else:
            try:
                energia_siguiente = float(valor_siguiente_str.replace(",", "."))
                print(f"   ✅ Valor registrado: {energia_siguiente:.4f} kWh")
                break
            except ValueError:
                print("   ❌ Introduce un número válido (ej: 140.0) o pulsa ENTER.")
    
    # --- Fichero de salida ---
    print()
    nombre_base = Path(fichero).stem
    salida_default = f"{nombre_base}_QH.xlsx"
    
    salida = input(f"💾 Fichero de salida (ENTER para '{salida_default}'): ").strip()
    if salida == "":
        salida = salida_default
    
    print(f"   ✅ Salida: {salida}")
    print()
    
    return fichero, energia_anterior, energia_siguiente, salida


# ============================================================================
# 2. LECTURA DE LA CURVA HORARIA
# ============================================================================

def leer_curva_horaria(filepath: str) -> pd.DataFrame:
    """
    Lee el fichero de curva horaria y devuelve un DataFrame con columnas:
    - datetime: timestamp de inicio de cada hora
    - energia_kwh: valor de energía de esa hora
    
    Formatos soportados:
    - SIPS distribuidora (fecha+hora separadas o datetime en una columna)
    - Columnas: fecha, cups, energia activa, energia reactiva, etc.
    """
    ext = Path(filepath).suffix.lower()
    
    if ext == ".xlsx":
        df_raw = pd.read_excel(filepath, engine="openpyxl")
    elif ext == ".xls":
        df_raw = pd.read_excel(filepath, engine="xlrd")
    elif ext == ".csv":
        df_raw = pd.read_csv(filepath, sep=";", decimal=",")
    else:
        raise ValueError(f"Formato no soportado: {ext}")
    
    # Normalizar nombres de columnas
    df_raw.columns = [str(c).strip().lower() for c in df_raw.columns]
    
    print(f"📄 Fichero leído: {filepath}")
    print(f"   Columnas encontradas: {list(df_raw.columns)}")
    print(f"   Filas: {len(df_raw)}")
    
    # --- Detectar columna de fecha ---
    col_fecha = None
    for c in df_raw.columns:
        if any(k in c for k in ["fecha", "date", "dia", "día", "timestamp"]):
            col_fecha = c
            break
    
    # --- Detectar columna de hora (puede no existir) ---
    col_hora = None
    for c in df_raw.columns:
        if any(k in c for k in ["hora", "hour", "periodo"]):
            col_hora = c
            break
    
    # --- Detectar columna de energía ACTIVA (priorizar "activa" exacta) ---
    col_energia = None
    # Primero buscar "energia activa" o "activa" de forma exacta
    for c in df_raw.columns:
        if "activa" in c and "reactiva" not in c and "capacitiva" not in c:
            col_energia = c
            break
    
    # Si no se encontró, buscar términos más genéricos
    if col_energia is None:
        for c in df_raw.columns:
            if any(k in c for k in ["consumo", "energy", "kwh", "magnitud", "valor"]):
                col_energia = c
                break
    
    if col_fecha is None or col_energia is None:
        print(f"\n   ⚠️  No se detectaron automáticamente las columnas necesarias.")
        print(f"   Columnas disponibles:")
        for i, c in enumerate(df_raw.columns):
            print(f"      [{i}] {c}")
        
        idx_fecha = int(input("\n   Índice de la columna de FECHA: "))
        idx_energia = int(input("   Índice de la columna de ENERGÍA: "))
        col_fecha = df_raw.columns[idx_fecha]
        col_energia = df_raw.columns[idx_energia]
        
        tiene_hora = input("   ¿Hay columna separada de HORA? (s/n): ").strip().lower()
        if tiene_hora == "s":
            idx_hora = int(input("   Índice de la columna de HORA: "))
            col_hora = df_raw.columns[idx_hora]
    
    print(f"   → Fecha: '{col_fecha}', Hora: '{col_hora}', Energía: '{col_energia}'")
    
    # --- Construir DataFrame ---
    df = pd.DataFrame()
    df["energia_kwh"] = pd.to_numeric(
        df_raw[col_energia].astype(str).str.replace(",", "."), errors="coerce"
    ).fillna(0.0)
    
    # --- Construir datetime ---
    if col_hora is not None:
        # Formato con fecha y hora en columnas separadas
        df["fecha"] = pd.to_datetime(df_raw[col_fecha], format="%d/%m/%Y %H:%M", errors="coerce")
        df["hora"] = pd.to_numeric(df_raw[col_hora], errors="coerce").astype(int)
        
        # Horas 1-24 → 0-23
        if df["hora"].max() == 24 and df["hora"].min() == 1:
            df["hora"] = df["hora"] - 1
        
        df["datetime"] = df["fecha"] + pd.to_timedelta(df["hora"], unit="h")
    else:
        # La hora viene DENTRO de la columna fecha (datetime completo)
        df["datetime"] = pd.to_datetime(df_raw[col_fecha], format="%d/%m/%Y %H:%M", errors="coerce")
        
        if df["datetime"].isna().all():
            # Intentar otros formatos
            df["datetime"] = pd.to_datetime(df_raw[col_fecha], errors="coerce")
    
    df = df.dropna(subset=["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    
    # --- Mostrar muestra ---
    print(f"\n   📋 Muestra de datos leídos:")
    print(f"   {'Datetime':<25} {'Energía (kWh)':>15}")
    print(f"   {'─' * 25} {'─' * 15}")
    for _, row in df.head(5).iterrows():
        print(f"   {str(row['datetime']):<25} {row['energia_kwh']:>15.4f}")
    print(f"   ... ({len(df)} registros en total)")
    
    print(f"\n   ✅ Periodo: {df['datetime'].min()} → {df['datetime'].max()}")
    print(f"   ✅ Horas leídas: {len(df)}")
    print(f"   ✅ Energía total: {df['energia_kwh'].sum():,.4f} kWh")
    
    return df[["datetime", "energia_kwh"]]


# ============================================================================
# 3.0 CURVA HORARIA H -> QH (APLANADA)
# ============================================================================
def añadir_curva_plana(df_h: pd.DataFrame, df_qh: pd.DataFrame) -> pd.DataFrame:
    """
    Añade al DataFrame cuartohorario una columna con la curva plana (Eh/4).
    
    Parámetros:
    - df_h: curva horaria original
    - df_qh: curva cuartohoraria (resultado BOE)
    
    Devuelve:
    - df_qh con columna 'energia_plana_kwh'
    """

    # Copia para no modificar original
    df_h_temp = df_h.copy()

    # Calcular Eh/4
    df_h_temp["energia_plana"] = df_h_temp["energia_kwh"] / 4

    # Expandir cada hora a 4 cuartos
    df_plana = df_h_temp.loc[df_h_temp.index.repeat(4)].copy()
    df_plana = df_plana.reset_index(drop=True)

    # Alinear timestamps con QH
    df_plana["datetime"] = df_qh["datetime"].values

    # Añadir columna al resultado
    df_qh = df_qh.copy()
    df_qh["energia_plana_kwh"] = df_plana["energia_plana"].values

    return df_qh
# ============================================================================
# 3. ALGORITMO DE ESTIMACIÓN H → QH (Anexo 11 PO 10.5)
# ============================================================================

def convertir_horaria_a_cuartohoraria(
    df_horaria: pd.DataFrame,
    energia_hora_anterior: float = None,
    energia_hora_siguiente: float = None
) -> pd.DataFrame:

    valores = df_horaria["energia_kwh"].values.astype(float)
    timestamps = df_horaria["datetime"].values
    n = len(valores)

    resultados = []

    for i in range(n):

        Eh = valores[i]

        # Valores vecinos
        Eh_1 = valores[i - 1] if i > 0 else (energia_hora_anterior or Eh)
        Eh1 = valores[i + 1] if i < n - 1 else (energia_hora_siguiente or Eh)

        E_prima = []

        # =========================
        # 🔹 INTERPOLACIÓN BOE (2 tramos)
        # =========================
        for q in range(4):
            x_q = 0.125 + 0.25 * q

            if q < 2:
                # Q1, Q2 → entre Eh-1 y Eh
                val = (1/4) * (
                    Eh_1 + (Eh - Eh_1) * ((x_q + 0.5) / 1.0)
                )
            else:
                # Q3, Q4 → entre Eh y Eh+1
                val = (1/4) * (
                    Eh + (Eh1 - Eh) * ((x_q - 0.5) / 1.0)
                )

            E_prima.append(val)  # 👈 IMPORTANTE: dentro del bucle

        # =========================
        # 🔴 NORMALIZACIÓN BOE
        # =========================
        suma = sum(E_prima)

        if suma != 0:
            E_norm = [e * Eh / suma for e in E_prima]
        else:
            E_norm = [0, 0, 0, 0]

        # =========================
        # 🔴 REDONDEO BOE
        # =========================
        Q = [0, 0, 0, 0]

        # Q1, Q2, Q3
        for q in range(3):
            Q[q] = int(round(E_norm[q]))

        # Q4 = ajuste
        Q[3] = int(Eh - sum(Q[:3]))

        # =========================
        # 🔴 AJUSTES ESPECIALES BOE
        # =========================
        if Q[3] < 0:
            Q[3] = 0
            Q[2] = int(Eh - sum(Q[:3]))

        if Q[3] > Eh:
            Q[3] = int(Eh)
            Q[2] = int(Eh - sum(Q[:3]))

        # =========================
        # Guardar resultados
        # =========================
        ts_base = pd.Timestamp(timestamps[i])

        for q in range(4):
            resultados.append({
                "datetime": ts_base + timedelta(minutes=15 * q),
                "energia_kwh": Q[q]
            })

    return pd.DataFrame(resultados)




# ============================================================================
# 4. EXPORTAR RESULTADO
# ============================================================================

def exportar_resultado(
    df_qh: pd.DataFrame,
    filepath: str,
    energia_ant: float = None,
    energia_sig: float = None
):
    """Exporta la curva cuartohoraria a Excel con resumen de fronteras."""

    df_export = df_qh.copy()

    df_export["fecha"] = df_export["datetime"].dt.date
    df_export["hora"] = df_export["datetime"].dt.strftime("%H:%M")

    df_export = df_export[
        ["datetime", "fecha", "hora", "energia_kwh", "energia_plana_kwh"]
    ]

    df_export.columns = [
        "Timestamp",
        "Fecha",
        "Hora",
        "Energía BOE (kWh)",
        "Energía Plana (kWh)"
    ]

    # (opcional pero muy útil)
    df_export["Diferencia"] = (
        df_export["Energía BOE (kWh)"] - df_export["Energía Plana (kWh)"]
    )

    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:

        # Dejar espacio arriba
        df_export.to_excel(writer, index=False, sheet_name="Curva QH", startrow=7)

        ws = writer.sheets["Curva QH"]

        # =========================
        # 🔵 BLOQUE RESUMEN
        # =========================
        ws["A1"] = "CONVERSIÓN HORARIA → CUARTOHORARIA"
        ws["A2"] = "Método: Anexo 11 PO 10.5 (BOE)"

        ws["A4"] = "Frontera mes anterior (kWh):"
        ws["B4"] = energia_ant if energia_ant is not None else "Usada primera hora"

        ws["A5"] = "Frontera mes siguiente (kWh):"
        ws["B5"] = energia_sig if energia_sig is not None else "Usada última hora"

        ws["A6"] = "Energía total BOE (kWh):"
        ws["B6"] = df_export["Energía BOE (kWh)"].sum()

        ws["A7"] = "Energía total plana (kWh):"
        ws["B7"] = df_export["Energía Plana (kWh)"].sum()

        # =========================
        # 🔹 FORMATO
        # =========================
        ws.column_dimensions["A"].width = 22
        ws.column_dimensions["B"].width = 16
        ws.column_dimensions["C"].width = 10
        ws.column_dimensions["D"].width = 18
        ws.column_dimensions["E"].width = 18
        ws.column_dimensions["F"].width = 14

    print(f"\n💾 Fichero exportado: {filepath}")
    print(f"   Registros: {len(df_export)}")


# ============================================================================
# 5. EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    
    try:
        # 1. Pedir datos
        fichero, energia_ant, energia_sig, salida = solicitar_datos()
        
        # 2. Leer curva horaria
        df_h = leer_curva_horaria(fichero)
        
        df_qh = convertir_horaria_a_cuartohoraria(df_h, energia_ant, energia_sig)

        # 👉 añadir curva plana
        df_qh = añadir_curva_plana(df_h, df_qh)
        
        # 4. Exportar
        exportar_resultado(df_qh, salida, energia_ant, energia_sig)
        
        print("\n" + "=" * 70)
        print(" ✅ PROCESO COMPLETADO CON ÉXITO")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print()
        input("Pulsa ENTER para salir...")