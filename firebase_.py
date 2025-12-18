import pyrebase

my_config = {"apiKey": "api_key",
  "authDomain": "python-b71a9.firebaseapp.com",
  "databaseURL": "https://python-b71a9-default-rtdb.firebaseio.com",
  "projectId": "python-b71a9",
  "storageBucket": "python-b71a9.firebasestorage.app",
  "messagingSenderId": "810660670598",
  "appId": "1:810660670598:web:5d0f0e2f2dd72b62a77507",
  "measurementId": "G-6SQXQ45HN9"}

firebase = pyrebase.initialize_app(config=my_config)
database = firebase.database()

def push(hospital_name, mail_ids):
    checker = database.child("hospitals").get().each()
    if checker:
        found = False
        for main_folder in checker:
            main_key = main_folder.key()
            if main_key == hospital_name:
                existing_data = database.child("hospitals").child(hospital_name).child("mail_ids").get()
                existing_mail_ids = existing_data.val() or []

                for mail in mail_ids:
                    if mail not in existing_mail_ids:
                        existing_mail_ids.append(mail)

                database.child("hospitals").child(hospital_name).update({"mail_ids": existing_mail_ids})
                found = True

        if not found:
            database.child("hospitals").child(hospital_name).set({"mail_ids": mail_ids})
    else:
        database.child("hospitals").child(hospital_name).set({"mail_ids": mail_ids})

def getmail(hospital_name):
    hospital_data = database.child("hospitals").child(hospital_name).child("mail_ids").get()

    if hospital_data.val():
        return hospital_data.val()
    else:

        return []
