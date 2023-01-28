# SP500_Predictor
S&P500 Predictor based percentage change

## Our method
Based on EDA, we can see that percentage change of each ticker will have a better correlation, and to match the problem is to predict that the change of this ticker will affect the following stocks as follows: any. Therefore, we will use the 14-day percentage change along with the ticker and category as the training data. To ensure consistency, we will encode the stock ticker as well as the category.

Applying CNN1D and using activation is tanh (because tanh falls in the range (-1,1), because stock cannot double after 1 day)

We will use the feature extracted from the last layer as the basis to calculate the correlation between stocks.

## Step-by-step instruction

### Step 1
- Install Streamlit, Pyvis and NetworkX packages (See `requirements.txt`)

### Step 2
- Open CLI and execute `python crawldata.py`

### Step 3
- Open `model.ipynb` and run all

### Step 4
- In CLI, execute `streamlit run app.py`

## Inference instruction
Run step 4 above, in CLI, execute `streamlit run app.py`
