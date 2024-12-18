import customtkinter as ctk
from tkinter import messagebox,Label,Frame,Canvas,Button,END,StringVar
from PIL import Image, ImageTk
from tkinter import Toplevel
import re
import sqlite3

class Mdps(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
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
          text="Récupérer votre mot de passe",
          font=("Helvetica", 36, "bold"),
          text_color="#FFA500",
          bg_color="white",
              )
        self.speedy_label.pack(pady=(100, 30))
        self.id_entry = ctk.CTkEntry(self,placeholder_text="Entrez votre CIN / ICE",font=("Arial", 14),corner_radius=50,bg_color="white",width=300)
        self.id_entry.place(x=530,y=250)

        self.email_entry = ctk.CTkEntry(self,placeholder_text="Entrez votre Email",font=("Arial", 14),corner_radius=50,bg_color="white",width=300)
        self.email_entry.place(x=530,y=300)
        self.mdps="monmdps"
        self.submit_button = ctk.CTkButton(self, text="Valider",command=lambda: self.envoi(),bg_color="white",font=("Arial", 30,"bold"),corner_radius=40,fg_color="#FFA500",
                                      text_color="white",hover_color="#FFB84D")
        self.submit_button.pack(pady=(170, 30))






    def revenir_page_precedente(self):
          from login2 import LoginPage
          self.controller.show_frame("LoginPage")
    def update_background(self,event):
    # Redimensionner l'image de fond à la taille actuelle de la fenêtre
      new_width = event.width
      new_height = event.height
      self.resized_image = self.background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
      self.background_photo = ImageTk.PhotoImage(self.resized_image)
    
    # Mettre à jour l'image dans le label
      self.background_label.configure(image=self.background_photo)
      self.background_label.image = self.background_photo  # Conserver une référence à l'image
    
    def envoi(self):
        import smtplib
        
        conn=sqlite3.connect('suivi_coli.db')
        c=conn.cursor()
        c.execute("select email_individu from individu where cin_individu=? and email_individu=?;", (self.id_entry.get(),self.email_entry.get()))
        listindv=c.fetchall()
        print(listindv)
        indv=False
        intr=False
        tup=None
        
        
        
        c.execute("select email_societ from societé where ice_societ=? and email_societ=? ;", (self.id_entry.get(),self.email_entry.get()))
        listsoc=c.fetchall()
        print(listsoc)
        if not listindv:  # No individual email found
            intr = True
        elif listsoc == [] and listindv[0][0] is not None:
            indv = True
        elif listsoc == [] and not listindv:
            intr = True
        if indv and not intr:
            c.execute("SELECT username, motPass_user FROM user,individu WHERE user.cin_individu=? and individu.email_individu=?;", (self.id_entry.get(),self.email_entry.get()))
        elif not indv and not intr:
            c.execute("SELECT username, motPass_user FROM user,societé WHERE user.ice_societ=? and societé.email_societ=? ;", (self.id_entry.get(),self.email_entry.get()))
        else:
            tup = None

        tup = c.fetchall()
        print("User data:", tup)
            
        
        conn.commit()
        conn.close()
        
        p=re.compile(r"^[a-zA-Z0-9._%+-]+@gmail\.com$")
        matche=p.match(self.email_entry.get().strip())
        print(matche)
        if matche!=None and intr==False:
             try:
                server=smtplib.SMTP_SSL("smtp.gmail.com",465)
                server.login("speedyexpress026@gmail.com","tuiy ccuh harn nnok")
                subject = "Recuperation de mot de passe"
                body = f" Dear {tup[0][0]};\nVotre mot de passe est : {tup[0][1]}"
                msg = f"Subject: {subject}\n\n{body}"
                server.sendmail("speedyexpress026@gmail.com",self.email_entry.get(),msg)
                server.quit()
                messagebox.showinfo("Succès", "L'e-mail a été envoyé avec succès.")
             except Exception as e:
                 messagebox.showerror("Erreur", f"Échec de l'envoi de l'e-mail : {e}")
        elif intr==True and matche!=None:
                 messagebox.showerror("Erreur","email introuvable")
        elif matche==None:
                 messagebox.showerror("Erreur","Format d'email incorrecte")
if __name__ == "__main__":
    # Crée une instance de l'application principale
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    
    # Crée la page de connexion et l'affiche
    login_page = Mdps(app, app)
    login_page.pack(fill="both", expand=True)

    # Lance la boucle principale de l'application
    app.mainloop()
     

   

































