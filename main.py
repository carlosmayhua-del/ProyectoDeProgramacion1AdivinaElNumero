import os
import Funciones
import pandas as pds
import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()
ventana.title("Juego de Adivinanza")
ventana.geometry("1000x400")
ventana.configure(bg="lightblue")
nombre_jugador = tk.StringVar()


def ganastecomputadora(num_intentos, numero):
    messagebox.showinfo(
        "Ganaste",
        f"Adivino el numero {numero} en {num_intentos} intentos."
    )


def pontunombre():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Ingresa tu nombre")
    ventana_nueva.geometry("350x250")
    ventana_nueva.configure(bg="lightblue")

    tk.Label(
        ventana_nueva,
        text="Ingresa tu nombre",
        bg="lightblue"
    ).pack(pady=5)

    entrada_nombre = tk.Entry(ventana_nueva, width=25)
    entrada_nombre.pack(pady=5)

    def procesar_nombre():
        nombre = entrada_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa tu nombre.")
            return

        nombre_jugador.set(nombre)
        messagebox.showinfo("Nombre ingresado", f"Nombre: {nombre}")
        ventana_nueva.destroy()
        
    tk.Button(
        ventana_nueva,
        text="Confirmar",
        command=procesar_nombre,
        bg="lightblue"
    ).pack(pady=15)
    ventana_nueva.grab_set()
    ventana_nueva.wait_window()
    return nombre_jugador.get()


def guardar_resultado(nombre, num_intentos):
    pds.DataFrame({
        "Nombre": [nombre],
        "Intentos": [num_intentos]
    }).to_csv(
        "top.csv",
        mode="a",
        header=not os.path.exists("top.csv"),
        index=False
    )

def mostrar_Top_adivinadores():
    if not os.path.exists("top.csv"):
        messagebox.showinfo("Top Adivinadores", "Todavia no hay resultados guardados.")
        return

    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Top Adivinadores")
    ventana_nueva.geometry("400x300")
    ventana_nueva.configure(bg="lightblue")
    tk.Label(
        ventana_nueva,
        text="Top Adivinadores",
        bg="lightblue",
        font=("Arial", 16)
    ).pack(pady=10)
    tk.Label(
        ventana_nueva,
        text= pds.read_csv("top.csv").to_string(index=False),
        bg="lightblue",
        font=("Arial", 12),
        justify="left"
    ).pack(pady=10)


tk.Label(
    ventana,
    text=(
        "El juego consiste en que un participante (la computadora o el usuario) piense en una\n"
        "secuencia de 3 elementos del conjunto elegido, y el otro participante intente adivinar\n"
        "dicha secuencia"
    ),
    bg="lightblue",
    font=("Arial", 14)
).pack(pady=10)

tk.Button(
    ventana,
    text="Jugar como adivinador",
    command=lambda: Funciones.mostrar_mensajeAdivinador(
        ventana,
        pontunombre,
        guardar_resultado
    )
).pack(pady=20)

tk.Button(
    ventana,
    text="Jugar como computadora",
    command=lambda: Funciones.mostrar_mensajeComputadora(
        ventana,
        ganastecomputadora
    )
).pack(pady=20)
tk.Button(
    ventana,
    text="Ver Top Adivinadores",
    command=mostrar_Top_adivinadores
).pack(pady=20)

ventana.mainloop()
