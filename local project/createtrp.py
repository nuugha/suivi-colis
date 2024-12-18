import customtkinter as ctk
from tkinter import messagebox, Label, Button, END, StringVar, Toplevel
from PIL import Image, ImageTk
from tkcalendar import Calendar
import random
import string
import re
import sqlite3


class CreatEntr(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")
        self.background_image = Image.open('logo2.png')  # Remplacez par le chemin de votre image
        self.background_image = self.background_image.resize((1366, 708), Image.Resampling.LANCZOS)  # Utilisation de LANCZOS pour un redimensionnement de haute qualité
        self.background_photo = ImageTk.PhotoImage(self.background_image)  # Convertir en format compatible Tkinter

# Créer un label pour l'image de fond et l'afficher
        self.background_label = ctk.CTkLabel(self,text="",image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)  # Occupe toute la fenêtre
#Attacher la fonction de redimensionnement au changement de taille de la fenêtre
        self.bind("<Configure>", self.update_background)
        self.image_retour = Image.open("retour.png")
    
# Redimensionner l'image
        self.resized_image = self.image_retour.resize((40, 40), Image.Resampling.LANCZOS)
    
# Convertir en format compatible avec tkinter
        self.RT_photo = ImageTk.PhotoImage(self.resized_image)
    
# Création du bouton avec l'image redimensionnée
        self.bouton_retour = Button(
           self,
           image=self.RT_photo,
           command=self.revenir_page_precedente,
           relief="flat",  # Look moderne
           cursor="hand2"  # Changer le curseur au survol
    )
        self.bouton_retour.place(x=430, y=50)
    
# Assurez-vous que l'image reste en mémoire en la liant à l'objet bouton
        self.bouton_retour.image=self.RT_photo

        # Dictionnaire des pays et leurs villes
        self.pays_villes = {
            
            "Maroc": ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger', 'Agadir', 'Meknès', 'Oujda', 
 'Kenitra', 'Tetouan', 'Safi', 'El Jadida', 'Nador', 'Beni Mellal', 'Mohammedia', 
 'Taza', 'Khouribga', 'Settat', 'Errachidia', 'Larache', 'Khemisset', 'Ouarzazate', 
 'Tiznit', 'Tan-Tan', 'Guelmim', 'Ifrane', 'Asilah', 'Chefchaouen', 'Al Hoceima', 
 'Taroudant', 'Oued Zem', 'Azrou', 'Sidi Kacem', 'Sidi Slimane', 'Boujdour', 
 'Laâyoune', 'Dakhla']
        }

        # Variables pour les menus déroulants
        self.selected_pays = StringVar(self)
        self.selected_ville = StringVar(self)

        # Initialisation des attributs pour la validation
        self.show_errors = False  # Example initialization
        self.error_labels = {}    # Dictionary to hold error labels

        # Création du label principal
        self.speedy_label = ctk.CTkLabel(
            self,
            text="Créer un compte pour \nEntreprise",
            font=("Helvetica", 30, "bold"),
            text_color="#FFA500"
        )
        self.speedy_label.pack(pady=(50, 30))

        # Champ pour le nom
        self.name_label = ctk.CTkLabel(self, text="Nom :",font=("Helvetica", 12,"bold"))
        self.name_label.place(x=490,y=140)
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Entrez le nom de votre Entreprise ", width=300,corner_radius=0)
        self.name_entry.place(x=530,y=140)

