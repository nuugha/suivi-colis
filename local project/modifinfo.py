from tkinter import messagebox,Frame
import customtkinter as ctk
import re
import sqlite3


class Modifinf(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")  # Fond blanc
    #couleur
        orange = "#FF7F32"  # Couleur orange
        blue_ciel = "#87CEFA"  # Bleu ciel
        bg_color = "#f5f5f5"  # Fond gris clair

    # Variables pour les menus déroulants
        self.selected_pays = ctk.StringVar(self)
        self.selected_ville = ctk.StringVar(self)
        self.pays_villes = {
         
         "Maroc": ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger', 'Agadir', 'Meknès', 'Oujda', 
 'Kenitra', 'Tetouan', 'Safi', 'El Jadida', 'Nador', 'Beni Mellal', 'Mohammedia', 
 'Taza', 'Khouribga', 'Settat', 'Errachidia', 'Larache', 'Khemisset', 'Ouarzazate', 
 'Tiznit', 'Tan-Tan', 'Guelmim', 'Ifrane', 'Asilah', 'Chefchaouen', 'Al Hoceima', 
 'Taroudant', 'Oued Zem', 'Azrou', 'Sidi Kacem', 'Sidi Slimane', 'Boujdour', 
 'Laâyoune', 'Dakhla']
     }


    #framesup
        self.framesup = ctk.CTkFrame(self,width=5,height=50,corner_radius=0,fg_color=blue_ciel)
        self.framesup.pack(fill="both",anchor="center")

    # Créer un bouton de retour avec une flèche gauche
        self.back_button = ctk.CTkButton(self.framesup, text="◁ Retour", 
                                        font=("Helvetica", 14, "bold"), corner_radius=10, fg_color="#87CEFA",
                                        text_color="white", hover_color="#FFB84D",command=self.retour)
        self.back_button.place(x=20, y=20)  # Positionner le bouton dans le coin supérieur gauche

    # Titre
        self.speedy_label = ctk.CTkLabel(
            self.framesup,
            text="Modifier les informations personnelles ",
            font=("Helvetica", 44, "bold"),
            text_color="#FFA500",
        )
        self.speedy_label.pack(pady=(10, 30))

    # Labels pour les erreurs
        self.error_labels = {}

    # Indicateur pour afficher les erreurs uniquement après la soumission
        self.show_errors = False

    #frame pour les infos
       
        self.frameinfo = ctk.CTkFrame(self,width=650,height=400,corner_radius=40,fg_color="white",border_width=2)
        self.frameinfo.pack(padx=400,pady=20,anchor="w")

        self.usr_label = ctk.CTkLabel(self, text="Username :", font=("Helvetica", 12, "bold"))
        self.usr_label.place(x=460, y=165)
        self.usr_entry = ctk.CTkEntry(self, placeholder_text="Entrez son adresse", font=("Arial", 14), corner_radius=0, height=30,width=300)
        self.usr_entry.place(x=530, y=165)


        # Menu déroulant pour les pays et villes
        self.pays_label = ctk.CTkLabel(self, text="Ville :", font=("Helvetica", 12, "bold"))
        self.pays_label.place(x=490, y=210)
        self.pays_menu = ctk.CTkOptionMenu(self, variable=self.selected_pays, values=['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger', 'Agadir', 'Meknès', 'Oujda', 
 'Kenitra', 'Tetouan', 'Safi', 'El Jadida', 'Nador', 'Beni Mellal', 'Mohammedia', 
 'Taza', 'Khouribga', 'Settat', 'Errachidia', 'Larache', 'Khemisset', 'Ouarzazate', 
 'Tiznit', 'Tan-Tan', 'Guelmim', 'Ifrane', 'Asilah', 'Chefchaouen', 'Al Hoceima', 
 'Taroudant', 'Oued Zem', 'Azrou', 'Sidi Kacem', 'Sidi Slimane', 'Boujdour', 
 'Laâyoune', 'Dakhla'], command=self.update_villes)
        self.pays_menu.place(x=530, y=210)

        

        # Champ pour l'adresse
        self.addr_label = ctk.CTkLabel(self, text="Adresse :", font=("Helvetica", 12, "bold"))
        self.addr_label.place(x=460, y=245)
        self.addr_entry = ctk.CTkEntry(self, placeholder_text="Entrez son adresse", font=("Arial", 14), corner_radius=0, height=30,width=300)
        self.addr_entry.place(x=530, y=245)

        # Champ pour l'email
        self.email_label = ctk.CTkLabel(self, text="Email :", font=("Helvetica", 12, "bold"))
        self.email_label.place(x=480, y=280)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Entrez son Email", font=("Arial", 14), corner_radius=0, width=300)
        self.email_entry.place(x=530, y=280)

        # Champ pour le numéro de téléphone
        self.phone_label = ctk.CTkLabel(self, text="N° de téléphone :", font=("Helvetica", 12, "bold"))
        self.phone_label.place(x=430, y=315)
        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Entrez son N° de téléphone", font=("Arial", 14), corner_radius=0, width=300)
        self.phone_entry.place(x=530, y=315)

        

    #frame enregistre et supprimer
        self.frameinferieur = ctk.CTkFrame(self,width=600,height=60,corner_radius=0,fg_color="white",border_width=0)
        self.frameinferieur.pack(padx=428,pady=0,side="top",anchor="w")

        # Ajouter un bouton de soumission
        self.submit_button = ctk.CTkButton(self, text="Enregistrer", command=self.submit_form,
                                        font=("Helvetica", 14, "bold"), corner_radius=20, fg_color=orange,
                                        text_color="white", hover_color="green",state="normal")
        self.submit_button.place(x=600, y=360)
        
        

        
        # Lier la fonction de validation des champs à l'événement KeyRelease des widgets
        for entry in [  self.email_entry, self.phone_entry]:
            entry.bind("<KeyRelease>", lambda event: self.validate_fields())
        self.pays_menu.bind("<Configure>", lambda event: self.validate_fields())
        

        #frame pour menu
        # Menu Frame
        self.menu_frame = Frame(self, bg=blue_ciel, height=40)
        self.menu_frame.pack(fill="x", side="bottom")

    # Créer les boutons du menu
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
            command=self.gohome
            
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
        


    

