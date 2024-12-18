import sqlite3
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv

class HistoriqueColis(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Connexion à la base de données
        self.conn = sqlite3.connect('suivi_coli.db')
        self.cursor = self.conn.cursor()

        # Définition des couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"
        self.blanc = "white"

        # Configuration de l'interface
        self.setup_interface()

    def setup_interface(self):
        # Frame principale
        self.main_frame = ctk.CTkFrame(self, fg_color=self.blanc)
        self.main_frame.pack(fill="both", expand=True)

        # Frame supérieure
        self.frame_sup = ctk.CTkFrame(self.main_frame, height=100, fg_color=self.blue_ciel)
        self.frame_sup.pack(fill="x")
        self.back_button = ctk.CTkButton(self.frame_sup, text="◁ Retour", command=self.revenir_page,
                                        font=("Helvetica", 14, "bold"), corner_radius=10, fg_color=self.orange,
                                        text_color="white", hover_color="#FFB84D")
        self.back_button.pack(side="left",pady=20, padx=10)
        # Titre
        self.titre = ctk.CTkLabel(
            self.frame_sup,
            text="Mes Colis",
            font=("Helvetica", 40, "bold"),
            text_color=self.orange
        )
        self.titre.pack(side="top",pady =20)
        # Frame de filtres
        self.frame_filtres = ctk.CTkFrame(self.main_frame, fg_color=self.blanc)
        self.frame_filtres.pack(fill="x", padx=20, pady=10)

        # Barre de recherche
        self.recherche = ctk.CTkEntry(
            self.frame_filtres,
            placeholder_text=" 🔍 Rechercher un colis...",
            width=300,
            height=35,
            font=("Helvetica", 15,"bold")
        )
        self.recherche.pack(side="left", padx=10, pady=10)

        # Filtre de statut
        self.statut_var = ctk.StringVar(value="Tous les statuts")
        self.filtre_statut = ctk.CTkOptionMenu(
            self.frame_filtres,
            values=["Tous les statuts", "En transit", "Livré", "En attente"],
            variable=self.statut_var,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.filtre_statut.pack(side="left", padx=10)

        # Boutons
        self.bouton_rechercher = ctk.CTkButton(
            self.frame_filtres,
            text="🔍 Rechercher",
            command=self.rechercher,
            fg_color=self.orange,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.bouton_rechercher.pack(side="left", padx=5)

        self.bouton_actualiser = ctk.CTkButton(
            self.frame_filtres,
            text="🔄 Actualiser",
            command=self.actualiser_donnees,
            fg_color=self.orange,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.bouton_actualiser.pack(side="left", padx=5)

        self.bouton_exporter = ctk.CTkButton(
            self.frame_filtres,
            text="📥 Exporter CSV",
            command=self.exporter_csv,
            fg_color=self.blue_ciel,
            width=150,
            height=55,
            font=("Helvetica", 15,"bold")
        )
        self.bouton_exporter.pack(side="left", padx=5)

        # Frame pour le tableau
        self.frame_tableau = ctk.CTkFrame(self.main_frame, fg_color=self.blanc)
        self.frame_tableau.pack(fill="both", expand=True, padx=20, pady=10)

        # Tableau
        colonnes = ('Numéro', 'Date', 'Expéditeur', 'Destinataire', 'Statut')
        self.tableau = ttk.Treeview(self.frame_tableau, columns=colonnes, show='headings')
        
        # Configuration des colonnes
        for col in colonnes:
            self.tableau.heading(col, text=col, command=lambda c=col: self.trier_tableau(c))
            self.tableau.column(col, width=150, anchor='center')

        # Style du tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 15, 'bold'))
        style.configure("Treeview", font=('Helvetica', 15), rowheight=30)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tableau, orient="vertical", command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tableau.pack(fill="both", expand=True)

        # Événements du tableau
        self.tableau.bind("<Button-3>", self.afficher_menu_contextuel)
        self.tableau.bind("<Double-1>", self.afficher_details_selection)

        # Frame statistiques
        self.frame_stats = ctk.CTkFrame(self.main_frame, height=100, fg_color=self.blue_ciel)
        self.frame_stats.pack(fill="x", side="bottom")

        # Charger les données initiales
        self.actualiser_donnees()

    def rechercher(self):
        terme = self.recherche.get().lower()
        statut = self.statut_var.get()
        
        # Effacer le tableau actuel
        for item in self.tableau.get_children():
            self.tableau.delete(item)

        try:
            # Construire la requête SQL avec les filtres
            query = """
            SELECT c.id_colis, c.date_livrs,
                   CASE 
                       WHEN s.nom_societ IS NOT NULL THEN s.nom_societ
                       WHEN i.nm_individu IS NOT NULL THEN i.nm_individu || ' ' || i.pr_individu
                       ELSE u.username
                   END as expediteur,
                   d.nm_dest || ' ' || d.prn_dest as destinataire,
                   CASE c.etatlivrs 
                       WHEN 0 THEN 'En attente'
                       WHEN 1 THEN 'En transit'
                       WHEN 2 THEN 'Livré'
                   END as statut,
                   
                   c.facture
            FROM colis c
            LEFT JOIN user u ON c.id_user = u.id_user
            LEFT JOIN societé s ON u.ice_societ = s.ice_societ
            LEFT JOIN individu i ON u.cin_individu = i.cin_individu
            LEFT JOIN destinataire d ON c.id_dest = d.id_dest
            WHERE 1=1
            """
            params = []
            
            if statut != "Tous les statuts":
                query += " AND c.etatlivrs = ?"
                params.append({'En attente': 0, 'En transit': 1, 'Livré': 2}[statut])
            
            if terme:
                query += """ AND (
                    c.id_colis LIKE ? OR 
                    u.username LIKE ? OR 
                    d.nm_dest LIKE ? OR 
                    d.addr_dest LIKE ?
                )"""
                terme_search = f"%{terme}%"
                params.extend([terme_search] * 4)
            
            self.cursor.execute(query, params)
            resultats = self.cursor.fetchall()
            
            for colis in resultats:
                self.tableau.insert('', 'end', values=colis[:-1])
                
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {str(e)}")

    def actualiser_donnees(self):
        # Effacer le tableau actuel
        for item in self.tableau.get_children():
            self.tableau.delete(item)

        try:
            from userclass import user_idg
            # Requête SQL pour récupérer les colis avec les informations associées
            query = """
            SELECT c.id_colis, c.date_livrs,
                   CASE 
                       WHEN s.nom_societ IS NOT NULL THEN s.nom_societ
                       WHEN i.nm_individu IS NOT NULL THEN i.nm_individu || ' ' || i.pr_individu
                       ELSE u.username
                   END as expediteur,
                   d.nm_dest || ' ' || d.prn_dest as destinataire,
                   CASE c.etatlivrs 
                       WHEN 0 THEN 'En attente'
                       WHEN 1 THEN 'En transit'
                       WHEN 2 THEN 'Livré'
                   END as statut,
                   d.addr_dest as lieu_actuel,
                   c.facture
            FROM colis c
            LEFT JOIN user u ON c.id_user = u.id_user
            LEFT JOIN societé s ON u.ice_societ = s.ice_societ
            LEFT JOIN individu i ON u.cin_individu = i.cin_individu
            LEFT JOIN destinataire d ON c.id_dest = d.id_dest
            WHERE c.id_user = ?
            ORDER BY c.date_livrs DESC
            """
            self.cursor.execute(query, (user_idg,))
            resultats = self.cursor.fetchall()

            # Insérer les données dans le tableau
            for colis in resultats:
                self.tableau.insert('', 'end', values=colis[:-1])  # Exclure la facture de l'affichage

            self.actualiser_statistiques()

        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des données : {str(e)}")

    def actualiser_statistiques(self):
        try:
            from userclass import user_idg
            # Requête pour obtenir les statistiques
            query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN etatlivrs = 1 THEN 1 ELSE 0 END) as en_transit,
                SUM(CASE WHEN etatlivrs = 2 THEN 1 ELSE 0 END) as livres,
                SUM(CASE WHEN etatlivrs = 0 THEN 1 ELSE 0 END) as en_attente
            FROM colis
            WHERE id_user = ?
            """
            self.cursor.execute(query, (user_idg,))
            stats = self.cursor.fetchone()

            # Configuration des statistiques
            stats_config = [
                {
                    "titre": "Total des colis",
                    "valeur": str(stats[0]),
                    "icone": "📦",
                    "couleur": "#FF7F32"
                },
                {
                    "titre": "En transit",
                    "valeur": str(stats[1]),
                    "icone": "🚚",
                    "couleur": "#4CAF50"
                },
                {
                    "titre": "Livrés",
                    "valeur": str(stats[2]),
                    "icone": "✅",
                    "couleur": "#2196F3"
                },
                {
                    "titre": "En attente",
                    "valeur": str(stats[3]),
                    "icone": "⏳",
                    "couleur": "#FFC107"
                }
            ]

            # Supprimer les anciens widgets
            for widget in self.frame_stats.winfo_children():
                widget.destroy()

            # Créer les cartes de statistiques
            for i, stat in enumerate(stats_config):
                # Frame pour chaque carte
                carte = ctk.CTkFrame(
                    self.frame_stats,
                    width=250,
                    height=80,
                    fg_color="white",
                    corner_radius=10
                )
                carte.pack(side="left", padx=20, pady=10)
                carte.pack_propagate(False)

                # Frame pour l'icône
                icon_frame = ctk.CTkFrame(
                    carte,
                    width=50,
                    height=50,
                    fg_color=stat["couleur"],
                    corner_radius=25
                )
                icon_frame.place(x=20, y=15)

                # Icône
                ctk.CTkLabel(
                    icon_frame,
                    text=stat["icone"],
                    font=("Helvetica", 20),
                    text_color="white"
                ).place(relx=0.5, rely=0.5, anchor="center")

                # Titre
                ctk.CTkLabel(
                    carte,
                    text=stat["titre"],
                    font=("Helvetica", 14),
                    text_color="gray"
                ).place(x=80, y=10)

                # Valeur
                ctk.CTkLabel(
                    carte,
                    text=stat["valeur"],
                    font=("Helvetica", 25, "bold"),
                    text_color=stat["couleur"]
                ).place(x=80, y=35)

        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des statistiques : {str(e)}")

    def revenir_page(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def exporter_csv(self):
        try:
            import os
            from datetime import datetime
            
            # Créer un nom de fichier avec la date et l'heure
            nom_fichier = f"historique_colis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            chemin_fichier = os.path.abspath(nom_fichier)
            
            # Export en CSV
            with open(chemin_fichier, 'w', newline='', encoding='utf-8-sig') as fichier:
                writer = csv.writer(fichier, delimiter=';')
                
                # En-têtes
                colonnes = ['Numéro', 'Date', 'Expéditeur', 'Destinataire', 'Statut', 'Lieu actuel']
                writer.writerow(colonnes)
                
                # Données
                for item in self.tableau.get_children():
                    writer.writerow(self.tableau.item(item)["values"])

            messagebox.showinfo("Succès", f"Export CSV réussi!\nFichier: {nom_fichier}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")

    def afficher_menu_contextuel(self, event):
        item = self.tableau.identify_row(event.y)
        if item:
            self.tableau.selection_set(item)
            menu = ctk.CTkMenu(self)
            menu.add_command(label="Voir détails", command=self.afficher_details_selection)
            menu.add_command(label="Modifier statut", command=self.modifier_statut)
            menu.add_separator()
            menu.add_command(label="Supprimer", command=self.supprimer_selection)
            menu.post(event.x_root, event.y_root)

    def afficher_details_selection(self, event=None):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un colis")
            return

        item = selection[0]
        valeurs = self.tableau.item(item)['values']
        
        # Création d'une fenêtre personnalisée pour les détails
        fenetre_details = ctk.CTkToplevel(self)
        fenetre_details.title(f"Détails du colis {valeurs[0]}")
        fenetre_details.geometry("400x700")
        
        # Frame principale
        frame_details = ctk.CTkFrame(fenetre_details)
        frame_details.pack(fill="both", expand=True, padx=20, pady=20)

        # Style des labels
        style_titre = ("Helvetica", 14, "bold")
        style_contenu = ("Helvetica", 12)

        # Informations du colis
        ctk.CTkLabel(frame_details, text="Numéro:", font=style_titre).pack(anchor="w", pady=(10,0))
        ctk.CTkLabel(frame_details, text=valeurs[0], font=style_contenu).pack(anchor="w")

        ctk.CTkLabel(frame_details, text="Date:", font=style_titre).pack(anchor="w", pady=(10,0))
        ctk.CTkLabel(frame_details, text=valeurs[1], font=style_contenu).pack(anchor="w")

        ctk.CTkLabel(frame_details, text="Expéditeur:", font=style_titre).pack(anchor="w", pady=(10,0))
        ctk.CTkLabel(frame_details, text=valeurs[2], font=style_contenu).pack(anchor="w")

        ctk.CTkLabel(frame_details, text="Destinataire:", font=style_titre).pack(anchor="w", pady=(10,0))
        ctk.CTkLabel(frame_details, text=valeurs[3], font=style_contenu).pack(anchor="w")

        # État avec couleur
        ctk.CTkLabel(frame_details, text="État:", font=style_titre).pack(anchor="w", pady=(10,0))
        
        # Couleurs pour les différents états
        couleurs_etats = {
            "En transit": "#FFA500",  # Orange
            "Livré": "#4CAF50",      # Vert
            "En attente": "#FF4444"   # Rouge
        }
        
        # Frame pour l'état avec couleur de fond
        frame_etat = ctk.CTkFrame(frame_details, fg_color=couleurs_etats.get(valeurs[4], "#808080"))
        frame_etat.pack(anchor="w", pady=5)
        ctk.CTkLabel(
            frame_etat, 
            text=valeurs[4],
            text_color="white",
            font=style_contenu
        ).pack(padx=10, pady=5)

        ctk.CTkLabel(frame_details, text="Lieu actuel:", font=style_titre).pack(anchor="w", pady=(10,0))
        ctk.CTkLabel(frame_details, text=valeurs[5], font=style_contenu).pack(anchor="w")

        # Bouton de téléchargement de facture
        bouton_facture = ctk.CTkButton(
            frame_details,
            text="📄 Télécharger la facture",
            command=lambda: self.telecharger_facture(valeurs[0]),
            fg_color=self.orange,
            hover_color="#FFB84D",
            height=40,
            font=("Helvetica", 12, "bold")
        )
        bouton_facture.pack(pady=20)

        # Bouton fermer
        ctk.CTkButton(
            frame_details,
            text="Fermer",
            command=fenetre_details.destroy,
            fg_color="#FF4444",
            hover_color="#FF6666",
            height=40,
            font=("Helvetica", 12, "bold")
        ).pack(pady=10)

   

        
    def trier_tableau(self, colonne):
        donnees = []
        for item in self.tableau.get_children():
            valeurs = self.tableau.item(item)['values']
            donnees.append(valeurs)

        colonne_index = list(self.tableau['columns']).index(colonne)
        donnees.sort(key=lambda x: x[colonne_index], reverse=hasattr(self, 'dernier_tri') and self.dernier_tri == colonne)
        self.dernier_tri = colonne if not hasattr(self, 'dernier_tri') or self.dernier_tri != colonne else None

        for item in self.tableau.get_children():
            self.tableau.delete(item)
        for item in donnees:
            self.tableau.insert('', 'end', values=item)

    def telecharger_facture(self, id_colis):
        try:
            # Récupérer la facture de la base de données
            query = "SELECT facture FROM colis WHERE id_colis = ?"
            self.cursor.execute(query, (id_colis,))
            facture = self.cursor.fetchone()

            if facture and facture[0]:
                # Demander à l'utilisateur où sauvegarder le fichier
                fichier = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=f"facture_colis_{id_colis}.pdf"
                )
                
                if fichier:
                    with open(fichier, 'wb') as f:
                        f.write(facture[0])
                    messagebox.showinfo("Succès", "Facture téléchargée avec succès!")
            else:
                messagebox.showwarning("Attention", "Aucune facture disponible pour ce colis")

        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors du téléchargement de la facture : {str(e)}")

    def __del__(self):
        # Fermer la connexion à la base de données
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    app = ctk.CTk()  
    login_page = HistoriqueColis(app, app)
    login_page.pack(fill="both", expand=True)
    app.mainloop()
