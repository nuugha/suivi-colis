import tkinter as tk
from login2 import LoginPage
import customtkinter as ctk
from creeuncpt import Choixcmpt
from createtrp import CreatEntr
from createuser import CreatUser
from mdpsoublier import Mdps
from acc import TrackingApp
from account import Account
from security import Security
from modifmdps import ModifMdps
from procurationamis import Procami

from modifinfo import Modifinf
from demenagementsfinal2 import Demanagement
from creecoli import Colis
from GPSsuiviecolis2 import SuiviColis

from supprimer import Suppcmpt

import userclass 
from tkinter import messagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Application SPEEDY")
        self.configure(fg_color="white")# Fond blanc
        self.iconbitmap('logo.ico')
        
        # Conteneur pour les pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        
        # Création des pages
        self.frames = {}
        for F in (LoginPage, Choixcmpt,CreatEntr,CreatUser,Mdps,TrackingApp,Account,Security,ModifMdps,Procami,Modifinf,Suppcmpt,Demanagement,Colis,SuiviColis):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Affiche la page de connexion par défaut
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    def show_frame_notif(self):
        try:
            from userclass import user_idg
            if user_idg is not None:  # Vérification explicite
                # Créer une nouvelle instance
                from notification import notif
                frame = notif(parent=self.container, controller=self,)
                self.frames["notif"] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                frame.tkraise()
                
                print(f"Page notification créée pour l'utilisateur {user_idg}")
                
            else:
                print("Utilisateur non connecté")
                messagebox.showwarning("Attention", "Veuillez vous connecter d'abord")
                self.show_frame("LoginPage")  # Redirection vers la page de connexion
                return
                
        except ImportError as ie:
            print(f"Erreur d'importation: {ie}")
            messagebox.showerror("Erreur", "Module notification non disponible")
            return
            
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            messagebox.showerror("Erreur", "Impossible d'afficher les notifications")
            return
    def show_frame_colis(self):
        try:
            from userclass import user_idg
            if user_idg is not None:  # Vérification explicite
                # Créer une nouvelle instance
                from mescolis import HistoriqueColis
                frame = HistoriqueColis(parent=self.container, controller=self)
                self.frames["HistoriqueColis"] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                frame.tkraise()
                
                print(f"Page mes colis créée pour l'utilisateur {user_idg}")
                
            else:
                print("Utilisateur non connecté")
                messagebox.showwarning("Attention", "Veuillez vous connecter d'abord")
                self.show_frame("LoginPage")  # Redirection vers la page de connexion
                return
                
        except ImportError as ie:
            print(f"Erreur d'importation: {ie}")
            messagebox.showerror("Erreur", "Module notification non disponible")
            return
            
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            messagebox.showerror("Erreur", "Impossible d'afficher les notifications")
            return

    def show_frame_paiement(self, colis_data):
        try:
            from userclass import user_idg
            if user_idg is not None:
                
                from paiement import Paiement
                frame = Paiement(parent=self.container, controller=self, colis_data=colis_data)
                self.frames["Paiement"] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                frame.tkraise()
                
                print(f"Page paiement créée pour l'utilisateur {user_idg}")
                
            else:
                print("Utilisateur non connecté")
                messagebox.showwarning("Attention", "Veuillez vous connecter d'abord")
                self.show_frame("LoginPage")
                return
                
        except ImportError as ie:
            print(f"Erreur d'importation: {ie}")
            messagebox.showerror("Erreur", "Module paiement non disponible")
            return
            
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            messagebox.showerror("Erreur", "Impossible d'afficher la page de paiement")
            return
if __name__ == "__main__":
    app = App()
    app.mainloop()
