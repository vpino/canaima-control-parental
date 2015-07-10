#!/usr/bin/python
# encoding=utf8

import subprocess
import tkFont
from PIL import ImageTk, Image
from Tkinter import *
from tkMessageBox import *

def add():
	 try:

	 	if ( askokcancel(title="Control Parental", message=" ¿ Está seguro que desea bloquear (URL y/o Frase) ?") ) :
	 		urlA = txtUrl.get()
	 		fraseA = txtFrase.get()

	 		if urlA != '' or fraseA != '' :

	 			subprocess.Popen("echo %s >> /etc/dansguardian/lists/bannedsitelist" % urlA, shell=True)
	 			subprocess.Popen("echo %s >> /etc/dansguardian/lists/bannedphraselist" % fraseA, shell=True)
	 			
	 			showinfo(title="Control Parental", message="URL y/o Frase Bloqueada correctamenta")

	 		else :

	 			showwarning(title="Control Parental", message="Debe ingresar una URL y/o Frase ")

	 	else :

	 		print "Ok"

	 
	 except ValueError:
	  
	  	showwarning(title="Control Parental", message="Error de Sintaxis a ingresado algo incorrecto ")
 


#Primero instanciamos un objeto de la clase TK el cual nos permite crear la aplicacion
app = Tk()

app.geometry("450x300+350+200")
#Ahora definimos el titulo de nuestra aplicacion
app.title("Control Parental")


#================================Creando los elementos de la Interfaz ==============================#

#background_image=PhotoImage(file = "imagenes/fondo2.png")
#background_label = Label(app, image=background_image)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)

#Creamos una imagen, para luego asignarsela a un label, el parametro file va la direccion donde se encuentra la imagen
url = PhotoImage(file = "imagenes/url-64.png")

#Creamos un label y le asignamos la imagen

textUrl = Label(app, text = "Control Parental", font=("Arial",16))
textUrl.place(x=180, y=20)

#Anadimos el label
urllabel = Label(app, image = url)
urllabel.place(x=50, y=43)

textUrl = Label(app, text = "URL:")
textUrl.place(x=126, y=70)

#Ahora creamos el campo de texto donde se va a ingresar la url
urlA = ""
txtUrl = Entry(app, width = 30, textvariable = urlA)
txtUrl.place(x=160, y=70)


#Repetimos los mismo paso para agregar otro campo con imagen
frase = PhotoImage(file = "imagenes/fra-64.png")
fraseLabel = Label(app, image = frase)
fraseLabel.place(x=50, y=110)

#Anadimos el label
textFrase = Label(app, text = "imagenes/Frase:")
textFrase.place(x=120, y=139)

fraseA = ""
txtFrase = Entry(app, width = 30, textvariable = fraseA)
txtFrase.place(x=160, y=138)


#Creamos los respectivos botones de cancelar y Agregar
imgCancelar = PhotoImage(file = "imagenes/cancel2-48.png")
btnCancelar = Button(app, image = imgCancelar, command=app.destroy)
btnCancelar.place(x=200, y=200)

imgAgregar = PhotoImage(file = "imagenes/ok-48.png")
btnAgregar = Button(app, image = imgAgregar, command=add)
btnAgregar.place(x=290, y=200)

#Ejecutamos la interfaz
app.mainloop()




















