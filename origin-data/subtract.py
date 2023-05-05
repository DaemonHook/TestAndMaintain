import pandas as pd

data = pd.read_excel("data.xlsx", 1, header=1, skipfooter=2)

print(data.to_json())