#Version 0.1 sin paradigma POO
from tkinter import ttk
from tkinter import *
from datetime import date

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import numpy as np

import sqlite3

db_name = 'restaurante.db'
nombre_Restaurante = 'COMIDA CORRIDA SELENE'
banderagerente=0
banderamesero=0
platillos_master=['Enchiladas','Arrachera','Pechuga','Caldo','Chilacas']


def run_Query(query,parameters=()): #
		with sqlite3.connect(db_name) as conn:
			cursor=conn.cursor()
			result=cursor.execute(query,parameters)
			conn.commit()
		return result

class PLATILLO:
	def __init__(self,name,ingredients):
		self.nombre = name
		self.ingredientes = ingredients
		self.status = 'Disponible'

class MESA:
	def __init__(self,number,status=0,waiter='',people=0):
		self.numero = number
		self.ocupada = status
		self.total = 0
		self.mesero = waiter
		self.personas = people

	def ocupar_Mesa(self,number,waiter,people):
		self.ocupada=1
		self.mesero=waiter
		self.peronas=people

	def agregar_Platillo(self,platillo):
		name = self.platillo
		query = 'SELECT precio FROM platillos WHERE nombre = ? ORDER BY name DESC '
		precio = run_Query(query,(name,))
		self.total=self.total + precio

	def imprimir_Cuenta(self,number):
		return self.total

class GERENTE:

	def __init__(self,id,password):
		self.usuario = id
		self.contraseña= password
		query='INSERT INTO gerentes VALUES(?,?)'
		parameters=(id,password)
		run_Query(query,parameters)


	def nuevo_Usuario(self,id):
		query='INSERT INTO meseros VALUES(?,?,?)'
		parameters=(id,0,0)
		run_Query(query,parameters)


def programa(window):

	wind = window
	wind.title(nombre_Restaurante)

	#meter_Id()

	#if banderagerente==1:

	frame = LabelFrame(wind, text = 'Inicio')
	frame.grid(row=0,column=0,columnspan=3,pady=20,sticky=W+E)
	frame.config(width='200',height='200')
	frame.pack(side='top',anchor='n')


	ttk.Button(frame,text='Iniciar sesion',command=lambda: meter_Id(wind)).grid(row=3,columnspan=2,sticky=W+E)
	ttk.Button(frame,text='salir',command=lambda: destruir(wind)).grid(row=4,columnspan=2,sticky=W+E) #

def meter_Id(window):
	editWind = Toplevel()
	editWind.title = 'Iniciar sesión'

	Label(editWind,text= 'ID').grid(row=0,column=1)
	ID = Entry(editWind)
	ID.focus()
	ID.grid(row=0,column=2)

	Button (editWind, text='Iniciar',command= lambda: iniciar(ID.get(),window)).grid(row=1,column=2,sticky=W) #

def meter_contraseña(id,window):
	usuario=id
	editWind = Toplevel()
	editWind.title = 'Iniciar sesión'

	Label(editWind,text= 'Contraseña:').grid(row=0,column=1)
	ID = Entry(editWind,show="*")
	ID.focus()
	ID.grid(row=0,column=2)

	Button (editWind, text='Iniciar',command= lambda: verificar(ID.get(),usuario,window)).grid(row=1,column=2,sticky=W)
	Button (editWind, text='regresar',command= editWind.destroy).grid(row=1,column=3) #

def verificar(contrasena,id,window):
	bandera=0
	query='SELECT contraseña FROM gerentes WHERE usuario = ?'
	consulta=run_Query(query,(id,))
	for row in consulta:
		if row[0]==contrasena:
			print('AHORA ERES GERENTE')
			bandera=1
	if bandera == 0:
		print('Contraseña no válida')
		error=Toplevel()
		error.title='Contraseña no válida'
		Label(error, text='Contraseña no válida ').grid(row=0,column=1)
		Button(error,text='regresar',command=lambda: destruir(error)).grid(row=1,column=1)
		print('Usuario no válido')
	if bandera ==1:
		window.destroy()
		crear_gerente()#

def crear_gerente():
	nuevaVentana =Tk()
	id='Gerente'
	nuevaVentana.geometry("400x400")
	ventana = Wind_gerente(nuevaVentana,id)
	nuevaVentana.mainloop()	#

def iniciar (id,window):
	ID = id
	bandera=0

	query1 = 'SELECT usuario FROM gerentes WHERE usuario = ?'
	query2 = 'SELECT Usuario FROM meseros WHERE Usuario = ?'

	consulta = run_Query(query1,(ID,))

	if ID!='cheff' and ID!='barra':

		for row in consulta:
			if row[0]==ID:
				bandera=1
				meter_contraseña(ID,window)

		if bandera == 0:
			consulta = run_Query(query2,(ID,))
			for row in consulta:
				if row[0]==ID:
					bandera=1
					window.destroy()

					nuevaVentana =Tk()
					nuevaVentana.geometry("400x400")
					ventana = Wind_waiter(nuevaVentana,ID)
					nuevaVentana.mainloop()

	elif ID == 'cheff':
		bandera=1
		window.destroy()
		nuevaVentana =Tk()
		nuevaVentana.geometry("400x400")
		ventana = Wind_cheff(nuevaVentana)
		nuevaVentana.mainloop()

	elif ID == 'barra':
		bandera=1
		window.destroy()
		nuevaVentana =Tk()
		nuevaVentana.geometry("400x400")
		ventana = Wind_bar(nuevaVentana)
		nuevaVentana.mainloop()


	if bandera == 0:
		error=Toplevel()
		error.title='usuario no válido'
		Label(error, text='Usuario no válido ').grid(row=0,column=1)
		Button(error,text='regresar',command=lambda: destruir(error)).grid(row=1,column=1)
		print('Usuario no válido')#


