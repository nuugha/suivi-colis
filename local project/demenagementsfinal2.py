from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3
from datetime import datetime


class Demanagement(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")  # Fond blanc

        # Couleurs
        orange = "#FF7F32"  # Couleur orange
        blue_ciel = "#87CEFA"  # Bleu ciel

        # Variables pour les menus déroulants
        self.selected_ville = ctk.StringVar(self)
        self.selected_services = ctk.StringVar(value="cartons")
        self.selected_transp = ctk.StringVar(value="camion")

        # Barre supérieure
        self.framesup = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=blue_ciel)
        self.framesup.pack(fill="x", side="top")

        self.back_button = ctk.CTkButton(
            self.framesup,
            text="◁ Retour",
            command=self.revenir_page,
            font=("Helvetica", 14, "bold"),
            corner_radius=10,
            fg_color=blue_ciel,
            text_color="white",
            hover_color="#FFB84D",
        )
        self.back_button.pack(side="left", padx=10, pady=10)

        self.speedy_label = ctk.CTkLabel(
            self.framesup,
            text="Déménagement",
            font=("Helvetica", 44, "bold"),
            text_color="#FFA500",
        )
        self.speedy_label.pack(pady=(10, 20))

        # Zone de contenu défilable
        self.bframe = ctk.CTkScrollableFrame(self, fg_color="white")
        self.bframe.pack(fill="both", expand=True, side="top")

                # Correction des doublons et des incohérences
               # Correction des doublons et des incohérences
                # Correction des doublons et des incohérences
        self.labelpetit = ctk.CTkLabel(
                self.bframe,
                text="Organisez votre déménagement en toute simplicité 😊!",
                font=("Arial", 25, "bold"),
                text_color=orange,
        )
        self.labelpetit.pack(pady=10)

        # Détails du déménagement
        self.label2 = ctk.CTkLabel(self.bframe, text="Détails de déménagement :", font=("Arial", 27, "bold"))
        self.label2.pack(pady=10)

        # Section 1: Informations sur le déménagement
        frame_info_demenagement = self.create_titled_frame(self.bframe, "Informations sur le Déménagement", blue_ciel)
        ctk.CTkLabel(frame_info_demenagement, text="Adresse de départ:", font=("Helvetica", 12, "bold"),fg_color=blue_ciel).pack(anchor="w", pady=(5, 0))
        self.addr_entry = ctk.CTkEntry(frame_info_demenagement, placeholder_text="Entrez l'adresse de départ", font=("Helvetica", 12))
        self.addr_entry.pack(fill="x", padx=5, pady=(0, 5))

