import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import customtkinter as ctk
import sqlite3

# Couleurs
orange = "#FF7F32"  # Couleur orange
blue_ciel = "#87CEFA"  # Bleu ciel
bg_color = "#f5f5f5"  # Fond gris clair

class ModifMdps(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")
        

        # Frame supérieure
        self.create_top_frame()
        
        # Menu Frame
        self.menu_frame = tk.Frame(self, bg=blue_ciel, height=40)
        self.menu_frame.pack(fill="x", side="bottom")
        
        image1 = Image.open("modif.jpg")
        new_width = 140
        new_height = 140
        resized_image = image1.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)

        # Affichage de l'image dans un widget Label
        label_image = tk.Label(self, image=self.photo)
        label_image.pack(pady=20)

        # Frame pour le contenu de modification de mot de passe
        self.framerect = ctk.CTkFrame(self, width=425, height=230, corner_radius=40, fg_color="white", border_width=2)
        self.framerect.pack_propagate(False)
        self.framerect.pack(padx=20, pady=15)

        # Ancien mot de passe
        self.old_password_label = ctk.CTkLabel(self.framerect, text="Ancien mot de passe :", font=("Helvetica", 16, "bold"), text_color=orange)
        self.old_password_label.place(x=14, y=20)
        self.old_password_entry = ctk.CTkEntry(self.framerect, placeholder_text="Entrez votre ancien mot de passe", font=("Arial", 14), corner_radius=0, width=400, show="*")
        self.old_password_entry.place(x=6, y=50)
        self.show_old_password_button = tk.Button(self.framerect, text="\U0001F441", command=self.toggle_old_password)
        self.show_old_password_button.place(x=382, y=51)

        # Nouveau mot de passe
        self.new_password_label = ctk.CTkLabel(self.framerect, text="Nouveau mot de passe :", font=("Helvetica", 16, "bold"), text_color=orange)
        self.new_password_label.place(x=14, y=90)
        self.new_password_entry = ctk.CTkEntry(self.framerect, placeholder_text="Entrez le nouveau mot de passe", font=("Arial", 14), corner_radius=0, width=400, show="*")
        self.new_password_entry.place(x=6, y=120)
        self.show_new_password_button = tk.Button(self.framerect, text="\U0001F441", command=self.toggle_new_password)
        self.show_new_password_button.place(x=382, y=121)

        # Bouton de confirmation
        confir = ctk.CTkButton(
            self.framerect,
            text="Confirmer",
            font=("Arial", 25, "bold"),
            corner_radius=15,
            width=100,
            height=40,
            fg_color=orange,
            hover_color="#FF9D5D",
            text_color="white",
            state="normal",
            command=self.changepswd
        )
        confir.place(x=130, y=160)

        # Boutons du menu
        home_icon = ctk.CTkButton(
            self.menu_frame,
            text="🏠",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color=blue_ciel,
            hover_color="#70B9F2",
            state="normal",
        )
        gps_icon = ctk.CTkButton(
            self.menu_frame,
            text="🧭",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color=blue_ciel,
            hover_color="#70B9F2",
            state="normal",
        )
        compte_icon = ctk.CTkButton(
            self.menu_frame,
            text="👤",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color=blue_ciel,
            hover_color="#70B9F2",
            state="normal",
            command=self.goacc
        )

        # Ajout des boutons au grid
        home_icon.grid(row=0, column=0, padx=10, pady=5)
        gps_icon.grid(row=0, column=1, padx=10, pady=5)
        compte_icon.grid(row=0, column=2, padx=10, pady=5)

        # Configuration des poids de colonnes pour le redimensionnement
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_columnconfigure(2, weight=1)

    def create_top_frame(self):
        """Crée la frame supérieure avec le titre de l'application."""
        top_frame = tk.Frame(self, height=50, bg=blue_ciel)
        top_frame.pack(fill="x", side="top")
        app_name = tk.Label(top_frame, text="Modifier le mot de passe", font=("Arial", 35, "bold"), fg=orange, bg=blue_ciel)
        app_name.place(relx=0.5, rely=0.5, anchor="center")
        self.back_button = ctk.CTkButton(self, text="◁ Retour", command=self.revenir_page_precedente,
                                        font=("Helvetica", 14, "bold"), corner_radius=0, fg_color= "#87CEFA",
                                        text_color="white", hover_color= "#87CEFA")
        self.back_button.place(x=0, y=0)  # Positionner le bouton dans le coin supérieur gauche

    def toggle_old_password(self):
        if self.old_password_entry.cget("show") == "":
            self.old_password_entry.configure(show="*")
        else:
            self.old_password_entry.configure(show="")

    def toggle_new_password(self):
        if self.new_password_entry.cget("show") == "":
            self.new_password_entry.configure(show="*")
        else:
            self.new_password_entry.configure(show="")
    def revenir_page_precedente(self):
        from security import Security
        self.controller.show_frame("Security")
    def goacc(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")
    def show_password_changed_message(self):
       """Affiche une boîte de dialogue de confirmation pour le changement de mot de passe."""
       tk.messagebox.showinfo("Succès", "Mot de passe changé avec succès.")
    def changepswd(self):
        from userclass import user_idg
        
        conn=sqlite3.connect('suivi_coli.db')
        c=conn.cursor()
        c.execute("select motPass_user from user where id_user=?",(user_idg,))
        bdmdps=c.fetchall()
        mdps=self.old_password_entry.get()
        if mdps==bdmdps[0][0]:
            print('mdps trouve')
            c.execute('update user set motPass_user=? where id_user=?',(self.new_password_entry.get(),user_idg))
            tk.messagebox.showinfo("Succès", "Mot de passe changé avec succès.")
        else:
            tk.messagebox.showerror("Erreur", "Mot de passe incorrecte.")
            
        conn.commit()
        conn.close()
        
    
        

# Lancer l'application
if __name__ == "__main__":
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    app.geometry("800x600")
    tracking_app = ModifMdps(app, app)
    tracking_app.pack(fill="both", expand=True)
    app.mainloop()
