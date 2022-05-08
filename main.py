from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    # List of letters, numbers, and symbols.
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    #populates a list of letters, numbers and symbols with a predetermined amount of each to ensure complexity.
    password_letters = [choice(letters) for x in range(randint(8, 10))]
    password_symbols = [choice(symbols) for x in range(randint(2, 4))]
    password_numbers = [choice(numbers) for x in range(randint(2, 4))]

    #joins passwords lists and shuffles the joined list to create final list. Then creates new string password.
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    #adds password to entry for user and also to clipboard for easy access
    password_entry.insert(END, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    #get variables from form
    email = email_entry.get()
    website = website_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password" : password,
        }
    }

    #check to make sure user filled in needed entries.
    if not website or not password:
        messagebox.showwarning(title="Error", message="Please do not leave any field empty")
    else:
        try:
            with open("passwords.json", "r") as f:
                # read old data
                data = json.load(f)
        except FileNotFoundError:
            with open("passwords.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            #update old data with new data
            data.update(new_data)

            with open("passwords.json", "w") as f:
                #save updated data
                json.dump(data, f, indent=4)
        finally:
            website_entry.delete(0, 'end')
            password_entry.delete(0, "end")

# ---------------------------- UI SETUP ------------------------------- #


def find_password():
    website = website_entry.get()
    try:
        with open("passwords.json", "r") as f:
            # read old data
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Data File not found.")
    else:
        #find the webiste in data
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox(title="Error", messagebox=f"No details for {website} exists.")

# ---------------------------- SEARCH ------------------------------- #

#create windows with title
window = Tk()
window.title("Password Generator")
window.config(padx=20, pady=20)

#create canvas, load background picture and place in correct place on the window
canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

#labels
website_label = Label(text="Website:", font=("Arial", 18))
website_label.grid(column=0, row=3)

email_label = Label(text="Email/Username:", font=("Arial", 18))
email_label.grid(column=0, row=4)

password_label = Label(text="Password:", font=("Arial", 18))
password_label.grid(column=0, row=5)

#buttons
button1 = Button(text="Generate Password", highlightthickness=0, command=generate_password)
button1.grid(column=2, row=5)

button2 = Button(text="Add", highlightthickness=0, width=36, command=save_password)
button2.grid(column=1, row=6, columnspan=2)

button3 = Button(text="Search", highlightthickness=0, width=13, command=find_password)
button3.grid(column=2, row=3)

#input
website_entry = Entry(width=20)
website_entry.grid(column=1, row=3)
website_entry.focus()

email_entry = Entry(width=38)
email_entry.grid(column=1, row=4, columnspan=2)
email_entry.insert(END, "joseph.cornejo@ymail.com")

password_entry = Entry(width=21)
password_entry.grid(column=1, row=5)


window.mainloop()