def Wind_cheff(ventana):
	wind = ventana
	wind.title(nombre_Restaurante + '  || CHEFF')

	frame=LabelFrame(wind, text='Acciones: ')
	frame.grid(row=2, column=1, columnspan=3, pady=10)

	ttk.Button(frame,text='Salir',command=lambda:[destruir(wind),principio_bucle()]).grid(row=10,column=1,sticky=W+E)#

def Wind_bar(ventana):
	wind=ventana
	wind.title(nombre_Restaurante + '  || BARRA')

	frame=LabelFrame(wind, text='Acciones: ')
	frame.grid(row=2, column=1, columnspan=3, pady=10)

	ttk.Button(frame,text='Salir',command=lambda:[destruir(wind),principio_bucle()]).grid(row=10,column=1,sticky=W+E)#


def Wind_gerente(window,gerente): #
	wind = window
	wind.title(nombre_Restaurante + '  || '+ gerente)

	frame=LabelFrame(wind, text='Acciones: ')
	frame.grid(row=2, column=1, columnspan=3, pady=10)

	ttk.Button(frame,text='Agregar/Quitar mesero',command=lambda: editar_meseros(wind)).grid(row=2,column=1,sticky=W+E,pady=10)
	ttk.Button(frame,text='Descontar cuenta',command=lambda: descontar_cuentas(wind)).grid(row=3,column=1,sticky=W+E)
	ttk.Button(frame,text='Modificar platillos',command=lambda: modificar_platillos(wind)).grid(row=4,column=1,sticky=W+E)
	ttk.Button(frame,text='Bloquear ingredientes',command=lambda: bloquear_platillos(wind)).grid(row=5,column=1,sticky=W+E)
	ttk.Button(frame,text='Modificar id',command=lambda: modificar_usuario()).grid(row=6,column=1,sticky=W+E,pady=10)
	ttk.Button(frame,text='Gestionar día',command=lambda: ventas()).grid(row=7,column=1,sticky=W+E)
	ttk.Button(frame,text='Inventario',command=lambda: inventario(wind)).grid(row=8,column=1,sticky=W+E)
	ttk.Button(frame,text='Ver ventas',command=lambda: ventastotales()).grid(row=9,column=1,sticky=W+E,pady=10)
	ttk.Button(frame,text='Salir',command=lambda:[destruir(wind),principio_bucle()]).grid(row=10,column=1,sticky=W+E)

	frame.pack(side='top',anchor='n')

def ventastotales(): #
	ventas_wind=Toplevel()
	ventas_wind.title='Ver ventas'

	message=Label(ventas_wind,text='Ventas ')
	message.grid(row=0,column=0,columnspan=2)

	frame=LabelFrame(ventas_wind,text='')
	frame.grid(row=1, column=0, columnspan=3, pady=10)

	tree=ttk.Treeview(frame,height=10,columns=2)
	tree.grid(row=1,column=0,pady=10,sticky=W+E)
	tree.heading('#0',text='Día',anchor=CENTER)
	tree.heading('#1',text='Total',anchor=CENTER)

	get_ventastotales(tree)

	Button(frame,text='Generar gráfico',command=lambda: generar_grafico(tree)).grid(row=2,column=0,sticky=W+E)
	Button(frame,text='Regresar',command=lambda: destruir(ventas_wind)).grid(row=3,column=0,sticky=W+E)

def inventario(window): #
	destruir(window)

	wind = window
	wind.title(nombre_Restaurante + '  ||  Inventario')

	frame=LabelFrame(wind, text='Acciones: ')
	frame.grid(row=0, column=1, columnspan=3, pady=10)

	pass

def generar_grafico(tree): #
	i=0
	lista=[]
	total=0
	root = Tk()
	root.wm_title("Gráfico de ventas")

	fig = Figure(figsize=(13,5), dpi=100)

	tabla = get_ventasa()

	for row in tabla:
		total+=1

	x = np.ones(total,dtype=str)
	y = np.ones(total,dtype=float)

	tabla2 = get_ventasa()

	for row2 in tabla2:
		lista.append(row2[0][5:10])
		y[i]=row2[1]
		i+=1
	x=np.array(lista)
	#print(x)
	#print(y)

	fig.add_subplot(111).bar(x, y, edgecolor='black')


	canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
	canvas.draw()

	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	toolbar = NavigationToolbar2Tk(canvas, root)
	toolbar.update()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	def on_key_press(event):
	    #print("you pressed {}".format(event.key))
	    key_press_handler(event, canvas, toolbar)


	canvas.mpl_connect("key_press_event", on_key_press)


	def _quit():
	    root.quit()     # stops mainloop
	    root.destroy()  # this is necessary on Windows to prevent
	                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

	button = Button(master=root, text="  Regresar  ", command=_quit)
	button.pack(side=BOTTOM)

	mainloop()

def get_ventasa():
	query='SELECT * FROM ventas'

	return run_Query(query)

def get_ventastotales(tree): #
	records = tree.get_children()

	for element in records:
		tree.delete(element)

	query='SELECT * FROM ventas'
	db_rows=run_Query(query)

	for row in db_rows:
		tree.insert('',0,text=row[0],values = row[1])

