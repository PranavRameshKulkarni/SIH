from django.contrib import messages, auth
from django.shortcuts import render, redirect
import pyrebase

# Create your views here.

# configuration from firebase project
config = {
    'apiKey': "AIzaSyCr-PMppoopMf8ZrswUPGqaULjuFpEqVGA",
    'authDomain': "djangowithfirebase.firebaseapp.com",
    'databaseURL': "https://djangowithfirebase.firebaseio.com",
    'projectId': "djangowithfirebase",
    'storageBucket': "djangowithfirebase.appspot.com",
    'messagingSenderId': "512767560835",
    'appId': "1:512767560835:web:cc23033261aa0e92be1fb6",
    'measurementId': "G-1B2K9WZ7V6",
    "serviceAccount": "C:/Users/prana/Downloads/serviceAccountKey.json",
}
firebase = pyrebase.initialize_app(config)
firebase_auth = firebase.auth()
database = firebase.database()


def signIn(request):
    return render(request, 'signin.html')


def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
    except:
        messages.info(request, 'Invalid user')
        return redirect('/')
    print(user)
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, 'postsign.html', {'name': email})


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    # auth.logout(request)
    return redirect('/')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = firebase_auth.create_user_with_email_and_password(email, password)
        except:
            messages.info(request, 'No user created')
            return render(request, 'signup.html')
        uid = user['localId']
        data = {'name': name, 'status': '1'}
        database.child("users").child(uid).child("details").set(data)

        return render(request, 'postsign.html', {'name': name})
    else:
        return render(request, 'signup.html')


def createreport(request):
    return render(request, 'createreport.html')


def postcreate(request):
    from datetime import timezone, datetime
    import time
    import pytz
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    url = request.POST.get('url')
    print(work)
    print(progress)
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))

    data = {
        'work': work,
        'progress': progress,
        'url': url
    }
    try:
        idToken = request.session['uid']
        print(str(idToken))
        account = firebase_auth.get_account_info(idToken)
        print(str(account))
        account = account['users']
        account = account[0]
        account = account['localId']
        database.child('users').child(account).child('report').child(millis).set(data, idToken)
        name = database.child('users').child(account).child('details').child('name').get(idToken).val()
        return render(request, 'postsign.html', {'name': name})
    except:
        messages.info(request, "Oops!!NO user signed in")
        return redirect('/')


def checkreport(request):
    import datetime
    idToken = request.session['uid']
    account = firebase_auth.get_account_info(idToken)
    account = account['users']
    account = account[0]
    account = account['localId']
    timestamp = database.child('users').child(account).child('report').shallow().get(idToken).val()
    print(timestamp)
    timestamp_list = []
    for time in timestamp:
        timestamp_list.append(time)

    timestamp_list.sort(reverse=True)
    print(timestamp_list)
    work = []
    progress = []
    for i in timestamp_list:
        work.append(database.child('users').child(account).child('report').child(i).child('work').get(idToken).val())
        name = database.child('users').child(account).child('details').child('name').get(idToken).val()
        progress.append(
            database.child('users').child(account).child('report').child(i).child('progress').get(idToken).val())
    date = []
    for i in timestamp_list:
        i = float(i)
        date.append(datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y'))
    comb_list = zip(timestamp_list, date, work)
    name = database.child('users').child(account).child('details').child('name').get(idToken).val()
    return render(request, 'checkreport.html', {'comb_list': comb_list, 'name': name, 'uid': account})


def post_report(request):
    import datetime
    timestamp = request.GET.get('z')
    idToken = request.session['uid']
    account = firebase_auth.get_account_info(idToken)
    account = account['users']
    account = account[0]
    account = account['localId']
    work = database.child('users').child(account).child('report').child(timestamp).child('work').get(idToken).val()
    progress = database.child('users').child(account).child('report').child(timestamp).child('progress').get(
        idToken).val()
    img_url = database.child('users').child(account).child('report').child(timestamp).child('url').get(idToken).val()
    print("img_url:     ",img_url)
    dat = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%H:%M %d-%m-%y')
    return render(request, 'postreport.html', {'time': timestamp, 'date': dat, 'work': work, 'progress': progress, 'img_url': img_url})