# Champ pour le ice
        self.ice_label = ctk.CTkLabel(self, text="ICE :",font=("Helvetica", 12,"bold"))
        self.ice_label.place(x=500,y=175)
        self.ice_entry =  ctk.CTkEntry(self, placeholder_text="Entrez ICE de votre entreprise ", width=300,corner_radius=0)
        self.ice_entry.place(x=530,y=175)

        self.domaine_label = ctk.CTkLabel(self, text="Domaine :",font=("Helvetica", 12,"bold"))
        self.domaine_label.place(x=460,y=210)
        self.domaine_entry = ctk.CTkEntry(self,placeholder_text="Entrez le domaine de votre entreprise",font=("Arial", 14),corner_radius=0,width=300)
        self.domaine_entry.place(x=530,y=210)




        self.pays_label = ctk.CTkLabel(self, text="Pays :", font=("Helvetica", 12,"bold"))
        self.pays_label.place(x=490,y=260)
        self.pays_menu =ctk.CTkOptionMenu(self, variable=self.selected_pays, values=list(self.pays_villes.keys()), command=self.update_villes)
        self.pays_menu.place(x=530,y=260)

# Label et menu déroulant pour la ville
        self.ville_label = ctk.CTkLabel(self, text="Ville :", font=("Helvetica", 12,"bold"))
        self.ville_label.place(x=730,y=260)
        self.ville_menu = ctk.CTkOptionMenu(self, variable=self.selected_ville)
        self.ville_menu.place(x=800,y=260)

# Lier la fonction de mise à jour des villes à la sélection du pays
        self.selected_pays.trace("w", self.update_villes)


        self.addr_label = ctk.CTkLabel(self, text="Adresse :",font=("Helvetica", 12,"bold"))
        self.addr_label.place(x=460,y=295)
        self.addr_entry = ctk.CTkEntry(self,placeholder_text="Entrez votre adress",font=("Arial", 14),corner_radius=0,width=300)
        self.addr_entry.place(x=530,y=295)



# Champ pour l'email
        self.email_label = ctk.CTkLabel(self, text="Email :",font=("Helvetica", 12,"bold"))
        self.email_label.place(x=480,y=330)
        self.email_entry = ctk.CTkEntry(self,placeholder_text="Entrez votre Email",font=("Arial", 14),corner_radius=0,width=300)
        self.email_entry.place(x=530,y=330)

# Champ pour le numéro de téléphone
        self.phone_label = ctk.CTkLabel(self, text="N° de téléphone :",font=("Helvetica", 12,"bold"))
        self.phone_label.place(x=430,y=365)
        self.phone_entry =ctk.CTkEntry(self,placeholder_text="Entrez votre N° de téléphone",font=("Arial", 14),corner_radius=0,width=300)
        self.phone_entry.place(x=530,y=365)

# Champ pour le nom d'utilisateur
        self.username_label = ctk.CTkLabel(self, text="Nom d'utilisateur :",font=("Helvetica", 12,"bold"))
        self.username_label.place(x=420,y=400)
        self.username_entry = ctk.CTkEntry(self,placeholder_text="Entrez votre nom d'utilisateur",font=("Arial", 14),corner_radius=0,width=300)

        self.username_entry.place(x=530,y=400)

# Champ pour le mot de passe
        self.password_label =ctk.CTkLabel(self, text="Mot de passe   :",font=("Helvetica", 12,"bold"))
        self.password_label.place(x=430,y=435)
        self.password_entry = ctk.CTkEntry(self,placeholder_text="Entrez votre nom d'utilisateur",font=("Arial", 14),corner_radius=0,width=300,show="*")
        self.password_entry.place(x=530,y=435)

# Bouton pour afficher/masquer le mot de passe
        self.show_password_button = Button(self, text="\U0001F441", command=self.toggle_password)
        self.show_password_button.place(x=808,y=435)

