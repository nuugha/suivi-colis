import customtkinter as ctk
from tkinter import messagebox,Label,Checkbutton,BooleanVar,Frame
from PIL import Image, ImageTk
import sqlite3
from userclass import SessionConfig



    
class LoginPage(Frame):
    def __init__(self, parent, controller):
     Frame.__init__(self, parent)
     self.controller = controller 
     self.session = SessionConfig()
     
     
     background_image = Image.open('logo2.png')
     background_image = background_image.resize((1366, 708), Image.Resampling.LANCZOS)  # Utilisation de LANCZOS pour un redimensionnement de haute qualité
     background_photo = ImageTk.PhotoImage(background_image)

     

     def update_background(event):
         # Redimensionner l'image de fond à la taille actuelle de la fenêtre
         resized_image = background_image.resize((1366, 708), Image.Resampling.LANCZOS)
         background_photo = ImageTk.PhotoImage(resized_image)
    
         # Mettre à jour l'image dans le label
         background_label.configure(image=background_photo)
         background_label.image = background_photo  # Conserver une référence à l'image

     # Créer un label pour l'image de fond et l'afficher
     background_label = ctk.CTkLabel(self,text="",image=background_photo)
     background_label.place(relwidth=1, relheight=1)  # Occupe toute la fenêtre
     #Attacher la fonction de redimensionnement au changement de taille de la fenêtre
     self.bind("<Configure>", update_background)

     def toggle_password():
         """Alterner l'affichage du mot de passe."""
          # Vérifier si le mot de passe est actuellement masqué
         if password_entry.cget('show') == '*':
             # Afficher le mot de passe
             password_entry.configure(show='')
             show_password_checkbox.configure(text="Cacher le mot de passe")
         else:
             # Masquer le mot de passe
             password_entry.configure(show='*')
             show_password_checkbox.configure(text="Afficher le mot de passe")



     # Fonction de connexion
     def login():
         username = username_entry.get()
         password = password_entry.get()
         conn=sqlite3.connect('suivi_coli.db')
         c=conn.cursor()
         c.execute("select id_user,username,motPass_user from user;")
         liste=c.fetchall()
         found=False
         for tup in liste:
             if username==tup[1] and password==tup[2]:
                 from acc import TrackingApp
                 messagebox.showinfo("Success", f"Welcome, {username}!")
                 
                 
                 import userclass 
                 import acc
                 userclass.user_idg=tup[0]
                 userclass.save_user(tup[0])
                 userclass.set_usrcon(True)
                 acc.set_user_idnot(tup[0])
                 print(acc.get_user_idnot())
                 print(userclass.get_usrcon())
                 print("utilisateur connecté")
                 print(userclass.user_idg)
                 user_id = tup[0]
            # Stocker les informations de session
                 self.session.set('USER_ID', str(user_id))
                 self.session.set('USERNAME', username)
                 self.session.set('IS_LOGGED_IN', 'true')
                 self.controller.show_frame("TrackingApp")
                 
                
                 
                 
                 conn.commit()
                 conn.close()
                 found=True
                 break
                 
         if not found:
                 messagebox.showerror("Connexion échouée", "Nom d'utilisateur ou mot de passe incorrect")
         
         
         
         
             
         

     # Fonction pour "Mot de passe oublié"
     def forgot_password():
         from mdpsoublier import Mdps
         self.controller.show_frame("Mdps")

     # Fonction pour "Créer un compte"
     def create_account():
         from creeuncpt import Choixcmpt
         controller.show_frame("Choixcmpt")
         

     # Chargement du logo





     speedy_label = ctk.CTkLabel(
         self,
         text="Speedy",
         font=("Helvetica", 64, "bold"),
         text_color="#FFA500",
         fg_color="white"
     )
     speedy_label.pack(pady=(50, 30))


     # Entrée du nom d'utilisateur
     username_label = ctk.CTkLabel(
         self, text="Nom d'utilisateur:", font=("Helvetica", 16,"bold"), text_color="#0D6EFD",corner_radius=0,fg_color="white"
     )
     username_label.pack(pady=(5, 5),padx=(530, 0), anchor="w")
     username_entry = ctk.CTkEntry(self, placeholder_text="Entrez votre nom d'utilisateur", width=300,corner_radius=0)
     username_entry.pack(pady=(0, 20))

     # Entrée du mot de passe
     password_label = ctk.CTkLabel(
         self, text="Mot de passe:", font=("Helvetica", 16,"bold"), text_color="#0D6EFD",corner_radius=0,fg_color="white"
     )
     password_label.pack(pady=(10, 5), padx=(530, 0), anchor="w")

     password_entry = ctk.CTkEntry(self, placeholder_text="Entrez votre mot de passe", width=300, show="*",corner_radius=0)
     password_entry.pack(pady=(0, 0))
     # Variable pour gérer l'état de la checkbox (afficher/cacher)
     show_password_var = BooleanVar()

     # Créer un Checkbutton pour afficher ou masquer le mot de passe
     show_password_checkbox = Checkbutton(self, text="Afficher le mot de passe", variable=show_password_var, command=toggle_password, font=("Helvetica", 12),bg="#FFFFFF")
     show_password_checkbox.pack(pady=10)




     # Bouton de connexion
     login_button = ctk.CTkButton(
         self, text="Se connecter", width=200, height=40, command=login, fg_color="#0D6EFD", hover_color="#87CEFA",corner_radius=20,font=("Helvetica", 14,"bold")
     )
     login_button.pack(pady=(20, 10))

     # Option : Mot de passe oublié
     forgot_password_button = ctk.CTkButton(
         self,
         text="Mot de passe oublié ?",
         width=200,
         height=30,
         command=forgot_password,
         fg_color="white",
         text_color="#FFA500",
         hover_color="#FFB84D",
         font=("Helvetica", 14, "underline"),
         corner_radius=6
    
     )
     forgot_password_button.pack(pady=(10, 5))

     # Bouton pour créer un compte
     vnv=Label(self,text="Vous n'avez pas de compte?",bg="#FFFFFF")
     vnv.pack(pady=(5))
     
     create_account_button = ctk.CTkButton(
         self,
         text="crée un compte ",
         width=200,
         height=30,
         command=create_account,#ouvrir la page cree
         fg_color="white",
         text_color="#0D6EFD",
         hover_color="#87CEFA",
         font=("Helvetica", 14, "underline"),
         corner_radius=6
     )
     create_account_button.pack(pady=(10, 30))

if __name__ == "__main__":
    # Crée une instance de l'application principale
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    
    # Crée la page de connexion et l'affiche
    login_page = LoginPage(app, app)
    login_page.pack(fill="both", expand=True)

    # Lance la boucle principale de l'application
    app.mainloop()

   

