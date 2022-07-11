import numpy as np 
import pandas as pd 

#Uploading the file with quotes NFT
df = pd.read_csv("data.csv", sep = ',')
#remove extra columns
df = df.drop(columns=['Unnamed: 0','Unnamed: 0_x', 'Unnamed: 0_y'])

def choose_ML(df):
    #Selection of the ML model with the best parameters
    #Select the best algorithm for our model, 
    # we  to use the TPOT algorithm, which stands 
    # for Tree-based Pipeline Optimization Tool. 
    # TPOT is a Python Automated Machine Learning tool 
    # that optimises machine learning pipelines using genetic programming
    
    #Libraries
    from tpot import TPOTRegressor
    import matplotlib.pyplot as plt
    import numpy as np 
    import pandas as pd 
    import seaborn as sns
    from sklearn import preprocessing
    import xgboost as xgb
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import train_test_split
    
    #Part I Prepare data
    
    #Сonfidence interval
    Q1 = df['Price'].quantile(0.25)
    Q3 = df['Price'].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5*IQR
    lim_sup = Q3 + 1.5*IQR
    df = df[(df['Price']>lim_inf) & (df['Price']<lim_sup)]
    
    #Create dummy variables
    df = pd.get_dummies(df, columns=['Name_collection'],drop_first=True)

    #Standardizing data
    s_scaler = preprocessing.StandardScaler()
    df_sc = s_scaler.fit_transform(df)
    col_names = list(df.columns)
    df_sc = pd.DataFrame(df_sc, columns = col_names) 
    
    #Part II Model selection
    
    #We form a dependent variable
    X = df_sc.drop('Price',axis=1).values
    Y = df_sc['Price']
    
    #Separate data into test and training
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)
    
    #TPOT algorithm Launch
    tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42)
    tpot.fit(X_train, y_train)
    print(tpot.score(X_test, y_test))

choose_ML(df)