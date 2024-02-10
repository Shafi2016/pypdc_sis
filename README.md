### Installation


```
!pip install git+https://github.com/Shafi2016/pypdc_sis.git
```

### Usage Examples



```python
import pandas as pd
import numpy as np
from pypdc_sis import PDC_SIS
np.random.seed(23) 
import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")

import logging

url = 'https://raw.githubusercontent.com/Shafi2016/pypdc_sis/main/data/google_trends.csv'
df = pd.read_csv(url)

# Extracting the GDP column as the target variable 'Y'
gdp = df['gdpm']

# Extracting the predictors
data = df.iloc[:, 3:83]  # Adjust column indices as per your dataset

# Creating lagged variables up to Lag 3
PredictLag3 = data.assign(**{
    f"{col}_lag{i}": data[col].shift(i) for i in range(1, 4) for col in data
}).reindex(columns=sorted(data.columns.tolist() + [f"{col}_lag{i}" for i in range(1, 4) for col in data], key=lambda x: (len(x), x)))

# Adjusting 'Xwl' to exclude rows with NAs introduced by lagging, ensuring alignment with 'Y'
Xwl = PredictLag3.dropna().to_numpy()

# Adjust 'gdp' to match the reduced dataset size
Y = gdp[3:].to_numpy()  # Excluding the first 3 rows due to NA from lagging

# Apply the function
results = PDC_SIS(Xwl, Y, lags=3, top_n=10)

#print(results['indices'])

# Output the data frame of lagged versions of Y
#print(results['Y_conditioning_df'].head())


selected_indices = results['indices']

# Retrieve the original names for the selected columns
original_column_names = PredictLag3.dropna().columns[selected_indices]

# Select the columns from PredictLag3 based on selected indices
selected_columns_df = PredictLag3[original_column_names]

# View the first few rows of the combined data frame
selected_columns_df.head()

```
### Reference

**Title:** Targeting Predictors Via Partial Distance Correlation With Applications to Financial Forecasting

**Authors:** Kashif Yousuf and Yang Feng

[Read the paper here](https://yangfeng.hosting.nyu.edu/publication/yousuf-2018-partial/yousuf-2018-partial.pdf)
