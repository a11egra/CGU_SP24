import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import ensemble
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.cm as cm
     

# import query file query.csv
query = pd.read_csv('query.csv')
query.info()
query



### CLEANING
# drop any weird rows with null values
full_query = query.dropna(how='any',axis=0)  # drop any rows with null values
full_query.info()
full_query

# split into program-specific dataframes
# qBOT = full_query[full_query['Program 1 Category'] == 'Botany']
qCISAT = full_query[full_query['Program 1 Category'] == 'CISAT']
qDBOS = full_query[full_query['Program 1 Category'] == 'DBOS']
qDPE = full_query[full_query['Program 1 Category'] == 'DPE']
qDSM = full_query[full_query['Program 1 Category'] == 'Drucker']
qIMS = full_query[full_query['Program 1 Category'] == 'IMS']
qSAH = full_query[full_query['Program 1 Category'] == 'SAH']
qSCGH = full_query[full_query['Program 1 Category'] == 'SCGH']
qSES = full_query[full_query['Program 1 Category'] == 'SES']

# drop the program category now that they're split
ROW = 0
COLUMN = 1

def clean_df (df):
  return df.drop(['Program 1 Category', 'Degree 1'], axis=COLUMN)

query_clean = clean_df(full_query)
CISAT_clean = clean_df(qCISAT)
DBOS_clean = clean_df(qDBOS)
DPE_clean = clean_df(qDPE)
DSM_clean = clean_df(qDSM)
IMS_clean = clean_df(qIMS)
SAH_clean = clean_df(qSAH)
SCGH_clean = clean_df(qSCGH)
SES_clean = clean_df(qSES)

### INDEXING
# column index
COLUMNS = query_clean.columns
COL_INDEX = {}
for i, name in enumerate(COLUMNS):
    COL_INDEX[name] = i
print(f"dictionary COL_INDEX is {COL_INDEX}")

# true/false index
TF = ['False','True']
TF_INDEX = {'False':0,'True':1}
for name in TF:
    print(f"{name} maps to {TF_INDEX[name]}")

## MAPPING
def map_values(df, column_name, mapping):
    if mapping is None:
        unique_values = df[column_name].unique()
        mapping = {value: idx for idx, value in enumerate(unique_values)}
    index_mapping = {idx: value for value, idx in mapping.items()}
    df[column_name] = df[column_name].map(mapping)
    return mapping, index_mapping

# create universal mappings
mappings = {}
for column_name in ['Country', 'Citizenship Status', 'Continent', 'Degree Type', 'Entry Semester']:
		# create universal mappings
    mappings[column_name], _ = map_values(query_clean, column_name, mappings.get(column_name))
    print(mappings[column_name])
		# apply mappings to other dataframes
    CISAT_clean[column_name] = CISAT_clean[column_name].map(mappings[column_name])
    DBOS_clean[column_name] = DBOS_clean[column_name].map(mappings[column_name])
    DPE_clean[column_name] = DPE_clean[column_name].map(mappings[column_name])
    DSM_clean[column_name] = DSM_clean[column_name].map(mappings[column_name])
    IMS_clean[column_name] = IMS_clean[column_name].map(mappings[column_name])
    SAH_clean[column_name] = SAH_clean[column_name].map(mappings[column_name])
    SCGH_clean[column_name] = SCGH_clean[column_name].map(mappings[column_name])
    SES_clean[column_name] = SES_clean[column_name].map(mappings[column_name])

# add these to reference-able indexes
CITIZENSHIP_INDEX = {v: k for k, v in mappings['Citizenship Status'].items()}
CONTINENT_INDEX = {v: k for k, v in mappings['Continent'].items()}
COUNTRY_INDEX = {v: k for k, v in mappings['Country'].items()}
TYPE_INDEX = {v: k for k, v in mappings['Degree Type'].items()}
SEMESTER_INDEX = {v: k for k, v in mappings['Entry Semester'].items()}



### NUMPY
# i'm not going to keep the full query around anymore
CISAT_arr = CISAT_clean.to_numpy()
DBOS_arr = DBOS_clean.to_numpy()
DPE_arr = DPE_clean.to_numpy()
DSM_arr = DSM_clean.to_numpy()
IMS_arr = IMS_clean.to_numpy()
SAH_arr = SAH_clean.to_numpy()
SCGH_arr = SCGH_clean.to_numpy()
SES_arr = SES_clean.to_numpy()