# Adresse d'arrivée
        ctk.CTkLabel(frame_info_demenagement, text="Adresse d'arrivée:", font=("Helvetica", 12, "bold"),fg_color=blue_ciel).pack(anchor="w", pady=(5, 0))
        self.adrfinalentry = ctk.CTkEntry(frame_info_demenagement, placeholder_text="Entrez l'adresse d'arrivée", font=("Helvetica", 12))
        self.adrfinalentry.pack(fill="x", padx=5, pady=(0, 5))

        # Section 2: Date et heure du déménagement
        frame_date_heure = self.create_titled_frame(self.bframe, "Date et Heure du Déménagement", blue_ciel)

        ctk.CTkLabel(frame_date_heure, text="Date (JJ/MM/AAAA):", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        self.date_entry = ctk.CTkEntry(frame_date_heure, placeholder_text="DD/MM/YYYY", font=("Helvetica", 12))
        self.date_entry.pack(anchor="w",pady=4,padx=4)
        # Ajouter un bouton pour afficher le calendrier
        self.calendar_button = tk.Button(frame_date_heure, text="📅", command=self.open_calendar)
        self.calendar_button.pack(anchor='w')
    
        ctk.CTkLabel(frame_date_heure, text="Heure préférée:", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        time_choices = ["Matin", "Après-midi", "Soir"]
        self.time_combo = ctk.CTkOptionMenu(frame_date_heure, values=time_choices, font=("Helvetica", 12), dynamic_resizing=False)
        self.time_combo.pack(anchor="w",pady=4,padx=4)

        # Section 3: Nature des biens
        frame_biens = self.create_titled_frame(self.bframe, "Nature des Biens", blue_ciel)

        ctk.CTkLabel(frame_biens, text="Objets volumineux:", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        self.objspecif_entry = ctk.CTkEntry(frame_biens, placeholder_text="Liste des objets volumineux", font=("Helvetica", 12))
        self.objspecif_entry.pack(anchor="w",pady=4,padx=4)

        ctk.CTkLabel(frame_biens, text="Nombre de cartons estimés:", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        self.carton_entry = ctk.CTkEntry(frame_biens, placeholder_text="Quantité de cartons", font=("Helvetica", 12))
        self.carton_entry.pack(anchor="w",pady=4,padx=4)

        # Section 4: Véhicules et assistance
        frame_vehicules = self.create_titled_frame(self.bframe, "Véhicules et Assistance", blue_ciel)

        ctk.CTkLabel(frame_vehicules, text="Nombre de véhicules:", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        self.vehicule_entry = ctk.CTkEntry(frame_vehicules, placeholder_text="Nombre de véhicules", font=("Helvetica", 12))
        self.vehicule_entry.pack(anchor="w",pady=4,padx=4)

        ctk.CTkLabel(frame_vehicules, text="Type de véhicules:", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        vehicules_choices = ["Petit camion", "Camion moyen", "Camion grande capacité"]
        self.vehicules_combo = ctk.CTkOptionMenu(frame_vehicules, values=vehicules_choices, font=("Helvetica", 12), dynamic_resizing=False)
        self.vehicules_combo.pack(anchor="w",pady=4,padx=4)

        ctk.CTkLabel(frame_vehicules, text="Nombre de personnes pour aide:", font=("Helvetica", 12, "bold")).pack(anchor="w",pady=4,padx=4)
        self.npers_entry = ctk.CTkEntry(frame_vehicules, placeholder_text="Nombre de personnes", font=("Helvetica", 12))
        self.npers_entry.pack(anchor="w",pady=4,padx=4)

        # Section 5: Services complémentaires
        frame_services = self.create_titled_frame(self.bframe, "Services Complémentaires", blue_ciel)

        self.services = [
            "Aide pour emballage",
            "Démontage/remontage des meubles",
            "Fourniture d'emballage",
            "Stockage temporaire",
        ]
        self.services_vars = []

        for i, service in enumerate(self.services):
            var = tk.BooleanVar()
            check = ctk.CTkCheckBox(frame_services, text=service, variable=var, font=("Helvetica", 12))
            check.pack(anchor="w",pady=4,padx=4)
            self.services_vars.append(var)

        # Section 6: Contraintes particulières
        frame_contraintes = self.create_titled_frame(self.bframe, "Contraintes Particulières", blue_ciel)

        self.constraints_text = ctk.CTkTextbox(frame_contraintes, font=("Helvetica", 12),width=400,height=50)
        self.constraints_text.pack(anchor="w",pady=4,padx=4)
        self.submite_button = ctk.CTkButton(self.bframe, text="Confirmer la demande", command=self.submit_form,
                                        font=("Helvetica", 30, "bold"), corner_radius=20, fg_color=orange,
                                        text_color="white", hover_color="green",state="normal")
        self.submite_button.pack(padx=250,side="right")
        

        #ajouter boutton de supprimer 
        self.delet_button = ctk.CTkButton(self.bframe, text="Supprimer", command=self.ask_confirmation,
                                        font=("Helvetica", 30, "bold"), corner_radius=20, fg_color=blue_ciel,
                                        text_color="white", hover_color="red")
        self.delet_button.pack(padx=40,pady=40)
       
    def revenir_page(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def ask_confirmation(self):
        response = messagebox.askquestion("Confirmation", "Voulez-vous effacer tous les champs ?")
        if response == "yes":
            self.reset_form()

    def reset_form(self):
        self.addr_entry.delete(0, tk.END)
        self.adrfinalentry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.carton_entry.delete(0, tk.END)
        self.objspecif_entry.delete(0, tk.END)
        self.npers_entry.delete(0, tk.END)
        self.selected_ville.set("El jadida")
        self.selected_services.set("cartons")
        self.selected_transp.set("camion")
        self.constraints_text.delete("1.0", tk.END)

    def validate_fields(self):
     if not self.addr_entry.get().strip():
        messagebox.showerror("Erreur", "L'adresse de départ est obligatoire.")
        return False
     if not self.adrfinalentry.get().strip():
        messagebox.showerror("Erreur", "L'adresse d'arrivée est obligatoire.")
        return False
     if not self.date_entry.get().strip():
        messagebox.showerror("Erreur", "La date est obligatoire.")
        return False
     if not self.carton_entry.get().isdigit():
        messagebox.showerror("Erreur", "Le nombre de cartons doit être un chiffre.")
        return False
     
     return True


    def submit_form(self):
            if not all(
               [self.addr_entry.get(), self.adrfinalentry.get(), self.date_entry.get(),self.carton_entry.get(),self.objspecif_entry.get(),
                   self.npers_entry.get()]):
                  messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
        #else:
        #if self.validate_fields():
            conn=sqlite3.connect('suivi_coli.db')
            curs=conn.cursor()
            from userclass import user_idg
            print(user_idg)
            selected_services = [
               service for var, service in zip(self.services_vars, self.services) if var.get()
                                  ]
    # Combine selected services into a single string or handle as needed
            selected_services_str = ", ".join(selected_services)
    
            print("Selected Services:", selected_services_str)

            

         
            


            curs.execute("""INSERT INTO demenagement(id_user,adress_depart, adress_arrive, date_dem, heure_dem,objet_volum, nbr_cart, type_vehic, nbr_pers, nom_service,contrainte)
                          VALUES (:id,:adress_depart, :adress_arrive, :date_dem, :heure_dem,:objet_volum, :nbr_cart, :type_vehic, :nbr_pers, :nom_service,:contrainte )""",
            {
                "adress_depart": self.addr_entry.get(),
                "adress_arrive": self.adrfinalentry.get(),
                "date_dem": self.date_entry.get(),
                "heure_dem": self.time_combo.get(),
                "objet_volum": self.objspecif_entry.get(),
                "nbr_cart": int(self.carton_entry.get()),
                "type_vehic": self.vehicules_combo.get(),  
                "nbr_pers": int(self.npers_entry.get()),
                "nom_service": selected_services_str ,
                "contrainte" :self.constraints_text.get("1.0", "end-1c").strip(),
                "id":user_idg
            })
            conn.commit()
            conn.close()
            messagebox.showinfo("succés","demenagement enregistré avec succés !\n Nous vous contacterons le plus tot possible\n Merci pour votre confiance 😊!")
            self.reset_form()

    def open_calendar(self):
         """Ouvre un calendrier pour sélectionner une date"""
         def select_date():
             selected_date = calendar.get_date()  # Récupère la date sélectionnée
             self.date_entry.delete(0, ctk.END)  # Efface l'entrée existante
             self.date_entry.insert(0, selected_date)  # Insère la date sélectionnée
             calendar_window.destroy()  # Ferme la fenêtre du calendrier

         # Créer une fenêtre pop-up pour le calendrier
         calendar_window = tk.Toplevel(self)
         calendar_window.title("Sélectionner une date")
         calendar = Calendar(calendar_window, date_pattern="dd/mm/yyyy")
         calendar.pack(pady=10)

         # Bouton pour confirmer la sélection de la date
         select_button = ctk.CTkButton(calendar_window, text="Sélectionner", command=select_date)
         select_button.pack(pady=10) 
    
    def create_titled_frame(self, parent, title, bg_color=None):
    # Create a CustomTkinter frame
       frame = ctk.CTkFrame(parent, fg_color=bg_color)
       frame.pack(fill="x", padx=20, pady=10)

    # Add a title to the frame using a CTkLabel widget
       title_label = ctk.CTkLabel(frame, text=title, font=("Arial", 16, "bold"), text_color="black", bg_color=bg_color)
       title_label.pack(anchor="w", padx=5, pady=5)

       return frame


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    dem_page = Demanagement(app, app)
    dem_page.pack(fill="both", expand=True)
    app.mainloop()


  
