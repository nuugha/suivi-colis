from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import os
import sqlite3
import io
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
import traceback     

class Paiement(ctk.CTkFrame):
    def __init__(self, parent, controller, colis_data):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")
        
        # Récupérer les informations de l'expéditeur depuis la base de données
        try:
            with sqlite3.connect('suivi_coli.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.*, 
                        CASE 
                            WHEN i.cin_individu IS NOT NULL THEN i.nm_individu 
                            WHEN s.ice_societ IS NOT NULL THEN s.nom_societ
                        END as nom,
                        CASE 
                            WHEN i.cin_individu IS NOT NULL THEN i.pr_individu
                            ELSE ''
                        END as prenom,
                        CASE
                            WHEN i.cin_individu IS NOT NULL THEN i.adr_individu
                            WHEN s.ice_societ IS NOT NULL THEN s.adr_societ
                        END as adresse,
                        CASE
                            WHEN i.cin_individu IS NOT NULL THEN i.email_individu
                            WHEN s.ice_societ IS NOT NULL THEN s.email_societ
                        END as email,
                        CASE
                            WHEN i.cin_individu IS NOT NULL THEN i.numTel_individu
                            WHEN s.ice_societ IS NOT NULL THEN s.num_telsoc
                        END as telephone
                    FROM user u
                    LEFT JOIN individu i ON u.cin_individu = i.cin_individu
                    LEFT JOIN societé s ON u.ice_societ = s.ice_societ
                    WHERE u.id_user = ?
                """, (colis_data['id_user'],))
                exp_data = cursor.fetchone()
                print(exp_data)

                if exp_data:
                    # Extraire les données du colis et de l'expéditeur depuis le dictionnaire
                    self.colis_data = {
                        'id_exp': colis_data['id_exp'],
                        'ville_exp': colis_data['ville_exp'],
                        'ville_dest': colis_data['ville_dest'],
                        'id_dest': colis_data['id_dest'],
                        'nom_dest': colis_data['nom_dest'],
                        'prn_dest': colis_data['prn_dest'],
                        'addr_dest': colis_data['addr_dest'], 
                        'num_dest': colis_data['num_dest'],
                        'email_dest': colis_data['email_dest'],
                        'poids': float(colis_data['poids']),
                        'dimension': colis_data['dimension'],
                        'description': colis_data['description'],
                        'id_user': colis_data['id_user'],
                        # Ajout des informations de l'expéditeur
                        'nom_exp': exp_data[5] if exp_data[5] else '',  # nom 
                        'prenom_exp': exp_data[6] if exp_data[6] else '',  # prenom
                        'adresse_exp': exp_data[7] if exp_data[7] else '',  # adresse
                        'email_exp': exp_data[8] if exp_data[8] else '',  # email
                        'telephone_exp': exp_data[9] if exp_data[9] else ''  # telephone
                    }
                else:
                    messagebox.showerror("Erreur", "Impossible de trouver les informations de l'expéditeur")
                    return
                
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", f"Une erreur est survenue: {str(e)}")
            return
        

        # Coordonnées des villes marocaines
        self.coords_villes = {
            
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
        

        # Tarifs
        self.prix_base = 50  # Prix de base en DH
        self.prix_par_kg = 5  # Prix par kg en DH
        self.prix_par_km = 0.5  # Prix par km en DH

        # Couleurs
        self.orange = "#FF7F32"
        self.blue_ciel = "#87CEFA"

        self.creer_en_tete()
        self.creer_corps()
        self.afficher_details()

    def creer_en_tete(self):
        self.frame_sup = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=self.blue_ciel)
        self.frame_sup.pack(fill="x", side="top")

        self.bouton_retour = ctk.CTkButton(
            self.frame_sup,
            text="◁ Retour",
            command=self.retour_page,
            font=("Helvetica", 14, "bold"),
            fg_color=self.blue_ciel,
            text_color="white",
            hover_color="#FFB84D"
        )
        self.bouton_retour.pack(side="left", padx=10, pady=10)

        self.label_titre = ctk.CTkLabel(
            self.frame_sup,
            text="Facture et Paiement",
            font=("Helvetica", 44, "bold"),
            text_color="#FFA500"
        )
        self.label_titre.pack(pady=(10, 20))

    def creer_corps(self):
        self.frame_principal = ctk.CTkScrollableFrame(self, fg_color="white")
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Création d'une frame principale pour les informations
        self.frame_info = ctk.CTkFrame(self.frame_principal, fg_color="#F0F8FF")
        self.frame_info.pack(fill="x", pady=10, padx=10)

        # Frame gauche pour expéditeur et colis
        self.frame_gauche = ctk.CTkFrame(self.frame_info, fg_color="transparent")
        self.frame_gauche.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame droite pour destinataire et articles
        self.frame_droite = ctk.CTkFrame(self.frame_info, fg_color="transparent")
        self.frame_droite.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Détails expéditeur
        self.frame_expediteur = self.creer_cadre_titre(self.frame_gauche, "Détails de l'expéditeur")
        self.label_exp = ctk.CTkLabel(
            self.frame_expediteur, 
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_exp.pack(pady=5, padx=10, anchor="w")

        # Détails colis
        self.frame_colis = self.creer_cadre_titre(self.frame_gauche, "Détails du colis")
        self.label_colis = ctk.CTkLabel(
            self.frame_colis,
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_colis.pack(pady=5, padx=10, anchor="w")

        # Détails destinataire
        self.frame_destinataire = self.creer_cadre_titre(self.frame_droite, "Détails du destinataire")
        self.label_dest = ctk.CTkLabel(
            self.frame_destinataire,
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_dest.pack(pady=5, padx=10, anchor="w")

        # Articles
        self.frame_articles = self.creer_cadre_titre(self.frame_droite, "Articles")
        self.label_articles = ctk.CTkLabel(
            self.frame_articles,
            text="",
            justify="left",
            font=("Helvetica", 12)
        )
        self.label_articles.pack(pady=5, padx=10, anchor="w")

        # Frame pour les frais (en bas)
        self.frame_bas = ctk.CTkFrame(self.frame_principal, fg_color="#F0F8FF")
        self.frame_bas.pack(fill="x", pady=(20,10), padx=10)

        # Calcul des frais
        self.frame_frais = self.creer_cadre_titre(self.frame_bas, "Détails des frais")
        self.label_frais = ctk.CTkLabel(
            self.frame_frais,
            text="",
            justify="left",
            font=("Helvetica", 14, "bold")
        )
        self.label_frais.pack(pady=10, padx=10, anchor="w")

        # Boutons
        self.frame_boutons = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_boutons.pack(fill="x", pady=20)

        self.bouton_payer = ctk.CTkButton(
            self.frame_boutons,
            text="Générer La Facture",
            command=self.payer_et_generer_facture,
            font=("Helvetica", 20, "bold"),
            fg_color=self.orange,
            hover_color="green",
            height=50
        )
        self.bouton_payer.pack(side="right", padx=20)

    def calculer_distance(self, ville1, ville2):
        if ville1 in self.coords_villes and ville2 in self.coords_villes:
            lat1, lon1 = self.coords_villes[ville1]
            lat2, lon2 = self.coords_villes[ville2]
            
            R = 6371  # Rayon de la Terre en km
            
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            
            return round(distance, 2)
        return 0

    def calculer_prix(self):
        poids = self.colis_data["poids"]
        distance = self.calculer_distance(
            self.colis_data["ville_exp"],
            self.colis_data["ville_dest"]
        )
        
        prix_poids = poids * self.prix_par_kg
        prix_distance = distance * self.prix_par_km
        total = self.prix_base + prix_poids + prix_distance
        
        return {
            "prix_base": self.prix_base,
            "prix_poids": round(prix_poids, 2),
            "prix_distance": round(prix_distance, 2),
            "total": round(total, 2),
            "distance": distance
        }

    def afficher_details(self):
        try:
            # Afficher détails expéditeur
            nom_complet = f"{self.colis_data['nom_exp']} {self.colis_data['prenom_exp']}" if self.colis_data['prenom_exp'] else self.colis_data['nom_exp']
            self.label_exp.configure(text=(
                f"Nom: {nom_complet}\n"
                f"Adresse: {self.colis_data['adresse_exp']}\n"
                f"Téléphone: {self.colis_data['telephone_exp']}\n"
                f"Email: {self.colis_data['email_exp']}\n"
                f"Ville: {self.colis_data['ville_exp']}"
            ))

            # Afficher détails destinataire
            self.label_dest.configure(text=(
                f"Nom: {self.colis_data['nom_dest']}\n"
                f"Prenom: {self.colis_data['prn_dest']}\n"
                f"Adresse: {self.colis_data['addr_dest']}\n"
                f"Téléphone: {self.colis_data['num_dest']}\n"
                f"Email: {self.colis_data['email_dest']}\n"
                f"Ville: {self.colis_data['ville_dest']}"
            ))

            # Afficher détails colis
            self.label_colis.configure(text=(
                f"Poids: {self.colis_data['poids']} kg\n"
                f"Dimensions: {self.colis_data['dimension']}"
            ))

            # Afficher articles
            articles_text = "Articles inclus:\n"
            articles_text += f"- {self.colis_data['description']}"
            self.label_articles.configure(text=articles_text)

            # Calculer et afficher les frais
            tarifs = self.calculer_prix()
            self.label_frais.configure(text=(
                f"Prix de base: {tarifs['prix_base']} DH\n"
                f"Frais de poids ({self.prix_par_kg} DH/kg × {self.colis_data['poids']} kg): {tarifs['prix_poids']} DH\n"
                f"Distance: {tarifs['distance']} km\n"
                f"Frais de distance ({self.prix_par_km} DH/km): {tarifs['prix_distance']} DH\n"
                f"Total: {tarifs['total']} DH"
            ))
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue est survenue: {str(e)}")

    def generer_facture(self):
        now = datetime.now()
        nom_fichier = f"facture_speedy_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)

        try:
            # Ajouter le logo et nom de l'entreprise
            try:
                logo_path = "logo.ico"
                c.drawImage(logo_path, 40, 750, width=100, height=80, preserveAspectRatio=True)
            except Exception as e:
                messagebox.showwarning("Attention", f"Impossible de charger le logo: {str(e)}")
                c.rect(40, 750, 100, 80, stroke=1, fill=0)
            
            # Nom de l'entreprise
            c.setFont("Helvetica-Bold", 24)
            c.drawString(150, 780, "SPEEDY EXPRESS")
            c.setFont("Helvetica", 12)
            c.drawString(150, 760, "Service de livraison rapide")
            
            # En-tête
            c.setFont("Helvetica-Bold", 24)
            c.drawString(200, 700, "FACTURE")
            
            # Date et numéro de facture
            c.setFont("Helvetica", 12)
            c.drawString(400, 670, f"Date: {now.strftime('%d/%m/%Y')}")
            c.drawString(400, 650, f"N° Facture: {now.strftime('%Y%m%d%H%M')}")
            
            # Informations expéditeur et destinataire
            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, 620, "Expéditeur:")
            c.drawString(300, 620, "Destinataire:")
            
            c.setFont("Helvetica", 12)
            # Expéditeur
            exp_info = self.label_exp.cget('text').split('\n')
            y = 600
            for line in exp_info:
                c.drawString(40, y, line)
                y -= 20
                
            # Destinataire    
            y = 600
            dest_info = [
                f"Nom: {self.colis_data['nom_dest']}",
                f"Prenom: {self.colis_data['prn_dest']}",
                
                f"Adresse: {self.colis_data['addr_dest']}",
                f"Téléphone: {self.colis_data['num_dest']}",
                f"Email: {self.colis_data['email_dest']}",
                f"Ville: {self.colis_data['ville_dest']}"
            ]
            for line in dest_info:
                c.drawString(300, y, line)
                y -= 20

            # Table des articles
            data = [
                ['Description', 'Poids', 'Dimensions'],
                [self.colis_data['description'], f"{self.colis_data['poids']} kg", self.colis_data['dimension']]
            ]
            
            table = Table(data, colWidths=[250, 100, 150])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            table.wrapOn(c, 40, 400)
            table.drawOn(c, 40, 400)
            
            # Table des calculs
            tarifs = self.calculer_prix()
            calc_data = [
                ['Description', 'Détail', 'Montant (DH)'],
                ['Prix de base', '-', f"{tarifs['prix_base']}"],
                ['Frais de poids', f"{self.prix_par_kg} DH/kg × {self.colis_data['poids']} kg", f"{tarifs['prix_poids']}"],
                ['Frais de distance', f"{tarifs['distance']} km × {self.prix_par_km} DH/km", f"{tarifs['prix_distance']}"],
                ['Total', '', f"{tarifs['total']}"]
            ]
            
            calc_table = Table(calc_data, colWidths=[150, 200, 150])
            calc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
            ]))
            calc_table.wrapOn(c, 40, 200)
            calc_table.drawOn(c, 40, 200)
            
            # Pied de page
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(40, 50, "Merci de votre confiance!")
            
            c.save()
            pdf_content = pdf_buffer.getvalue()
            
  

            with sqlite3.connect('suivi_coli.db') as conn:
                cursor = conn.cursor()
            
            # Insérer d'abord le destinataire
                cursor.execute("""
                INSERT INTO destinataire (
                    id_dest, nm_dest, prn_dest, addr_dest, 
                    email_dest, num_dest, ville
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.colis_data['id_dest'],  
                self.colis_data['nom_dest'],
                self.colis_data['prn_dest'],
                self.colis_data['addr_dest'],
                self.colis_data['email_dest'],
                self.colis_data['num_dest'],
                self.colis_data['ville_dest']
            ))
            
                dest_id = cursor.lastrowid
                tarifs = self.calculer_prix()
            
            # Obtenir les coordonnées des villes
                ville_exp = self.coords_villes[self.colis_data['ville_exp']]
                ville_dest = self.coords_villes[self.colis_data['ville_dest']]
            
            # Insérer le colis
                cursor.execute("""
                INSERT INTO colis (
                    poids, dimension, dist, date_livrs, 
                    id_user, id_dest, prix, facture,
                    x, y,
                    
                    etatlivrs,posit_desti_lat,posit_desti_lon
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
            """, (
                self.colis_data['poids'],
                self.colis_data['dimension'],
                tarifs["distance"],
                datetime.now().strftime('%Y-%m-%d'),
                self.colis_data['id_user'],
                self.colis_data['id_dest'],
                tarifs["total"],
                pdf_content,
                ville_exp[0],  # latitude départ
                ville_exp[1],  # longitude départ
                0,
                ville_dest[0],
                ville_dest[1]
                ))
                print((
                self.colis_data['poids'],
                self.colis_data['dimension'],
                tarifs["distance"],
                datetime.now().strftime('%Y-%m-%d'),
                self.colis_data['id_user'],
                dest_id,
                tarifs["total"],
                
                ville_exp[0],  # latitude départ
                ville_exp[1],  # longitude départ
                0,
                ville_dest[0],
                ville_dest[1]
                ))
                conn.commit()
        
            return nom_fichier
        
        except sqlite3.Error as e:
            full_traceback = traceback.format_exc()  # Obtenir la trace complète
            raise Exception(f"Erreur de base de données:\n{full_traceback}")
        except Exception as e:
            full_traceback = traceback.format_exc()  # Obtenir la trace complète
            raise Exception(f"Erreur lors de la génération de la facture:\n{full_traceback}")
        finally:
            pdf_buffer.close()

    def payer_et_generer_facture(self):
        try:
            confirmation = messagebox.askyesno(
                "Confirmation",
                "Voulez-vous vraiment générer la facture et enregistrer le colis?"
            )
            if confirmation:
                nom_fichier = self.generer_facture()
                messagebox.showinfo(
                    "Succès", 
                    f"Paiement effectué avec succès!\n"
                    f"La facture a été générée et enregistrée dans la base de données"
                )
                self.retour_page()
            
        except Exception as e:
            messagebox.showerror(
                "Erreur", 
                f"Une erreur est survenue lors de la génération de la facture:\n{str(e)}"
            )

    def retour_page(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")

    def creer_cadre_titre(self, parent, titre):
        frame = ctk.CTkFrame(parent, fg_color=self.blue_ciel)
        frame.pack(fill="x", padx=20, pady=10)
        
        label_titre = ctk.CTkLabel(
            frame, 
            text=titre, 
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        label_titre.pack(anchor="w", padx=5, pady=5)
        
        return frame

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x900")
    app.title("Speedy - Page de paiement")
    
    # Test data
    test_data = {
        'id_exp': 1,
        'ville_exp': 'Casablanca',
        'ville_dest': 'Rabat',
        'id_dest': 1,
        'nom_dest': 'Test Destinataire',
        'prn_dest': 'test_prenom',
        'addr_dest': 'Test Address',
        'num_dest': '0600000000',
        'email_dest': 'test@test.com',
        'poids': 5.0,
        'dimension': '30x40x50',
        'description': 'Test package',
        'id_user': 1
    }
    
    paiement_page = Paiement(app, app, test_data)
    paiement_page.pack(fill="both", expand=True)
    app.mainloop()
