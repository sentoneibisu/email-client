import getpass
import imaplib
import email

def is_attached(msg):
    cont_disp = msg['Content-Disposition']
    if cont_disp and cont_disp.startswith('attachment'):
        return True
    else:
        return False

class MailReceiver:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.imap_host = "imap.spmode.ne.jp"
        self.imap_port = 993

    def get_attached_files(self):
        conn = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
        conn.login(self.user_id, self.password)
        conn.select()
        typ, data = conn.search(None, 'ALL')
        nums = data[0].split()
        for num in nums:
            print '[+] ', num
            typ, data = conn.fetch(num, '(RFC822)')
            raw_data = data[0][1]
            msg = email.message_from_string(raw_data)
        
            if msg.is_multipart() is True:
                print "[+] msg is multipart."
                for sub_msg in msg.get_payload():
                    if is_attached(sub_msg):
                        file_name = str(num) + '.dat'
                        attached_data = sub_msg.get_payload(decode=True)
                        with open(file_name, 'wb') as f:
                             f.write(attached_data)
            else:
                print "[+] msg is not multipart."
        conn.close()
        conn.logout()

if __name__ == '__main__':
    user_id = raw_input("ID: ")
    password = getpass.getpass()
    mail_recv = MailReceiver(user_id, password)
    mail_recv.get_attached_files()
