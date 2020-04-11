
from tkinter import *

def join_group():
    clicked_items = l.curselection()
    for item in clicked_items:
        print("Joined GRP:" + " " + l.get(item))


def send_message():	
	result = e1.get()
	l2["text"] = result
	e1.delete(0,END)
	print(result)
	

root = Tk()
l = Listbox(root, width=20, height=10, selectmode= EXTENDED)
l.insert(1,"Friends")
l.insert(2,"Family")
l.insert(3,"Work")
l.insert(4,"Gym")
l.insert(5,"Park")
l.pack()

button = Button(root, text="Join Group", command=join_group)
button.pack()


# button_delete = Button(root, text="Exit Group", command=exit_group)
# button_delete.pack()

labelframe1 = LabelFrame(root, text="Messages")  
labelframe1.pack(fill="both", expand="yes")

l1 = Label(root,text="Enter message")
l1.pack(side ="top" , pady = 5)
e1 = Entry(root)
e1.pack(side ="top")


button_message = Button(root, text="Send", command=send_message)
button_message.pack()

b3 = Button(root, text='Quit', command=root.quit)
b3.pack()

l2 = Label(labelframe1)
l2.pack(side ="top" , pady = 5)

root.geometry("500x500+200+200")

root.mainloop()