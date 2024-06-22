import sys
import getopt
import wget
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn import preprocessing
import joblib
import os

global ROOT_DIR; 
ROOT_DIR= os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
print(ROOT_DIR)

def usage():
    print('Automate download data in Python')
    print()
    print("NAME")
    print('      Question 2 section A')
    print("SYNOPSIS")
    print('      q2_a_cli.py {--help | -h} {--download | -d}')
    print("DESCRIPTION")
    print('   --help -h')
    print('      display help page')
    print('   --download -d')
    print('      download data from Github')   
    print("AUTHORS")
    print(' This python script was written by Mark Yean Tuck Ming <yeanmark@gmail.com> ')
    sys.exit(0)
    
    
def download_allow():
    test_url="https://gist.githubusercontent.com/mahadirz/c1fed0d25c8db3a406a62fffd0560446/raw/bf2f5f75a90cc63daea119c9d415b262f5e16ac4/test.csv"
    train_url="https://gist.githubusercontent.com/mahadirz/c1fed0d25c8db3a406a62fffd0560446/raw/bf2f5f75a90cc63daea119c9d415b262f5e16ac4/train.csv"
    
    dir_p = os.path.expanduser(ROOT_DIR+"/Web_data_engineering/data_cli/")    
    file = test_url.split("/")[-1]
    file2 = train_url.split("/")[-1]
    train_csv=os.path.join(dir_p, file2)
    test_csv=os.path.join(dir_p, file)    
    if os.path.exists(os.path.join(dir_p, file)):
        os.remove(test_csv)
        os.remove(train_csv)
        wget.download(url=test_url, out=dir_p) 
        wget.download(url=train_url, out=dir_p) 
    elif os.path.exists(os.path.join(dir_p, file2)):
        os.remove(test_csv)
        os.remove(train_csv)
        wget.download(url=test_url, out=dir_p) 
        wget.download(url=train_url, out=dir_p) 
    else:        
        wget.download(url=test_url, out=dir_p) 
        wget.download(url=train_url, out=dir_p) 
    # wget.download(test_url, out=ROOT_DIR+"/temp_data/")

def read_transform():
    df=pd.read_csv(ROOT_DIR+'/Web_data_engineering/data_cli/train.csv')
    df_test= pd.read_csv(ROOT_DIR+'/Web_data_engineering/data_cli/test.csv')
    df=df.iloc[:,1:]
    df_test=df_test.iloc[:,1:]
    scaler = preprocessing.MinMaxScaler()
    df_trans = pd.DataFrame(scaler.fit_transform(df),columns=df.columns)
    df_trans_test=pd.DataFrame(scaler.transform(df_test),columns=df_test.columns)
    return df_trans,df_trans_test,scaler

def modeling(df_trans):
    X_train=df_trans[['x1','x2']].values
    y_train=df_trans['y']
    regressor = LinearRegression() 
    regressor.fit(X_train, y_train)   
    return regressor

def dumpfile(scaler,model):
    dir_p = os.path.expanduser(ROOT_DIR+"/Web_data_engineering/data_cli/")
    scaler_p=os.path.join(dir_p, "scaler.gz")
    model_p=os.path.join(dir_p, "model.pkl")
    if os.path.exists(scaler_p):
        os.remove(scaler_p)
        os.remove(model_p)
        joblib.dump(scaler,scaler_p)
        joblib.dump(model, model_p) 
    elif os.path.exists(model_p):
        os.remove(scaler_p)
        os.remove(model_p)
        joblib.dump(scaler,scaler_p)
        joblib.dump(model, model_p) 
    else:        
        joblib.dump(scaler,scaler_p)
        joblib.dump(model, model_p)
    
    return 0

def metrc(df_trans_test,y_pred):
    score=metrics.r2_score(df_trans_test['y'],y_pred)
    print('r2 socre is' ,score)
    print('mean_sqrd_error is',metrics.mean_squared_error(df_trans_test['y'],y_pred))
    print('root_mean_squared error of is ',np.sqrt(metrics.mean_squared_error(df_trans_test['y'],y_pred)))
    return 0
    
def main():   
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd",
                                   ['help', 'download'])
        d_status=0
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
            elif o in ("-d", "--download"):
                d_status = int(1)            
            else:
                assert False, "Unhandled Option"
    except getopt.GetoptError as err:
        print(str(err))
    if d_status == 1:
        download_allow()
        df_trans, df_trans_test,scaler =read_transform()
        mdl=modeling(df_trans)
        x_test=df_trans_test[['x1','x2']] 
        y_pred=mdl.predict(x_test)
        metrc(df_trans_test,y_pred)
        dumpfile(scaler,mdl)        
    else:
        df_trans, df_trans_test,scaler =read_transform()
        mdl=modeling(df_trans)
        x_test=df_trans_test[['x1','x2']] 
        y_pred=mdl.predict(x_test)
        metrc(df_trans_test,y_pred)
        dumpfile(scaler,mdl)
main()
