import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()
ventana.title("Juego de Adivinanza")
ventana.geometry("1000x400")
ventana.configure(bg="lightblue")


def mostrar_mensajeAdivinador():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Ingresa tus adivinanzas")
    ventana_nueva.geometry("350x250")
    ventana_nueva.configure(bg="lightblue")
    
    label_numero = tk.Label(ventana_nueva, text="adivinaxanxote", bg="lightblue")
    label_numero.pack(pady=5)
    entrada_numero = tk.Entry(ventana_nueva, width=25)
    entrada_numero.pack(pady=5)

    def procesar_adivinanzas():
        numero = entrada_numero.get()

        messagebox.showinfo("Adivinanzas guardadas", f"Número: {numero}")
    boton_confirmar = tk.Button(ventana_nueva, text="Confirmar", command=procesar_adivinanzas, bg="lightblue")
    boton_confirmar.pack(pady=15)

def mostrar_mensajeComputadora():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Ingresa el numero que quieres que adivine la computadora")
    ventana_nueva.geometry("350x250")
    ventana_nueva.configure(bg="lightblue")
    
    label_numero = tk.Label(ventana_nueva, text="Ingresa el numero, palabra o color", bg="lightblue")
    label_numero.pack(pady=5)
    entrada_numero = tk.Entry(ventana_nueva, width=25)
    entrada_numero.pack(pady=5)

    def procesar_adivinanzas():
        numero = entrada_numero.get()
        messagebox.showinfo("Número ingresado", f"Número: {numero}")
    boton_confirmar = tk.Button(ventana_nueva, text="Confirmar", command=procesar_adivinanzas, bg="lightblue")
    boton_confirmar.pack(pady=15)
tk.Label(ventana, text="""El juego consiste en que un participante (la computadora o el usuario) piense en una
secuencia de 3 elementos del conjunto elegido, y el otro participante intente adivinar
dicha secuencia""", bg="lightblue", font=("Arial", 14)).pack(pady=10)
boton = tk.Button(ventana, text="jugar como adivinador", command=mostrar_mensajeAdivinador)
boton.pack(pady=20)
boton2 = tk.Button(ventana, text="jugar como computadora", command=mostrar_mensajeComputadora)
boton2.pack(pady=20)

ventana.mainloop()