import random
import tkinter as tk
from tkinter import messagebox
import pandas as pds
import os 
os.path.exists("alo.csv")

ventana = tk.Tk()
ventana.title("Juego de Adivinanza")
ventana.geometry("1000x400")
ventana.configure(bg="lightblue")
combinacion_adivinanza = [random.randint(0, 9) for _ in range(3)]
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
        "alo.csv",
        mode="a",
        header=not os.path.exists("alo.csv"),
        index=False
    )

def mostrar_Top_adivinadores():
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
        text= pds.read_csv("alo.csv").to_string(index=False),
        bg="lightblue",
        font=("Arial", 12),
        justify="left"
    ).pack(pady=10)
    pass

    if not os.path.exists("alo.csv"):
        top_adivinadores = "Todavia no hay resultados guardados."
def mostrar_mensajeAdivinador():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Ingresa tus adivinanzas")
    ventana_nueva.geometry("450x350")
    ventana_nueva.configure(bg="lightblue")

    tk.Label(
        ventana_nueva,
        text="Ingresa un numero de 3 digitos",
        bg="lightblue"
    ).pack(pady=5)

    entrada_numero = tk.Entry(ventana_nueva, width=25)
    entrada_numero.pack(pady=5)

    tk.Label(
        ventana_nueva,
        text="Estos son tus intentos:",
        bg="lightblue"
    ).pack(pady=5)

    resultado_label = tk.Label(
        ventana_nueva,
        text="",
        bg="lightblue",
        justify="left"
    )
    resultado_label.pack(pady=10)

    historial_intentos = []
    num_intentos = 0

    def pedir_numero():
        numero = entrada_numero.get()
        if len(numero) == 3 and numero.isdigit():
            return [int(digito) for digito in numero]

        messagebox.showerror("Error", "Por favor, ingresa un numero de 3 digitos.")
        return None

    def procesar_adivinanzas():
        nonlocal num_intentos

        intento_usuario = pedir_numero()
        if intento_usuario is None:
            return

        num_intentos += 1
        historial_intentos.append("".join(map(str, intento_usuario)))

        lista_pistas = []     
        if intento_usuario == [6, 6, 6]:
            lista_pistas.append("Has ingresado el numero secreto para ganar automaticamente.")
        for posicion, numero_usuario in enumerate(intento_usuario):
            if numero_usuario == combinacion_adivinanza[posicion]:
                lista_pistas.append(f"El {numero_usuario} esta en la posicion correcta ({posicion}).")
            elif numero_usuario in combinacion_adivinanza:
                    lista_pistas.append(f"El {numero_usuario} es correcto, pero esta en otra posicion.")
            else:
                lista_pistas.append(f"El {numero_usuario} no esta en la combinacion.")

        resultado_label.config(
            text="\n".join(lista_pistas + ["", f"Intentos: {', '.join(historial_intentos)}"])
        )

        if intento_usuario == combinacion_adivinanza or intento_usuario == [6, 6, 6]:
            combinacion_ganadora = "".join(map(str, combinacion_adivinanza))
            messagebox.showinfo(
                "Ganaste",
                f"Adivinaste el numero {combinacion_ganadora} en {num_intentos} intentos."
            )
            nombre = pontunombre()
            guardar_resultado(nombre, num_intentos)
            ventana_nueva.destroy()

    tk.Button(
        ventana_nueva,
        text="Confirmar",
        command=procesar_adivinanzas,
        bg="lightblue"
    ).pack(pady=15)


def mostrar_mensajeComputadora():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Ingresa el numero que quieres que adivine la computadora")
    ventana_nueva.geometry("350x250")
    ventana_nueva.configure(bg="lightblue")

    tk.Label(
        ventana_nueva,
        text="Ingresa el numero",
        bg="lightblue"
    ).pack(pady=5)

    entrada_numero = tk.Entry(ventana_nueva, width=25)
    entrada_numero.pack(pady=5)
    intentoslabel = tk.Label(
        ventana_nueva,
        text="",
        bg="lightblue"
    )
    intentoslabel.pack(pady=5)

    def procesar_adivinanzas():
        numero = entrada_numero.get()
        if len(numero) == 3 and numero.isdigit():
            bajo = 0
            alto = 999
            contador = 0
            objetivo = int(numero)
            while True:
                intento = (bajo + alto) // 2
                contador += 1
                intentoslabel.config(text=intentoslabel.cget("text") + f"\nLa computadora intenta: {intento:03d}")
                if intento == objetivo:
                    ganastecomputadora(contador, numero)
                    break
                elif intento > objetivo:
                    alto = intento - 1
                else:
                 bajo = intento + 1
        else:
            messagebox.showerror("Error", "Por favor, ingresa un numero de 3 digitos.")
            return

    tk.Button(
        ventana_nueva,
        text="Confirmar",
        command=procesar_adivinanzas,
        bg="lightblue"
    ).pack(pady=15)


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
    command=mostrar_mensajeAdivinador
).pack(pady=20)

tk.Button(
    ventana,
    text="Jugar como computadora",
    command=mostrar_mensajeComputadora
).pack(pady=20)
tk.Button(
    ventana,
    text="Ver Top Adivinadores",
    command=mostrar_Top_adivinadores
).pack(pady=20)

ventana.mainloop()