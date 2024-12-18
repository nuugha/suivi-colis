from tkinter import *
import customtkinter as ctk
from datetime import datetime, date
import sqlite3
from tkinter import messagebox
import sys
import importlib
from importlib import reload
    




class ColisFenetre(ctk.CTkToplevel):
    def __init__(self, parent, colis_data):
        super().__init__(parent)
        self.geometry("600x500")
        self.title("Détails du colis")
        
        # Couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"
        
        # En-tête
        header = ctk.CTkFrame(self, fg_color=self.blue_ciel, height=80)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(
            header,
            text="Détails de la livraison",
            font=("Arial", 24, "bold"),
            text_color=self.orange
        )
        title.pack(pady=20)

        # Contenu principal
        content = ctk.CTkFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # ID Colis
        id_frame = ctk.CTkFrame(content, fg_color="transparent")
        id_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            id_frame,
            text=f"🏷️ ID Colis: {colis_data['id_colis']}",
            font=("Arial", 18, "bold"),
            text_color="black"
        ).pack(anchor="w", padx=20)

        # Date et Heure
        date_frame = ctk.CTkFrame(content, fg_color="transparent")
        date_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            date_frame,
            text=f"📅 Date: {colis_data['date'].strftime('%d/%m/%Y')}",
            font=("Arial", 18),
            text_color="black"
        ).pack(side="left", padx=20)

        ctk.CTkLabel(
            date_frame,
            text=f"🕒 Horaire: {colis_data['heure_debut']} - {colis_data['heure_fin']}",
            font=("Arial", 18),
            text_color="black"
        ).pack(side="left", padx=20)

        # Séparateur
        self.create_separator(content)

        # Localisation
        location_frame = ctk.CTkFrame(content, fg_color="transparent")
        location_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            location_frame,
            text=f"🏙️ Ville: {colis_data['ville']}",
            font=("Arial", 18),
            text_color="black"
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            location_frame,
            text=f"📍 Adresse: {colis_data['adresse']}",
            font=("Arial", 18),
            text_color="black"
        ).pack(anchor="w", padx=20)

        # Séparateur
        self.create_separator(content)

        # Prix
        price_frame = ctk.CTkFrame(content, fg_color="transparent")
        price_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            price_frame,
            text=f"💰 Prix de livraison: {colis_data['prix']} DH",
            font=("Arial", 20, "bold"),
            text_color=self.orange
        ).pack(anchor="w", padx=20)

        # Séparateur
        self.create_separator(content)

        # Boutons
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)

        ctk.CTkButton(
            buttons_frame,
            text="Fermer",
            font=("Arial", 18),
            fg_color="grey",
            command=self.destroy,
            width=200
        ).pack(padx=20)

    def create_separator(self, parent):
        separator = ctk.CTkFrame(parent, height=2, fg_color="grey")
        separator.pack(fill="x", padx=20, pady=10)

