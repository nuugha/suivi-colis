import customtkinter as ctk
from tkinter import messagebox,Label,Frame,Canvas,Button
from PIL import Image, ImageTk






class Choixcmpt(ctk.CTkFrame):
 def __init__(self, parent, controller):
   super().__init__(parent)
   image_path2 = "entr.png"
   image_path = "usr.png"
   self.controller = controller
   self.configure(fg_color="white")
   from login2 import LoginPage
   background_image = Image.open('logo2.png')
   background_image = background_image.resize((1366, 708), Image.Resampling.LANCZOS)  # Utilisation de LANCZOS pour un redimensionnement de haute qualité
   background_photo = ImageTk.PhotoImage(background_image)
   

   def update_background(event):
         # Redimensionner l'image de fond à la taille actuelle de la fenêtre
           resized_image = background_image.resize((1366, 708), Image.Resampling.LANCZOS)
           background_photo = ImageTk.PhotoImage(resized_image)
    
         # Mettre à jour l'image dans le label
           background_label.configure(image=background_photo)
           background_label.image = background_photo  # Conserver une référence à l'image

     # Créer un label pour l'image de fond et l'afficher
   background_label = ctk.CTkLabel(self,text="",image=background_photo)
   background_label.place(relwidth=1, relheight=1)  # Occupe toute la fenêtre
     #Attacher la fonction de redimensionnement au changement de taille de la fenêtre
   self.bind("<Configure>", update_background)
   speedy_label = ctk.CTkLabel(
       self,
       text="Bienvenue sur\nSPEEDY",
       font=("Helvetica", 50, "bold"),
       text_color="#FFA500",
   )
   def revenir_page_precedente():
       controller.show_frame("LoginPage")
   image_retour = Image.open("retour.png")
    
   # Redimensionner l'image
   resized_image = image_retour.resize((40, 40), Image.Resampling.LANCZOS)
    
   # Convertir en format compatible avec tkinter
   RT_photo = ImageTk.PhotoImage(resized_image)
    
   # Création du bouton avec l'image redimensionnée
   bouton_retour = Button(
           self,
           image=RT_photo,
           command=revenir_page_precedente,
           relief="flat",  # Look moderne
           cursor="hand2"  # Changer le curseur au survol
       )
   bouton_retour.place(x=430, y=50)
    
   # Assurez-vous que l'image reste en mémoire en la liant à l'objet bouton
   bouton_retour.image = RT_photo
   speedy_label.pack(pady=(50, 30))
   etvlabel = ctk.CTkLabel(
       self,
       text="Etes-vous?",
       font=("Arial", 40, "bold"),
       text_color="#000000",
   )
   etvlabel.place(x=580,y=200)
   # Load and resize the image
     # Replace with your image path
   image1 = Image.open(image_path)

   # Resize the image to desired dimensions (e.g., 110x110)
   new_width = 110
   new_height = 110
   resized_image = image1.resize((new_width, new_height), Image.Resampling.LANCZOS)

   # Convert the resized image for Tkinter
   self.photo = ImageTk.PhotoImage(resized_image)

   # Display the image in a Label widget
   label_image = Label(self, image=self.photo)
   label_image.place(x=630, y=250)

   def gotouser():
      from createuser import CreatUser
      self.controller.show_frame("CreatUser")
   def gotoetrp():
       from createtrp import CreatEntr
       controller.show_frame("CreatEntr")
       
   ind_button = ctk.CTkButton(
       self, text="Individu", width=150, height=40, command=gotouser, fg_color="#FFA500",
       text_color="white",
       hover_color="#FFB84D",corner_radius=20,font=("Helvetica", 14, "bold")
   )
   ind_button.place(x=610,y=370)
   line = Label(self, text="____________________", font=("Arial", 12,"bold"), fg="black", bg="white")
   line.place(x=720,y=420)
   oulabel = ctk.CTkLabel(
       self,
       text="ou",
       font=("Arial", 40, "bold"),
       text_color="#000000",)
   oulabel.place(x=660,y=410)
   line = Label(self, text="____________________", font=("Arial", 12,"bold"), fg="black", bg="white")
   line.place(x=460,y=420)


   
   image2 = Image.open(image_path2)

   # Resize the image to desired dimensions (e.g., 110x110)
   new_width2 = 110
   new_height2 = 110
   resized_image2 = image2.resize((new_width2, new_height2), Image.Resampling.LANCZOS)

   # Convert the resized image for Tkinter
   self.photo2 = ImageTk.PhotoImage(resized_image2)

   # Display the image in a Label widget
   label_image2 = Label(self, image=self.photo2)
   label_image2.place(x=630, y=480)  # Set the position of the label
   ent_button = ctk.CTkButton(
       self, text="Entreprise", width=150, height=40, command=gotoetrp, fg_color="#FFA500",
       text_color="white",
       hover_color="#FFB84D",corner_radius=20,font=("Helvetica", 14, "bold")
   )
   ent_button.place(x=610,y=600)
















































