# -*- coding: utf-8 -*-
"""Módulo con funciones para el juego de adivinanza de números."""

import random
from collections import Counter

import tkinter as tk
from tkinter import messagebox

# ==========================================================
# SECCIÓN 1: CÁLCULO DE COINCIDENCIAS
# ==========================================================
def calcular_pista(combinacion_a, combinacion_b):
    """Calcula cuántos números de combinacion_a están en combinacion_b.
    
    Args:
        combinacion_a: Lista de dígitos a verificar
        combinacion_b: Lista de dígitos donde buscar
    
    Returns:
        int: Cantidad de números coincidentes
    """
    """Calcula cuántos números de combinacion_a están en combinacion_b.
    
    Args:
        combinacion_a: Lista de dígitos a verificar
        combinacion_b: Lista de dígitos donde buscar
    
    Returns:
        int: Cantidad de números coincidentes
    """
    copia = combinacion_b.copy()  # Crear copia para no modificar el original
    pista = 0
    for numero in combinacion_a:
        if numero in copia:
            pista += 1
            copia.remove(numero)  # Eliminar para no contar duplicados
    return pista
# ==========================================================
# SECCIÓN 2: UTILIDADES DE DATOS Y ENTRADA DE CONSOLA
# ==========================================================


def generar_jugadas_posibles():
    """Genera todas las combinaciones posibles de 3 dígitos (000-999).
    
    Returns:
        list: Lista de todas las combinaciones posibles
    """
    return [[int(digito) for digito in f"{numero:03d}"] for numero in range(1000)]


def pedir_intento():
    """Solicita al usuario que ingrese un número de 3 dígitos válido.
    
    Returns:
        list: Lista de 3 dígitos ingresados por el usuario
    """
    while True:
        intento = input("\nIngresa un numero de 3 digitos (000-999): ")
        # Validar que sea exactamente 3 dígitos
        if len(intento) == 3 and intento.isdigit():
            return [int(digito) for digito in intento]
        print("\nError, volver a intentar")
# ==========================================================
# SECCIÓN 3: REPORTES DE RESULTADOS - CONSOLA
# ==========================================================

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
    """Muestra un resumen del juego cuando el usuario gana.
    
    Args:
        historial: Lista de intentos fallidos del usuario
        pcnm: Número secreto que el usuario adivinó
        contador: Total de intentos realizados
    """
    historia = " otro: ".join(map(str, historial))
    extra = "".join(map(str, pcnm))
    print(f"\nTodos los intentos fueron: {historia}")
    print(f"\nGanaste, la respuesta correcta era: {extra}")
    print(f"\nIntentaste un total de: {contador}")

# ==========================================================
# SECCIÓN 4: INTERFAZ GRÁFICA (GUI) - EL USUARIO ADIVINA
# ==========================================================

def mostrar_mensajeAdivinador(ventana, pontunombre, guardar_resultado):
    """Abre una ventana para que el usuario adivine el número secreto.
    
    Args:
        ventana: Ventana principal de tkinter
        pontunombre: Función para obtener el nombre del jugador
        guardar_resultado: Función para guardar el resultado en CSV
    """
    # Generar un número secreto aleatorio de 3 dígitos
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

    historial_intentos = []  # Registrar todos los intentos del usuario
    num_intentos = 0  # Contador de intentos

    def pedir_numero_gui():
        """Valida y convierte el número ingresado en la GUI."""
        numero = entrada_numero.get()
        if len(numero) == 3 and numero.isdigit():
            return [int(digito) for digito in numero]

        messagebox.showerror("Error", "Por favor, ingresa un numero de 3 digitos.")
        return None

    def procesar_adivinanzas():
        """Procesa cada adivinanza del usuario y actualiza la interfaz."""
        nonlocal num_intentos

        intento_usuario = pedir_numero_gui()
        if intento_usuario is None:
            return

        num_intentos += 1
        historial_intentos.append("".join(map(str, intento_usuario)))

        lista_pistas = []
        # Código secreto para ganar automáticamente (042) lo utilizamos para facilitar pruebas y demostraciones osea debuggear el juego sin tener que adivinar el numero real
        if intento_usuario == [0, 4, 2]:
            lista_pistas.append("Has ingresado el numero secreto para ganar automaticamente.")

        # Calcular pista basada en números coincidentes
        pista = calcular_pista(intento_usuario, combinacion_secreta)
        lista_pistas.append(f"Hay {pista} numeros en la combinacion.")
        resultado_label.config(
            text="\n".join(lista_pistas + ["", f"Intentos: {', '.join(historial_intentos)}"])
        )

        # Verificar si el usuario adivinó correctamente
        if intento_usuario == combinacion_secreta or intento_usuario == [0, 4, 2]:
            combinacion_ganadora = "".join(map(str, combinacion_secreta))
            messagebox.showinfo(
                "Ganaste",
                f"Adivinaste el numero {combinacion_ganadora} en {num_intentos} intentos."
            )
            # Obtener nombre del jugador y guardar resultado
            nombre = pontunombre()
            guardar_resultado(nombre, num_intentos)
            ventana_nueva.destroy()

    tk.Button(
        ventana_nueva,
        text="Confirmar",
        command=procesar_adivinanzas,
        bg="lightblue"
    ).pack(pady=15)


