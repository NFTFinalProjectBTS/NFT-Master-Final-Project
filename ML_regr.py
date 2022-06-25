#Uploading the file with quotes NFT
df = pd.read_csv("data.csv", sep = ',')
#remove extra columns
df = df.drop(columns=['Unnamed: 0','Unnamed: 0_x', 'Unnamed: 0_y'])

def choose_ML(df):
    #Selection of the ML model with the best parameters
    
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
    
    #
    tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42)
    tpot.fit(X_train, y_train)
    print(tpot.score(X_test, y_test))

def ML(df):
    
    #Libraries
    import matplotlib.pyplot as plt
    import numpy as np 
    import pandas as pd 
    import seaborn as sns
    from sklearn import preprocessing
    import xgboost as xgb
    import sklearn.metrics as metrics
    from sklearn.model_selection import train_test_split
    
    #Part I Prepare data
    
    #Сonfidence interval
    Q1 = df['Price'].quantile(0.25)
    Q3 = df['Price'].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5*IQR
    lim_sup = Q3 + 1.5*IQR
    df = df[(df['Price']>lim_inf) & (df['Price']<lim_sup)]
    
    #Looking at the correlation of variables
    #f, ax = plt.subplots(figsize=(12, 10))
    #sns.heatmap(df.corr(), square=True, annot=True, cbar=True, ax=ax)
    
    #Create dummy variables
    df = pd.get_dummies(df, columns=['Name_collection'],drop_first=True)

    #Standardizing data
    s_scaler = preprocessing.StandardScaler()
    df_sc = s_scaler.fit_transform(df)
    col_names = list(df.columns)
    df_sc = pd.DataFrame(df_sc, columns = col_names)

    #Graphs 1 и 2

    #'Before standardization'
    #fig, (ax1) = plt.subplots(ncols = 1, figsize = (10, 8))
    #ax1.set_title('Before standardization Price NFT and ETH')
    #sns.kdeplot(df['Price'], ax = ax1)
    #sns.kdeplot(df['close_price_eth'], ax = ax1)
    #'After standardization'
    #fig, (ax1) = plt.subplots(ncols = 1, figsize = (10, 8))
    #ax1.set_title('After standardization')
    #sns.kdeplot(df_sc['Price'], ax = ax1)
    #sns.kdeplot(df_sc['close_price_eth'], ax = ax1)

    #Part II ML
    
    #We form a dependent variable
    X = df_sc.drop('Price',axis=1).values
    Y = df_sc['Price']
    
    #Separate data into test and training
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)
    
    #Machine learning model
    #Chose this model based on TPOTRegressor
    xgbr = xgb.XGBRegressor(learning_rate=0.5, max_depth=3, min_child_weight=10, n_estimators=100, n_jobs=1, objective="reg:squarederror", subsample=1.0, verbosity=0) 
    xgbr.fit(X_train, y_train)

    #Evaluation of training data
    score = xgbr.score(X_train, y_train)  
    print("Training score: ", score)
    
    #Prediction
    prediction = xgbr.predict(X_test)

    #Test Data Evaluation
    print('Test Score:')
    print('MAE', metrics.mean_absolute_error(y_test, prediction))
    print('MSE', metrics.mean_squared_error(y_test, prediction,squared = True))
    print('RMSE', metrics.mean_squared_error(y_test, prediction,squared = False))
    print('R2 score', metrics.r2_score(y_test, prediction))
    
    #Graphs 3 "Test and predicted data after standardization"
    x_ax = range(len(y_test))
    plt.plot(x_ax, y_test, label="original")
    plt.plot(x_ax, prediction, label="predicted")
    plt.title("Test and predicted data")
    plt.legend()
    plt.show()

ML(df)