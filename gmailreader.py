# Author : Sandhan Sarma <sandhansmailbox@gmail.com>
# Description : A simple script that logs into your gmail account and fetches your emails
# Note : you will have to enable imap forwarding in your gmail settings

import sys
import imaplib
import getpass
import email

class GmailReader:
    def __init__(self):
        self.imap_object = imaplib.IMAP4_SSL('imap.gmail.com')

    def login(self, email_id, password):
        try:
            self.imap_object.login(email_id,password)
            print("Login success!")
            return True
        except imaplib.IMAP4.error:
            print("Login failed!")
        return False

    def select_mailbox(self,label):
        status, response = self.imap_object.select(label)
        if 'OK' in status:
            print("{} selected!".format(label))
            return True
        else:
            print("Failed to select {} !".format(label))
            return False

    def fetch_emails(self, email_type="ALL"):
        # other options :UNSEEN, SEEN, ALL
        print("Trying to fetch {} emails ...".format(email_type.lower()))
        status, response = self.imap_object.search(None, '({})'.format(email_type))
        email_queue = []

        if 'OK' in status:
            emails = response[0].decode().split()
            if emails:
                for num in emails:
                    fetch_status, data = self.imap_object.fetch(num,'(RFC822)')
                    if 'OK' in fetch_status:
                        msg = email.message_from_string(data[0][1].decode())
                        email_queue.append(
                        {
                          "date":msg['Date'],
                          "from":msg['From'],
                          "subject":msg['Subject'],
                          "body":"".join([part.get_payload() for part in msg.walk()][1]).replace("\r","").replace("\n"," ")
                        })
            else:
                print("No vaild emails found!")

        return email_queue

    def close(self):
        print("Logging out ...",end=" ")
        self.imap_object.close()
        self.imap_object.logout()
        print("Done.")


if __name__ =="__main__":
    if len(sys.argv)==2:
        email_id = sys.argv[1]
        mygmail = GmailReader()
        if mygmail.login(email_id, getpass.getpass()):
            if mygmail.select_mailbox("INBOX"):
                emails = mygmail.fetch_emails()
                if emails:
                    for mail in emails:
                        print(mail)
                        print()
        mygmail.close()
    else:
        print("usage : python3 {} abc@gmail.com".format(sys.argv[0]))
        sys.exit()