### DATA DEFINITIONS + TRAINING
def RF_creator(qarray):
  y_all = qarray[:,0]  # y = labels
  X_all = qarray[:,1:15] # X = features

  # scrambling the data using a permuation list
  indices = np.random.permutation(len(y_all))  # indices is a permutation-list
  X_permed = X_all[indices]
  y_permed = y_all[indices]

  X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
  print(f"training with {len(y_train)} rows;  testing with {len(y_test)} rows" )
  return X_all, X_train, X_test, y_all, y_train, y_test

CISAT_X_all, CISAT_X_train, CISAT_X_test, CISAT_y_all, CISAT_y_train, CISAT_y_test = RF_creator(CISAT_arr)
DBOS_X_all, DBOS_X_train, DBOS_X_test, DBOS_y_all, DBOS_y_train, DBOS_y_test = RF_creator(DBOS_arr)
DPE_X_all, DPE_X_train, DPE_X_test, DPE_y_all, DPE_y_train, DPE_y_test = RF_creator(DPE_arr)
DSM_X_all, DSM_X_train, DSM_X_test, DSM_y_all, DSM_y_train, DSM_y_test = RF_creator(DSM_arr)
IMS_X_all, IMS_X_train, IMS_X_test, IMS_y_all, IMS_y_train, IMS_y_test = RF_creator(IMS_arr)
SAH_X_all, SAH_X_train, SAH_X_test, SAH_y_all, SAH_y_train, SAH_y_test = RF_creator(SAH_arr)
SCGH_X_all, SCGH_X_train, SCGH_X_test, SCGH_y_all, SCGH_y_train, SCGH_y_test = RF_creator(SCGH_arr)
SES_X_all, SES_X_train, SES_X_test, SES_y_all, SES_y_train, SES_y_test = RF_creator(SES_arr)

CISAT_list = [CISAT_X_train, CISAT_X_test, CISAT_y_train, CISAT_y_test]
DBOS_list = [DBOS_X_train, DBOS_X_test, DBOS_y_train, DBOS_y_test]
DPE_list = [DPE_X_train, DPE_X_test, DPE_y_train, DPE_y_test]
DSM_list = [DSM_X_train, DSM_X_test, DSM_y_train, DSM_y_test]
IMS_list = [IMS_X_train, IMS_X_test, IMS_y_train, IMS_y_test]
SAH_list = [SAH_X_train, SAH_X_test, SAH_y_train, SAH_y_test]
SCGH_list = [SCGH_X_train, SCGH_X_test, SCGH_y_train, SCGH_y_test]
SES_list = [SES_X_train, SES_X_test, SES_y_train, SES_y_test]



### FIRST RF MODEL
best_d = 1            # a guess
best_num_trees = 42   # a guess
rforest_model = ensemble.RandomForestClassifier(max_depth=best_d,
                                                n_estimators=best_num_trees,
                                                max_samples=0.5)

def RF_training(df_list):
  rforest_model.fit(df_list[0], df_list[1])
  print(f"Built an RF with depth={best_d} and number of trees={best_num_trees}")
  return rforest_model

CISAT_rforest_model = RF_training([CISAT_X_train, CISAT_y_train])
DBOS_rforest_model = RF_training([DBOS_X_train, DBOS_y_train])
DPE_rforest_model = RF_training([DPE_X_train, DPE_y_train])
DSM_rforest_model = RF_training([DSM_X_train, DSM_y_train])
IMS_rforest_model = RF_training([IMS_X_train, IMS_y_train])
SAH_rforest_model = RF_training([SAH_X_train, SAH_y_train])
SCGH_rforest_model = RF_training([SCGH_X_train, SCGH_y_train])
SES_rforest_model = RF_training([SES_X_train, SES_y_train])



### CROSS-VALIDATION
DIVISIONS = ['CISAT','DBOS','DPE','DSM','IMS','SAH','SCGH','SES']

