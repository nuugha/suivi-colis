import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import customtkinter as ctk

# Couleurs
orange = "#FF7F32"  # Couleur orange
blue_ciel = "#87CEFA"  # Bleu ciel
bg_color = "#f5f5f5"  # Fond gris clair

class Security(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")

        # Frame supérieure
        self.create_top_frame()
        # Menu Frame
        self.menu_frame = tk.Frame(self, bg=blue_ciel, height=40)
        self.menu_frame.pack(fill="x", side="bottom")
        image1 = Image.open("sec.jpg")

        # Resize the image to desired dimensions (e.g., 110x110)
        new_width = 140
        new_height = 140
        resized_image = image1.resize((new_width, new_height), Image.Resampling.LANCZOS)

   # Convert the resized image for Tkinter
        self.photo = ImageTk.PhotoImage(resized_image)

   # Display the image in a Label widgetblack
        label_image = tk.Label(self, image=self.photo)
        label_image.pack(pady=20)
        self.framerect = ctk.CTkFrame(self, width=450, height=200,corner_radius=40, fg_color="white", border_width=2)
        self.framerect.pack_propagate(False) 
        self.framerect.pack(padx=20,pady=15)
        info = ctk.CTkButton(
            self.framerect,
            text="🔑  Changer le mot de passe",
            font=("Arial", 15, "bold"),
            corner_radius=0,
            width=390,
            height=60,
            fg_color="white",
            text_color="black",
            hover_color="#f5f5f5",
            anchor="w",
            command=self.gomodifmdps)
           
        info.pack(pady=30)
        sec = ctk.CTkButton(
            self.framerect,
            text="🗑️Supprimer votre compte",
            font=("Arial", 15, "bold"),
            corner_radius=0,
            width=390,
            height=60,
            fg_color="white",
            text_color="red",
            hover_color="#f5f5f5",
            anchor="w",
            command=self.gosup)
           
        sec.pack(pady=0)
       

        
        

        # Créer les boutons du menu
        home_icon = ctk.CTkButton(
            self.menu_frame,
            text="🏠",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            state="normal",
        )

        gps_icon = ctk.CTkButton(
            self.menu_frame,
            text="🧭",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            state="normal",
            command=self.gomap
        )

        compte_icon = ctk.CTkButton(
            self.menu_frame,
            text="👤",
            font=("Arial", 35, "bold"),
            corner_radius=15,
            width=200,
            height=60,
            fg_color="#87CEFA",
            hover_color="#70B9F2",
            state="normal",
            command=self.alleracc
        )

        # Add buttons to the grid
        home_icon.grid(row=0, column=0, padx=10, pady=5)
        gps_icon.grid(row=0, column=1, padx=10, pady=5)
        compte_icon.grid(row=0, column=2, padx=10, pady=5)

        # Configure column weights for resizing
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_columnconfigure(2, weight=1)

        

       

       

    def create_top_frame(self):
        """Crée la frame supérieure avec le titre de l'application."""
        top_frame = tk.Frame(self, height=50, bg=blue_ciel)
        top_frame.pack(fill="x", side="top")
        app_name = tk.Label(top_frame, text="Sécurité", font=("Arial", 35, "bold"), fg="#FF7F32", bg=blue_ciel)
        app_name.place(relx=0.5, rely=0.5, anchor="center")
        self.back_button = ctk.CTkButton(self, text="◁ Retour", command=self.revenir_page_precedente,
                                        font=("Helvetica", 14, "bold"), corner_radius=0, fg_color= "#87CEFA",
                                        text_color="white", hover_color= "#87CEFA")
        self.back_button.place(x=0, y=0)
    def revenir_page_precedente(self):
        from account import Account
        self.controller.show_frame("Account")
    def alleracc(self):
        from acc import TrackingApp
        self.controller.show_frame("TrackingApp")
    def gomodifmdps(self):
        from modifmdps import ModifMdps
        self.controller.show_frame("ModifMdps")
    def gosup(self):
        from supprimer import Suppcmpt
        self.controller.show_frame("Suppcmpt")
    def gomap(self):
        from GPSsuiviecolis import SuiviColis
        self.controller.show_frame("SuiviColis")
    
        
    

        

    

    




        
        
       
        
        

# Lancer l'application
if __name__ == "__main__":
    app = ctk.CTk()  # Utilise CTk pour une application avec des widgets modernes
    app.geometry("800x600")
    tracking_app = Security(app, app)
    tracking_app.pack(fill="both", expand=True)
    app.mainloop()