##########changer page de revenir§§§§§###########################################
    def revenir_page(self):
        from acc import TrackingApp
        self.controller.show_frame("accueil.py")
######################################################################################
    def update_villes(self, *args):
        pays = self.selected_pays.get()
        villes = ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger', 'Agadir', 'Meknès', 'Oujda', 
 'Kenitra', 'Tetouan', 'Safi', 'El Jadida', 'Nador', 'Beni Mellal', 'Mohammedia', 
 'Taza', 'Khouribga', 'Settat', 'Errachidia', 'Larache', 'Khemisset', 'Ouarzazate', 
 'Tiznit', 'Tan-Tan', 'Guelmim', 'Ifrane', 'Asilah', 'Chefchaouen', 'Al Hoceima', 
 'Taroudant', 'Oued Zem', 'Azrou', 'Sidi Kacem', 'Sidi Slimane', 'Boujdour', 
 'Laâyoune', 'Dakhla']
        
        if pays in villes:
            self.ville_menu.configure(values=villes[pays])
            self.ville_menu.set('')
        else:
            self.ville_menu.configure(values=[])

    def validate_fields(self, event=None):
        # Cette méthode devrait être appelée à chaque modification de champ pour valider l'ensemble du formulaire
        is_valid = True

        for entry in [self.email_entry, self.phone_entry]:
            if not entry.get():  # Si un champ est vide
                is_valid = False

        if self.selected_pays.get() == '' or self.selected_ville.get() == '':
            is_valid = False

        # Si le formulaire est valide, activer le bouton de soumission, sinon le désactiver
        
    
    
    def goacc(self):
        from account import Account
        self.controller.show_frame("Account")
    def retour(self):
        self.addr_entry.delete(0, ctk.END)
        self.email_entry.delete(0, ctk.END)
        self.phone_entry.delete(0, ctk.END)
        self.usr_entry.delete(0, ctk.END)
        from account import Account
        self.controller.show_frame("Account")
    def gohome(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    
    def submit_form(self):
        if not self.show_errors:
            self.show_errors = True

        # Collecter les données des champs
       
        country = self.selected_pays.get()
        city = self.selected_ville.get()
        address = self.addr_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        username=self.usr_entry.get()
       

        # Validation basique pour les champs requis
        if not username  or not country  or not address or not email or not phone :
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

    # Utiliser une expression régulière pour valider l'email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messagebox.showerror("Erreur", "L'adresse email est invalide.")
            return

    # Message de confirmation
        messagebox.showinfo("Succès", "la procuration de votre ami a été enregistré avec succès\n Merçi pour votre confiance 😊.")
        from userclass import user_idg
        conn=sqlite3.connect('suivi_coli.db')
        c=conn.cursor()
        c.execute("select username,cin_individu,ice_societ from user where id_user=?",(user_idg,))
        l1=c.fetchall()
        soc=False
        l2=[]
        if l1[0][1] is None:
                 soc=True
        elif l1[0][2] is None:
                 soc=False
        
        c.execute("update user set username=:usr where id_user=:id",{'usr':self.usr_entry.get(),'id':user_idg})
        if soc:
           c.execute("update societé set adr_societ=:adr, num_telsoc=:num ,email_societ=:email, ville=:vil  where ice_societ=:id",{'adr':address,
                                                                                                                                     'num':phone,
                                                                                                                                     'email':email,
                                                                                                                                     'vil':country,
                                                                                                                                     
                                                                                                                                     'id':l1[0][2]
                                                                                                                                     })
        else:
            c.execute("update individu set adr_individu=:adr, numTel_individu=:num, email_individu=:email, ville=:vil where cin_individu=:id",{'adr':address,
                                                                                                                                     'num':phone,
                                                                                                                                     'email':email,
                                                                                                                                     'vil':country,
                                                                                                                                     
                                                                                                                                     'id':l1[0][1]
                                                                                                                                     })
            
        
            
            
             
        
             
             
             
             
               
             
        conn.commit()
        conn.close()
        
    def insertent(self):
             from userclass import user_idg
             conn=sqlite3.connect('suivi_coli.db')
             c=conn.cursor()
        
             c.execute("select username,cin_individu,ice_societ from user where id_user=?",(user_idg,))
             l1=c.fetchall()
             soc=False
             l2=[]
             if l1[0][1] is None:
                 soc=True
             elif l1[0][2] is None:
                 soc=False
             if soc:
               c.execute("select ville,adr_societ,email_societ,num_telsoc from societé where ice_societ=?",(l1[0][2],))
               l2=c.fetchall()
               print(l2)
             else:
               c.execute("select ville,adr_individu,email_individu,numTel_individu from individu where cin_individu=?",(l1[0][1],))
               l2=c.fetchall()
               print(l2)
             
             self.usr_entry.insert(0,l1[0][0])
             self.pays_menu.set(l2[0][0])
             
             self.addr_entry.insert(0,l2[0][1])
             self.email_entry.insert(0,l2[0][2])
             self.phone_entry.insert(0,l2[0][3])
             
             
             
             
               
             print(user_idg)
             print(l1)
             conn.commit()
             conn.close()
        

    

     
      

        

       

       

    """def create_top_frame(self):
        Crée la frame supérieure avec le titre de l'application.
        top_frame = tk.Frame(self, height=50, bg=blue_ciel)
        top_frame.pack(fill="x", side="top")
        app_name = tk.Label(top_frame, text="My Account", font=("Arial", 35, "bold"), fg="#FF7F32", bg=blue_ciel)
        app_name.place(relx=0.5, rely=0.5, anchor="center")"""
if __name__ == "__main__":
    # Crée une instance de l'application principale
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    
    # Crée la page de connexion et l'affiche
    login_page = Modifinf(app, app)
    login_page.pack(fill="both", expand=True)

    # Lance la boucle principale de l'application
    app.mainloop()
