import smtplib
import random
from tkinter import Tk, Label, Entry, Button, font
from tkinter.ttk import Progressbar
import threading
continue_button = None  

def send_email():
    email = email_entry.get()

    if not email:
        print("Please enter an email address.")
        return

    def send_email_thread():
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        password = 'bqxsvzbboxovzxmj'
        server.login('kansara2909@gmail.com', password)
        otp = ''.join([str(random.randint(0, 9)) for i in range(4)])
        msg = 'Hello, Your OTP is ' + str(otp)
        sender = 'kansara2909@gmail.com'
        receiver = email
        progress_window = Tk()
        progress_window.title("Sending Email")
        progress_window.geometry("200x120")
        progress_label = Label(progress_window, text="Sending Email...", font=font.Font(family="Helvetica", size=12))
        progress_label.pack(pady=10)
        progress_bar = Progressbar(progress_window, length=150, mode='indeterminate')
        progress_bar.pack()
        message_label = Label(progress_window, text="", font=font.Font(family="Helvetica", size=12))
        message_label.pack(pady=10)
        progress_bar.start()

        try:
            server.sendmail(sender, receiver, msg)
            progress_window.after(2000, lambda: update_message_label(message_label, "Email sent successfully. Please check your inbox."))
        except smtplib.SMTPException as e:
            progress_window.after(2000, lambda: update_message_label(message_label, "Error occurred while sending email: " + str(e)))

        progress_bar.stop()
        progress_window.destroy()
        server.quit()
        update_main_message_label("Email sent successfully. \nPlease check the Inbox.", "red")
        display_continue_button(otp)

    email_thread = threading.Thread(target=send_email_thread)
    email_thread.start()

def update_message_label(label, text):
    label.config(text=text)

def update_main_message_label(text, color):
    main_message_label.config(text=text, fg=color)

def display_continue_button(otp):
    global continue_button  # Use the global keyword to access the global variable
    continue_button = Button(window, text="Continue", command=lambda: display_otp_input_page(otp), font=custom_font)
    continue_button.pack(pady=10)

def display_otp_input_page(sent_otp):
    email_label.pack_forget()  # Hide the "Enter Email" label
    email_entry.pack_forget()
    send_button.pack_forget()
    main_message_label.pack_forget()
    continue_button.pack_forget()
    otp_label = Label(window, text="Enter OTP:", font=custom_font)
    otp_label.pack(pady=10)
    otp_entry = Entry(window, font=custom_font)
    otp_entry.pack()
    verify_button = Button(window, text="Verify OTP", command=lambda: verify_otp(otp_entry.get(), sent_otp), font=custom_font, bg="#4CAF50", fg="white")
    verify_button.pack(pady=10)


def verify_otp(entered_otp, sent_otp):
    if entered_otp == sent_otp:
        update_main_message_label("OTP verification successful!", "green")
        display_success_message()
    else:
        update_main_message_label("OTP verification failed. Please try again.", "red")
        display_retry_message()

def display_success_message():
    success_message_label = Label(window, text="Success!", font=custom_font, fg="green")
    success_message_label.pack(pady=10)

def display_retry_message():
    retry_message_label = Label(window, text="Try Again!", font=custom_font, fg="red")
    retry_message_label.pack(pady=10)

window = Tk()
window.title("Email Sender")
window.geometry("300x250")
custom_font = font.Font(family="Helvetica", size=12)
email_label = Label(window, text="Enter Email:", font=custom_font)
email_label.pack(pady=10)
email_entry = Entry(window, font=custom_font)
email_entry.pack()
send_button = Button(window, text="Send Email", command=send_email, font=custom_font, bg="#4CAF50", fg="white")
send_button.pack(pady=10)
main_message_label = Label(window, text="", font=font.Font(family="Helvetica", size=12))
main_message_label.pack()
window.mainloop()
