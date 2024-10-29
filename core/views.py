from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .decorators import *
from contact.models import *

import pandas as pd
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

def load_data():
    df = pd.read_csv('dataset/Liver Patient Dataset (LPD)_train.csv', encoding='unicode_escape')
    df.columns = df.columns.str.strip()
    label2int = {'Male': 1, 'Female': 0}
    df['Gender of the patient'] = df['Gender of the patient'].map(label2int)
    imputer = SimpleImputer(strategy='mean')
    df.iloc[:, :-1] = imputer.fit_transform(df.iloc[:, :-1])
    x = df.drop(['Result'], axis=1)
    y = df['Result']
    return train_test_split(x, y, test_size=0.2, random_state=0)

x_train, x_test, y_train, y_test = load_data()

lr = LogisticRegression().fit(x_train, y_train)
rf = RandomForestClassifier().fit(x_train, y_train)
cv = SVC().fit(x_train, y_train)
dg = DecisionTreeClassifier().fit(x_train, y_train)

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def predection(request):
    if request.method == "POST":
        try:
            # Get user inputs and convert them to appropriate types
            txt1 = float(request.POST.get("txt1", 0))
            txt2 = float(request.POST.get("txt2", 0))
            txt3 = float(request.POST.get("txt3", 0))
            txt4 = float(request.POST.get("txt4", 0))
            txt5 = float(request.POST.get("txt5", 0))
            txt6 = float(request.POST.get("txt6", 0))
            txt7 = float(request.POST.get("txt7", 0))
            txt8 = float(request.POST.get("txt8", 0))
            txt9 = float(request.POST.get("txt9", 0))
            txt10 = float(request.POST.get("txt10", 0))

            user_data = pd.DataFrame({
                'Age of the patient': [txt1],
                'Gender of the patient': [txt2],
                'Total Bilirubin': [txt3],
                'Direct Bilirubin': [txt4],
                'Alkphos Alkaline Phosphotase': [txt5],
                'Sgpt Alamine Aminotransferase': [txt6],
                'Sgot Aspartate Aminotransferase': [txt7],
                'Total Protiens': [txt8],
                'ALB Albumin': [txt9],
                'A/G Ratio Albumin and Globulin Ratio': [txt10],
            })
            user_data.columns = user_data.columns.str.strip()

            user_result1 = lr.predict(user_data)[0]
            user_result2 = rf.predict(user_data)[0]
            user_result3 = cv.predict(user_data)[0]
            user_result4 = dg.predict(user_data)[0]

            context = {
                'user_result1': "liver disease" if user_result1 == 1 else "No liver disease",
                'user_result2': "liver disease" if user_result2 == 1 else "No liver disease",
                'user_result3': "liver disease" if user_result3 == 1 else "No liver disease",
                'user_result4': "liver disease" if user_result4 == 1 else "No liver disease",
            }

            return render(request, 'predection.html', context)

        except Exception as e:
            return render(request, 'predection.html', {'error': str(e)})
    return render(request, 'predection.html')

@login_required(login_url='login')
def contact(request):
    try:
        if request.method == "POST":
            txt1 = request.POST['txt1']          
            txt2 = request.POST['txt2']          
            txt3 = request.POST['txt3']          
            txt4 = request.POST['txt4']          
            obj = Contact(
                email = txt1,
                phone = txt2,
                website = txt3,
                message = txt4,
                )
            obj.save()
    except:
        print('Error!.. Try Again Later')
        return  redirect('contact')
    return render(request, 'contact.html')


@unathenticated_user
def ac_login(request):
    if request.method == 'POST':
        username = request.POST.get('login-txt1')
        password = request.POST.get('login-txt2')
        try:
            lstatus = User.objects.get(username=username)
            if lstatus.is_active:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    print('Invalid Credentials..!')
            else:
                print('Contact Dean to activate Account')
        except:
            print('Invalid Credentials..!')
            return redirect ('login')
    return render (request, 'login.html')

def ac_logout(request):
    logout(request)
    return redirect('login')



