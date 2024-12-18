import tkinter as tk
from tkinter import messagebox
import tkintermapview
import customtkinter as ctk

# Dictionnaire des coordonnées GPS des principales villes marocaines
VILLES_MAROC = {
    'Casablanca': (33.5731, -7.5898),
    'Rabat': (34.0209, -6.8416), 
    'Marrakech': (31.6295, -7.9811),
    'Fès': (34.0333, -5.0000),
    'Tanger': (35.7595, -5.8340),
    'Agadir': (30.4278, -9.5981),
    'Meknès': (33.8731, -5.5407),
    'Oujda': (34.6867, -1.9114),
    'Kenitra': (34.2610, -6.5802),
    'Tetouan': (35.5784, -5.3630),
    'Safi': (32.2994, -9.2372),
    'El Jadida': (33.2316, -8.5007),
    'Nador': (35.1667, -2.9333),
    'Beni Mellal': (32.3373, -6.3498),
    'Mohammedia': (33.6833, -7.3833),
    'Taza': (34.2167, -4.0167),
    'Khouribga': (32.8833, -6.9167),
    'Settat': (33.0000, -7.6167),
    'Errachidia': (31.9333, -4.4167),
    'Larache': (35.1833, -6.1500),
    'Khemisset': (33.8167, -6.0667),
    'Ouarzazate': (30.9167, -6.8833),
    'Tiznit': (29.7000, -9.7333),
    'Tan-Tan': (28.4333, -11.1000),
    'Guelmim': (28.9833, -10.0667),
    'Ifrane': (33.5333, -5.1000),
    'Asilah': (35.4667, -6.0333),
    'Chefchaouen': (35.1667, -5.2667),
    'Al Hoceima': (35.2500, -3.9333),
    'Taroudant': (30.4667, -8.8833),
    'Oued Zem': (32.8667, -6.5667),
    'Azrou': (33.4333, -5.2167),
    'Sidi Kacem': (34.2167, -5.7000),
    'Sidi Slimane': (34.2667, -5.9167),
    'Boujdour': (26.1333, -14.4833),
    'Laâyoune': (27.1500, -13.2000),
    'Dakhla': (23.7167, -15.9333)
}

