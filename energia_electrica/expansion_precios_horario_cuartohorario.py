import pandas as pd
from pathlib import Path
import datetime
import os
from openpyxl import load_workbook
import openpyxl

#-----------------------------------------------------------------------------
# Obtener la fecha actual
fecha_actual = datetime.datetime.now()
# Extraer el año y el mes actual
año = fecha_actual.year
mes = fecha_actual.strftime("%m")  # Formatea el mes como dos dígitos
# Formatea el día para que siempre tenga dos dígitos
dia = str(fecha_actual.day).zfill(2)
#-----------------------------------------------------------------------------

# Definir la ruta origen de los archivos excel de SERES y DEUDA. -> Sustituir archivos para realizar tarea
# Pedir al usuario que introduzca la ruta origen
path_input = input("Introduce la ruta origen de los archivos Excel: ")

# Convertir la entrada a un objeto Path
path_origen = Path(path_input)

print(f"Ruta introducida: {path_origen}")


# Especificar el path_destino donde se guardará el archivo
path_destino = path_origen

# Generar el nombre del archivo FINAL para los rechazos basado en el año y el mes actual
nombre_archivo = f"{año}{mes}{dia}_PrecioMedioHorarioFinalSumaCompnentes_QH.xlsx"
# Combinar el path_destino con el nombre del archivo para obtener la ruta completa donde se depositará el archivo final
ruta_archivo = os.path.join(path_destino, nombre_archivo)
#-----------------------------------------------------------------------------

# Función para encontrar los archivos necesarios en el path_destino
def encontrar_archivos(path_destino, patrones):
    archivos = {}
    for patron in patrones:
        archivo = list(path_destino.glob(patron))
        if archivo:
            archivos[patron] = archivo[0]
    return archivos

# Patrones de los nombres de los archivos a buscar
patrones = ['export_export_PrecioMedioHorarioFinalSuma*.xlsx']

# Encontrar los archivos necesarios
archivos_encontrados = encontrar_archivos(path_origen, patrones)

# Verificar que se han encontrado los archivos necesarios
if 'export_export_PrecioMedioHorarioFinalSuma*.xlsx' in archivos_encontrados:
    precio_file = archivos_encontrados['export_export_PrecioMedioHorarioFinalSuma*.xlsx']
# Leer los archivos de Excel
precios = pd.read_excel(precio_file, index_col=None)
# Eliminar las primeras 10 filas y resetear el índice

# Usar la nueva primera fila como encabezado y eliminarla del DataFrame
precios.columns = precios.iloc[0]  # Asignar la fila como nombres de columna
precios = precios.iloc[1:].reset_index(drop=True)  # Eliminar la fila duplicada y resetear índice-


precios["datetime"] = pd.to_datetime(precios["datetime"]).dt.tz_localize(None)

# Crear la tabla dinámica
tabla_pivot = pd.pivot_table(
    precios,
    values="value",
    index=["datetime"],
    columns=["name"],
    aggfunc="sum",
    fill_value=0
).reset_index()  # Convertimos el índice en columna

# Asegurar que "datetime" es la primera columna
columnas_ordenadas = ["datetime"] + [col for col in tabla_pivot.columns if col != "datetime"]
tabla_pivot = tabla_pivot[columnas_ordenadas]

# Asegurar que la columna "datetime" sea de tipo datetime
tabla_pivot["datetime"] = pd.to_datetime(tabla_pivot["datetime"])

# Expandir a cuartohorario
df_precios_qh = tabla_pivot.loc[tabla_pivot.index.repeat(4)].reset_index(drop=True)

# Crear la lista de timedelta del mismo tamaño que df_precios_qh
timedeltas = ["0min", "15min", "30min", "45min"] * (len(df_precios_qh) // 4)
df_precios_qh["datetime"] = df_precios_qh["datetime"] + pd.to_timedelta(timedeltas[:len(df_precios_qh)])

# Resetear índice para mejor visualización
tabla_pivot.reset_index(inplace=True)

# Seleccionar y reordenar columnas
df_precios_qh = df_precios_qh[['datetime',
                'Precio medio horario componente mercado diario',
                'Precio medio horario componente restricciones PBF',
                'Precio medio horario componente restricciones tiempo real',
                'Precio medio horario componente reserva de potencia adicional a subir',
                'Precio medio horario componente banda secundaria',
                'Precio medio horario componente saldo P.O.14.6',
                'Precio medio horario componente fallo nominación UPG',
                'Precio medio horario componente servicio de interrumpibilidad',
                'Precio medio horario componente incumplimiento energía de balance',
                'Precio medio horario componente control factor potencia']]

with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
    precios.to_excel(writer, sheet_name='Export', index=False)
    precios.to_excel(writer, sheet_name='Precios', index=False)
    df_precios_qh.to_excel(writer, sheet_name='Precios_QH', index=False)

# Cargar el libro de trabajo con openpyxl
wb = openpyxl.load_workbook(ruta_archivo)

# Acceder a la hoja 'Precios_QH'
worksheet = wb['Precios_QH']

# Ajustar el texto en las celdas de encabezado para que se divida en varias líneas
for cell in worksheet[1]:  # 1 se refiere a la fila de encabezados
    cell.alignment = cell.alignment.copy(wrapText=True)

# Establecer el ancho de las columnas a 19
for col in worksheet.columns:
    max_length = 0
    column = col[0].column_letter  # Obtener la letra de la columna
    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    # Establecer el ancho de columna a 19
    worksheet.column_dimensions[column].width = 23

# Guardar los cambios en el archivo
wb.save(ruta_archivo)