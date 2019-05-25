# Data Import / Processing Class.
#
# Author: Jane, Senior Consultant
# All Rights Reserved. 
# Date: May, 2019
#
# Author: Jane Nikolova
# Occupation: Senior Consultant
# All Rights Reserved. 
# Date: May, 2019

import pandas
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer

# Default Salesforce data import function -
# @ Imports the full data
# @ Transforms to categorical variables
# @ Removes NaNs
# @ Keeps all records.

def allDataForOutcome(filename, yVaribale):
    data = pd.read_csv(filename, delimiter=',' , encoding='latin-1')
    data = pd.DataFrame(data)
    print(data.head())

    #transform to numerical values - 
    #data['ListYear'] = pd.to_numeric(data['ListYear'])
    #data['AssessedValue'] = data['AssessedValue'].astype(float)
    #data['SaleAmount'] = data['SaleAmount'].astype(float)
    #data['SalesRatio'] = data['SalesRatio'].astype(float)
    
    data['ListYear'] = data['ListYear'].fillna(0)
    data['AssessedValue'] = data['AssessedValue'].fillna(0)
    data['SaleAmount'] = data['SaleAmount'].fillna(0)
    data['SalesRatio'] = data['SalesRatio'].fillna(0)

    #Drop the variables which do not add any meaning - 
    data = data.drop(['SerialNumber'], axis=1)#meaningless - its an ID

    #Define the X and Y variables - 
    Y = data[yVaribale]
    X = data
    X = X.drop([yVaribale], axis=1)

    # Fit/Transform - Y var
    number = LabelEncoder()
    Y = number.fit_transform(Y)

    # Adjust / Fill the NA values - 
    X['ResidentialType'] = X['ResidentialType'].fillna('')
    X['NonUseCode'] = X['NonUseCode'].fillna('')
    X['PropertyType'] = X['PropertyType'].fillna('')
    
    # Fit/Transform the X categorical variables -
    number = LabelEncoder()
    X['Town'] = number.fit_transform(X['Town'])
    X['PropertyType'] = number.fit_transform(X['PropertyType'])
    X['ResidentialType'] = number.fit_transform(X['ResidentialType'])
    X['NonUseCode'] = number.fit_transform(X['NonUseCode'])

    #TODO - Exact geolocation - convert to Latitude/Longitude.
    # for now address can be dropped - 
    X = X.drop(['Address'], axis=1)
    
    return [X,Y]

# Default Salesforce data import function with options to transform the Y variable-
# @Imports the full data
# @Transforms to categorical variables
# @Removes NaNs
# @Keeps all records & Drops specified Y variable outcomes.

def dataForDependentVariableByDroppingYOutcomes(filename, yVaribale, dropYOutcome):
    print("to do")
