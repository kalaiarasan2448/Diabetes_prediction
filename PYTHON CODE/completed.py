import pandas as rd
import pickle
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import ttk
df = rd.read_csv("E:\king\diabetes2.csv")
print(df)
print(df.head(10))

X = df.drop('Outcome', axis = 1)
y = df[['Outcome']]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print(X_train.shape)
print(X_test.shape)

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

model = lr.fit(X_train,y_train)
y_pred = lr.predict(X_test)

print(y_pred)
print("Accuracy is :")
print(accuracy_score(y_pred,y_test))


Model = pickle.dumps(model)

win = tk.Tk()
win.geometry("750x500")
win.title('Diabetes Testing')
win.configure(bg='light pink')

Preg = ttk.Label(win, text="Preg", width=20, font=("algerian", 15), background='light pink')
Preg.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
Preg_var = tk.StringVar()
Preg_entrybox = ttk.Entry(win, width=30, textvariable=Preg_var)
Preg_entrybox.grid(row=0, column=1, padx=10, pady=10)
Preg_entrybox.configure(background='white')

Gluco = ttk.Label(win, text="Glucose", width=20, font=("algerian", 15), background='light pink')
Gluco.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
Gluco_var = tk.StringVar()
Gluco_entrybox = ttk.Entry(win, width=30, textvariable=Gluco_var)
Gluco_entrybox.grid(row=1, column=1, padx=10, pady=10)
Gluco_entrybox.configure(background='white')

BP = ttk.Label(win, text="BP", width=20, font=("algerian", 15), background='light pink')
BP.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
BP_var = tk.StringVar()
BP_entrybox = ttk.Entry(win, width=30, textvariable=BP_var)
BP_entrybox.grid(row=2, column=1, padx=10, pady=10)
BP_entrybox.configure(background='white')

skinTH = ttk.Label(win, text="Skin Thickness", width=20, font=("algerian", 15), background='light pink')
skinTH.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
skinTH_var = tk.StringVar()
skinTH_entrybox = ttk.Entry(win, width=30, textvariable=skinTH_var)
skinTH_entrybox.grid(row=3, column=1, padx=10, pady=10)
skinTH_entrybox.configure(background='white')

Insulin = ttk.Label(win, text="Insulin", width=20, font=("algerian", 15), background='light pink')
Insulin.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
Insulin_var = tk.StringVar()
Insulin_entrybox = ttk.Entry(win, width=30, textvariable=Insulin_var)
Insulin_entrybox.grid(row=4, column=1, padx=10, pady=10)
Insulin_entrybox.configure(background='white')

BMI = ttk.Label(win, text="BMI", width=20, font=("algerian", 15), background='light pink')
BMI.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
BMI_var = tk.StringVar()
BMI_entrybox = ttk.Entry(win, width=30, textvariable=BMI_var)
BMI_entrybox.grid(row=5, column=1, padx=10, pady=10)
BMI_entrybox.configure(background='white')

Pedigreefunc = ttk.Label(win, text="Pedigreefunc", width=20, font=("algerian", 15), background='light pink')
Pedigreefunc.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
Pedigreefunc_var = tk.StringVar()
Pedigreefunc_entrybox=ttk.Entry(win,width=30,textvariable=Pedigreefunc_var)
Pedigreefunc_entrybox.grid(row=6,column=1)
Pedigreefunc_entrybox.configure(background='white')
                                  


Age=ttk.Label(win,text="Age",width=35,font=("algerian", 15), background='light pink')
Age.grid(row=7,column=0,sticky=tk.W, padx=10,pady=10)
Age_var=tk.StringVar()
Age_entrybox=ttk.Entry(win,width=30,textvariable=Age_var)
Age_entrybox.grid(row=7,column=1)
   

