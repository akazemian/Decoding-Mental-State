import mne
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.metrics import roc_auc_score as auc
import pickle
import os

from tqdm import tqdm
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution1D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout



def getData(testSubject, testTrial, test=False):
  """ description: returns training and test data given the subject and trial chosen as the test set
  parameters: testSubject(string), testTrial(int), test(boolean)
  output: List of DataFrames for the training (test=False) or test (test=True) trials and states """

  files = []
  for f in os.listdir('/content/drive/MyDrive/Colab Notebooks/Muse Project/Original Data/Muse/'):
    files.append(f)

  testList = []
  trainList = []
  
  for f in files:  
    if (f.split('-')[0] == f'subject{testSubject}') & (f.split('-')[2] == f'{testTrial}.csv'):
      testList.append(f)
  trainList = list(set(files).difference(set(testList)))
  trainList.remove('name-concentrating-1.csv')

  
  trainDf = []
  testDf = []

  trainStates = []
  testStates = []

  if test == True:
    for i in testList:

      df = pd.read_csv(f'/content/drive/MyDrive/Colab Notebooks/Muse Project/Original Data/Muse/{i}')
      df = df.iloc[:,1:-1]
      splitted = i.split('-')
      states = pd.DataFrame(np.zeros((len(df),3)),columns = ['C','R','N'])
      if splitted[1] == 'concentrating':
        states['C'] = 1
      elif splitted[1] == 'relaxed':
        states['R'] = 1
      elif splitted[1] == 'neutral':
        states['N'] = 1
      testDf.append(df)
      testStates.append(states)
    return testDf, testStates,  testList

  else:
    for i in trainList:

      df = pd.read_csv(f'/content/drive/MyDrive/Colab Notebooks/Muse Project/Original Data/Muse/{i}')
      df = df.iloc[:,1:-1]
      splitted = i.split('-')
      states = pd.DataFrame(np.zeros((len(df),3)),columns = ['C','R','N'])
      if splitted[1] == 'concentrating':
        states['C'] = 1
      elif splitted[1] == 'relaxed':
        states['R'] = 1
      elif splitted[1] == 'neutral':
        states['N'] = 1

      trainDf.append(df)
      trainStates.append(states)

    return trainDf, trainStates, trainList


def processData(data,states,sfreq=200,lowF=4,highF=30,Normalize=True,window = 64):
  """ description: processes the data by filtering and windowing
  parameters: data(List),states(List),sfreq(int) = sampling frequency,lowF(int)=lower band frequency ,highF(int)=upper band frequency ,
  Normalize(boolean), window(int) = window size
  output: 3 dimensional array of processed data and 2 dimensional array of the corresponding mental states """
  
  electrodes = 4
  for i in range(len(data)):
    #filter data:
    filtered_data = mne.filter.filter_data(data[i].transpose(), sfreq=sfreq, l_freq=lowF, h_freq=highF, verbose=None)
    data[i] = pd.DataFrame(filtered_data.transpose())
    
    #normalize data:
    data[i] = (data[i] - data[i].mean(axis=0)) / data[i].std(axis=0)
    
  #window:
  size = 0
  for i in data:
    size += (len(i)-window)

  allData = np.zeros((size,window,electrodes))
  allStates = np.zeros((size,3))

  b= 0
  for i in range(len(data)):  
    x = data[i]
    y = states[i]
  
    for row in range(window,len(x)):
      tmpx = x.iloc[row-window:row,:]
      tmpy = y.iloc[row,:].to_numpy()
      allData[b,:,:] = tmpx
      allStates[b,:] = tmpy
      b += 1
  
  return allData, allStates

def getModel():
  """ description: Neural Net model consisting of CNN layers and fully connected layers
  parameters: -
  output: the model """
  # Initialising the model
  classifier = Sequential()
  # Convolutions
  classifier.add(Convolution1D(64, 3, 1, input_shape = (64, 4), activation = 'relu'))
  classifier.add(Convolution1D(64, 3, 1, activation = 'relu'))
  # Droput, MaxPool, Flatten
  classifier.add(Dropout(0.5))
  classifier.add(MaxPooling1D(pool_size = (2)))
  classifier.add(Flatten())
  # Full connection (hidden layers)
  classifier.add(Dense(512, activation = 'relu'))
  classifier.add(Dense(256, activation = 'relu'))
  classifier.add(Dense(64, activation = 'relu'))
  # output
  classifier.add(Dense(3, activation = 'softmax'))

  # Compiling the CNN
  classifier.compile(optimizer = 'adadelta', loss = 'categorical_crossentropy', metrics = ['accuracy'])

  return classifier