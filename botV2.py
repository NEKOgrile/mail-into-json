import imaplib
import email
from email.header import decode_header
from traceback import print_tb
import os
import json
import html2text
import re


# -------------------Function--------------------

def encodage(corps, dico):

    h = html2text.HTML2Text()
    h.ignore_links = True
    corps = str(h.handle(corps))

    # --------------------------------------------------------
    regex = r'\n'

    corps = re.sub(regex, "", corps, 0)

    regex = r"\!\[.+?\]\(https://[\w\./\-\\\?\=\&\%\~\@\-\-\_\+]+\)"

    corps = re.sub(regex, "", corps, 0)

    regex = r"\!\[\]\(https://[\w\./\-\\\?\=\&\%\~\@\-\-\_\+]+\)"

    corps = re.sub(regex, "", corps, 0)

    regex = r"[\s|\||\-\#]{2,}"

    # ---------- a faire une function car surement desactivé
    # si le bot discord li bien les ascii

    corps = re.sub(regex, "", corps, 0)

    regex = r'é'

    corps = re.sub(regex, "e", corps, 0)

    regex = r'ê'

    corps = re.sub(regex, "e", corps, 0)

    regex = r'à'

    corps = re.sub(regex, "a", corps, 0)

    regex = r'è'

    corps = re.sub(regex, "e", corps, 0)

    regex = r'î'

    corps = re.sub(regex, "i", corps, 0)

    regex = r"’"

    corps = re.sub(regex, " ", corps, 0)

    # ---------- a faire une function car surement desactivé
    # si le bot discord li bien les ascii

    # --------------------------------------------------------

    print("body:", corps)
    dico['body'] = str(corps)
    # --------------------------------------------------------


# -------------------/Function--------------------
# account credentials
username = "thebestforeve81@gmail.com"
password = "mdp"
# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# or check this page: https://www.systoolsgroup.com/imap/
# for office 365, it's this:
imap_server = "imap.gmail.com"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)

status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 1
# total number of emails

messages = int(messages[0])


maildict = {}
maildict['n message'] = str(messages)

for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]

            if isinstance(encoding, str):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)

            # decode email sender

            From, encoding = decode_header(msg.get("From"))[0]

            if isinstance(From, bytes):
                try:
                    From = From.decode(encoding)
                except:
                    pass

            print("Subject:", subject)
            print("From:", From)

            maildict['Subject'] = str(subject)
            maildict['From'] = str(From)

            content_type = msg.get_content_type()
            print("content_type:", content_type)

            try:

                body = msg.get_payload(decode=True).decode()

            except:

                pass

            if content_type == "text/plain":

                # --------------------------------------------------------
                encodage(body, maildict)

            # if the email message is multipart
            if content_type == "text/html":
                # --------------------------------------------------------

                encodage(body, maildict)

                # --------------------------------------------------------

                print("="*100)
                print(msg.is_multipart())

            if msg.is_multipart():
                # --------------------------------------------------------
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(
                        part.get("Content-Disposition"))
                    body = ''
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass

                    # --------------------------------------------------------

                    encodage(body, maildict)
                    # --------------------------------------------------------
                encodage(body, maildict)

with open(f'{os.path.abspath( os.path.dirname( __file__ ))}\\valeur_bot.json', 'w') as f:
    json.dump(maildict, f, indent=4)
    f.close()
# close the connection and logout


imap.close()
imap.logout()
