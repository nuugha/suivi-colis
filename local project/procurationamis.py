from tkinter import messagebox,Frame
import customtkinter as ctk
import re
import sqlite3


class Procami(ctk.CTkFrame):
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
         "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
         "Espagne": ["Madrid", "Barcelone", "Séville", "Valence", "Bilbao"],
         "Italie": ["Rome", "Milan", "Florence", "Venise", "Turin"],
         "États-Unis": ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"],
         "Maroc": ["Casablanca", "Rabat", "Marrakech", "Fes", "Agadir"]
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
            text="Procurer un amis ",
            font=("Helvetica", 44, "bold"),
            text_color="#FFA500",
        )
        self.speedy_label.pack(pady=(10, 30))

    # Labels pour les erreurs
        self.error_labels = {}

    # Indicateur pour afficher les erreurs uniquement après la soumission
        self.show_errors = False

    #frame pour les infos 
        self.frameinfo = ctk.CTkFrame(self,width=650,height=400,corner_radius=0,fg_color="white",border_width=2)
        self.frameinfo.pack(padx=428,pady=20,anchor="w")

        # Champ pour le nom
        self.name_label = ctk.CTkLabel(self, text="Nom :", font=("Helvetica", 12, "bold"))
        self.name_label.place(x=490, y=150)
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Entrez son nom", width=300,height=30, corner_radius=0)
        self.name_entry.place(x=530, y=150)

        # Champ pour le prénom
        self.surname_label = ctk.CTkLabel(self, text="Prénom :", font=("Helvetica", 12, "bold"))
        self.surname_label.place(x=470, y=185)
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Entrez son prénom", width=300, height=30,corner_radius=0)
        self.surname_entry.place(x=530, y=185)

        # Champ pour CIN
        self.cin_label = ctk.CTkLabel(self, text="CIN :", font=("Helvetica", 12, "bold"))
        self.cin_label.place(x=500, y=220)
        self.cin_entry = ctk.CTkEntry(self, placeholder_text="Entrez son CIN", width=300,height=30, corner_radius=0)
        self.cin_entry.place(x=530, y=220)


        # Menu déroulant pour les pays et villes
        self.pays_label = ctk.CTkLabel(self, text="Pays :", font=("Helvetica", 12, "bold"))
        self.pays_label.place(x=490, y=260)
        self.pays_menu = ctk.CTkOptionMenu(self, variable=self.selected_pays, values=["France", "Espagne", "Italie", "États-Unis", "Maroc"], command=self.update_villes)
        self.pays_menu.place(x=530, y=260)

        self.ville_label = ctk.CTkLabel(self, text="Ville :", font=("Helvetica", 12, "bold"))
        self.ville_label.place(x=730, y=260)
        self.ville_menu = ctk.CTkOptionMenu(self, variable=self.selected_ville)
        self.ville_menu.place(x=770, y=260)

        # Champ pour l'adresse
        self.addr_label = ctk.CTkLabel(self, text="Adresse :", font=("Helvetica", 12, "bold"))
        self.addr_label.place(x=460, y=295)
        self.addr_entry = ctk.CTkEntry(self, placeholder_text="Entrez son adresse", font=("Arial", 14), corner_radius=0, height=30,width=300)
        self.addr_entry.place(x=530, y=295)

        # Champ pour l'email
        self.email_label = ctk.CTkLabel(self, text="Email :", font=("Helvetica", 12, "bold"))
        self.email_label.place(x=480, y=330)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Entrez son Email", font=("Arial", 14), corner_radius=0, width=300)
        self.email_entry.place(x=530, y=330)

        
        self.phone_label = ctk.CTkLabel(self, text="N° de téléphone :", font=("Helvetica", 12, "bold"))
        self.phone_label.place(x=430, y=365)
        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Entrez son N° de téléphone", font=("Arial", 14), corner_radius=0, width=300)
        self.phone_entry.place(x=530, y=365)

    
        self.frameinferieur = ctk.CTkFrame(self,width=600,height=60,corner_radius=0,fg_color="white",border_width=0)
        self.frameinferieur.pack(padx=428,pady=0,side="top",anchor="w")

    
        self.submit_button = ctk.CTkButton(self, text="Enregistrer", command=self.submit_form,
                                        font=("Helvetica", 14, "bold"), corner_radius=20, fg_color=orange,
                                        text_color="white", hover_color="green",state="normal")
        self.submit_button.place(x=740, y=440)
        

        
        self.delet_button = ctk.CTkButton(self, text="Supprimer", command=self.supprimer_infos,
                                        font=("Helvetica", 14, "bold"), corner_radius=20, fg_color=blue_ciel,
                                        text_color="white", hover_color="red")
        self.delet_button.place(x=470, y=440)
       
        for entry in [self.name_entry, self.surname_entry,  self.email_entry, self.phone_entry]:
            entry.bind("<KeyRelease>", lambda event: self.validate_fields())
        self.pays_menu.bind("<Configure>", lambda event: self.validate_fields())
        self.ville_menu.bind("<Configure>", lambda event: self.validate_fields())

      
        self.menu_frame = Frame(self, bg=blue_ciel, height=40)
        self.menu_frame.pack(fill="x", side="bottom")

    
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
            command=self.retour
            
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

       
        home_icon.grid(row=0, column=0, padx=10, pady=5)
        gps_icon.grid(row=0, column=1, padx=10, pady=5)
        compte_icon.grid(row=0, column=2, padx=10, pady=5)

        
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_columnconfigure(2, weight=1)
    def supprimer_infos(self):
        for entry in [self.name_entry, self.surname_entry, self.cin_entry,  self.addr_entry, 
                  self.email_entry, self.phone_entry]:
            entry.delete(0, ctk.END)
        self.selected_pays.set('')
        self.selected_ville.set('')


    


    def update_villes(self, *args):
        pays = self.selected_pays.get()
        villes = {
            "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
            "Espagne": ["Madrid", "Barcelone", "Séville", "Valence", "Bilbao"],
            "Italie": ["Rome", "Milan", "Florence", "Venise", "Turin"],
            "États-Unis": ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"],
            "Maroc": ["Casablanca", "Rabat", "Marrakech", "Fes", "Agadir"]
        }
        if pays in villes:
            self.ville_menu.configure(values=villes[pays])
            self.ville_menu.set('')
        else:
            self.ville_menu.configure(values=[])

    def validate_fields(self, event=None):
        
        is_valid = True

        for entry in [self.name_entry, self.surname_entry,self.email_entry, self.phone_entry]:
            if not entry.get():  
                is_valid = False

        if self.selected_pays.get() == '' or self.selected_ville.get() == '':
            is_valid = False

       
        
    
    
    def goacc(self):
        from account import Account
        self.controller.show_frame("Account")
    def retour(self):
        self.supprimer_infos()
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    
    def submit_form(self):
        if not self.show_errors:
            self.show_errors = True

        
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        cin = self.cin_entry.get()
        country = self.selected_pays.get()
        city = self.selected_ville.get()
        address = self.addr_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
       

       
        if not name or not surname or not cin  or not country or not city or not address or not email or not phone :
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

   
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messagebox.showerror("Erreur", "L'adresse email est invalide.")
            return

    
        messagebox.showinfo("Succès", "la procuration de votre ami a été enregistré avec succès\n Merçi pour votre confiance 😊.")
        from userclass import user_idg
        print(user_idg)
        conn=sqlite3.connect("suivi_coli.db")
        c=conn.cursor()
        c.execute(f"select * from amiprocure where id_user={user_idg}")
        l=c.fetchall()
        if l==[]:
          c.execute("insert into amiprocure values(:id,:nm,:prn,:addr,:email,:tel,:iduser,:ville,:pays)" ,{
            "id":self.cin_entry.get(),
            'nm':self.name_entry.get(),
            'prn':self.surname_entry.get(),
            'addr':self.addr_entry.get(),
            'email':self.email_entry.get(),
            'tel':self.phone_entry.get(),
            'ville':self.selected_ville.get(),
            'iduser':user_idg,
            'pays':self.selected_pays.get()
            })
        else:
            c.execute("""
                        UPDATE amiprocure
                        SET 
                        nm_ampr = :nm,
                        prn_ampr = :prn,
                        addr_ampr = :addr,
                        email_ampr = :email,
                        tel_ampr = :tel,
                        ville = :ville,
                        pays = :pays
                        WHERE id_ami = :id AND id_user = :iduser
                      """, {
                          "id": self.cin_entry.get(),
                          'nm': self.name_entry.get(),
                          'prn': self.surname_entry.get(),
                          'addr': self.addr_entry.get(),
                          'email': self.email_entry.get(),
                          'tel': self.phone_entry.get(),
                          'ville': self.selected_ville.get(),
                          'iduser': user_idg,
                          'pays': self.selected_pays.get()
                            })
            
        conn.commit()
        conn.close()
    def insertent(self):
             from userclass import user_idg
             conn=sqlite3.connect('suivi_coli.db')
             c=conn.cursor()
             l1=[]
        
             c.execute("select username,cin_individu,ice_societ from user where id_user=?",(user_idg,))
             l1=c.fetchall()
             soc=False
            
             if l1[0][1] is None:
                 soc=True
             elif l1[0][2] is None:
                 soc=False
             if soc:
                 pass
             else:
               c.execute("select Nm_ampr,prn_ampr,id_ami,pays,ville,addr_ampr,email_ampr,tel_ampr from amiprocure where id_user=?",(user_idg,))
               l2=c.fetchall()
               print(l2)
               if l2==[]:
                   pass
               else:
                    self.name_entry.insert(0,l2[0][0])
                    self.surname_entry.insert(0,l2[0][1])
                    self.cin_entry.insert(0,l2[0][2])
                    self.addr_entry.insert(0,l2[0][5])
                    self.pays_menu.set(l2[0][3])
                    self.ville_menu.set(l2[0][4])
                    self.email_entry.insert(0,l2[0][6])
                    self.phone_entry.insert(0,l2[0][7])
                   
            
             
            
             
             
             
             
               
             print(user_idg)
             print(l1)
             conn.commit()
             conn.close()
        
        
        

    

     
      

        

       

       

    
if __name__ == "__main__":
    # Crée une instance de l'application principale
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    
    # Crée la page de connexion et l'affiche
    login_page = Procami(app, app)
    login_page.pack(fill="both", expand=True)

    # Lance la boucle principale de l'application
    app.mainloop()