class notif(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.configure(fg_color="white")
        # Pour l'utiliser:
        
        self.notifications=None
        
        # Initialiser la page directement dans __init__
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA" 
        self.bg_color = "#f5f5f5"

        # En-tête
        self.create_header()

        # Frame temps 
        self.create_time_frame()

        # Frame principale scrollable pour les notifications
        self.framegrande = ctk.CTkScrollableFrame(self, width=900, height=600, corner_radius=3, fg_color=self.blue_ciel, border_width=5)
        self.framegrande.pack(fill="both", expand=True, padx=30, pady=10)

        # Récupération des notifications
        self.get_notifications()
        self.display_notifications()
    
    def get_notifications(self):
        
        from userclass import user_idg
        if user_idg is None:
            print(user_idg,"Notif")
            return []
        
        print(user_idg,'succe')
        
        conn = sqlite3.connect("suivi_coli.db")
        c = conn.cursor()
        
        c.execute("""
        SELECT c.prix, d.ville, d.addr_dest, n.date_notif, n.contenu_notif, 
               n.id_colis, n.horraire1, n.horraire2, n.date_estime 
        FROM notification n 
        JOIN colis c ON n.id_colis = c.id_colis 
        JOIN destinataire d ON c.id_dest = d.id_dest 
        WHERE n.id_user = ?
        """, (user_idg,))
        
        self.notifications = c.fetchall()
        conn.close()
        
        # Convertir en format stockable (liste de dictionnaires)
        notifications_data = [
            {
                'prix': n[0],
                'ville': n[1],
                'adresse': n[2],
                'date_notif': n[3],
                'contenu': n[4],
                'id_colis': n[5],
                'heure_debut': n[6],
                'heure_fin': n[7],
                'date_estime': n[8]
            } for n in self.notifications
        ]
        return notifications_data
    
    def create_header(self):
        self.framenotif = ctk.CTkFrame(self, height=100, corner_radius=0, fg_color=self.blue_ciel)
        self.framenotif.pack(fill="x")
        
        back_button = ctk.CTkButton(
            self.framenotif, 
            text="⬅️ Retour",
            corner_radius=13,
            font=("Arial", 18, "bold"),
            fg_color=self.orange,
            command=self.go_back,
            width=100
        )
        back_button.pack(side="left", padx=20, pady=10)

        self.labelnotif = ctk.CTkLabel(
            self.framenotif,
            text="Notifications", 
            text_color=self.orange,
            font=("Arial", 28, "bold")
        )
        self.labelnotif.pack(pady=20)

    def create_time_frame(self):
        self.frametemp = ctk.CTkFrame(self, height=50, corner_radius=10, fg_color="white")
        self.frametemp.pack(fill="x", padx=30, pady=10)

    def display_notifications(self):
        for widget in self.framegrande.winfo_children():
            widget.destroy()

        # Obtenir les notifications
        notifications = self.get_notifications()
        
        if not notifications:
            no_notif_label = ctk.CTkLabel(
                self.framegrande,
                text="Vous n'avez aucune notification",
                font=("Arial", 20, "bold"),
                text_color="black"
            )
            no_notif_label.pack(pady=50)
            return

        # Grouper les notifications par date
        notifications_by_date = {}
        for notif in self.notifications:
            prix, ville, adresse, date_notif, contenu, id_colis, heure_debut, heure_fin, date_estime = notif
            date_obj = datetime.strptime(date_notif, '%d/%m/%Y').date()
            
            if date_obj not in notifications_by_date:
                notifications_by_date[date_obj] = []
            
            notifications_by_date[date_obj].append({
                'prix': prix,
                'ville': ville,
                'adresse': adresse,
                'date': date_obj,
                'contenu': contenu,
                'id_colis': id_colis,
                'heure_debut': heure_debut,
                'heure_fin': heure_fin,
                'date_estime': date_estime
            })

        # Afficher les notifications groupées par date
        for notif_date in sorted(notifications_by_date.keys(), reverse=True):
            self.create_date_section(notif_date, notifications_by_date[notif_date])

    def create_date_section(self, notif_date, notifications):
        date_text = "Aujourd'hui" if notif_date == date.today() else notif_date.strftime("%d/%m/%Y")
        date_frame = ctk.CTkFrame(self.framegrande, fg_color="transparent")
        date_frame.pack(fill="x", pady=5)
        
        date_label = ctk.CTkLabel(
            date_frame,
            text=date_text,
            font=("Arial", 22, "bold"),
            text_color="black"
        )
        date_label.pack(anchor="w", padx=20)

        for notif_data in notifications:
            self.create_notification_card(notif_data)

    def create_notification_card(self, notif_data):
        card_frame = ctk.CTkFrame(
            self.framegrande,
            fg_color="white",
            corner_radius=10,
            border_width=2,
            border_color=self.blue_ciel
        )
        card_frame.pack(fill="x", padx=20, pady=5)

        left_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        # Ajout de l'ID du colis
        ctk.CTkLabel(
            left_frame,
            text=f"🏷️ Colis #{notif_data['id_colis']}",
            font=("Arial", 16),
            text_color="black"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_frame,
            text=f"📦 {notif_data['contenu']}",
            font=("Arial", 20, "bold"),
            text_color="black"
        ).pack(anchor="w")

        details_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            details_frame,
            text=f"🕒 {notif_data['heure_debut']} - {notif_data['heure_fin']}",
            font=("Arial", 16),
            text_color="#12818d"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            details_frame,
            text=f"💰 {notif_data['prix']} DH",
            font=("Arial", 16),
            text_color="#12818d"
        ).pack(side="left", padx=10)

        location_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        location_frame.pack(fill="x")

        ctk.CTkLabel(
            location_frame,
            text=f"🏙️ {notif_data['ville']}",
            font=("Arial", 16),
            text_color=self.orange
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            location_frame,
            text=f"📍 {notif_data['adresse']}",
            font=("Arial", 16),
            text_color=self.orange
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            card_frame,
            text="➡️",
            font=("Arial", 24),
            fg_color="transparent",
            text_color=self.blue_ciel,
            width=50,
            command=lambda: self.open_colis_details(notif_data)
        ).pack(side="right", padx=15)

    def open_colis_details(self, colis_data):
        colis_fenetre = ColisFenetre(self, colis_data)
        colis_fenetre.focus()

    def go_back(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")




    



if __name__ == "__main__":
  
   
    app = ctk.CTk()
    app.geometry("1000x800")
    notific = notif(app, app)
    notific.pack(fill="both", expand=True)
    app.mainloop()
