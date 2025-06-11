import os
import pandas as pd
from datetime import datetime, timedelta

# Crear carpeta de salida si no existe
if not os.path.exists('output'):
    os.makedirs('output')

# Lista para almacenar los resultados
resultados = []

# Leer archivos desde la carpeta 'input'
for archivo in os.listdir('input'):
    if archivo.endswith('.csv') or archivo.endswith('.xls') or archivo.endswith('.xlsx'): # recorre todos los archivos desde la carpte input
        # Leer el archivo
        df = pd.read_excel(os.path.join('input', archivo)) if archivo.endswith('.xls') or archivo.endswith('.xlsx') else pd.read_csv(os.path.join('input', archivo), engine='python')
        #Convierte la columna Time a formato de fecha y hora.
        df.columns = df.columns.str.strip()
        df['Time'] = pd.to_datetime(df['Time'])
        df['Date'] = df['Time'].dt.date
        df['Hour'] = df['Time'].dt.time
        #Filtra por tipo del Evento
        for serie in ['FAILED', 'OK']:
            df_serie = df[df['Series'] == serie]

            # Intervalo de dia: 07:00 a 18:00 por fecha
            df_diurno = df_serie[(df_serie['Time'].dt.time >= datetime.strptime('07:00', '%H:%M').time()) &
                                 (df_serie['Time'].dt.time <= datetime.strptime('18:00', '%H:%M').time())]
            # Filtra los registros
            for fecha in df_diurno['Date'].unique():
                df_fecha = df_diurno[df_diurno['Date'] == fecha]
                if not df_fecha.empty:
                    resultados.append([
                        archivo, serie, 'Diurno', '07:00 - 18:00', fecha,
                        df_fecha['Value'].max(),
                        df_fecha['Value'].min(),
                        df_fecha['Value'].mean(),
                        df_fecha['Value'].median()
                    ])

            # Intervalo nocturno: 18:01 del día anterior a 07:00 del día actual
            fechas = sorted(df_serie['Date'].unique())
            for i in range(1, len(fechas)):

                inicio = pd.Timestamp(datetime.combine(fechas[i-1], datetime.strptime('18:01', '%H:%M').time()), tz='America/Mexico_City')
                fin = pd.Timestamp(datetime.combine(fechas[i], datetime.strptime('07:00', '%H:%M').time()), tz='America/Mexico_City')
                df_noche = df_serie[(df_serie['Time'] >= inicio) & (df_serie['Time'] <= fin)]
                if not df_noche.empty:
                    resultados.append([
                        archivo, serie, 'Nocturno', '18:01 - 07:00', fechas[i],
                        df_noche['Value'].max(),
                        df_noche['Value'].min(),
                        df_noche['Value'].mean(),
                        df_noche['Value'].median()
                    ])

# Crear DataFrame con resultados
df_resultados = pd.DataFrame(resultados, columns=[
    'Nombre Archivo', 'Serie', 'Intervalo', 'Rango Horario', 'Fecha',
    'Maximo', 'Minimo', 'Promedio', 'Mediana'
])

# Guardar resultados
df_resultados.to_excel(os.path.join('output', 'resultados_completos.xlsx'), index=False)

print("El procesamiento ha finalizado. Los resultados se han guardado en 'output/resultados_completos.xlsx'.")
