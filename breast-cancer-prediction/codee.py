import numpy as np 
import pandas as pd  
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import mpld3 as mpl
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

df = pd.read_csv("breast-cancer-prediction\data.csv",header = 0)
df.head()

df.drop('id',axis=1,inplace=True)
df.drop('Unnamed: 32',axis=1,inplace=True)
print(len(df))
df.diagnosis.unique()

df['diagnosis'] = df['diagnosis'].map({'M':1,'B':0})
df.head()

df.describe()

df.describe()
plt.hist(df['diagnosis'])
plt.title('Diagnosis (M=1 , B=0)')
plt.show()

features_mean=list(df.columns[1:11])
dfM=df[df['diagnosis'] ==1]
dfB=df[df['diagnosis'] ==0]

plt.rcParams.update({'font.size': 8})
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8,10))
axes = axes.ravel()
for idx,ax in enumerate(axes):
    ax.figure
    binwidth= (max(df[features_mean[idx]]) - min(df[features_mean[idx]]))/50
    ax.hist([dfM[features_mean[idx]], dfB[features_mean[idx]]], bins=np.arange(min(df[features_mean[idx]]), max(df[features_mean[idx]]) + binwidth, binwidth), alpha=0.5, stacked=True, label=['M', 'B'], color=['r', 'g'])
    ax.legend(loc='upper right')
    ax.set_title(features_mean[idx])
plt.tight_layout()
plt.show()

traindf, _ = train_test_split(df, test_size = 0.3)
def classification_model(model, data, predictors, outcome):
  model.fit(data[predictors],data[outcome])
  
  predictions = model.predict(data[predictors])
  
  accuracy = metrics.accuracy_score(predictions,data[outcome])
  print("Accuracy : %s" % "{0:.3%}".format(accuracy))

  kf = KFold(n_splits=5)

  error = []
  for train, test in kf.split(data):
    train_predictors = (data[predictors].iloc[train,:])
    
    train_target = data[outcome].iloc[train]
    test_predictors = data[predictors].iloc[test, :]
    model.fit(train_predictors, train_target)
    
    error.append(model.score(data[predictors].iloc[test,:], data[outcome].iloc[test]))
    
    print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(error)))
    
  model.fit(data[predictors],data[outcome]) 
  return model

predictor_var = ['radius_mean','perimeter_mean','area_mean','compactness_mean','concave points_mean','area_worst']
outcome_var='diagnosis'
model=LogisticRegression()
classification_model(model,traindf,predictor_var,outcome_var)

predictor_var = ['radius_mean']
model=LogisticRegression()
classification_model(model,traindf,predictor_var,outcome_var)

predictor_var = ['radius_mean','perimeter_mean','area_mean','compactness_mean','concave points_mean','area_worst']
model = DecisionTreeClassifier()
classification_model(model,traindf,predictor_var,outcome_var)

predictor_var = ['radius_mean']
model = DecisionTreeClassifier()
classification_model(model,traindf,predictor_var,outcome_var)

predictor_var = features_mean
model = RandomForestClassifier(n_estimators=100,min_samples_split=25, max_depth=7, max_features=2)
classification_model(model, traindf,predictor_var,outcome_var)

featimp = pd.Series(model.feature_importances_, index=predictor_var).sort_values(ascending=False)
print(featimp)

predictor_var = ['concave points_mean','area_mean','radius_mean','perimeter_mean','concavity_mean','area_worst']
model = RandomForestClassifier(n_estimators=100, min_samples_split=25, max_depth=7, max_features=2)
classification_model(model,traindf,predictor_var,outcome_var)

predictor_var =  ['radius_mean']
model = RandomForestClassifier(n_estimators=100)
classification_model(model, traindf,predictor_var,outcome_var)

predictor_var = features_mean
model = RandomForestClassifier(n_estimators=100,min_samples_split=25, max_depth=7, max_features=2)
classification_model(model, traindf,predictor_var,outcome_var)

import joblib
joblib.dump(model,'model.pkl')

def predict_new_data():
    radius = float(entry_radius.get())
    perimeter = float(entry_perimeter.get())
    area = float(entry_area.get())
    compactness = float(entry_compactness.get())
    concave_points = float(entry_concave_points.get())
    area_worst = float(entry_area_worst.get())
    new_data = pd.DataFrame({'radius_mean': [radius],
                             'perimeter_mean': [perimeter],
                             'area_mean': [area],
                             'compactness_mean': [compactness],
                             'concave points_mean': [concave_points],
                             'area_worst':[area_worst]})
    

    predictors = ['radius_mean', 'perimeter_mean', 'area_mean', 'compactness_mean', 'concave points_mean','area_worst']
    outcome = 'diagnosis'
    model = LogisticRegression()
    trained_model = classification_model(model,traindf,predictors, outcome)
    
    prediction = trained_model.predict(new_data)
    
    if prediction[0] == 1:
        result = 'Malignant(cancer found take doctor presciption.)'
    else:
        result = 'Benign(not cancer just a unusual growth of tissue.)'
    messagebox.showinfo("Prediction Result", f"The diagnosis is: {result}")


window = tk.Tk()
window.title("Breast Cancer Diagnosis Prediction")

label_radius = ttk.Label(window, text="Radius Mean:")
label_radius.grid(row=0, column=0)
entry_radius = ttk.Entry(window)
entry_radius.grid(row=0, column=1)

label_perimeter = ttk.Label(window, text="Perimeter Mean:")
label_perimeter.grid(row=1, column=0)
entry_perimeter = ttk.Entry(window)
entry_perimeter.grid(row=1, column=1)

label_area = ttk.Label(window, text="Area Mean:")
label_area.grid(row=2, column=0)
entry_area = ttk.Entry(window)
entry_area.grid(row=2, column=1)

label_compactness = ttk.Label(window, text="Compactness Mean:")
label_compactness.grid(row=3, column=0)
entry_compactness = ttk.Entry(window)
entry_compactness.grid(row=3, column=1)

label_concave_points = ttk.Label(window, text="Concave Points Mean:")
label_concave_points.grid(row=4, column=0)
entry_concave_points = ttk.Entry(window)
entry_concave_points.grid(row=4, column=1)

label_area_worst = ttk.Label(window, text="area worst:")
label_area_worst.grid(row=5, column=0)
entry_area_worst = ttk.Entry(window)
entry_area_worst.grid(row=5, column=1)

predict_button = ttk.Button(window, text="Predict Diagnosis", command=predict_new_data)
predict_button.grid(row=6, columnspan=2)

window.mainloop()
