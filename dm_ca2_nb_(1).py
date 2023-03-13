# -*- coding: utf-8 -*-
"""dm_ca2_nb (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lx5AdiJhaAYH7rwTuFAxVK93icncuDae
"""

def feature_count(df,col, count):  #constructing a dictionary with key = unique feature values and value = list of count_yes, count_no 
  featuredict = {}                  # eg: {sunny = [count_yes, count_no], ...}
  for i in range(len(col)):
    for j in df[col[i]].unique():
      cy = 0
      cn = 0
      lis = []
      for k in range(len(df[col[i]])):
        row_list = df.iloc[k].tolist()
        if row_list[i+1] == j and row_list[-1] == 'yes':
          cy += 1
        elif row_list[i+1] == j and row_list[-1] == 'no':
          cn += 1
      lis.append(cy)
      lis.append(cn)
      featuredict[j] = lis

  return featuredict

def predict(df,test, featuredict, count):  #predicting the probability for the test case
  prob_y = 1
  prob_n = 1
  iter = 0 
  for i in test:
    counter_y = featuredict[i][0]
    counter_n = featuredict[i][1]
    total_y = count[0]
    total_n = count[1]

    if featuredict[i][0] == 0:
      counter_y = featuredict[i][0] + 1/(len(df[iter + 1].unique()))
      total_y += 1

    if featuredict[i][1] == 0:
      counter_n = featuredict[i][1] + 1/(len(df[iter + 1].unique()))
      total_n += 1

    prob_y = prob_y * counter_y / total_y
    prob_n = prob_n * counter_n / total_n
    iter += 1

  prob_y = prob_y * count[0]/len(df)
  prob_n = prob_n * count[1]/len(df)

  prob_yes = prob_y/(prob_y + prob_n)
  prob_no = prob_n/(prob_y + prob_n)

  print("probability of playing:", prob_yes)
  print("Probability of not playing:", prob_no)

  if prob_yes > prob_no:
    print("Playing = Yes")
  else:
    print("Playing = No")

def main():
  df = pd.read_csv("Buy_Computer.csv")
  col = df.columns.tolist()
  col.pop(0)
  col.pop(-1)
  count = list(df['Buy_Computer'].value_counts())
  featuredict = feature_count(df,col,count)
  test = ['youth','medium','yes','excellent']
  predict(df,test, featuredict, count)

import pandas as pd
main()