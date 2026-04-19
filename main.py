import random
import tkinter as tk
from tkinter import messagebox


ventana = tk.Tk()
ventana.title("Juego de Adivinanza")
ventana.geometry("1000x400")
ventana.configure(bg="lightblue")
combinacion_adivinanza = [random.randint(0, 9) for _ in range(3)]


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

        intentos_usuario = pedir_numero()
        if intentos_usuario is None:
            return

        num_intentos += 1
        historial_intentos.append("".join(map(str, intentos_usuario)))

        lista_pistas = []
        for posicion, numero_usuario in enumerate(intentos_usuario):
            if numero_usuario == combinacion_adivinanza[posicion]:
                lista_pistas.append(f"El {numero_usuario} esta en la posicion correcta ({posicion}).")
            elif numero_usuario in combinacion_adivinanza:
                lista_pistas.append(f"El {numero_usuario} es correcto, pero esta en otra posicion.")
            else:
                lista_pistas.append(f"El {numero_usuario} no esta en la combinacion.")

        resultado_label.config(
            text="\n".join(lista_pistas + ["", f"Intentos: {', '.join(historial_intentos)}"])
        )

        if intentos_usuario == combinacion_adivinanza:
            combinacion_ganadora = "".join(map(str, combinacion_adivinanza))
            messagebox.showinfo(
                "Ganaste",
                f"Adivinaste el numero {combinacion_ganadora} en {num_intentos} intentos."
            )

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

    def procesar_adivinanzas():
        numero = entrada_numero.get()
        messagebox.showinfo("Numero ingresado", f"Numero: {numero}")

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

ventana.mainloop()