class SuiviColis(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
      
        # Couleurs
        orange = "#FF7F32"
        blue_ciel = "#87CEFA"

        # Header
        self.header_frame = ctk.CTkFrame(self, height=80, fg_color=blue_ciel)
        self.header_frame.pack(fill="x")

        self.back_button = ctk.CTkButton(self.header_frame, text="◁ Retour",
                                         font=("Helvetica", 19, "bold"),
                                         corner_radius=10, fg_color=blue_ciel,
                                         text_color="white", hover_color=orange,
                                         command=self.revenir_page)
        self.back_button.pack(side="left", padx=20, pady=40)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Suivi de Colis",
                                        font=("Helvetica",50, "bold"), text_color=orange)
        self.title_label.pack(pady=10)

        # Corps principal
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Entrée pour numéro de suivi
        self.track_label = ctk.CTkLabel(self.main_frame, text="Entrez le numéro de suivi :",
                                        font=("Helvetica", 20, "bold"), text_color=orange)
        self.track_label.pack(pady=(10, 5))

        self.track_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Numéro de suivi...",
                                        font=("Arial", 14), width=300, height=40, corner_radius=10)
        self.track_entry.pack(pady=8)

        self.search_button = ctk.CTkButton(self.main_frame, text="Rechercher", font=("Helvetica", 16, "bold"),
                                           fg_color=orange, text_color="white", corner_radius=10,
                                           hover_color=blue_ciel, command=self.get_tracking_info)
        self.search_button.pack(pady=15)

        # Informations de suivi
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=10, border_color=blue_ciel,
                                       border_width=2)
        self.info_frame.pack(fill="x", pady=15, padx=20)

        self.info_label = ctk.CTkLabel(self.info_frame, text="Informations de suivi :",
                                       font=("Helvetica", 20, "bold"), text_color=orange)
        self.info_label.pack(pady=8)

        self.status_label = ctk.CTkLabel(self.info_frame, text="Statut : En attente de recherche...",
                                         font=("Helvetica", 16,"bold"), text_color="black")
        self.status_label.pack(pady=5)

        

        # Zone pour afficher la carte
        self.map_frame = ctk.CTkFrame(self, fg_color="white")
        self.map_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialisation de la carte
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=800, height=400)
        self.map_widget.pack(fill="both", expand=True)

        # Initialisation de la carte sur le Maroc
        self.initial_map_position()

    def revenir_page(self):
        """Revenir à la page précédente."""
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def get_tracking_info(self):
        """Récupère les informations de suivi depuis la base de données SQLite"""
        import sqlite3
        
        tracking_number = self.track_entry.get()
        if not tracking_number:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de suivi valide.")
            return

        try:
            from userclass import user_idg
            conn = sqlite3.connect('suivi_coli.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT 
                    c.id_colis,
                    c.y,
                    c.x,
                    c.etatlivrs,
                    c.date_livrs,
                    
                    c.posit_desti_lat,c.posit_desti_lon
                    
                FROM colis c
                LEFT JOIN destinataire d ON c.id_dest = d.id_dest
                LEFT JOIN user u ON c.id_user = u.id_user
                WHERE c.id_colis = ? and c.id_user=?
            ''', (tracking_number,user_idg))
            
            result = cursor.fetchone()

            if result:
                id_colis, x, y, etat_livraison, date_livraison,posit_desti_lat,posit_desti_lon = result
                
                etats = {
                    0: "En attente",
                    1: "En cours de livraison",
                    2: "Livré",
                    3: "Annulé"
                }
                etat_texte = etats.get(etat_livraison, "État inconnu")
                
                # Afficher la position actuelle et la destination sur la carte
                if x is not None and y is not None:
                    self.map_widget.delete_all_marker()

# Set marker for the current parcel position
                    self.map_widget.set_marker(y, x, text="Position actuelle du colis", marker_color_circle="red")

# Set marker for the destination
                    dest_lat, dest_lon = posit_desti_lat, posit_desti_lon
                    self.map_widget.set_marker(dest_lat, dest_lon, text="Destination", marker_color_circle="green")

# Draw a path between the current position and destination
                    self.map_widget.set_path([(y, x), (dest_lat, dest_lon)])

# Fit the map view to show both points
                    position_top_left = (min(y, dest_lat), min(x, dest_lon))  # Top-left corner
                    position_bottom_right = (max(y, dest_lat), max(x, dest_lon))  # Bottom-right corner
                    self.map_widget.fit_bounding_box(position_top_left, position_bottom_right)


                    
                
                # Mettre à jour les labels
                self.status_label.configure(
                    text=f"Statut : {etat_texte}\nDate de livraison : {date_livraison}"
                )
                self.location_label.configure(
                    text=f"Position actuelle : {y},{x}\n"
                    f"Destination : {addr_dest}, {ville_dest}, MAROC"
                )
            else:
                self.status_label.configure(text="Statut : Numéro de colis inconnu")
                self.location_label.configure(text="Position GPS : -")

        except sqlite3.Error as err:
            messagebox.showerror("Erreur de base de données", f"Une erreur est survenue : {err}")

        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

    def initial_map_position(self):
        """Initialiser la carte sur une position approximative du Maroc."""
        latitude = 31.7917
        longitude = -7.0926
        self.map_widget.set_position(latitude, longitude)
        self.map_widget.set_zoom(6)

    def display_map(self, lat, lon):
        """Affiche la carte avec la position du colis."""
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(12)
        self.map_widget.set_marker(lat, lon, text="Position actuelle du colis")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Suivi de Colis")
    root.geometry("1200x800")
    app = SuiviColis(root, root)
    app.pack(fill="both", expand=True)
    root.mainloop()