def ventas(): #
	ventas_wind=Toplevel()
	ventas_wind.title='Gestionar ventas'
	fecha=str(date.today())

	message=Label(ventas_wind,text='Ventas del día '+fecha)
	message.grid(row=0,column=0,columnspan=2,sticky=W+E)

	frame=LabelFrame(ventas_wind,text='Ventas por mesero: ')
	frame.grid(row=1, column=0, columnspan=3, pady=10)

	tree=ttk.Treeview(frame,height=10,columns=2)
	tree.grid(row=1,column=0,pady=10,sticky=W+E)
	tree.heading('#0',text='Mesero',anchor=CENTER)
	tree.heading('#1',text='Ventas',anchor=CENTER)

	get_ventasm(tree)

	frame2=LabelFrame(ventas_wind,text='Ventas totales: ')
	frame2.grid(row=2, column=0, columnspan=3, pady=10)

	query='SELECT ventas FROM meseros'
	db_rows=run_Query(query)

	total=0

	for row in db_rows:
		total=total+row[0]


	total_st=str(total)+'0'

	Label(frame2,text='Efectivo: ').grid(row=0,column=0)
	Entry(frame2,textvariable=StringVar(frame2,value=total_st),state='readonly').grid(row=0,column=1)

	get_ventasm(tree)

	Button(ventas_wind,text='TERMINAR  DÍA',command= lambda: terminar_dia(ventas_wind,total)).grid(row=3,column=0,sticky=W+E)
	Button(ventas_wind,text='Regresar',command=lambda: destruir(ventas_wind)).grid(row=3,column=1,sticky=E)

def terminar_dia(wind,total): #
	bandera=0
	fecha=str(date.today())
	query='SELECT * FROM mesa WHERE ocupada=1'
	ocupadas=run_Query(query)
	for row in ocupadas:
		bandera=1

	if bandera==1:
		error_terminar()

	if bandera==0:
		query='UPDATE meseros SET Ventas=0,Propinas=0'
		run_Query(query)
		query='INSERT INTO ventas (dia,total) VALUES(?,?)'
		parameters=(fecha,total)
		run_Query(query,parameters)

		error_wind=Toplevel()
		error_wind.title='error'

		frame=LabelFrame(error_wind,text='')
		frame.grid(row=0,column=0,columnspan=3,pady=10)

		Label(frame,text='Día terminado').grid(row=0,column=0)
		Button(frame,text='Salir',command=lambda: quit()).grid(row=1,column=0,sticky=W+E)

def error_terminar(): #
	error_wind=Toplevel()
	error_wind.title='error'

	frame=LabelFrame(error_wind,text='')
	frame.grid(row=0,column=0,columnspan=3,pady=10)

	Label(frame,text='ERROR: Hay mesas ocupadas').grid(row=0,column=0)
	Button(frame,text='Regresar',command=lambda: destruir(error_wind)).grid(row=1,column=0,sticky=W+E)

def get_ventasm(tree): #
	records = tree.get_children()

	for element in records:
		tree.delete(element)

	query='SELECT * FROM meseros'
	db_rows=run_Query(query)

	for row in db_rows:
		tree.insert('',0,text=row[0],values = row[1])

	print("Actualizada con exito")

def modificar_usuario(): #
	pagar_wind=Toplevel()
	pagar_wind.title='Modificar usuario'

	message=Label(pagar_wind,text='',fg='red')
	message.grid(row=0,column=0,columnspan=2,sticky=W+E)

	Label(pagar_wind,text='Nuevo usuario: ').grid(row=1,column=0)
	nuevo_usuario=Entry(pagar_wind)
	nuevo_usuario.grid(row=1,column=1)
	nuevo_usuario.focus()

	Label(pagar_wind,text='Nueva contraseña: ').grid(row=2,column=0)
	nueva_contra=Entry(pagar_wind,show='*')
	nueva_contra.grid(row=2,column=1)

	Label(pagar_wind,text='Confirmar contraseña: ').grid(row=3,column=0)
	nuevo_contra2=Entry(pagar_wind,show='*')
	nuevo_contra2.grid(row=3,column=1)

	Label(pagar_wind,text=' ').grid(row=4,column=0)

	Button(pagar_wind,text='Guardar',command=lambda: editar_id(nuevo_usuario,nueva_contra,nuevo_contra2,message)).grid(row=5,column=0,sticky=E)
	Button(pagar_wind,text='Salir',command=lambda: destruir(pagar_wind)).grid(row=5,column=1,sticky=W)

def editar_id(user,passw,passw2,message):#
	if passw.get() != passw2.get():
		message['text']='Las contraseñas no coinciden'
	else:
		query='UPDATE gerentes SET usuario=?,contraseña=? WHERE registro = 2'
		parameters=(user.get(),passw.get())
		run_Query(query,parameters)
		message['text']='Id y contraseña actualizados'
		user.delete(0,END)
		passw.delete(0,END)
		passw2.delete(0,END)

def editar_meseros(window): #
	window.destroy()

	window=Tk()
	application=Meseros(window)
	window.mainloop()

def descontar_cuentas(window): #
	window.destroy()
	window2=Tk()
	application=wind_descuentos(window2)
	window2.mainloop()

def wind_descuentos(window): #
    wind = window
    wind.title('GESTIONAR DESCUENTOS')
    wind.geometry("300x200")

    frame=LabelFrame(wind, text='Descontar a mesa: ')
    message=Label(frame,text='',fg='red')
    message.grid(row=0,column=0,columnspan=2,sticky=W+E)

    Label(frame, text='Mesa: ').grid(row=1,column=0)
    mesa=Entry(frame)
    mesa.grid(row=1,column=1)
    mesa.focus()

    Label(frame, text='Descuento: ').grid(row=2,column=0)
    descuento=Entry(frame)
    descuento.grid(row=2,column=1)

    Button(frame,text='Descontar',command=lambda: descontard(wind,message,mesa,descuento)).grid(row=3,column=0,sticky=W+E)
    Button(frame,text='Regresar',command=lambda: [destruir(wind),crear_gerente()]).grid(row=3,column=1,sticky=W+E)
    frame.pack(side='top',anchor='n')

