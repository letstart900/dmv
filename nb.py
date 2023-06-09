def feature_count(df):
  table = {}
  output = df['Buy_Computer'].values.tolist()
  print('Output => ',output)
  attributes = df.columns.tolist()
  attributes.remove('id')
  attributes.remove('Buy_Computer')
  for each in attributes:
    values = list(set(df[each].values.tolist()))
    input = df[each].values.tolist()
    for val in values:
      cy = 0
      cn = 0
      for i in range(0,len(input)):
        if input[i] == val:
          if output[i] == 'yes':
            cy = cy + 1
          elif output[i] == 'no':
            cn = cn + 1
      table[val] = [cy,cn]
  print(table)
  return table

def predict(df, test, table, count):
  level = 1
  total = sum(count)
  prob_y = count[0]/total
  prob_n = count[1]/total
  for each in test:
    counter_y = table[each][0]
    counter_n = table[each][1]
    total_y = count[0]
    total_n = count[1]

    if counter_y == 0:
      counter_y = counter_y + 1/(len(df[level].unique()))
      total_y = total_y + 1
    if counter_n == 0:
      counter_n = counter_n + 1/(len(df[level].unique()))
      total_n = total_n + 1

    prob_y = prob_y * (counter_y/total_y)
    prob_n = prob_n * (counter_n/total_n)

    level = level + 1
    
  prob_yes = prob_y/(prob_y + prob_n)
  prob_no = prob_n/(prob_y + prob_n)

  print('Probability(Yes) = ',prob_yes)
  print('Probability(No) = ',prob_no)

  if(prob_yes>prob_no):
    print('\nOutput => Yes')
  else:
    print('\nOutput => No')

import pandas as pd
df = pd.read_csv('Buy_Computer.csv')
table = feature_count(df)
count = df['Buy_Computer'].value_counts()
test = ['youth','medium','yes','excellent']
predict(df,test,table,count)
