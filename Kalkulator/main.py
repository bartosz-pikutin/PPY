import math
from pynput import keyboard
import threading
import re

# Historia działań
historia = []
indeks_historia = -1
biezace_wyrazenie = ""
ostatni_wynik = 0

def pokaz_historie():
    print("\nHistoria ostatnich 5 operacji:")
    for i, wpis in enumerate(historia[-5:], start=1):
        print(f"{i}: {wpis}")
    print()

def proc(wyrazenie):
    wyrazenie = re.sub(r'(\d+(\.\d+)?)%', r'(\1 / 100)', wyrazenie)
    return wyrazenie

def pierw(wyrazenie):
    wyrazenie = re.sub(r'sqrt(\d+(\.\d+)?)', r'math.sqrt(\1)', wyrazenie)
    return wyrazenie

def tryg(wyrazenie):
    wyrazenie = re.sub(r'ctg\((.*?)\)', r'1 / math.tan(math.radians(\1))', wyrazenie)
    wyrazenie = re.sub(r'tg\((.*?)\)', r'math.tan(math.radians(\1))', wyrazenie)
    wyrazenie = re.sub(r'sin\((.*?)\)', r'math.sin(math.radians(\1))', wyrazenie)
    wyrazenie = re.sub(r'cos\((.*?)\)', r'math.cos(math.radians(\1))', wyrazenie)
    return wyrazenie

def oblicz(wyrazenie, ostatni_wynik):
    try:
        wyrazenie = proc(wyrazenie)
        wyrazenie = pierw(wyrazenie)
        wyrazenie = tryg(wyrazenie)
        if '!' in wyrazenie:
            wyrazenie = re.sub(r'(\d+)!', lambda m: str(math.factorial(int(m.group(1)))), wyrazenie)
        print(f"Przetworzone wyrażenie: {wyrazenie}")
        wynik = eval(wyrazenie)
        return wynik
    except ZeroDivisionError:
        return "Błąd: Dzielenie przez zeroo"
    except SyntaxError:
        return "Błąd: Nieprawidłowe wyrażenie"
    except Exception as e:
        return f"Błąd: {str(e)}"

def przycisk(przyc):
    global biezace_wyrazenie, indeks_historia
    try:
        if przyc == keyboard.Key.up:
            if historia:
                indeks_historia = (indeks_historia - 1) % len(historia)
                wyrazenie_baza = historia[indeks_historia].split(' = ')[0]
                biezace_wyrazenie = wyrazenie_baza
                print(f"\r{biezace_wyrazenie}", end="", flush=True)
        elif przyc == keyboard.Key.down:
            if historia:
                indeks_historia = (indeks_historia + 1) % len(historia)
                wyrazenie_baza = historia[indeks_historia].split(' = ')[0]
                biezace_wyrazenie = wyrazenie_baza
                print(f"\r{biezace_wyrazenie}", end="", flush=True)
    except Exception as e:
        print(f"Błąd: {str(e)}")

def keyboard_listener():
    sluchacz = keyboard.Listener(on_press=przycisk)
    sluchacz.start()

def main():
    global ostatni_wynik, biezace_wyrazenie
    keyboard_listener()
    while True:
        pokaz_historie()
        wyrazenie_uzytkownika = input("Wprowadź wyrażenie (lub 'exit' aby zakończyć): ")

        if wyrazenie_uzytkownika.lower() == 'exit':
            break

        if biezace_wyrazenie:
            wyrazenie_uzytkownika = biezace_wyrazenie + wyrazenie_uzytkownika

        wynik = oblicz(wyrazenie_uzytkownika, ostatni_wynik)

        if isinstance(wynik, str):
            print(wynik)
        else:
            print(f"Wynik: {wynik}")
            historia.append(wyrazenie_uzytkownika + " = " + str(wynik))
            ostatni_wynik = wynik
            biezace_wyrazenie = ""

if __name__ == "__main__":
    main()
