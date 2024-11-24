import tkinter as tk
import json
import os

# Ścieżka do pliku
FILENAME = "dziennik.json"


# Funkcja zapisu do pliku
def save_data():
    with open(FILENAME, 'w') as file:
        json.dump(subjects, file)


# Funkcja wczytania danych z pliku
def load_data():
    default_structure = {
        "Systemy operacyjne": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 2},
        "Projektowanie interfejsów": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 2},
        "Paradygmaty programowania": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 1},
        "Technologie obiektowe i komponentowe": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 2},
        "Inżynieria oprogramowania": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 1},
        "Programowanie systemów mobilnych": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 1},
        "Bazy danych": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 2},
        "Angielski": {"oceny": [], "nieobecnosci": 0, "max_nieobecnosci": 4}
    }

    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as file:
            content = file.read().strip()
            if content:
                data = json.loads(content)
                for subject in default_structure:
                    if subject not in data:
                        data[subject] = default_structure[subject]
                    else:
                        if 'oceny' not in data[subject]:
                            data[subject]['oceny'] = []
                        if 'nieobecnosci' not in data[subject]:
                            data[subject]['nieobecnosci'] = 0
                        if 'max_nieobecnosci' not in data[subject]:
                            data[subject]['max_nieobecnosci'] = default_structure[subject]['max_nieobecnosci']
                return data
    return default_structure


# Wczytanie danych
subjects = load_data()


# Funkcje do obsługi dziennika
def add_grade():
    subject = subject_var.get()
    grade = grade_entry.get()
    if subject and grade.isdigit() and 2 <= int(grade) <= 5:
        subjects[subject]['oceny'].append(int(grade))
        update_display()
        save_data()  # Zapisanie danych po dodaniu oceny


def add_absent():
    subject = subject_var.get()
    if subject:
        max_nieobecnosci = subjects[subject]['max_nieobecnosci']
        if subjects[subject]['nieobecnosci'] < max_nieobecnosci:
            subjects[subject]['nieobecnosci'] += 1
        update_display()
        save_data()  # Zapisanie danych po dodaniu nieobecności


def update_display():
    display.delete(1.0, tk.END)
    header = f"{'Przedmiot':<40}{'Oceny':<20}{'Nieobecności':<15}\n"
    display.insert(tk.END, header)
    display.insert(tk.END, "-" * 75 + "\n")
    for subject, data in subjects.items():
        oceny = ', '.join(map(str, data['oceny'])) if data['oceny'] else "Brak"
        nieobecnosci_info = f"{data['nieobecnosci']}/{data['max_nieobecnosci']}"
        row = f"{subject:<40}{oceny:<20}{nieobecnosci_info:<15}\n"
        display.insert(tk.END, row)


# Konfiguracja GUI
root = tk.Tk()
root.title("Dziennik")

subject_var = tk.StringVar(value="Systemy operacyjne")

# Etykiety i pola wyboru
tk.Label(root, text="Wybierz przedmiot:").pack()
subject_menu = tk.OptionMenu(root, subject_var, *subjects.keys())
subject_menu.pack()

# Sekcja oceny
tk.Label(root, text="Wprowadź ocenę (2-5):").pack()
grade_entry = tk.Entry(root)
grade_entry.pack()

# Przycisk dodawania oceny
tk.Button(root, text="Dodaj ocenę", command=add_grade).pack()

# Przycisk dodawania nieobecności
tk.Button(root, text="Dodaj nieobecność", command=add_absent).pack()

# Wyświetlanie danych
tk.Label(root, text="Twoje oceny i nieobecności:").pack()
display = tk.Text(root, height=20, width=75)
display.pack()

update_display()

# Uruchomienie GUI
root.mainloop()
