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
from dateutil import parser

# Default Salesforce data import function -
# @ Imports the full data
# @ Transforms to categorical variables
# @ Removes NaNs
# @ Keeps all records.

def allDataForOutcome(filename, yVaribale):
    data = pd.read_csv(filename, delimiter=',' , encoding='latin-1')
    data = data.dropna(subset=['SaleAmount','SalesRatio', 'AssessedValue', 'DateRecorded'])
    #print(data.head())
    #Drop the variables which do not add any meaning - 
    data = data.drop(['SerialNumber'], axis=1)#meaningless - its an ID

    #Define the X and Y variables - 
    Y = data['SalesRatio']
    X = data
    X = X.drop(['SalesRatio'], axis=1)

    # Fit/Transform - Y var
    number = LabelEncoder()
    Y = number.fit_transform(Y)

    # Adjust / Fill the NA values - 
    X['ResidentialType'] = X['ResidentialType'].fillna('')
    X['NonUseCode'] = X['NonUseCode'].fillna('')
    X['PropertyType'] = X['PropertyType'].fillna('')

    # Fit/Transform the X categorical variables -
    number = LabelEncoder()
    townLabels = X['Town'].values
    X['Town'] = number.fit_transform(X['Town'])
    mappedTownLabels = X['Town'].values

    propertyTypeLabels = X['PropertyType'].values
    X['PropertyType'] = number.fit_transform(X['PropertyType'])
    mappedPropertyTypeLabels = X['PropertyType'].values

    residentialTypeLabels = X['ResidentialType'].values
    X['ResidentialType'] = number.fit_transform(X['ResidentialType'])
    mappedResidentialTypeLabels = X['ResidentialType'].values
    X['NonUseCode'] = number.fit_transform(X['NonUseCode'])

    #TODO - Exact geolocation - convert to Latitude/Longitude.
    # for now address can be dropped - 
    #Using Google maps geolocation - 
    X = X.drop(['Address'], axis=1)

    #Process the date column - 
    from dateutil import parser
    def dateObject(date_str):
        #print('parsing ', date_str)
        dt = parser.parse(date_str)
        return dt

    X['DateRecorded'] = X['DateRecorded'].apply(dateObject)

    # Include columns to capture year, month, day - this is more accurate because 
    # will help us to capture cyclical patterns - if ratios depend on such.  

    def dateYear(date):
        return date.year

    def dateMonth(date):
        return date.month

    def dateDay(date):
        return date.day

    X['Year'] = X['DateRecorded'].apply(dateYear)
    X['Month'] = X['DateRecorded'].apply(dateMonth)
    X['Day'] = X['DateRecorded'].apply(dateDay)
    X = X.drop(['DateRecorded'], axis=1)

    #Add time to sell - 
    def timeToSell(year, listYear):
        time = year - listYear
        return time

    X['TimeToSell'] = np.vectorize(timeToSell)(X['Year'], X['ListYear'])

    #Remarks - add a column for properties owned by the bank - 
    def ownedByTheBank(remarks):
        if remarks == 'PROPERTY WAS OWNED BY THE BANK':
            return 1
        else:
            return 0

    X['OwnedByBank'] = X['Remarks'].apply(ownedByTheBank)
    #More columns can be engineered out of remarks but for now drop the rest - 
    X = X.drop(['Remarks'], axis=1)
    
    return [X,Y]

# Default Salesforce data import function with options to transform the Y variable-
# @Imports the full data
# @Transforms to categorical variables
# @Removes NaNs
# @Keeps all records & Drops specified Y variable outcomes.

def dataForDependentVariableByDroppingYOutcomes(filename, yVaribale, dropYOutcome):
    print("to do")
