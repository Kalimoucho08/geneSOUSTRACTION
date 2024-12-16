import tkinter as tk
import random
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SoustractionGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur de Soustractions")

        # Entrée pour le nombre maximum
        self.max_label = tk.Label(root, text="Nombre maximum :", font=("Helvetica", 12))
        self.max_label.pack(pady=5)
        self.max_entry = tk.Entry(root)
        self.max_entry.pack(pady=5)

        # Entrée pour la borne inférieure
        self.lower_bound_label = tk.Label(root, text="Borne inférieure :", font=("Helvetica", 12))
        self.lower_bound_label.pack(pady=5)
        self.lower_bound_entry = tk.Entry(root)
        self.lower_bound_entry.pack(pady=5)

        # Entrée pour la borne supérieure
        self.upper_bound_label = tk.Label(root, text="Borne supérieure :", font=("Helvetica", 12))
        self.upper_bound_label.pack(pady=5)
        self.upper_bound_entry = tk.Entry(root)
        self.upper_bound_entry.pack(pady=5)

        # Entrée pour le nombre de soustractions
        self.num_subtractions_label = tk.Label(root, text="Nombre de soustractions :", font=("Helvetica", 12))
        self.num_subtractions_label.pack(pady=5)
        self.num_subtractions_entry = tk.Entry(root)
        self.num_subtractions_entry.pack(pady=5)

        # Case à cocher pour afficher le cercle rouge
        self.show_circle_var = tk.BooleanVar(value=True)
        self.show_circle_checkbox = tk.Checkbutton(root, text="Afficher le cercle rouge", variable=self.show_circle_var)
        self.show_circle_checkbox.pack(pady=5)

        # Case à cocher pour interdire les doublons d'opérations
        self.allow_duplicates_var = tk.BooleanVar(value=True)
        self.allow_duplicates_checkbox = tk.Checkbutton(root, text="Autoriser les doublons d'opérations", variable=self.allow_duplicates_var)
        self.allow_duplicates_checkbox.pack(pady=5)

        # Case à cocher pour interdire le résultat nul
        self.allow_zero_result_var = tk.BooleanVar(value=True)
        self.allow_zero_result_checkbox = tk.Checkbutton(root, text="Autoriser le résultat nul", variable=self.allow_zero_result_var)
        self.allow_zero_result_checkbox.pack(pady=5)

        # Bouton pour générer les soustractions
        self.generate_button = tk.Button(root, text="Générer des soustractions", command=self.generate_soustractions)
        self.generate_button.pack(pady=20)

        # Bouton pour enregistrer en tant que PDF
        self.save_pdf_button = tk.Button(root, text="Enregistrer comme PDF", command=self.save_as_pdf)
        self.save_pdf_button.pack(pady=5)

    def generate_soustractions(self):
        try:
            max_num = int(self.max_entry.get())
            lower_bound = int(self.lower_bound_entry.get())
            upper_bound = int(self.upper_bound_entry.get())
            num_subtractions = int(self.num_subtractions_entry.get())

            if lower_bound < 0 or upper_bound > max_num or lower_bound >= upper_bound:
                raise ValueError("Les bornes doivent être valides.")
            if num_subtractions <= 0:
                raise ValueError("Le nombre de soustractions doit être positif.")

            self.subtractions = []
            used_operations = set()

            while len(self.subtractions) < num_subtractions:
                a = random.randint(lower_bound, upper_bound)
                b = random.randint(lower_bound, a)  # s'assurer que b <= a

                if not self.allow_zero_result_var.get() and a == b:
                    continue

                if not self.allow_duplicates_var.get() and (a, b) in used_operations:
                    continue

                self.subtractions.append((a, b))
                used_operations.add((a, b))

            # Afficher les résultats dans une nouvelle fenêtre
            self.display_results()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def save_as_pdf(self):
        """Enregistre les soustractions et bandes numériques sous forme de PDF."""
        pdf_file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                       filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])

        if not pdf_file_path:
            return

        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        width, height = letter

        margin = 20  # Marges de 20 points
        y_position = height - margin
        max_num = int(self.max_entry.get())

        for a, b in self.subtractions:
            if y_position < margin + 100:  # Si la position y est trop basse, ajouter une nouvelle page
                c.showPage()
                y_position = height - margin

            # Dessiner le fond grisé
            c.setFillColorRGB(0.9, 0.9, 0.9)
            c.rect(margin, y_position - 30, width - 2 * margin, 30, fill=1)

            c.setFillColorRGB(0, 0, 0)
            c.drawString(margin + 10, y_position - 15, f"{a} - {b} =")
            y_position -= 40

            c.drawString(margin, y_position - 10, "Bande numérique :")
            y_position -= 20

            c.line(margin, y_position, width - margin, y_position)  # Ligne de graduation

            for i in range(1, max_num + 1):
                x = margin + (i - 1) * ((width - 2 * margin) / (max_num - 1))
                if i % 5 == 0:
                    c.line(x, y_position - 10, x, y_position + 8)  # Trait de graduation plus grand
                else:
                    c.line(x, y_position - 5, x, y_position + 4)  # Trait de graduation normal

                if i % 5 == 0:
                    c.drawCentredString(x, y_position - 20, str(i))  # Ajustez la position verticale ici

                if self.show_circle_var.get() and i == a:
                    c.setStrokeColorRGB(1, 0, 0)
                    c.circle(x, y_position, 5)
                    c.setStrokeColorRGB(0, 0, 0)

            y_position -= 50

        c.save()

        messagebox.showinfo("Succès", "PDF enregistré avec succès.")

    def display_results(self):
        """Affiche les résultats dans une nouvelle fenêtre."""
        result_window = tk.Toplevel(self.root)
        result_window.title("Résultats des Soustractions")
        result_window.resizable(True, True)  # Rendre la fenêtre redimensionnable

        result_frame = tk.Frame(result_window)
        result_frame.pack(fill=tk.BOTH, expand=True)

        result_canvas = tk.Canvas(result_frame, bg="white")
        result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        result_scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_canvas.yview)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        result_canvas.configure(yscrollcommand=result_scrollbar.set)

        result_inner_frame = tk.Frame(result_canvas)
        result_canvas.create_window((0, 0), window=result_inner_frame, anchor="nw")

        max_num = int(self.max_entry.get())

        for a, b in self.subtractions:
            expression_label = tk.Label(result_inner_frame, text=f"{a} - {b} =", font=("Helvetica", 12), bg="lightgrey")
            expression_label.pack(fill=tk.X)

            number_line_canvas = tk.Canvas(result_inner_frame, width=600, height=100, bg="white")
            number_line_canvas.pack(pady=10)

            number_line_canvas.create_line(30, 50, 570, 50, width=2)

            for i in range(1, max_num + 1):
                x = 30 + (i - 1) * (540 / (max_num - 1))
                if i % 5 == 0:
                    number_line_canvas.create_line(x, 40, x, 60, width=2)  # Trait de graduation plus grand
                else:
                    number_line_canvas.create_line(x, 45, x, 55, width=2)  # Trait de graduation normal

                if i % 5 == 0:
                    number_line_canvas.create_text(x, 65, text=str(i))

            if self.show_circle_var.get():
                x_superior = 30 + (a - 1) * (540 / (max_num - 1))
                number_line_canvas.create_oval(x_superior-10, 35, x_superior+10, 55, outline="red", width=2)

        result_inner_frame.update_idletasks()
        result_canvas.config(scrollregion=result_canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SoustractionGenerator(root)
    root.mainloop()