def descontard(window,message,mesa,descuento): #
	bandera=0
	query='SELECT * FROM mesa WHERE ocupada = 1 AND num = ?'
	parameters=(mesa.get(),)

	mesasd=run_Query(query,parameters)

	for row in mesasd:
		bandera = 1

	if bandera ==1:
		query='UPDATE mesa SET descuento= ? WHERE num=?'
		parameters=(descuento.get(),mesa.get())
		run_Query(query,parameters)
		message['text']='Descuento aplicado a mesa {}'.format(mesa.get())
		mesa.delete(0,END)
		descuento.delete(0,END)
	else:
		message['text']='Mesa vacía o no encontrada'

def modificar_platillos(window): #
	window.destroy()
	window=Tk()
	application=Platillosn(window)
	window.mainloop()

def bloquear_platillos(window): #
	window.destroy()
	window2=Tk()
	ventana=wind_bloquear(window2)
	window2.mainloop()

def wind_bloquear(window):	#
    wind = window
    wind.title('GESTIONAR INGREDIENTES')
    wind.geometry("300x200")

    frame=LabelFrame(wind, text='Opciones: ')

    Button(frame,text='Bloquear platillos',command=lambda: bloqueo_platillo(wind)).grid(row=0,column=0,sticky=W+E)
    Button(frame,text='Desbloquear platillos',command=lambda: desbloqueo_platillo(wind)).grid(row=1,column=0,sticky=W+E,pady=10)
    Button(frame,text='Regresar',command=lambda: [destruir(wind),crear_gerente()]).grid(row=2,column=0,sticky=W+E)
    frame.pack(side='top',anchor='n')

def bloqueo_platillo(window): #
	bloqueo_wind=Toplevel()
	bloqueo_wind.title='Ingredientes'
	frame=LabelFrame(bloqueo_wind, text='Bloquear platillos con: ')

	message=Label(frame,text='',fg='red')
	message.grid(row=0,column=0,columnspan=2,sticky=W+E)

	Label(frame, text='Ingrediente: ').grid(row=1,column=0)
	producto=Entry(frame)
	producto.grid(row=1,column=1)
	producto.focus()

	Button(frame,text='Bloquear',command=lambda: bloquear_accion(message,producto)).grid(row=2,column=0,sticky=W+E)
	Button(frame,text='Regresar',command=lambda: destruir(bloqueo_wind)).grid(row=2,column=1,sticky=W+E)

	frame.pack(side='top',anchor='n')

def bloquear_accion(message,producto): #
	banderab=0
	productob=producto.get()
	query='SELECT nombre from platillos WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ?'
	parameters=(productob,productob,productob)
	platos=run_Query(query,parameters)

	for row in  platos:
		#platillos_master.remove(productob)
		banderab=1

	if banderab==1:
		query='UPDATE platillos SET disponible = 0 WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ? '
		parameters=(productob,productob,productob)
		run_Query(query,parameters)

		message['text']='Platillos con {} bloqueados'.format(producto.get())
		producto.delete(0,END)

	else:
		message['text']='{} no encontrado'.format(producto.get())
		producto.delete(0,END)

def desbloqueo_platillo(window): #
	bloqueo_wind=Toplevel()
	bloqueo_wind.title='Ingredientes'
	frame=LabelFrame(bloqueo_wind, text='Desbloquear platillos con: ')

	message=Label(frame,text='',fg='red')
	message.grid(row=0,column=0,columnspan=2,sticky=W+E)

	Label(frame, text='Ingrediente: ').grid(row=1,column=0)
	producto=Entry(frame)
	producto.grid(row=1,column=1)
	producto.focus()

	Button(frame,text='Desbloquear',command=lambda: desbloquear_accion(message,producto)).grid(row=2,column=0,sticky=W+E)
	Button(frame,text='Regresar',command=lambda: destruir(bloqueo_wind)).grid(row=2,column=1,sticky=W+E)

	frame.pack(side='top',anchor='n')

def desbloquear_accion(message,producto):#
	banderab=0
	productob=producto.get()
	query='SELECT * from platillos WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ?'
	parameters=(productob,productob,productob)
	platos=run_Query(query,parameters)

	for row in  platos:
		#platillos_master.remove(productob)
		banderab=1

	if banderab==1:
		query='UPDATE platillos SET disponible = 1 WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ? '
		parameters=(productob,productob,productob)
		run_Query(query,parameters)

		message['text']='Platillos con {} desbloqueados'.format(producto.get())
		producto.delete(0,END)

	else:
		message['text']='{} no encontrado'.format(producto.get())
		producto.delete(0,END)


def Wind_waiter(window,mesero):#
    wind = window
    wind.title(nombre_Restaurante + '  || '+ mesero)

    frame=LabelFrame(wind, text='Mesas disponibles o asignadas:')
    frame.grid(row=0, column=1, columnspan=3, pady=10)
    Label(frame,text=' ').grid(row=0,column=1)

    tree=ttk.Treeview(frame,height=10,columns=2)
    tree.grid(row=1,column=1,pady=10)
    tree.heading('#0',text='Mesa',anchor=CENTER)
    tree.heading('#1',text='Total',anchor=CENTER)

    get_mesas(tree,mesero)

   # ttk.Button(text='Imprimir cuenta').grid(row=2,column=0)
    ttk.Button(frame,text='Editar mesa',command=lambda: editar_mesa(tree,mesero)).grid(row=2,column=1,sticky=W+E)
    ttk.Button(frame,text='Pagar cuenta',command=lambda: pagar_cuenta(tree,mesero)).grid(row=3,column=1,sticky=W+E)
    ttk.Button(frame,text='Actualizar tabla',command=lambda: get_mesas(tree,mesero)).grid(row=4,column=1,sticky=W+E)
    ttk.Button(frame,text='Salir',command=lambda:[destruir(wind),principio_bucle()]).grid(row=5,column=1,sticky=W+E) #