import pandas as pd
DF = pd.DataFrame()
def action():
    global DB
    import pandas as pd
    DF = pd.DataFrame(columns=['Preg','Gluco','BP','skinTH','Insulin','BMI','Pedigreefunc','Age'])
    PREG=Preg_var.get()
    DF.loc[0,'Preg']=PREG
    PLAS=Gluco_var.get()
    DF.loc[0,'Gluco']=PLAS
    PRES=BP_var.get()
    DF.loc[0,'BP']=PRES
    SKIN=skinTH_var.get()
    DF.loc[0,'skinTH']=SKIN
    TEST=Insulin_var.get()
    DF.loc[0,'Insulin']=TEST
    MASS=BMI_var.get()
    DF.loc[0,'BMI']=MASS
    PEDI=Pedigreefunc_var.get()
    DF.loc[0,'Pedigreefunc']=PEDI
    AGE=Age_var.get()
    DF.loc[0,'Age']=AGE
    print(DF.shape)
    DB=DF

Submit_button=ttk.Button(win,text="Submit",command=action)
Submit_button.grid(row=30,column=1)


def diet():
   top= tk.Toplevel(win)
   top.geometry("750x250")
   top.title("Diet")
   tk.Label(top, text= "* Carbohydrates - 50%",font=('18')).place(x=150,y=80)
   tk.Label(top, text= "* Proteins      - 25%",font=('18')).place(x=150,y=120)
   tk.Label(top, text= "* Fats          - 25%",font=('18')).place(x=150,y=160)
   tk.Label(top, text= "                     ",font=('18')).place(x=150,y=200)
   tk.Label(top, text= "* Carbohydrates - Starch,Bread,Milk,Yogurt,Vegetables,fruits",font=('18')).place(x=150,y=240)
   tk.Label(top, text= "* Proteins      - Eggs,Cheese,fish,poultry",font=('18')).place(x=150,y=280)
   tk.Label(top, text= "* Fats          - Oils,Nuts,Animal fats,Shellfish",font=('18')).place(x=150,y=320)

def precaution():
   top= tk.Toplevel(win)
   top.geometry("750x250")
   top.title("Tips to control")
   tk.Label(top, text= "* Be more physically active", font=('18')).place(x=150,y=80)
   tk.Label(top, text= "* Eat healthy plant foods. Plants provide vitamins, minerals and carbohydrates", font=('18')).place(x=150,y=120)
   tk.Label(top, text= "* Eat healthy fats.", font=('18')).place(x=150,y=160)

def Output():
    DB["Preg"] = pd.to_numeric(DB["Preg"])
    DB["Gluco"] = pd.to_numeric(DB["Gluco"])
    DB["BP"] = pd.to_numeric(DB["BP"])
    DB["skinTH"] = pd.to_numeric(DB["skinTH"])
    DB["Insulin"] = pd.to_numeric(DB["Insulin"])
    DB["BMI"] = pd.to_numeric(DB["BMI"])
    DB["Pedigreefunc"] = pd.to_numeric(DB["Pedigreefunc"])
    DB["Age"] = pd.to_numeric(DB["Age"])

    output=model.predict(DB)
    if output==1:
        result='Diabetic'
        res=1
    elif output==0:
        result='Non-Diabetic'
        res=0
    Predict_entrybox=ttk.Entry(win,width=16)
    Predict_entrybox.grid(row=20,column=1)
    Predict_entrybox.insert(1,str(result))
    if output==1:
        lab = ttk.Entry(win,width=25)
        lab.grid(row=50,column=0)
        lab.insert(1,str("Check your diet here!"))
        Click_button=ttk.Button(win,text="Click here",command=diet)
        Click_button.grid(row=50,column=1)
    elif output==0:
        lab = ttk.Entry(win,width=25)
        lab.grid(row=50,column=0)
        lab.insert(1,str("Click here for Tips!"))
        Click_button=ttk.Button(win,text="Click here",command=precaution)
        Click_button.grid(row=50,column=1)

Predict_button=ttk.Button(win,text="Predict",command=Output,)
Predict_button.grid(row=32,column=1)
win.mainloop()
