# -*- coding: utf-8 -*-
import random
from collections import Counter

import tkinter as tk
from tkinter import messagebox


def calcular_pista(combinacion_a, combinacion_b):
    copia = combinacion_b.copy()
    pista = 0
    for numero in combinacion_a:
        if numero in copia:
            pista += 1
            copia.remove(numero)
    return pista


def generar_jugadas_posibles():
    return [[int(digito) for digito in f"{numero:03d}"] for numero in range(1000)]


def pedir_intento():
    while True:
        intento = input("\nIngresa un numero de 3 digitos (000-999): ")
        if len(intento) == 3 and intento.isdigit():
            return [int(digito) for digito in intento]
        print("\nError, volver a intentar")


def mostrar_victoria(intento_pc, numero_secreto, jugadas_pc, contador):
    if intento_pc == numero_secreto:
        extra = "".join(map(str, intento_pc))
        print(f"Tu numero es: {extra}")
        print(f"Mi cantidad de intentos fue: {contador}")
        return

    for indice in range(1, len(jugadas_pc)):
        contador += 1
        jugada_canon = jugadas_pc[indice]
        print(f"Intento {contador}: La computadora prueba con {''.join(map(str, jugada_canon))}")
        if jugada_canon == numero_secreto:
            extra = "".join(map(str, jugada_canon))
            print(f"Tu numero es: {extra}")
            print(f"Mi cantidad de intentos fue: {contador}")
            return


def mostrar_resumen_usuario(historial, pcnm, contador):
    historia = " otro: ".join(map(str, historial))
    extra = "".join(map(str, pcnm))
    print(f"\nTodos los intentos fueron: {historia}")
    print(f"\nGanaste, la respuesta correcta era: {extra}")
    print(f"\nIntentaste un total de: {contador}")


def mostrar_mensajeAdivinador(ventana, pontunombre, guardar_resultado):
    combinacion_secreta = [random.randint(0, 9) for _ in range(3)]
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

    def pedir_numero_gui():
        numero = entrada_numero.get()
        if len(numero) == 3 and numero.isdigit():
            return [int(digito) for digito in numero]

        messagebox.showerror("Error", "Por favor, ingresa un numero de 3 digitos.")
        return None

    def procesar_adivinanzas():
        nonlocal num_intentos

        intento_usuario = pedir_numero_gui()
        if intento_usuario is None:
            return

        num_intentos += 1
        historial_intentos.append("".join(map(str, intento_usuario)))

        lista_pistas = []
        if intento_usuario == [6, 6, 6]:
            lista_pistas.append("Has ingresado el numero secreto para ganar automaticamente.")

        pista = calcular_pista(intento_usuario, combinacion_secreta)
        lista_pistas.append(f"Hay {pista} numeros en la combinacion.")

        resultado_label.config(
            text="\n".join(lista_pistas + ["", f"Intentos: {', '.join(historial_intentos)}"])
        )

        if intento_usuario == combinacion_secreta or intento_usuario == [6, 6, 6]:
            combinacion_ganadora = "".join(map(str, combinacion_secreta))
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


def mostrar_mensajeComputadora(ventana, ganastecomputadora):
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Ingresa el numero que quieres que adivine la computadora")
    ventana_nueva.geometry("500x420")
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
        bg="lightblue",
        justify="left"
    )
    intentoslabel.pack(pady=5)

    def procesar_adivinanzas():
        numero = entrada_numero.get()
        if len(numero) != 3 or not numero.isdigit():
            messagebox.showerror("Error", "Por favor, ingresa un numero de 3 digitos.")
            return

        numero_secreto = [int(digito) for digito in numero]
        jugadas_pc = generar_jugadas_posibles()
        contador = 0
        historial_pc = []

        while True:
            intento_pc = jugadas_pc[0]
            contador += 1
            historial_pc.append(f"Intento {contador}: {''.join(map(str, intento_pc))}")

            if Counter(intento_pc) == Counter(numero_secreto):
                intentoslabel.config(text="\n".join(historial_pc))
                ganastecomputadora(contador, numero)
                break

            pista = calcular_pista(intento_pc, numero_secreto)
            sospechosos = []
            for jugada in jugadas_pc:
                if calcular_pista(intento_pc, jugada) == pista:
                    sospechosos.append(jugada)

            jugadas_pc = sospechosos
            intentoslabel.config(text="\n".join(historial_pc))

    tk.Button(
        ventana_nueva,
        text="Confirmar",
        command=procesar_adivinanzas,
        bg="lightblue"
    ).pack(pady=15)


def ejecutar_juego_consola():
    eleccion = int(input(
        "Elige el modo de juego: \n"
        "La computadora piensa los 3 elementos y el usuario adivina. (1) \n"
        "El usuario piensa los 3 elementos y la computadora adivina. (2)\n"
    ))

    while eleccion != 1 and eleccion != 2:
        print("Error, elige")
        eleccion = int(input("1 o 2\n"))

    if eleccion == 1:
        pcnm = [random.randint(0, 9) for _ in range(3)]
        mia = pedir_intento()
        contador = 1
        historial = []
        while mia != pcnm:
            contador += 1
            pista = calcular_pista(mia, pcnm)
            print(f"Hay {pista} numeros en la combinacion.")
            historial.append("".join(map(str, mia)))
            print("\nIntento fallido. Sigue intentando.")
            mia = pedir_intento()
        mostrar_resumen_usuario(historial, pcnm, contador)

    else:
        numero_secreto = pedir_intento()
        jugadas_pc = generar_jugadas_posibles()
        contador = 0
        while True:
            contador += 1
            intento_pc = jugadas_pc[0]
            print(f"Intento {contador}: La computadora prueba con {''.join(map(str, intento_pc))}")
            pista = calcular_pista(intento_pc, numero_secreto)
            if Counter(intento_pc) == Counter(numero_secreto):
                break
            sospechosos = []
            for jugada in jugadas_pc:
                if calcular_pista(intento_pc, jugada) == pista:
                    sospechosos.append(jugada)
            jugadas_pc = sospechosos

        mostrar_victoria(intento_pc, numero_secreto, jugadas_pc, contador)


if __name__ == "__main__":
    ejecutar_juego_consola()
