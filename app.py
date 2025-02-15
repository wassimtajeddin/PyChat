import tkinter as tk
import pymongo
from tkinter import messagebox

# Connect to mongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["PyChat"]
message_col = db["messages"]


# Tkinter GUI
root = tk.Tk()
root.title("PyChat")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

def send_message():
    if entry.get():
        message_col.insert_one({"text": entry.get()})
        entry.delete(0, tk.END)
        fetch_messages()
        

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)


messages_label = tk.Label(root, text="Messages:\n") 
messages_label.pack()

def fetch_messages():
    messages = message_col.find().sort("_id", -1)
    messages_label.config(text="Messages:\n" + "\n".join(f"-{m['text']}"for m in messages))
    root.after(2000, fetch_messages)



def confirm_delete_messages():
    response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all messages?")
    if response:
        delete_all_messages()
        
        
delete_button = tk.Button(root, text="Delete Messages", command=confirm_delete_messages)
delete_button.pack(pady=5)
    
        
def delete_all_messages():
    message_col.delete_many({})
    fetch_messages()

fetch_messages()
root.mainloop()