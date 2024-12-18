import customtkinter as ctk
from tkinter import messagebox,Label,Frame,Canvas,Button,END,StringVar
from PIL import Image, ImageTk
from tkcalendar import Calendar
import random
import string
from tkinter import Toplevel
import re
from datetime import datetime
import sqlite3

class CreatUser(ctk.CTkFrame):
  def __init__(self, parent, controller):
     super().__init__(parent)
     self.controller = controller
     self.configure(fg_color="white")
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
      # Charger l'image de fond
     self.background_image = Image.open('logo2.png')  # Remplacez par le chemin de votre image
     self.background_image = self.background_image.resize((600, 500), Image.Resampling.LANCZOS)  # Utilisation de LANCZOS pour un redimensionnement de haute qualité
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
     self.bouton_retour.image = self.RT_photo


     self.speedy_label = ctk.CTkLabel(
      self,
      text="Crée un utilisateur",
      font=("Helvetica", 44, "bold"),
      text_color="#FFA500",
    )


     self.speedy_label.pack(pady=(50, 30))

# Labels pour les erreurs
     self.error_labels = {}

     # Indicateur pour afficher les erreurs uniquement après la soumission
     self.show_errors = False


# Champ pour le nom
     self.name_label = ctk.CTkLabel(self, text="Nom :",font=("Helvetica", 12,"bold"))
     self.name_label.place(x=490,y=120)
     self.name_entry = ctk.CTkEntry(self, placeholder_text="Entrez votre nom ", width=300,corner_radius=0)
     self.name_entry.place(x=530,y=120)

# Champ pour le prénom
     self.surname_label = ctk.CTkLabel(self, text="Prénom :",font=("Helvetica", 12,"bold"))
     self.surname_label.place(x=470,y=155)
     self.surname_entry =  ctk.CTkEntry(self, placeholder_text="Entrez votre prénom ", width=300,corner_radius=0)
     self.surname_entry.place(x=530,y=155)

# Champ pour CIN
     self.cin_label = ctk.CTkLabel(self, text="CIN :",font=("Helvetica", 12,"bold"))
     self.cin_label.place(x=500,y=190)
     self.cin_entry =  ctk.CTkEntry(self, placeholder_text="Entrez votre CIN ", width=300,corner_radius=0)
     self.cin_entry.place(x=530,y=190)

# Champ pour la date de naissance
     self.dat= ctk.CTkLabel(self, text="Date de naissance :", font=("Helvetica", 12,"bold"))
     self.dat.place(x=415,y=225)

# Champ CTkEntry pour la date
     self.date_entry = ctk.CTkEntry(self,placeholder_text="JJ/MM/AAAA",font=("Arial", 14),corner_radius=0)
     self.date_entry.place(x=530,y=225)

# Ajouter un bouton pour afficher le calendrier
     self.calendar_button = Button(self, text="📅", command=self.open_calendar)
     self.calendar_button.place(x=647,y=226)


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
     self.password_entry = ctk.CTkEntry(self,placeholder_text="Entrez votre mot de passe",font=("Arial", 14),corner_radius=0,width=300,show="*")
     self.password_entry.place(x=530,y=435)

# Bouton pour afficher/masquer le mot de passe
     self.show_password_button = Button(self, text="\U0001F441", command=self.toggle_password)
     self.show_password_button.place(x=808,y=435)

# Bouton pour générer un mot de passe aléatoire
     self.generate_button = ctk.CTkButton(self, text="Générer un mot de passe", command=self.generate_password)
     self.generate_button .place(x=840,y=435)



# Ajouter un bouton de soumission désactivé par défaut
     self.submit_button = ctk.CTkButton(self, text="Créer un compte", command=self.submit_form, state="normal",font=("Arial", 30,"bold"),corner_radius=40,fg_color="#FFA500",
                                        text_color="white",hover_color="#FFB84D")
     self.submit_button.place(x=550, y=520)