def pagar_cuenta(tree,mesero,saldo=0,propinas=0):#
	pagar_wind=Toplevel()
	pagar_wind.title='Pagar la cuenta'
	mesa=tree.item(tree.selection())['text']

	query='SELECT * FROM mesa where num = ?'

	mesa_datos=run_Query(query,(mesa,))
	for row in mesa_datos:
		numero_mesa=row[0]
		personas=row[2]
		total=row[3]
		descuento=row[5]

	nuevo_total=total-saldo-descuento
	Label(pagar_wind, text='Pagar cuenta de mesa No. ' + str(mesa)).grid(row=0,column=1)
	Label(pagar_wind, text='Total consumo: ').grid(row=1,column=1)
	Entry(pagar_wind,textvariable=StringVar(pagar_wind,value=total),state='readonly').grid(row=1,column=2)

	Label(pagar_wind, text='Descuento: ').grid(row=2,column=1)
	Entry(pagar_wind,textvariable=StringVar(pagar_wind,value=descuento),state='readonly').grid(row=2,column=2)

	Label(pagar_wind, text='Total a pagar: ').grid(row=3,column=1)
	Entry(pagar_wind,textvariable=StringVar(pagar_wind,value=nuevo_total),state='readonly').grid(row=3,column=2)

	Label(pagar_wind, text='Total pagado: ').grid(row=4,column=1)
	pagado = Entry(pagar_wind,textvariable=StringVar(pagar_wind,value=saldo))
	pagado.grid(row=4,column=2)

	if propinas ==0:
		propinas_previas = total*0.1
	else:
		propinas_previas=propinas

	Label(pagar_wind, text='Propinas: ').grid(row=5,column=1)
	propinas = Entry(pagar_wind,textvariable=StringVar(pagar_wind,value=propinas_previas))
	propinas.grid(row=5,column=2)

	Button(pagar_wind,text='Aceptar',command=lambda: matar_cuenta(mesa,mesero,pagar_wind,nuevo_total,pagado.get(),propinas.get(),tree)).grid(row=6,column=2,sticky=W)
	Button(pagar_wind,text='Cancelar',command=pagar_wind.destroy).grid(row=6,column=2,sticky=E)

def matar_cuenta(mesa,mesero,ventana,total,pagado,propinas,tree):#
	bandera=0
	if total>float(pagado):
		ventana.destroy()
		pagar_cuenta(tree,mesero,float(pagado),float(propinas))
	elif total==float(pagado):
		ventana.destroy()
		cambio=Toplevel()
		cambio.title='ok'
		Label(cambio, text='Mesa pagada con éxito ').grid(row=0,column=1)
		Label(cambio, text='Cambio: '+'$0.00').grid(row=1,column=1)
		Button(cambio,text='Aceptar',command=lambda: destruir(cambio)).grid(row=2,column=1)
		bandera=1
	elif total<float(pagado):
		cambio_total=float(pagado)-total
		ventana.destroy()
		cambio=Toplevel()
		cambio.title='ok'
		Label(cambio, text='Mesa pagada con éxito ').grid(row=0,column=1)
		Label(cambio, text='Cambio: '+str(cambio_total)).grid(row=1,column=1)
		Button(cambio,text='Aceptar',command=lambda: destruir(cambio)).grid(row=2,column=1)
		bandera=1

	if bandera==1:
		reiniciar_mesa(mesa,mesero,tree)
		query='SELECT Ventas FROM meseros WHERE Usuario = ? '
		ventas_pasadas=run_Query(query,(mesero,))
		for row in ventas_pasadas:
			ventas_ori=row[0]

		query='SELECT Propinas FROM meseros WHERE Usuario = ?'
		propinas_pasadas=run_Query(query,(mesero,))
		for row in propinas_pasadas:
			propinas_ori=row[0]

		total_ventas=ventas_ori+total
		propinas_total=propinas_ori+float(propinas)

		query='UPDATE meseros SET Ventas=?, Propinas=? WHERE Usuario=?'
		parameters=(total_ventas,propinas_total,mesero)
		run_Query(query,parameters)
		get_mesas(tree,mesero)

def reiniciar_mesa(mesa,meser,tree):#
	query='UPDATE mesa SET total=0,mesero="",ocupada=0,personas=0,descuento=0 WHERE num=?'
	run_Query(query,(mesa,))

	#for platillo in platillos_master:
	#	query='UPDATE mesa SET {} = 0 WHERE num = ?'.format(platillo)
	#	parameters=(mesa,)
	#	run_Query(query,parameters)

	query='UPDATE platillos_mesas SET {}=0'.format(mesa)
	run_Query(query)

