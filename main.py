"""Aplicación GUI principal del juego de adivinanza de números.

Utiliza tkinter para crear la interfaz gráfica del juego donde los usuarios
pueden jugar como adivinadores o dejar que la computadora adivine.
"""

import os
import Funciones
import pandas as pds
import tkinter as tk
from tkinter import messagebox

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Juego de Adivinanza")
ventana.geometry("1000x400")
ventana.configure(bg="lightblue")
nombre_jugador = tk.StringVar()  # Variable para almacenar el nombre del jugador


def ganastecomputadora(num_intentos, numero):
    """Muestra mensaje cuando la computadora adivina correctamente.
    
    Args:
        num_intentos: Número de intentos que realizó la computadora
        numero: El número que la computadora adivinó
    """
    messagebox.showinfo(
        "Ganaste",
        f"Adivino el numero {numero} en {num_intentos} intentos."
    )


def pontunombre():
    """Abre una ventana para que el usuario ingrese su nombre.
    
    Returns:
        str: El nombre ingresado por el usuario
    """
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
        """Valida y procesa el nombre ingresado."""
        nombre = entrada_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa tu nombre.")
            return

        nombre_jugador.set(nombre)  # Guardar nombre en variable global
        messagebox.showinfo("Nombre ingresado", f"Nombre: {nombre}")
        ventana_nueva.destroy()
        
    tk.Button(
        ventana_nueva,
        text="Confirmar",
        command=procesar_nombre,
        bg="lightblue"
    ).pack(pady=15)
    ventana_nueva.grab_set()  # Hacer ventana modal
    ventana_nueva.wait_window()  # Esperar hasta que se cierre
    return nombre_jugador.get()


def guardar_resultado(nombre, num_intentos):
    """Guarda el resultado del jugador en el archivo CSV.
    
    Args:
        nombre: Nombre del jugador
        num_intentos: Número de intentos que realizó
    """
    pds.DataFrame({
        "Nombre": [nombre],
        "Intentos": [num_intentos]
    }).to_csv(
        "top.csv",
        mode="a",  # Añadir sin sobrescribir
        header=not os.path.exists("top.csv"),  # Crear header si no existe
        index=False
    )

def mostrar_Top_adivinadores():
    """Abre una ventana para mostrar el ranking de mejores adivinadores."""
    # Verificar si el archivo de resultados existe
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
    # Leer y mostrar los resultados en una tabla
    tk.Label(
        ventana_nueva,
        text= pds.read_csv("top.csv").to_string(index=False),
        bg="lightblue",
        font=("Arial", 12),
        justify="left"
    ).pack(pady=10)


# ============= INTERFAZ PRINCIPAL =============

# Etiqueta con las instrucciones del juego
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

# Botón para jugar como adivinador
tk.Button(
    ventana,
    text="Jugar como adivinador",
    command=lambda: Funciones.mostrar_mensajeAdivinador(
        ventana,
        pontunombre,
        guardar_resultado
    )
).pack(pady=20)

# Botón para que la computadora adivine
tk.Button(
    ventana,
    text="Jugar como computadora",
    command=lambda: Funciones.mostrar_mensajeComputadora(
        ventana,
        ganastecomputadora
    )
).pack(pady=20)

# Botón para ver el ranking
tk.Button(
    ventana,
    text="Ver Top Adivinadores",
    command=mostrar_Top_adivinadores
).pack(pady=20)

# Iniciar la aplicación
ventana.mainloop()
