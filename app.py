from flask import Flask
from flask import request
from flask import render_template
import numpy as np
import pandas as pd

dataset = pd.read_csv('heart_disease.csv')
X = dataset.drop(['HeartDiseaseorAttack','Education','Income','NoDocbcCost'],axis=1)
y = dataset['HeartDiseaseorAttack']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)
print("Training Done...")

app = Flask(__name__, static_url_path='/static')

@app.route('/',methods=['POST','GET'])
def send():
    if request.method== 'POST':
        highBP = request.form['bp']
        highCholestrol = request.form['cholestrol']
        cholestrolCheck = request.form['cholestrolcheck']
        age = int(request.form['age'])
        height = request.form['height']
        weight = request.form['weight']
        smoke100 = request.form['cigar']
        stroke = request.form['stroke']
        diabetes = request.form['diabetes']
        physicalActivity = request.form['activity']
        fruit = request.form['fruit']
        vegetable = request.form['vegetable']
        alcohol = request.form['alcohol']
        healthCareAccess = request.form['healthcare']
        genHealth = request.form['genhealth']
        menHealth = request.form['menhealth']
        phyHealth = request.form['phyhealth']
        difficultyWalk = request.form['walk']
        gender = request.form['gender']
    
        bmi = round(float(weight)*10000/(float(height)*float(height)),2)

        if gender=="option1":
            gender = 0.0
        else:
            gender = 1.0
        
        if diabetes=="option1":
            diabetes = 2.0
        elif diabetes=="option2":
            diabetes = 1.0
        else:
            diabetes = 0.0

        correctedAge=0
        if age>=18 and age<=24:
            correctedAge=1
        elif age>=25 and age<=29:
            correctedAge=2
        elif age>=30 and age<=34:
            correctedAge=3
        elif age>=35 and age<=39:
            correctedAge=4
        elif age>=40 and age<=44:
            correctedAge=5
        elif age>=45 and age<=49:
            correctedAge=6
        elif age>=50 and age<=54:
            correctedAge=7
        elif age>=55 and age<=59:
            correctedAge=8
        elif age>=60 and age<=64:
            correctedAge=9
        elif age>=65 and age<=69:
            correctedAge=10
        elif age>=70 and age<=74:
            correctedAge=11
        elif age>=75 and age<=79:
            correctedAge=12
        elif age>=80:
            correctedAge=13

        values = [highBP,highCholestrol,cholestrolCheck,bmi,smoke100,stroke,
              diabetes,physicalActivity,fruit,vegetable,alcohol,
              healthCareAccess,float(genHealth),float(menHealth),float(phyHealth),
              difficultyWalk,gender,float(correctedAge)]
        for i in range(len(values)):
            if values[i]=="option1":
                values[i] = 1.0
            elif values[i]=="option2":
                values[i] = 0.0
        print(values)
        pred = classifier.predict([values])
        print(pred)
        if pred == [1.]:
            return render_template("fail-result.html")
        else:
            return render_template("success-result.html")
        
    return render_template("index.html")




if __name__=="__main__":
    app.run(debug=True)