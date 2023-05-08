import pandas as pd

df = pd.read_excel("data.xlsx", 1, header=1, skipfooter=2)

print(df.to_json(orient='records'))