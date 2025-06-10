import os
import pandas as pd

# Crear carpeta de salida si no existe
if not os.path.exists('output'):
    os.makedirs('output')

# Lista para almacenar los resultados
resultados = []
# Leer archivos Excel desde la carpeta 'input'
for archivo in os.listdir('input'):
    if archivo.endswith('.csv'):
        # Leer el archivo Excel
        df = pd.read_csv(os.path.join('input', archivo), sep=None, engine='python')
        #df = pd.read_csv(os.path.join('input', archivo), encoding='utf-8-sig', sep=None, engine='python')

        df.columns = df.columns.str.strip()

        print(df.columns)

        # Calcular estadísticas para 'OK'
        df_ok = df[df['Series'] == 'OK']
        
        resultados.append([archivo, 'OK', 'Media', df_ok['Value'].mean()])
        resultados.append([archivo, 'OK', 'Maximo', df_ok['Value'].max()])
        resultados.append([archivo, 'OK', 'Minimo', df_ok['Value'].min()])
        
        # Calcular estadísticas para 'FAILED'
        df_failed = df[df['Series'] == 'FAILED']
        resultados.append([archivo, 'FAILED', 'Media', df_failed['Value'].mean()])
        resultados.append([archivo, 'FAILED', 'Maximo', df_failed['Value'].max()])
        resultados.append([archivo, 'FAILED', 'Minimo', df_failed['Value'].min()])


# Crear un DataFrame con los resultados
df_resultados = pd.DataFrame(resultados, columns=['Nombre Archivo', 'Serie', 'Tipo de Cálculo', 'Valor'])

# Guardar los resultados en un archivo Excel en la carpeta 'output'
df_resultados.to_excel(os.path.join('output', 'resultados.xlsx'), index=False)

print("El procesamiento ha finalizado. Los resultados se han guardado en 'output/resultados.xlsx'.")


