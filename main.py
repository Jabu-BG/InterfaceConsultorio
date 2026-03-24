from database.database import inicializar_banco
import tkinter as tk
from interfaces.login import TelaLogin 


inicializar_banco()

root = tk.Tk()
TelaLogin(root)
root.mainloop()