# Bouton pour générer un mot de passe aléatoire
        self.generate_button = ctk.CTkButton(self, text="Générer un mot de passe", command=self.generate_password)
        self.generate_button .place(x=840,y=435)



        self.submit_button = ctk.CTkButton(self, text="Créer un compte", state="normal",font=("Arial", 30,"bold"),corner_radius=40,fg_color="#FFA500",text_color="white",hover_color="#FFB84D",command=lambda: self.submit_form())
        self.submit_button.place(x=550, y=520)

        # Lier les événements pour la validation des champs après la création des menus
        self.bind("<Configure>", self.validate_fields)
        self.pays_menu.bind("<Configure>", lambda event, menu=self.pays_menu: self.validate_fields())
        self.ville_menu.bind("<Configure>", lambda event, menu=self.ville_menu: self.validate_fields())

    

    def update_villes(self, *args):
        pays = self.selected_pays.get()
        if pays in self.pays_villes:
            self.ville_menu.configure(values=self.pays_villes[pays])
            self.ville_menu.set('')  # Réinitialiser la ville sélectionnée
        else:
            self.ville_menu.configure(values=[])
            self.ville_menu.set('')

    def validate_fields(self, event=None):
        valid = True
        if not self.show_errors:
            return True

        # Effacer les messages d'erreur existants
        for label in self.error_labels.values():
            label.place_forget()

        # Validation des champs
        validations = {
            "name": (self.name_entry, "Champ obligatoire", 140),
            "domaine": (self.domaine_entry, "Champ obligatoire", 175),
            "ice": (self.ice_entry, "Champ obligatoire", 210),
            "email": (self.email_entry, "Champ obligatoire", 330),
            "address": (self.addr_entry, "Champ obligatoire", 295),
            "phone": (self.phone_entry, "Champ obligatoire", 365),
            "username": (self.username_entry, "Champ obligatoire", 400),
            "password": (self.password_entry, "Champ obligatoire", 435)
        }

        # Valider chaque champ
        for key, (entry, msg, y_pos) in validations.items():
            if not entry.get().strip():
                self.error_labels[key] = ctk.CTkLabel(self, text=msg, text_color="red")
                self.error_labels[key].place(x=850, y=y_pos)
                valid = False

        # Valider l'email
        email = self.email_entry.get().strip()
        if email and not email.endswith("@gmail.com"):
            self.error_labels["email"] = ctk.CTkLabel(self, text="Doit se terminer par @gmail.com", text_color="red")
            self.error_labels["email"].place(x=850, y=330)
            valid = False

        # Valider le téléphone
        phone = self.phone_entry.get().strip()
        if phone and not re.match(r"^\+212\d{9}$", phone):
            self.error_labels["phone"] = ctk.CTkLabel(self, text="Format invalide (+212XXXXXXXXX)", text_color="red")
            self.error_labels["phone"].place(x=850, y=365)
            valid = False

        return valid

    def submit_form(self):
        self.show_errors = True  # Afficher les erreurs après la soumission
        if self.validate_fields():
            conn=sqlite3.connect("suivi_coli.db")
            c=conn.cursor()
            c.execute("INSERT INTO societé values(:ice,:nom,:adr,:domaine,:num,:email,:ville,:pays)",
                      {'ice':self.ice_entry.get(),
                       'nom':self.name_entry.get(),
                       'adr':self.addr_entry.get(),
                       'domaine':self.domaine_entry.get(),
                       'num':self.phone_entry.get(),
                       'email':self.email_entry.get(),
                       'ville':self.ville_menu.get(),
                       'pays':self.pays_menu.get()
                          })
            c.execute("INSERT INTO user(username,motPass_user,ice_societ) values(:usrnm,:psswrd,:ice)",{
                'usrnm':self.username_entry.get(),
                'psswrd':self.password_entry.get(),
                'ice':self.ice_entry.get()})
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Compte créé avec succès !")
            # Code pour soumettre les données
            self.controller.show_frame("ConnexionPage")

    def toggle_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def generate_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)

    def revenir_page_precedente(self):
        from login2 import LoginPage
        self.controller.show_frame("LoginPage")

    def update_background(self, event=None):
        new_width = 1366
        new_height = 708
        self.resized_image = self.background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.resized_image)
    
    # Mettre à jour l'image dans le label
        self.background_label.configure(image=self.background_photo)
        self.background_label.image = self.background_photo

# Code principal pour lancer l'selflication à partir de l'importation
if __name__ == "__main__":
    root = ctk.CTk()
    app = CreatEntr(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()























  