# Lier la fonction de validation des champs à l'événement KeyRelease des widgets
     for entry in [self.name_entry, self.surname_entry, self.date_entry, self.email_entry, self.phone_entry, self.username_entry, self.password_entry]:
         entry.bind("<KeyRelease>", lambda event: self.validate_fields())
     self.pays_menu.bind("<Configure>", lambda event: self.validate_fields())
     self.ville_menu.bind("<Configure>", lambda event: self.validate_fields())
     # Dictionnaire des pays et leurs villes
     

     # Fonction pour mettre à jour la liste des villes en fonction du pays sélectionné
  def revenir_page_precedente(self):
         from login2 import LoginPage
         self.controller.show_frame("LoginPage")
  def update_villes(self,*args):
          pays = self.selected_pays.get()
          if pays in self.pays_villes:
          # Met à jour les valeurs du menu déroulant de la ville
             self.ville_menu.set('')  # Réinitialiser la ville sélectionnée
             self.ville_menu.configure(values=self.pays_villes[pays])  # Mettre à jour les villes du pays
          else:
        # Réinitialise les villes si aucun pays n'est sélectionné
             self.ville_menu.configure(values=[])
             self.ville_menu.set('')


      

  def validate_fields(self,event=None):
         
         valid = True

         # Si les erreurs ne doivent pas s'afficher, ne pas continuer
         if not self.show_errors:
             return True

         # Effacer les messages d'erreur existants
         for label in self.error_labels.values():
             label.place_forget()

         # Valider le nom
         if not self.name_entry.get().strip():
             self.error_labels["name"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["name"].place(x=850, y=120)
             valid = False

         # Valider le prénom
         if not self.surname_entry.get().strip():
             self.error_labels["surname"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["surname"].place(x=850, y=155)
             valid = False

         #valider cin
         if not self.cin_entry.get().strip():
             self.error_labels["cin"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["cin"].place(x=850, y=190)
             valid = False

         # Valider la date de naissance
         date = self.date_entry.get().strip()
         if not date:
             self.error_labels["date"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["date"].place(x=850, y=225)
             valid = False
         elif not re.match(r"^\d{2}/\d{2}/\d{4}$", date):
             self.error_labels["date"] = ctk.CTkLabel(self, text="Format invalide (JJ/MM/AAAA)", text_color="red")
             self.error_labels["date"].place(x=850, y=225)
             valid = False

         # Valider l'email
         email = self.email_entry.get().strip()
         if not email:
             self.error_labels["email"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["email"].place(x=850, y=330)
             valid = False
         elif not email.endswith("@gmail.com"):
             self.error_labels["email"] = ctk.CTkLabel(self, text="Doit se terminer par @gmail.com", text_color="red")
             self.error_labels["email"].place(x=850, y=330)
             valid = False
         #valider address
         if not self.addr_entry.get().strip():
             self.error_labels["address"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["address"].place(x=850, y=295)
             valid = False

         # Valider le téléphone
         phone = self.phone_entry.get().strip()
         if not phone:
             self.error_labels["phone"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["phone"].place(x=850, y=365)
             valid = False
         elif not re.match(r"^\+212\d{9}$", phone):
             self.error_labels["phone"] = ctk.CTkLabel(self, text="Format invalide (+212XXXXXXXXX)", text_color="red")
             self.error_labels["phone"].place(x=850, y=365)
             valid = False

         # Valider le nom d'utilisateur
         if not self.username_entry.get().strip():
             self.error_labels["username"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["username"].place(x=850, y=400)
             valid = False

         # Valider le mot de passe
         if not self.password_entry.get().strip():
             self.error_labels["password"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["password"].place(x=850, y=435)
             valid = False
  
         # Valider le pays
         if not self.selected_pays.get():
             self.error_labels["pays"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["pays"].place(x=850, y=260)
             valid = False

         # Valider la ville
         if not self.selected_ville.get():
             self.error_labels["ville"] = ctk.CTkLabel(self, text="Champ obligatoire", text_color="red")
             self.error_labels["ville"].place(x=850, y=260)
             valid = False

         return valid

     # Fonction pour soumettre le formulaire
  def submit_form(self):
         
         self.show_errors = True  # Afficher les erreurs après la soumission
         if self.validate_fields():
            
                 conn=sqlite3.connect('suivi_coli.db')
                 c=conn.cursor()
                 c.execute("INSERT INTO individu values(:cin,:nm,:pr,:date,:adr,:num,:email,:ville,:pays)",
                    {'cin':self.cin_entry.get(),
                     'nm':self.name_entry.get(),
                     'pr':self.surname_entry.get(),
                     'date':self.date_entry.get(),
                     'adr':self.addr_entry.get(),
                     'num':self.phone_entry.get(),
                     'email':self.email_entry.get(),
                     'ville':self.ville_menu.get(),
                     'pays':self.pays_menu.get()})
                 c.execute("INSERT INTO user(username,motPass_user,cin_individu) values(:username,:password,:cin)",{
                                                                         'username':self.username_entry.get(),
                                                                         'password':self.password_entry.get(),
                                                                                'cin':self.cin_entry.get(),
                                                                              })
                 conn.commit()
                 conn.close()
                 messagebox.showinfo("Succès", "Compte créé avec succès!")
         else:
             # Les erreurs sont déjà affichées dans l'interface.
             pass
#FCT CALENDAR

  def open_calendar(self):
         """Ouvre un calendrier pour sélectionner une date"""
         def select_date():
             selected_date = calendar.get_date()  # Récupère la date sélectionnée
             self.date_entry.delete(0, ctk.END)  # Efface l'entrée existante
             self.date_entry.insert(0, selected_date)  # Insère la date sélectionnée
             calendar_window.destroy()  # Ferme la fenêtre du calendrier

         # Créer une fenêtre pop-up pour le calendrier
         calendar_window = Toplevel(self)
         calendar_window.title("Sélectionner une date")
         calendar = Calendar(calendar_window, date_pattern="dd/mm/yyyy")
         calendar.pack(pady=10)

         # Bouton pour confirmer la sélection de la date
         select_button = ctk.CTkButton(calendar_window, text="Sélectionner", command=select_date)
         select_button.pack(pady=10)
# Fonction pour générer un mot de passe aléatoire
  def generate_password(self,longueur=12):
    # Caractères requis
         lettres_majuscules = random.choice(string.ascii_uppercase)
         lettres_minuscules = random.choice(string.ascii_lowercase)
         chiffres = random.choice(string.digits)
         caracteres_speciaux = "@"
    
         # Générer les caractères restants
         reste = ''.join(random.choices(string.ascii_letters + string.digits + "@", k=longueur - 4))
    
         # Combiner tous les caractères et les mélanger
         mot_de_passe = lettres_majuscules + lettres_minuscules + chiffres + caracteres_speciaux + reste
         mot_de_passe = ''.join(random.sample(mot_de_passe, len(mot_de_passe)))
    

         self.password_entry.delete(0, END)  # Efface le champ actuel
         self.password_entry.insert(0, mot_de_passe)  # Insère le mot de passe généré
# Fonction pour afficher/masquer le mot de passe
  def toggle_password(self):
         if self.password_entry.cget("show") == "":
             self.password_entry.configure(show="*")
        
         else:
             self.password_entry.configure(show="")
        

  def validate_and_submit(self):
        """Valider la date et afficher un message"""
        date_text = self.date_entry.get()
        if validate_date_format(date_text):
       
             ctk.CTkMessagebox.show_info("Succès", "Date valide : " + date_text)
        else:
             ctk.CTkMessagebox.show_error("Erreur", "Format de date invalide. Veuillez utiliser jj/mm/yyyy")






  def update_background(self,event=None):
         # Redimensionner l'image de fond à la taille actuelle de la fenêtre
         self.resized_image = self.background_image.resize((1366, 708), Image.Resampling.LANCZOS)
         self.background_photo = ImageTk.PhotoImage(self.resized_image)
    
         # Mettre à jour l'image dans le label
         self.background_label.configure(image=self.background_photo)
         self.background_label.image = self.background_photo  # Conserver une référence à l'image
if __name__ == "__main__":
    # Crée une instance de l'application principale
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    
    # Crée la page de connexion et l'affiche
    login_page = CreatUser(app, app)
    login_page.pack(fill="both", expand=True)

    # Lance la boucle principale de l'application
    app.mainloop()



    