def editar_mesa(tree,mesero):#
	#try:
	#	tree.item(tree.selection())['text'][0]
	#except IndexError as e:
	#	print('error')
	#	return
	editar_wind=Toplevel()
	editar_wind.title = 'Editar mesa'
	mesa=tree.item(tree.selection())['text']

	query='SELECT * FROM mesa where num = ?'

	mesa_datos=run_Query(query,(mesa,))
	for row in mesa_datos:
		numero_mesa=row[0]
		personas=row[2]
		total=row[3]
		meseropasado=row[4]

	Label(editar_wind, text='Editar mesa No. ' + str(mesa)).grid(row=0,column=0)
	Label(editar_wind, text='Personas: ').grid(row=1,column=0)
	Nuevas_personas=Entry(editar_wind,textvariable=StringVar(editar_wind,value=personas))
	Nuevas_personas.grid(row=1,column=1)
	#

	Label(editar_wind, text='Mesero: ').grid(row=2,column=0)
	Nuevo_mesero=Entry(editar_wind,textvariable=StringVar(editar_wind,value=meseropasado))
	Nuevo_mesero.grid(row=2,column=1)

	#Agregar platillo
	frame=LabelFrame(editar_wind, text='Platillos')
	frame.grid(row=3, column=0, columnspan=3, pady=10)

	tree_platillos=ttk.Treeview(frame,height=10,columns=('Precio','Cantidad'))
	#tree_platillos['columns']=('one','two')

	tree_platillos.heading('#0',text='Nombre',anchor=CENTER)
	tree_platillos.heading('#1',text='Precio',anchor=CENTER)
	tree_platillos.heading('#2',text='Cantidad',anchor=CENTER)
	tree_platillos.grid(row=5,column=1,pady=10)

	get_platillos(tree_platillos,mesa)

	Label(frame,text='Total').grid(row=6,column=1,sticky=E)
	Entry(frame,textvariable=StringVar(frame,value=total),state='readonly').grid(row=6,column=2,sticky=W)

	Button(frame,text='Agregar',command=lambda: agregar_plato(mesa,tree_platillos,frame)).grid(row=7,column=1,sticky=E)
	Button(frame,text='Quitar',command=lambda: quitar_plato(mesa,tree_platillos,frame)).grid(row=7,column=2,sticky=W)


	Button(editar_wind,text='Aceptar',command=lambda:modificar_mesa(mesa,Nuevas_personas.get(),Nuevo_mesero.get(),mesero,tree,editar_wind)).grid(row=6,column=0,sticky=E)
	Button(editar_wind,text='Cancelar',command=editar_wind.destroy).grid(row=6,column=2,sticky=W)

def agregar_plato(mesa,tree,frame):#
	platillo=tree.item(tree.selection())['text']
	cantidad=tree.item(tree.selection())['values'][1]
	cantidad+=1

	query='SELECT disponible from platillos WHERE nombre = ?'
	disponibilidad_db=run_Query(query,(platillo,))

	for row in disponibilidad_db:
		disponibilidad=row[0]

	if disponibilidad==1:
		query='SELECT precio from platillos Where nombre=?'
		precio=run_Query(query,(platillo,))
		for row in precio:
			precio_platillo=row[0]

		query='SELECT total from mesa Where num=?'
		precio=run_Query(query,(mesa,))
		for row in precio:
			precio_mesa=row[0]

		precio_total=precio_platillo+precio_mesa

		query='UPDATE mesa SET total=? WHERE num = ?'
		parameters=(precio_total,mesa)
		run_Query(query,parameters)

		query='UPDATE platillos_mesas SET {} = {} WHERE platillo = ? '.format(mesa,cantidad,platillo)

		platillosss=run_Query(query,(platillo,))

		#for row in platillosss:
			#print(row)

		get_platillos(tree,mesa)

		Entry(frame,textvariable=StringVar(frame,value=precio_total),state='readonly').grid(row=6,column=2,sticky=W)
	else:
		error=Toplevel()
		error.title='Contraseña no válida'
		Label(error, text='Platillo bloqueado ').grid(row=0,column=1)
		Button(error,text='Regresar',command=lambda: destruir(error)).grid(row=1,column=1)
		print('Usuario no válido')

def quitar_plato(mesa,tree,frame):#
	platillo=tree.item(tree.selection())['text']
	cantidad=tree.item(tree.selection())['values'][1]

	query='SELECT precio from platillos Where nombre=?'
	precio=run_Query(query,(platillo,))
	for row in precio:
		precio_platillo=row[0]

	query='SELECT total from mesa Where num=?'
	precio=run_Query(query,(mesa,))
	for row in precio:
		precio_mesa=row[0]

	precio_total=precio_mesa-precio_platillo


	if cantidad>0:
		cantidad-=1
		#query='UPDATE mesa SET {} = ? WHERE num = ?'.format(platillo)
		#parameters=(cantidad,mesa)
		#run_Query(query,parameters)

		query='UPDATE platillos_mesas SET {} = {} WHERE platillo = ? '.format(mesa,cantidad,platillo)
		platillosss=run_Query(query,(platillo,))

		query='UPDATE mesa SET total=? WHERE num = ?'.format(platillo)
		parameters=(precio_total,mesa)
		run_Query(query,parameters)
		Entry(frame,textvariable=StringVar(frame,value=precio_total),state='readonly').grid(row=6,column=2,sticky=W)
		get_platillos(tree,mesa)

def modificar_mesa(num,personas,mesero,meseroactual,tree,windows):#
	if mesero!='' and personas!=0:
		query= 'UPDATE mesa SET personas= ?,mesero=?,ocupada=1 WHERE num=? '
		parameters=(personas,mesero,num)
		run_Query(query,parameters)
		get_mesas(tree,mesero)
	elif mesero=='' and personas!=0:
		mesero=meseroactual
		query= 'UPDATE mesa SET personas= ?,mesero=?,ocupada=1 WHERE num=? '
		parameters=(personas,mesero,num)
		run_Query(query,parameters)
	elif mesero!='' and personas==0:
		personas=1
		query= 'UPDATE mesa SET personas= ?,mesero=?,ocupada=1 WHERE num=? '
		parameters=(personas,mesero,num)
		run_Query(query,parameters)
	elif mesero=='' and personas==0:
		query= 'UPDATE mesa SET personas= 0,mesero=0,ocupada=0 WHERE num=? '
		run_Query(query,(num,))

	windows.destroy()

	get_mesas(tree,meseroactual)

def get_platillos(tree,mesa):#
	lista=[]
	records = tree.get_children()
	for element in records:
	    tree.delete(element)
	query='SELECT * FROM platillos'
	#query2='SELECT * FROM mesa WHERE num=?'
	query3='SELECT * FROM platillos_mesas  '

	#db_platillos=run_Query(query2,(mesa,))
	db_rows=run_Query(query)

	db_numerosplatillos=run_Query(query3,)
	nummesa=int(mesa[4])
	for row in db_numerosplatillos:
		lista.append(row[nummesa])

	i=0

	for row in db_rows:
	    tree.insert('',END,text=row[1],values = (row[0],lista[i])) #lista[i]
	    i+=1
	print('Actualizada con extito')