def RF_cross_validation(div, rforest_model, X_train, y_train, dep, tree):
  best_d = 1
  best_ntrees = 1
  best_accuracy = 0

  kf = KFold(n_splits=5, shuffle=True)
  for d in dep:
      for ntrees in tree:
          accuracy_sum = 0
          for train_index, test_index in kf.split(X_train, y_train):
              X_train_fold, X_test_fold = X_train[train_index], X_train[test_index]
              y_train_fold, y_test_fold = y_train[train_index], y_train[test_index]

              rforest_model = ensemble.RandomForestClassifier(
                  max_depth=d,
                  n_estimators=ntrees,
                  max_samples=0.5
              )
              rforest_model.fit(X_train_fold, y_train_fold)
              y_pred = rforest_model.predict(X_test_fold)
              accuracy_sum += accuracy_score(y_test_fold, y_pred)

          average_cv_accuracy = accuracy_sum / kf.get_n_splits()
          # print(f"depth: {d:2d} ntrees: {ntrees:3d} cv accuracy: {average_cv_accuracy:7.4f}")
          if average_cv_accuracy > best_accuracy:
              best_accuracy = average_cv_accuracy
              best_d = d
              best_ntrees = ntrees

  print(f"\nFor {DIVISIONS[div]}:")
  print(f"the best depth is {best_d}")
  print(f"the best number of trees is {best_ntrees}")
  print(f"the best accuracy is {best_accuracy}\n\n")
  return best_d, best_ntrees, best_accuracy

depth=range(1,6)
trees=[50,100,150,200,250,300]

CISAT_best_d, CISAT_best_ntrees, CISAT_best_accuracy = RF_cross_validation(0, CISAT_rforest_model, CISAT_X_train, CISAT_y_train, depth, trees)
DBOS_best_d, DBOS_best_ntrees, DBOS_best_accuracy = RF_cross_validation(1, DBOS_rforest_model, DBOS_X_train, DBOS_y_train, depth, trees)
DPE_best_d, DPE_best_ntrees, DPE_best_accuracy = RF_cross_validation(2, DPE_rforest_model, DPE_X_train, DPE_y_train, depth, trees)
DSM_best_d, DSM_best_ntrees, DSM_best_accuracy = RF_cross_validation(3, DSM_rforest_model, DSM_X_train, DSM_y_train, depth, trees)
IMS_best_d, IMS_best_ntrees, IMS_best_accuracy = RF_cross_validation(4, IMS_rforest_model, IMS_X_train, IMS_y_train, depth, trees)
SAH_best_d, SAH_best_ntrees, SAH_best_accuracy = RF_cross_validation(5, SAH_rforest_model, SAH_X_train, SAH_y_train, depth, trees)
SCGH_best_d, SCGH_best_ntrees, SCGH_best_accuracy = RF_cross_validation(6, SCGH_rforest_model, SCGH_X_train, SCGH_y_train, depth, trees)
SES_best_d, SES_best_ntrees, SES_best_accuracy = RF_cross_validation(7, SES_rforest_model, SES_X_train, SES_y_train, depth, trees)


### TUNED MODEL
CISAT_model = ensemble.RandomForestClassifier(max_depth=CISAT_best_d,n_estimators=CISAT_best_ntrees,max_samples=0.5)
CISAT_model.fit(CISAT_X_all, CISAT_y_all)
print(f"Built an RF classifier for CISAT with depth={CISAT_best_d} and ntrees={CISAT_best_ntrees}")

DBOS_model = ensemble.RandomForestClassifier(max_depth=DBOS_best_d,n_estimators=DBOS_best_ntrees,max_samples=0.5)
DBOS_model.fit(DBOS_X_all, DBOS_y_all)
print(f"Built an RF classifier for DBOS with depth={DBOS_best_d} and ntrees={DBOS_best_ntrees}")

DPE_model = ensemble.RandomForestClassifier(max_depth=DPE_best_d,n_estimators=DPE_best_ntrees,max_samples=0.5)
DPE_model.fit(DPE_X_all, DPE_y_all)
print(f"Built an RF classifier for DPE with depth={DPE_best_d} and ntrees={DPE_best_ntrees}")

DSM_model = ensemble.RandomForestClassifier(max_depth=DSM_best_d,n_estimators=DSM_best_ntrees,max_samples=0.5)
DSM_model.fit(DSM_X_all, DSM_y_all)
print(f"Built an RF classifier for DSM with depth={DSM_best_d} and ntrees={DSM_best_ntrees}")

