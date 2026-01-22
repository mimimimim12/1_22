import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드
pate = "./Netflix.csv"
netflix = pd.read_csv("./Netflix.csv")

print(netflix.head())
print(netflix.info())
print(netflix.columns)


