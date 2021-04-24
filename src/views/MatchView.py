import json
import math
import sys
import time
from functools import partial
from pathlib import Path
from tkinter import *
from tkinter import ttk

pathfile = Path(__file__).resolve()
sharedRoot = pathfile.parents[1]
sys.path.append(str(sharedRoot))

from shared.Message import Request, Response


def viewMatchByID(view, client, idMatch):
    view.destroy()
    time.sleep(0.5)
    client.send(bytes(json.dumps({ "code": Request.VIEW_MATCH_BY_ID, "data": idMatch}), "utf8"))

def viewMatchByID2(view, client, idMatch):
    #view.destroy()
    time.sleep(0.5)
    client.send(bytes(json.dumps({ "code": Request.VIEW_MATCH_BY_ID, "data": idMatch}), "utf8"))

def allMatchView(client, data):
    def onDoubleClick(event):
        currId = treeMatch.focus()
        viewMatchByID(view, client, currId)
    view = Tk()
    view.title("All matches")
    WIDTH = view.winfo_screenwidth()
    HEIGHT = view.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 3)
    PADDING_TOP = math.ceil(HEIGHT / 4)
    view.geometry(str(math.ceil(WIDTH / 3)) + "x" + str(math.ceil(HEIGHT / 3)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))
    view.configure(bg="#000000")

    styles = ttk.Style(view)
    styles.theme_use("default")
    styles.configure("Treeview", background="#000000", rowheight=30)
    styles.map("Treeview", background=[("selected", "#414141")], foreground=[("selected", "#ff8300"), ("!selected", "#f48f29")])

    treeMatch = ttk.Treeview(view)
    scrollbar = ttk.Scrollbar(view, orient=VERTICAL, command=treeMatch.yview)
    scrollbar.pack(side="right", fill=X)

    # Define columns:
    treeMatch["columns"] = ("Status", "Home", "Result", "Away")

    # Format:
    treeMatch.column("#0", anchor=CENTER, width=40, minwidth=25)
    treeMatch.column("Status", anchor=CENTER, width=60, minwidth=40)
    treeMatch.column("Home", anchor=CENTER, width=150, minwidth=100)
    treeMatch.column("Result", anchor=CENTER, width=100, minwidth=100)
    treeMatch.column("Away", anchor=CENTER, width=150, minwidth=100)

    # Headings:
    treeMatch.heading("#0", text="No", anchor=CENTER)
    treeMatch.heading("Status", text="Status", anchor=CENTER)
    treeMatch.heading("Home", text="Home", anchor=CENTER)
    treeMatch.heading("Result", text="Result", anchor=CENTER)
    treeMatch.heading("Away", text="Away", anchor=CENTER)

    treeMatch.pack(fill=BOTH)

    if len(data) > 0:
        for i in range(0, len(data)):
            item = data[i]
            result = item["homeScore"] + " - " + item["awayScore"]
            treeMatch.insert("", "end", text=i + 1, iid=item["idMatch"], values=(item["status"], item["home"], result, item["away"]))

    treeMatch.bind("<Double-1>", onDoubleClick)

    view.mainloop()

def onCloseWindow(client):
    client.send(bytes(json.dumps({ "code": Request.HALT_RT_MODE }), "utf8"))

def realTimeView(client, data):
    view = Tk()
    view.title("Auto-Reload all matches")
    WIDTH = view.winfo_screenwidth()
    HEIGHT = view.winfo_screenheight()
    PADDING_LEFT = math.ceil(WIDTH / 3)
    PADDING_TOP = math.ceil(HEIGHT / 4)
    view.geometry(str(math.ceil(WIDTH / 3)) + "x" + str(math.ceil(HEIGHT / 3)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))
    view.configure(bg="#000000")

    styles = ttk.Style(view)
    styles.configure("Treeview", background="#000000", rowheight=30)
    styles.map("Treeview", background=[("selected", "#414141")], foreground=[("selected", "#ff8300"), ("!selected", "#f48f29")])

    treeMatch = ttk.Treeview(view)
    scrollbar = ttk.Scrollbar(view, orient=VERTICAL, command=treeMatch.yview)
    scrollbar.pack(side="right", fill=X)

    # Define columns:
    treeMatch["columns"] = ("Status", "Home", "Result", "Away")

    # Format:
    treeMatch.column("#0", anchor=CENTER, width=40, minwidth=25)
    treeMatch.column("Status", anchor=CENTER, width=60, minwidth=40)
    treeMatch.column("Home", anchor=CENTER, width=150, minwidth=100)
    treeMatch.column("Result", anchor=CENTER, width=100, minwidth=100)
    treeMatch.column("Away", anchor=CENTER, width=150, minwidth=100)

    # Headings:
    treeMatch.heading("#0", text="No", anchor=CENTER)
    treeMatch.heading("Status", text="Status", anchor=CENTER)
    treeMatch.heading("Home", text="Home", anchor=CENTER)
    treeMatch.heading("Result", text="Result", anchor=CENTER)
    treeMatch.heading("Away", text="Away", anchor=CENTER)

    treeMatch.pack(fill=BOTH)

    if len(data) > 0:
        for i in range(0, len(data)):
            item = data[i]
            result = item["homeScore"] + " - " + item["awayScore"]
            treeMatch.insert("", "end", text=i + 1, iid=item["idMatch"], values=(item["status"], item["home"], result, item["away"]))

    my_button= Button(master=view, text= "Stop real-time reload", font=('Helvetica bold', 10),
    borderwidth=2, command= lambda: onCloseWindow(client))
    my_button.pack(pady=5)
    view.after(5000, lambda: view.destroy())
    view.mainloop()