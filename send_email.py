import smtplib

# Funkcja wysyłania wiadomości e-mail
def send_email():
    email = "kruszynskibartosz1@gmail.com"
    recipient_email = "bartosz.kruszynski@student.put.poznan.pl"
    subject = "Zaraz wszystko wybuchnie"
    message = "O nie"

    text = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, "tdlndbvuxmtocihi")
    server.sendmail(email, recipient_email, text)
    server.quit()
    print("Wiadomość e-mail wysłana!")