IMS_model = ensemble.RandomForestClassifier(max_depth=IMS_best_d,n_estimators=IMS_best_ntrees,max_samples=0.5)
IMS_model.fit(IMS_X_all, IMS_y_all)
print(f"Built an RF classifier for IMS with depth={IMS_best_d} and ntrees={IMS_best_ntrees}")

SAH_model = ensemble.RandomForestClassifier(max_depth=SAH_best_d,n_estimators=SAH_best_ntrees,max_samples=0.5)
SAH_model.fit(SAH_X_all, SAH_y_all)
print(f"Built an RF classifier for SAH with depth={SAH_best_d} and ntrees={SAH_best_ntrees}")

SCGH_model = ensemble.RandomForestClassifier(max_depth=SCGH_best_d,n_estimators=SCGH_best_ntrees,max_samples=0.5)
SCGH_model.fit(SCGH_X_all, SCGH_y_all)
print(f"Built an RF classifier for SCGH with depth={SCGH_best_d} and ntrees={SCGH_best_ntrees}")

SES_model = ensemble.RandomForestClassifier(max_depth=SES_best_d,n_estimators=SES_best_ntrees,max_samples=0.5)
SES_model.fit(SES_X_all, SES_y_all)
print(f"Built an RF classifier for SES with depth={SES_best_d} and ntrees={SES_best_ntrees}")



### FEATURE IMPORTANCES
IMP_LIST = [CISAT_model.feature_importances_,
            DBOS_model.feature_importances_,
            DPE_model.feature_importances_,
            DSM_model.feature_importances_,
            IMS_model.feature_importances_,
            SAH_model.feature_importances_,
            SCGH_model.feature_importances_,
            SES_model.feature_importances_]

j = 0
for IMP in IMP_LIST:
    print(f"\nFeature importances for {DIVISIONS[j]}:")
    for i, importance in enumerate(IMP):
        perc = importance * 100
        print(f"  {COLUMNS[i+1]:>21s} has {perc:>5.1f}% of the decision-making importance.")
    j += 1

DIVISIONS = ['CISAT', 'DBOS', 'DPE', 'DSM', 'IMS', 'SAH', 'SCGH', 'SES']
feature_list = []

for item in DIVISIONS:
  new_var = item + "_features"
  feature_list.append(new_var)

print(feature_list)

j = 0
for IMP in IMP_LIST:
    print(f"\n{feature_list[j]}") # sense check

    new_df = pd.DataFrame(columns=['Feature Index #', 'Feature', 'Importance %']) # create an empty DataFrame

    for i, importance in enumerate(IMP): # construct the new dataframe
        new_df.loc[len(new_df)] = [i+1, COLUMNS[i+1], importance*100]

    new_df.to_csv(f'{DIVISIONS[j]}_features.csv', index=False) # export
    feature_list[j] = new_df # store as a variable
    print(feature_list[j])

    j+=1
    new_df = pd.DataFrame()



### COUNTING

## Admitted Students
# some handy lists to start
clean_list = [CISAT_clean, DBOS_clean, DPE_clean, DSM_clean, IMS_clean, SAH_clean, SCGH_clean, SES_clean]
columns = ['Country', 'Citizenship Status', 'Continent', 'Degree Type', 'Entry Semester']
indexes = [COUNTRY_INDEX, CITIZENSHIP_INDEX, CONTINENT_INDEX, TYPE_INDEX, SEMESTER_INDEX]
DIVISIONS = ['CISAT', 'DBOS', 'DPE', 'DSM', 'IMS', 'SAH', 'SCGH', 'SES']
     

# define a function to find the top 3 most common values
def find_counts(df, column, index):
    counts = Counter(df[column])

    if len(counts) < 3:
        top = counts.most_common(2)
    else:
        top = counts.most_common(3)

    top_data = {index[item[0]]:item[1] for item in top}
    return top_data


# get this into its own dataframe
def count_df(df,division):
    count_df = pd.DataFrame(columns=['Division', 'Feature', 'Value', 'Count'])
    for column, index in zip(columns, indexes):
        top = find_counts(df, column, index)
        if top:
          for item in top.items():
            count_df.loc[len(count_df)] = [division, column, item[0], item[1]]
    count_df.to_csv(f'{division}_counts_all.csv', index=False) # export
    count_df.info()
    return count_df

