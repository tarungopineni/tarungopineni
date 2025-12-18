from imap_tools import MailBox

def check_mail(req):
    password = "XXXXXXXXXXXXXXXXXXXX"
    mail = "sendermail@gmail.com"

    with MailBox("imap.gmail.com").login(mail,password,"Inbox") as mb:
        for msg in mb.fetch(limit=1,reverse=True,mark_seen=True):
            if req == msg.from_:
                return True
    return False

print(check_mail("examplemail@gmail.com"))