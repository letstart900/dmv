import pandas as pd
from math import log2
import copy

df = pd.read_csv('play_tennis.csv')

df

def data_setup(df):
  #Collect the list of attributes in the dataset
  attributes = df.columns.tolist()
  #output dict will contain the name of the output attribute as key and the list of values that the attribute takes as values
  output = {}
  output['play'] = df['play'].values.tolist()
  #remove unwanted attributes that do not take part in decision tree building
  attributes.remove('play')
  attributes.remove('day')
  #Construct a dict for input attributes
  #{ 'outlook':['Sunny','Sunny',...,'Overcast','Rain'],
  #  'temp':['Hot','Hot',...,'Hot','Mild'],
  #  ...
  #}
  input = {}
  for x in attributes:
    input[x] = df[x].values.tolist()
  #Put all these into data - a list
  data = []
  data.append(input)
  data.append(output)
  data.append(attributes)
  # print('@data_setup\n')
  # print('Attributes => ',attributes)
  # print('Input => ', input)
  # print('Output => ',output)
  return data

def get_unique_attr_values(input,attributes,level):
  #This function will return a list in which the first element is the attribute -attr
  # and the second is a list of unique values that the attribute - attr takes.
  # ['outlook',['Overcast','Sunny','Rain']]
  values = []
  values.append(attributes[level])
  values.append(list(set(input[attributes[level]])))
  return values

def check_output(attr,value,input,output):
  #This function is used to check the output
  count_yes = 0
  count_no = 0
  attr_values_list = input[attr]
  for i in range(0,len(attr_values_list)):
    if attr_values_list[i] == value:
      if output['play'][i] == 'Yes': 
        count_yes = count_yes + 1
      elif output['play'][i] == 'No': 
        count_no = count_no + 1
  if count_no == 0: return 1 #pure yes
  elif count_yes == 0: return -1 #pure no
  else: return 0 #mixed outcomes

def filter_data(df,value,attr):
  new_df = df.loc[df[attr]==value]
  new_df.drop([attr],axis=1)
  return new_df

tree = {}

def build_tree(df,path,level,attributes):
  data = data_setup(df)
  input = data[0]
  output = data[1]
  attr_values = get_unique_attr_values(input,attributes,level)
  path.append(attr_values[0])
  for each in attr_values[1]:
    path.append(each)
    flag = check_output(attributes[level],each,input,output)
    
    if flag == 1:
      tree[tuple(path)] = 'Yes'
      print(path,end=" ")
      print('Yes')

    elif flag == -1:
      tree[tuple(path)] = 'No'
      print(path,end=" ")
      print('No')

    else:
      new_df = filter_data(df,each,attributes[level])
      build_tree(new_df,path,level+1,attributes)
    path.pop()
  path.pop()

attributes = df.columns.tolist()
attributes.remove('play')
attributes.remove('day')
build_tree(df,[],0,attributes)

f = open('DecisionTree.txt','w')
for key in tree:
  f.write("%s => %s\n" %(str(key),str(tree[key])))
f.close()
