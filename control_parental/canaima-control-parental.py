#!/usr/bin/env python

# Canaima Control parental 
#	Carlos Escobar (obi-wan) <cescobar@gnu.org.ve>

try:
	import os
	import commands
	import sys
	import gtk
    	import gtk.glade
	import gettext
	import re
	import commands
except Exception, detail:
	print detail
	pass

try:
	import pygtk
	pygtk.require("2.0")
except Exception, detail:
	print detail	
	pass

#
gettext.install("canaima-control-parental", "/usr/share/canaima-control-parental/")

#descripcion del  menu 
menuName = _("Bloqueador de Dominio")
menuGenericName = _("Control parental")
menuComment = _("Bloquear el acceso a los nombres de dominio seleccionado")

def open_about(widget):
	dlg = gtk.AboutDialog()
	dlg.set_title(_("About") + " - canaima-control-parental")
	version = ("V1.0")
	dlg.set_version(version)
	dlg.set_program_name("canaima-control-parental")
	dlg.set_comments(_("Bloqueador de Dominio"))
        try:
            h = open('/usr/share/common-licenses/GPL','r')
            s = h.readlines()
	    gpl = ""
            for line in s:
               gpl += line
            h.close()
            dlg.set_license(gpl)
        except Exception, detail:
            print detail        
        dlg.set_authors(["Autor: Carlos Escobar <carlos@gnu.org.ve>", "Modificado por: Yoel Jerez <yoel.jerez@gmail.com>", "Juan Mejias <algolius@gmail.com>", "Gracias: dansguardian, mintnany, tinyproxy"])
 
	dlg.set_icon_from_file("/usr/share/canaima-control-parental/icon.svg")
	dlg.set_logo(gtk.gdk.pixbuf_new_from_file("/usr/share/canaima-control-parental/icon.svg"))
        def close(w, res):
            if res == gtk.RESPONSE_CANCEL:
                w.hide()
        dlg.connect("response", close)
        dlg.show()

def agragar_dns(widget, Bloqueador_dns):
	name = commands.getoutput("zenity --entry --text=\"" + _("Escriba la Direccion de Internet:") + "\" --title=canaima-control-parental --window-icon=/usr/share/canaima-control-parental/icon.svg 2> /dev/null")
	domain = name.strip()
	if domain != '':
		domain = re.sub('http://w*\.*','',domain, re.IGNORECASE)
		if domain != '':
			model = Bloqueador_dns.get_model()
			iter = model.insert_before(None, None)
			model.set_value(iter, 0, domain)
			domain = "" + domain + " # Bloqueado por canaima-control-parental"
			os.system("echo \"" + domain + "\" >> /etc/dansguardian/lists/blacklists/ads/urls")		

def cerrar_app(widget):
	os.system("invoke-rc.d dansguardian restart")
	gtk.main_quit()
	
#Si no existe ninguna copia de seguridad del /etc/dansguardian/lists/blacklists/ads/urls se hace una quedando con el nombre de urls.bck
if not os.path.exists("/etc/dansguardian/lists/blacklists/ads/urls.bck"):
	os.system("cp /etc/dansguardian/lists/blacklists/ads/urls /etc/dansguardian/lists/blacklists/ads/urls.bck")

#Se Establese el archivo de glade
gladefile = "/usr/share/canaima-control-parental/canaima-control-parental.glade"
wTree = gtk.glade.XML(gladefile, "ventana1")
wTree.get_widget("ventana1").set_title(_("Canaima Control parental"))
vbox = wTree.get_widget("caja_menu")
Bloqueador_dns = wTree.get_widget("Bloqueador_dns")
wTree.get_widget("ventana1").set_icon_from_file("/usr/share/canaima-control-parental/icon.svg")

# Se establece la vista del arbol por columnas 
column1 = gtk.TreeViewColumn(_("Direcciones de Internet Bloquedas"), gtk.CellRendererText(), text=0)
column1.set_sort_column_id(0)
column1.set_resizable(True)
Bloqueador_dns.append_column(column1)
Bloqueador_dns.set_headers_clickable(True)
Bloqueador_dns.set_reorderable(False)
Bloqueador_dns.show()

model = gtk.TreeStore(str)
model.set_sort_column_id( 0, gtk.SORT_ASCENDING )
Bloqueador_dns.set_model(model)

#Se Obtiene la lista de dominios no permitidos
blocks_domains = commands.getoutput("cat /etc/dansguardian/lists/blacklists/ads/urls | grep canaima-control-parental | cut -d' ' -f1")
for line in blocks_domains.split('\n'):
	line = line.strip()
	iter = model.insert_before(None, None)
	model.set_value(iter, 0, line)		

wTree.get_widget("boton_cerrar").connect("clicked", cerrar_app)
wTree.get_widget("boton_agregar").connect("clicked", agragar_dns, Bloqueador_dns)

fileMenu = gtk.MenuItem(_("_Archivo"))
fileSubmenu = gtk.Menu()
fileMenu.set_submenu(fileSubmenu)
closeMenuItem = gtk.ImageMenuItem(gtk.STOCK_CLOSE)
closeMenuItem.get_child().set_text(_("Cerrar"))
closeMenuItem.connect("activate", cerrar_app)
fileSubmenu.append(closeMenuItem)

helpMenu = gtk.MenuItem(_("_Ayuda"))
helpSubmenu = gtk.Menu()
helpMenu.set_submenu(helpSubmenu)
aboutMenuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
aboutMenuItem.get_child().set_text(_("Acerca de"))
aboutMenuItem.connect("activate", open_about)
helpSubmenu.append(aboutMenuItem)

wTree.get_widget("barra_menu1").append(fileMenu)
wTree.get_widget("barra_menu1").append(helpMenu)

wTree.get_widget("ventana1").connect("destroy", cerrar_app)	

wTree.get_widget("ventana1").show_all()	

gtk.main()
