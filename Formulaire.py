import tkinter as tk
from tkinter import messagebox
from tkcalendar import *
from cryptography.fernet import Fernet
import os
import pymysql


root = tk.Tk()
root.title("login")
root.configure(bg='#333333')

#Création des champs
##title = tk.Label(root, text="Formulaire d'Enregistrements")

#Label et champ pour s'enregistrer
label_nom = tk.Label(root, text="Nom :", bg="#333333", fg="white")
label_nom.pack(pady=5)
entry_nom = tk.Entry(root)
entry_nom.pack(pady=5)

label_prenom = tk.Label(root, text="Prenom :", bg="#333333", fg="white")
label_prenom.pack(pady=5)
entry_prenom = tk.Entry(root)
entry_prenom.pack(pady=5)

label_email = tk.Label(root, text="Adresse mail :", bg="#333333", fg="white")
label_email.pack(pady=5)
entry_email = tk.Entry(root)
entry_email.pack(pady=5)

label_telephone = tk.Label(root, text="Numéro de téléphone :", bg="#333333", fg="white")
label_telephone.pack(pady=5)
entry_telephone = tk.Entry(root)
entry_telephone.pack(pady=5)

label_date_naiss = tk.Label(root, text="date de naissance :", bg="#333333", fg="white")
label_date_naiss.pack(pady=5)
entry_date_naiss = DateEntry(root, state="readonly")
entry_date_naiss.pack(pady=5)

def formulaire_donnees():
    try:
        connect=pymysql.connect(host="localhost", user="root", password="", database="formulaire")
        curseur=connect.cursor()
        
        #sauvegarde dans la base de données
        curseur.execute("select * from login where email=%s", entry_email.get())
        row=curseur.fetchone()

        if row != None:
            
            messagebox.showerror("Erreur", "Ce mail existe dejà. Veuillez essayer une autre adresse mail", parent=root)
        else:
            curseur.execute("insert into login(Nom, Prenom, email, telephone, date) values(%s,%s,%s,%s,%s)",
                          (entry_nom.get(), 
                          entry_prenom.get(),
                          entry_email.get(),
                          entry_telephone.get(),
                          entry_date_naiss.get()
            ))
            connect.commit()
            connect.close()
            messagebox.showinfo("Success", "Ajout effectué", parent=root)


    except Exception as es:
        messagebox.showerror("Erreur", f"Erreur de connexion : {str(es)}", parent=root) 


# Bouton pour enregistrer le formulaire
button_save = tk.Button(root, text="Enregistrer", bg="#990099", fg="white", command=formulaire_donnees)
button_save.pack(pady=20)


root.mainloop()