def get_mesas(tree,mesero):#
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    query='SELECT * FROM mesa where ocupada = 0 or mesero = ?'
    db_rows=run_Query(query,(mesero,))
    for row in db_rows:
        tree.insert('',END,text=row[0],values = row[3])
    print('Actualizada con extito')


def destruir(ventana):#
	ventana.destroy()

class Meseros: #

    db_name = 'restaurante.db'

    def __init__(self,window):
        self.wind=window
        self.wind.title('EDITAR MESEROS')

        frame=LabelFrame(self.wind, text='Agregar un nuevo usuario')
        frame.grid(row=0, column=0, columnspan=3, pady=50)


        Label(frame,text='Usuario: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)

        ttk.Button(frame,text='Agregar',command = self.add_product).grid(row=3,columnspan=2, sticky= W + E)

        self.message=Label(text='',fg='red') ###
        self.message.grid(row=3,column=0,columnspan=2,sticky= W + E)###

        self.tree=ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Nombre',anchor=CENTER)
        self.tree.heading('#1',text='Ventas',anchor=CENTER)

        ttk.Button(text= 'Borrar',command= self.delete_product).grid(row = 5, column = 0, sticky= W + E )
        ttk.Button(text= 'Editar',command = self.edit_product).grid(row = 5, column = 1, sticky= W + E )
        ttk.Button(text= 'Regresar',command = lambda: [destruir(self.wind),crear_gerente()]).grid(row = 6, column = 0, sticky= W + E )

        self.get_products()

    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query='SELECT * FROM meseros '
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[0],values = row[1])

    def validation(self):
        return len(self.name.get())!=0

    def add_product(self):
        if self.validation():
            query='INSERT INTO meseros (Usuario,Ventas,Propinas) VALUES(?,0,0)'
            parameters=(self.name.get(),)
            self.run_query(query,parameters)
            self.message['text']='Mesero {} agregado'.format(self.name.get())
            self.name.delete(0,END)

        else:
            self.message['text']='Llenar nombre'

        self.get_products()

    def delete_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']= 'Seleccione un registro'
            return

        name= self.tree.item(self.tree.selection())['text']
        query = 'DELETE from meseros WHERE Usuario = ?'
        self.run_query(query,(name,))
        self.message['text']= 'Mesero {} actualizado correctamente'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']= 'Seleccione un mesero'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price =  self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind=Toplevel()
        self.edit_wind.title = 'editar product'

        Label(self.edit_wind,text= 'Usuario: ').grid(row=0,column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind,value=name),state='readonly').grid(row=0,column = 2)

        Label(self.edit_wind,text= 'Nuevo usuario').grid(row=1,column=1)
        new_name=Entry(self.edit_wind)
        new_name.grid(row=1,column=2)


        Button(self.edit_wind,text='Guardar cambios',command= lambda: self.edit_records(new_name.get(),name,old_price)).grid(row=4,column=2,sticky=W)

    def edit_records(self,new_name,name,old_price):
        query = 'UPDATE meseros SET Usuario = ? WHERE Usuario = ?'
        parameters = (new_name,name)
        self.run_query(query,parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Mesero {} actualizado correctamente'.format(name)
        self.get_products()

class Platillosn: #

    db_name = 'restaurante.db'

    def __init__(self,window):
        self.bebidasi=IntVar()
        self.wind=window
        self.wind.title('EDITAR PLATILLOS')

        frame=LabelFrame(self.wind, text='Agregar un platillo nuevo')
        frame.grid(row=0, column=0, columnspan=3, pady=50)


        Label(frame,text='Nombre: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)

        Label(frame,text='Precio: ').grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2,column=1)

        Label(frame,text='Ingrediente 1: ').grid(row=3, column=0)
        self.ingrediente1 = Entry(frame)
        self.ingrediente1.grid(row=3,column=1)

        Label(frame,text='Ingrediente 2: ').grid(row=4, column=0)
        self.ingrediente2 = Entry(frame)
        self.ingrediente2.grid(row=4,column=1)

        Label(frame,text='Ingrediente 3: ').grid(row=5, column=0)
        self.ingrediente3 = Entry(frame)
        self.ingrediente3.grid(row=5,column=1)

        Label(frame,text='Bebida: ').grid(row=6, column=0)

        self.bebida = Checkbutton(frame,variable=self.bebidasi,onvalue=1,offvalue=0)
        self.bebida.grid(row=6,column=1,sticky=W)


        ttk.Button(frame,text='Agregar',command = self.add_product).grid(row=7,columnspan=2, sticky= W + E)

        self.message=Label(text='',fg='red') ###
        self.message.grid(row=3,column=0,columnspan=2,sticky= W + E)###

        self.tree=ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Nombre',anchor=CENTER)
        self.tree.heading('#1',text='Precio',anchor=CENTER)

        ttk.Button(text= 'Borrar',command= self.delete_product).grid(row = 5, column = 0, sticky= W + E )
        ttk.Button(text= 'Editar',command = self.edit_product).grid(row = 5, column = 1, sticky= W + E )
        ttk.Button(text= 'Regresar',command = lambda: [destruir(self.wind),crear_gerente()]).grid(row = 6, column = 0, sticky= W + E )
        ttk.Button(text= 'Actualizar',command = lambda: self.get_products()).grid(row = 6, column = 1, sticky= W + E )

        self.get_products()

    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query='SELECT * FROM platillos '
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[1],values = row[0])
        print("Actualizada con exito")

    def validation(self):
        return len(self.name.get())!=0 and len(self.precio.get())!=0 and len(self.ingrediente1.get())!=0 and len(self.ingrediente2.get())!=0 and len(self.ingrediente3.get())!=0

    def add_product(self):
        #print(self.bebidasi.get())
        if self.validation():
        	if self.bebidasi.get()==0:
	            query='INSERT INTO platillos (precio,nombre,disponible,ingrediente1,ingrediente2,ingrediente3,bebida) VALUES(?,?,1,?,?,?,0)'
	            nombref=self.name.get()
	            preciof=self.precio.get()
	            ingrediente1f=self.ingrediente1.get()
	            ingrediente2f=self.ingrediente2.get()
	            ingrediente3f=self.ingrediente3.get()
	            parameters=(preciof,nombref,ingrediente1f,ingrediente2f,ingrediente3f)

	            platillos_master.append(nombref)

	            self.run_query(query,parameters)

	        #    query='ALTER TABLE mesa ADD {} text'.format(nombref)
	         #   self.run_query(query)

	          #  query='UPDATE mesa SET {} = 0'.format(nombref)
	           # self.run_query(query)

	            #query = 'UPDATE platillos SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ?'
	            query='INSERT INTO platillos_mesas (platillo,mesa1,mesa2,mesa3,mesa4,mesa5,mesa6) VALUES(?,0,0,0,0,0,0)'
	            parameters=(nombref,)

	            self.run_query(query,parameters)

	            self.message['text']='Platillo {} agregado'.format(self.name.get())
	            self.name.delete(0,END)
	            self.precio.delete(0,END)
	            self.ingrediente1.delete(0,END)
	            self.ingrediente2.delete(0,END)
	            self.ingrediente3.delete(0,END)
	            platillos_master.append(self.name.get())

	        elif self.bebidasi.get() ==1:
	            query='INSERT INTO platillos (precio,nombre,disponible,ingrediente1,ingrediente2,ingrediente3,bebida) VALUES(?,?,1,?,?,?,1)'
	            nombref=self.name.get()
	            preciof=self.precio.get()
	            ingrediente1f=self.ingrediente1.get()
	            ingrediente2f=self.ingrediente2.get()
	            ingrediente3f=self.ingrediente3.get()
	            parameters=(preciof,nombref,ingrediente1f,ingrediente2f,ingrediente3f)

	            platillos_master.append(nombref)

	            self.run_query(query,parameters)

	        #    query='ALTER TABLE mesa ADD {} text'.format(nombref)
	         #   self.run_query(query)

	          #  query='UPDATE mesa SET {} = 0'.format(nombref)
	           # self.run_query(query)

	            #query = 'UPDATE platillos SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ?'
	            query='INSERT INTO platillos_mesas (platillo,mesa1,mesa2,mesa3,mesa4,mesa5,mesa6) VALUES(?,0,0,0,0,0,0)'
	            parameters=(nombref,)

	            self.run_query(query,parameters)

	            self.message['text']='Bebida {} agregado'.format(self.name.get())
	            self.name.delete(0,END)
	            self.precio.delete(0,END)
	            self.ingrediente1.delete(0,END)
	            self.ingrediente2.delete(0,END)
	            self.ingrediente3.delete(0,END)

	            platillos_master.append(self.name.get())

        else:
            self.message['text']='Llenar las casillas'

        self.get_products()

    def delete_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']= 'Seleccione un registro'
            return

        name= self.tree.item(self.tree.selection())['text']
        query = 'DELETE from platillos WHERE nombre = ?'
        self.run_query(query,(name,))

        try:
        	platillos_master.remove(name)
        except:
        	pass

        query='DELETE FROM platillos_mesas WHERE platillo = ?'
        parameters=(name,)
        self.run_query(query,parameters)


        #query='ALTER TABLE mesa DROP COLUMN {} '.format(name)

        #self.run_query(query)

        self.message['text']= 'Platillo {} borrado correctamente'.format(name)
        platillos_master.remove(self.name.get())
        self.get_products()

    def edit_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']= 'Seleccione un platillo'
            return

        name = self.tree.item(self.tree.selection())['text']
        old_price =  self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind=Toplevel()
        self.edit_wind.title = 'editar product'

        Label(self.edit_wind,text= 'Platillo: ').grid(row=0,column=1)
        new_name=Entry(self.edit_wind, textvariable = StringVar(self.edit_wind,value=name))
        new_name.grid(row=0,column = 2)

        Label(self.edit_wind,text= 'Pecio: ').grid(row=1,column=1)
        new_price=Entry(self.edit_wind, textvariable = StringVar(self.edit_wind,value=old_price))
        new_price.grid(row=1,column = 2)


        Button(self.edit_wind,text='Guardar cambios',command= lambda: self.edit_records(new_name.get(),name,old_price,new_price.get())).grid(row=4,column=2,sticky=W)

    def edit_records(self,new_name,name,old_price,new_price):
        o=0
        query = 'UPDATE platillos SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ?'
        parameters = (new_name,new_price,name,old_price)
        self.run_query(query,parameters)
        self.edit_wind.destroy()

        for x in platillos_master:

            if x == name:
                posicion=o
            o+=1

        platillos_master[posicion] = new_name


        #query='ALTER TABLE mesa RENAME COLUMN ? TO ?'

        query = 'UPDATE platillos_mesas SET platillo = ? WHERE platillo = ?'
        parameters = (new_name,name)
        self.run_query(query,parameters)

        self.message['text'] = 'platillo {} actualizado correctamente'.format(name)
        self.get_products()

#root = GERENTE('admin','password')

#ricardo= GERENTE('Flous','1243')
def principio_bucle(): #
	window = Tk()
	window.geometry("300x200")
	ventana = programa(window)
	window.mainloop()

#principio_bucle()#

#if __name__ == '__main__':
#	window = Tk()
#	window.geometry("300x200")
#	ventana = programa(window)
#	window.mainloop()