# and do it for all the divisions!
for df, division in zip(clean_list,DIVISIONS):
    count_df(df, division)

## Enrolled Students
# new dataframes to only include enrolled students
CISAT_enrolled = CISAT_clean[CISAT_clean['Enrolled'] == 1].copy()
DBOS_enrolled = DBOS_clean[DBOS_clean['Enrolled'] == 1].copy()
DPE_enrolled = DPE_clean[DPE_clean['Enrolled'] == 1].copy()
DSM_enrolled = DSM_clean[DSM_clean['Enrolled'] == 1].copy()
IMS_enrolled = IMS_clean[IMS_clean['Enrolled'] == 1].copy()
SAH_enrolled = SAH_clean[SAH_clean['Enrolled'] == 1].copy()
SCGH_enrolled = SCGH_clean[SCGH_clean['Enrolled'] == 1].copy()
SES_enrolled = SES_clean[SES_clean['Enrolled'] == 1].copy()

enrolled_list = [CISAT_enrolled, DBOS_enrolled, DPE_enrolled, DSM_enrolled, IMS_enrolled, SAH_enrolled, SCGH_enrolled, SES_enrolled]

def count_df2(df, division):
    count_df2 = pd.DataFrame(columns=['Division', 'Feature', 'Value', 'Count'])
    for column, index in zip(columns, indexes):
        top = find_counts(df, column, index)
        if top:
            for item in top.items():
                count_df2.loc[len(count_df2)] = [division, column, item[0], item[1]]
    count_df2.to_csv(f'{division}_counts_enrolled.csv', index=False) # export
    count_df2.info()
    return count_df2

for df, division in zip(enrolled_list, DIVISIONS):
    count_df2(df, division)


### VISUALIZING

## feature importances for ALL divisions (column chart)
# I didn't end up analyzing Degree 1 for this visual
for df in feature_list:
    df.drop(df[df['Feature'] == 'Degree 1'].index, inplace=True)

# using CISAT arbitrarily since the feature list index will be the same across dfs
feature_index=CISAT_features['Feature']

CISAT=dict(zip(CISAT_features['Feature'],CISAT_features['Importance %']))
DBOS=dict(zip(DBOS_features['Feature'],DBOS_features['Importance %']))
DPE=dict(zip(DPE_features['Feature'],DPE_features['Importance %']))
DSM=dict(zip(DSM_features['Feature'],DSM_features['Importance %']))
IMS=dict(zip(IMS_features['Feature'],IMS_features['Importance %']))
SAH=dict(zip(SAH_features['Feature'],SAH_features['Importance %']))
SCGH=dict(zip(SCGH_features['Feature'],SCGH_features['Importance %']))
SES=dict(zip(SES_features['Feature'],SES_features['Importance %']))

featureplot = pd.DataFrame({'CISAT': CISAT, 'DBOS':DBOS, 'DPE':DPE, 'DSM':DSM,
                      'IMS':IMS, 'SAH':SAH, 'SCGH':SCGH, 'SES':SES}, index=feature_index)

# setting a rainbow color scheme
colordef = plt.cm.rainbow(np.linspace(0, 1, 8))

# create the plot
featureplot.plot.bar(figsize=(16, 6),color=colordef ,width=0.8)

# title, legend, and axes
plt.title("Feature Importances")
plt.legend(title="Divisions")
plt.ylabel("Importance %")

# export and show the plot
plt.savefig('feature_importances.png',bbox_inches='tight')
plt.show()


## feature importances for each division (pie chart)
def pie_chart(df, division):
    labels = df['Feature']
    sizes = df['Importance %']

    # Define a custom color palette
    colors = cm.rainbow([x / len(labels) for x in range(len(labels))])

    # plot display  
    plt.figure(figsize=(20, 10))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.axis('equal')
    plt.title(f'Feature Importance for {division}', weight='bold', pad=20)
    plt.legend(loc='upper left', bbox_to_anchor=(0.85, 1))

    # exporting and viewing
    plt.savefig(f'{division}_pie_chart.png')
    plt.show()

# now do it for all the divisions
for df, division in zip(feature_list, DIVISIONS):
    pie_chart(df, division)