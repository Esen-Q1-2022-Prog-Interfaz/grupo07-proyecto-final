import pandas as pd
#needed pip install pandas & pip install openpyxl
archivo = "C:\\Users\\ADMIN\Desktop\\Proyecto Final\\DETALLE DE VEHICULOS.xlsx"
df = pd.read_excel(archivo, sheet_name='Hoja1')
print(df)