# ==========================================================
# SECCIÓN 5: INTERFAZ GRÁFICA (GUI) - LA PC ADIVINA
# ==========================================================

def mostrar_mensajeComputadora(ventana, ganastecomputadora):
    """Abre una ventana para que la computadora adivine el número del usuario.
    
    Args:
        ventana: Ventana principal de tkinter
        ganastecomputadora: Función callback cuando la computadora gana
    """
    
    # Ventana para que el usuario elija el número que la computadora debe adivinar
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
        """Inicia el algoritmo de adivinanza en un hilo separado."""
        numero = entrada_numero.get()
        # Validar entrada
        if len(numero) != 3 or not numero.isdigit():
            messagebox.showerror("Error", "Por favor, ingresa un numero de 3 digitos.")
            return

        import threading

        def correr_algoritmo():
        # Inicia la resolución del juego mediante un algoritmo de descarte
            """Ejecuta el algoritmo de adivinanza de la computadora de forma recursiva."""
            from itertools import permutations
            numero_secreto = [int(digito) for digito in numero]
            jugadas_pc = generar_jugadas_posibles()
            contador = 0
            historial_pc = []

            while True:
                # Si todos los candidatos son permutaciones del mismo grupo, probarlas en orden
                primer_candidato = sorted(jugadas_pc[0])
                todos_permutaciones = all(sorted(j) == primer_candidato for j in jugadas_pc)

                # Cuando solo quedan permutaciones, probarlas todas
                if todos_permutaciones:
                    perms = list(dict.fromkeys(tuple(p) for p in permutations(jugadas_pc[0])))
                    for perm in perms:
                        intento_pc = list(perm)
                        contador += 1
                        historial_pc.append(f"Intento {contador}: {''.join(map(str, intento_pc))}")
                        intentoslabel.config(text="\n".join(historial_pc))
                        if intento_pc == numero_secreto:
                            ventana_nueva.after(0, lambda c=contador, n=numero: ganastecomputadora(c, n))
                            return
                    break

                # Probar el primer candidato
                intento_pc = jugadas_pc[0]
                contador += 1
                historial_pc.append(f"Intento {contador}: {''.join(map(str, intento_pc))}")

                # Verificar si adivinó
                if intento_pc == numero_secreto:
                    intentoslabel.config(text="\n".join(historial_pc))
                    ventana_nueva.after(0, lambda c=contador, n=numero: ganastecomputadora(c, n))
                    break

                # Filtrar candidatos según la pista obtenida
                pista = calcular_pista(intento_pc, numero_secreto)
                jugadas_pc = [jugada for jugada in jugadas_pc if calcular_pista(intento_pc, jugada) == pista]
                intentoslabel.config(text="\n".join(historial_pc))

        threading.Thread(target=correr_algoritmo, daemon=True).start()

    tk.Button(
        ventana_nueva,
        text="Confirmar",
        command=procesar_adivinanzas,
        bg="lightblue"
    ).pack(pady=15)

# ==========================================================
# SECCIÓN 6: LÓGICA GENERAL PARA EJECUCIÓN EN CONSOLA
# ==========================================================

def ejecutar_juego_consola():
    """Ejecuta el juego en modo consola con dos opciones de juego."""
    eleccion = int(input(
        "Elige el modo de juego: \n"
        "La computadora piensa los 3 elementos y el usuario adivina. (1) \n"
        "El usuario piensa los 3 elementos y la computadora adivina. (2)\n"
    ))

    while eleccion != 1 and eleccion != 2:
        print("Error, elige")
        eleccion = int(input("1 o 2\n"))

    # Modo 1: Usuario adivina el número de la computadora
    if eleccion == 1:
        pcnm = [random.randint(0, 9) for _ in range(3)]  # Número secreto
        mia = pedir_intento()
        contador = 1
        historial = []
        # Bucle hasta que el usuario adivine
        while mia != pcnm:
            contador += 1
            pista = calcular_pista(mia, pcnm)
            print(f"Hay {pista} numeros en la combinacion.")
            historial.append("".join(map(str, mia)))
            print("\nIntento fallido. Sigue intentando.")
            mia = pedir_intento()
        mostrar_resumen_usuario(historial, pcnm, contador)

    # Modo 2: Computadora adivina el número del usuario
    else:
        numero_secreto = pedir_intento()  # Usuario ingresa su número
        jugadas_pc = generar_jugadas_posibles()
        contador = 0
        # Bucle hasta que la computadora adivine
        while True:
            contador += 1
            intento_pc = jugadas_pc[0]
            print(f"Intento {contador}: La computadora prueba con {''.join(map(str, intento_pc))}")
            pista = calcular_pista(intento_pc, numero_secreto)
            # Verificar si adivinó (sin importar orden de dígitos)
            if Counter(intento_pc) == Counter(numero_secreto):
                break
            # Filtrar candidatos que coincidan con la pista
            sospechosos = []
            for jugada in jugadas_pc:
                if calcular_pista(intento_pc, jugada) == pista:
                    sospechosos.append(jugada)
            jugadas_pc = sospechosos

        mostrar_victoria(intento_pc, numero_secreto, jugadas_pc, contador)

