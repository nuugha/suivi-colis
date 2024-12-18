import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import json
from tkinter import messagebox
import sqlite3

orange = "#FF7F32"  # Couleur orange
blue_ciel = "#87CEFA"  # Bleu ciel
bg_color = "#f5f5f5"  # Fond gris clair

class Suppcmpt(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")
        
        # Récupérer l'ID utilisateur
        

        # Frame du menu
        self.menu_frame = tk.Frame(self, bg=blue_ciel, height=40)
        self.menu_frame.pack(fill="x", side="bottom")

        # Frame supérieure
        self.create_top_frame()

        # Image de sécurité
        image1 = Image.open("warning.png")
        new_width = 140
        new_height = 140
        resized_image = image1.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)
        label_image = tk.Label(self, image=self.photo)
        label_image.pack(pady=20)

        # Frame principale
        self.main_frame = ctk.CTkFrame(self, width=450, height=200, corner_radius=40, fg_color="white", border_width=2)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=20, pady=15)

        # Message d'avertissement
        warning_label = ctk.CTkLabel(
            self.main_frame,
            text="⚠️ Attention: Cette action est irréversible",
            font=("Arial", 16, "bold"),
            text_color="red"
        )
        warning_label.pack(pady=10)

        # Champ de mot de passe
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Entrez votre mot de passe pour confirmer",
            width=300,
            show="*"
        )
        self.password_entry.pack(pady=20)
        
        # Bouton afficher/masquer mot de passe
        self.show_password_button = tk.Button(
            self.main_frame, 
            text="\U0001F441", 
            command=self.toggle_password
        )
        self.show_password_button.place(x=350, y=70)

        # Bouton de suppression
        delete_button = ctk.CTkButton(
            self.main_frame,
            text="Supprimer mon compte",
            font=("Arial", 15, "bold"),
            fg_color="red",
            hover_color="#8B0000",
            command=self.submit_form
        )
        delete_button.pack(pady=20)

        # Boutons du menu
        self.create_menu_buttons()

    def create_top_frame(self):
        top_frame = tk.Frame(self, height=50, bg="#87CEFA")
        top_frame.pack(fill="x", side="top")
        
        app_name = tk.Label(
            top_frame, 
            text="Suppression du compte", 
            font=("Arial", 35, "bold"), 
            fg="#FF7F32", 
            bg="#87CEFA"
        )
        app_name.place(relx=0.5, rely=0.5, anchor="center")
        
        self.back_button = ctk.CTkButton(
            self, 
            text="◁ Retour",
            command=self.revenir_page_precedente,
            font=("Helvetica", 14, "bold"),
            corner_radius=0,
            fg_color="#87CEFA",
            text_color="white",
            hover_color="#87CEFA"
        )
        self.back_button.place(x=0, y=0)

    def create_menu_buttons(self):
        # Boutons du menu
        buttons_data = [
            ("🏠", self.goacc),
            ("🧭", self.gomap),
            ("👤", self.alleraccount)
        ]

        for col, (text, command) in enumerate(buttons_data):
            button = ctk.CTkButton(
                self.menu_frame,
                text=text,
                font=("Arial", 35, "bold"),
                corner_radius=15,
                width=200,
                height=60,
                fg_color="#87CEFA",
                hover_color="#70B9F2",
                command=command
            )
            button.grid(row=0, column=col, padx=10, pady=5)
            self.menu_frame.grid_columnconfigure(col, weight=1)

    def submit_form(self):
        
            
        try:
            from userclass import user_idg
            conn = sqlite3.connect("suivi_coli.db")
            cursor = conn.cursor()
            
            print(f"Tentative de suppression pour l'utilisateur ID: ?",(user_idg,))
            
            cursor.execute("SELECT motPass_user FROM user WHERE id_user=?", (user_idg,))
            stored_password = cursor.fetchone()
            
            print(f"Mot de passe stocké: {stored_password}")
            print(f"Mot de passe saisi: {self.password_entry.get()}")
            
            if stored_password:
                if self.password_entry.get() == stored_password[0]:
                    response = messagebox.askyesno(
                        "Confirmation", 
                        "Voulez-vous supprimer ce compte définitivement ?"
                    )
                    
                    if response:
                        try:
                            from login2 import LoginPage
                            cursor.execute("DELETE FROM user WHERE id_user=?", (user_idg,))
                            conn.commit()
                            print(f"Utilisateur {user_idg} supprimé avec succès")
                            messagebox.showinfo("Succès", "Votre compte a été supprimé avec succès")
                            self.controller.show_frame("LoginPage")
                        except sqlite3.Error as e:
                            print(f"Erreur lors de la suppression: {e}")
                            conn.rollback()
                            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")
                else:
                    print("Mot de passe incorrect")
                    messagebox.showerror("Erreur", "Mot de passe incorrect")
            else:
                print(f"Aucun utilisateur trouvé avec l'ID: {self.user_id}")
                messagebox.showerror("Erreur", "Utilisateur non trouvé")
                
        except sqlite3.Error as e:
            print(f"Erreur SQL: {e}")
            messagebox.showerror("Erreur", f"Erreur de base de données : {str(e)}")
            
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

    def toggle_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def revenir_page_precedente(self):
        from security import Security
        self.controller.show_frame("Security")

    def alleraccount(self):
        from account import Account
        self.controller.show_frame("Account")

    def gomap(self):
        from GPSsuiviecolis import SuiviColis
        self.controller.show_frame("SuiviColis")

    def goacc(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    suppcmpt = Suppcmpt(app, app)
    suppcmpt.pack(fill="both", expand=True)
    app.mainloop()
