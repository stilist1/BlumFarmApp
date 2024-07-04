import requests as req
import json
import time
import random
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import ttk

head = {}  

def fetch_balance(jwt):
    global head
    head = {
        'Authorization': 'Bearer ' + jwt,
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    try:
        resp = req.get('https://game-domain.blum.codes/api/v1/user/balance', headers=head)
        response_data = json.loads(resp.text)
        count = response_data['playPasses']
        lbl_balance.config(text=f"У вас есть {count} билетов")
        return count
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        return None

def start_game(jwt, count):
    global head
    try:
        games = int(entry_games.get())
        if games > count:
            messagebox.showerror("Ошибка", "У вас не хватает билетов")
            return
        elif games == 0:
            messagebox.showerror("Ошибка", "У вас нет билетов")
            return

        lbl_status.config(text="Начал играть...")
        root.update_idletasks()

        total_point = 0
        for i in range(games):
            post_id = req.post('https://game-domain.blum.codes/api/v1/game/play', headers=head)
            id = json.loads(post_id.text)['gameId']
            time.sleep(random.randrange(30, 60, 5))
            points = random.randint(150, 250)
            endGame = req.post('https://game-domain.blum.codes/api/v1/game/claim', headers=head, json={
                "gameId": id, "points": points})
            lbl_status.config(text=f"{i + 1} / {games} игр")
            root.update_idletasks()
            time.sleep(random.randint(1, 5))
            total_point += points

        lbl_total_points.config(text=f"Всего зафармлено поинтов: {total_point}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def on_fetch_balance():
    jwt = entry_jwt.get()
    global balance_count
    balance_count = fetch_balance(jwt)

def on_start_game():
    jwt = entry_jwt.get()
    start_game(jwt, balance_count)

root = ThemedTk(theme="equilux")
root.title("Game Farming App")
root.geometry("520x180")
root.resizable(False, False)

background_color = "#333333"

background_label = tk.Label(root, bg=background_color)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

style = ttk.Style(root)
style.configure("TLabel", background="#333333", foreground="#ffffff")
style.configure("TButton", background="#333333", foreground="#ffffff")
style.configure("TEntry", fieldbackground="#555555", foreground="#ffffff")

tk.Label(root, text="Введите Bearer токен:", bg="#333333", fg="#ffffff").place(x=10, y=10)
entry_jwt = ttk.Entry(root, width=50)
entry_jwt.place(x=200, y=10)

btn_fetch_balance = ttk.Button(root, text="Проверить баланс", command=on_fetch_balance)
btn_fetch_balance.place(x=10, y=40)

lbl_balance = ttk.Label(root, text="У вас есть 0 билетов")
lbl_balance.place(x=200, y=40)

tk.Label(root, text="Сколько билетов вы хотите использовать?", bg="#333333", fg="#ffffff").place(x=10, y=70)
entry_games = ttk.Entry(root, width=5)
entry_games.place(x=270, y=70)

btn_start_game = ttk.Button(root, text="Начать игру", command=on_start_game)
btn_start_game.place(x=10, y=100)

lbl_status = ttk.Label(root, text="")
lbl_status.place(x=200, y=100)

lbl_total_points = ttk.Label(root, text="Всего зафармлено поинтов: 0")
lbl_total_points.place(x=10, y=130)

balance_count = 0

root.mainloop()
