import tkinter as tk
from tkinter import ttk
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
    try:
        grade_float = float(grade)
        if subject and 2 <= grade_float <= 5:
            subjects[subject]['oceny'].append(grade_float)
            update_display()
            save_data()  # Zapisanie danych po dodaniu oceny
    except ValueError:
        pass  # Możesz dodać komunikat o błędzie, jeśli potrzebujesz

def add_absent():
    subject = subject_var.get()
    if subject:
        max_nieobecnosci = subjects[subject]['max_nieobecnosci']
        if subjects[subject]['nieobecnosci'] < max_nieobecnosci:
            subjects[subject]['nieobecnosci'] += 1
        update_display()
        save_data()  # Zapisanie danych po dodaniu nieobecności

def update_display():
    for i in tree.get_children():
        tree.delete(i)
    for subject, data in subjects.items():
        oceny = ', '.join(map(str, data['oceny'])) if data['oceny'] else "Brak"
        nieobecnosci_info = f"{data['nieobecnosci']}/{data['max_nieobecnosci']}"
        tree.insert('', tk.END, values=(subject, oceny, nieobecnosci_info))

# Konfiguracja GUI
root = tk.Tk()
root.title("Dziennik")
root.configure(bg='#e0f7fa')

subject_var = tk.StringVar(value="Systemy operacyjne")

# Etykiety i pola wyboru
tk.Label(root, text="Wybierz przedmiot:", bg='#e0f7fa', fg='#00695c', font=('Arial', 12)).pack(pady=5)

# Nowoczesna lista rozwijana
subject_menu = ttk.Combobox(root, textvariable=subject_var, values=list(subjects.keys()), font=('Arial', 12), state="readonly")
subject_menu.pack(pady=5)
subject_menu.config(width=35)  # Ustawienie szerokości

# Sekcja oceny
tk.Label(root, text="Wprowadź ocenę (2-5):", bg='#e0f7fa', fg='#00695c', font=('Arial', 12)).pack(pady=5)
grade_entry = tk.Entry(root)
grade_entry.pack(pady=5)

# Przycisk dodawania oceny
add_grade_button = tk.Button(root, text="Dodaj ocenę", command=add_grade, bg='#00796b', fg='white', font=('Arial', 12, 'bold'))
add_grade_button.pack(pady=5)

# Przycisk dodawania nieobecności
add_absent_button = tk.Button(root, text="Dodaj nieobecność", command=add_absent, bg='#00796b', fg='white', font=('Arial', 12, 'bold'))
add_absent_button.pack(pady=5)

# Wyświetlanie danych w tabeli
tk.Label(root, text="Twoje oceny i nieobecności:", bg='#e0f7fa', fg='#00695c', font=('Arial', 12)).pack(pady=5)
style = ttk.Style()
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map("Treeview", background=[('selected', '#00695c')])

tree = ttk.Treeview(root, columns=("Przedmiot", "Oceny", "Nieobecności"), show='headings', height=10)
tree.pack(pady=10)

tree.heading("Przedmiot", text="Przedmiot")
tree.heading("Oceny", text="Oceny")
tree.heading("Nieobecności", text="Nieobecności")

tree.column("Przedmiot", anchor=tk.W, width=300)
tree.column("Oceny", anchor=tk.W, width=200)
tree.column("Nieobecności", anchor=tk.W, width=150)

# Dodanie linii siatki
tree.tag_configure('oddrow', background='#f4f4f4')
tree.tag_configure('evenrow', background='white')

def update_display():
    for i in tree.get_children():
        tree.delete(i)
    count = 0
    for subject, data in subjects.items():
        oceny = ', '.join(map(str, data['oceny'])) if data['oceny'] else "Brak"
        nieobecnosci_info = f"{data['nieobecnosci']}/{data['max_nieobecnosci']}"
        if count % 2 == 0:
            tree.insert('', tk.END, values=(subject, oceny, nieobecnosci_info), tags=('evenrow',))
        else:
            tree.insert('', tk.END, values=(subject, oceny, nieobecnosci_info), tags=('oddrow',))
        count += 1

update_display()

# Uruchomienie GUI
root.mainloop()
