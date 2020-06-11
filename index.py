#Version 1.0: final funcional, a veces se bloquea la base de datos. Interface cheff y barra sin terminar 
from tkinter import ttk
from tkinter import *

from datetime import date

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

import sqlite3


db_name='restaurante.db'
nombre_Restaurante = 'COMIDA CORRIDA'
banderagerente = 0
banderamesero=0

def run_Query(query,parameters=()):
		with sqlite3.connect(db_name) as conn:
			cursor=conn.cursor()
			result=cursor.execute(query,parameters)
			conn.commit()
		return result

def destruir(window):
    window.destroy()

def crear_Inicio():
    window = Tk()
    window.geometry("300x200")
    ventana = VentanaPrincipal(window)
    window.mainloop()

def crear_Gerente():
    nuevaVentana = Tk()
    nuevaVentana.geometry("400x400")
    objeto = WindGerente(nuevaVentana,'Gerente')

class PagarCuenta:
	def __init__(self,tree,saldo,propinas,mesero):

		self.mesero= mesero
		self.saldo = saldo
		self.propinas = propinas

		self.pagar_wind=Toplevel()
		self.pagar_wind.title='Pagar la cuenta'
		self.mesa=self.tree.item(self.tree.selection())['text']

		self.Calculos()

		Label(self.pagar_wind, text='Pagar cuenta de mesa No. ' + str(self.mesa)).grid(row=0,column=1)
		Label(self.pagar_wind, text='Total consumo: ').grid(row=1,column=1)
		Entry(self.pagar_wind,textvariable=StringVar(self.pagar_wind,value=self.total),state='readonly').grid(row=1,column=2)

		Label(self.pagar_wind, text='Descuento: ').grid(row=2,column=1)
		Entry(self.pagar_wind,textvariable=StringVar(self.pagar_wind,value=self.descuento),state='readonly').grid(row=2,column=2)

		Label(self.pagar_wind, text='Total a pagar: ').grid(row=3,column=1)
		Entry(self.pagar_wind,textvariable=StringVar(self.pagar_wind,value=self.nuevo_total),state='readonly').grid(row=3,column=2)

		Label(self.pagar_wind, text='Total pagado: ').grid(row=4,column=1)
		self.pagado = Entry(self.pagar_wind,textvariable=StringVar(self.pagar_wind,value=self.saldo))
		self.pagado.grid(row=4,column=2)

		if self.propinas ==0:
		    self.propinas_previas = self.total*0.1
		else:
		    self.propinas_previas=self.propinas

		Label(self.pagar_wind, text='Propinas: ').grid(row=5,column=1)
		self.propinas = Entry(self.pagar_wind,textvariable=StringVar(self.pagar_wind,value=self.propinas_previas))
		self.propinas.grid(row=5,column=2)

		Button(self.pagar_wind,text='Aceptar',command=lambda: self.matar_Cuenta()).grid(row=6,column=2,sticky=W)
		Button(self.pagar_wind,text='Cancelar',command=lambda: self.pagar_wind.destroy()).grid(row=6,column=2,sticky=E)

	def Calculos(self):
		self.query='SELECT * FROM mesa where num = ?'

		self.mesa_datos=run_Query(self.query,(self.mesa,))

		for row in self.mesa_datos:
		    self.numero_mesa=row[0]
		    self.personas=row[2]
		    self.total=row[3]
		    self.descuento=row[5]

		self.nuevo_total = self.total - self.saldo - self.descuento

	def matar_Cuenta(self):
		self.pagado1 = int(self.pagado.get()) #+ self.saldo
		self.propinas1 = self.propinas.get()
		self.ventana = self.pagar_wind
		self.total = self.nuevo_total


		self.bandera=0

		if self.total>float(self.pagado1):
			self.ventana.destroy()
			self.pagar_Cuenta(float(self.pagado1),float(self.propinas1))

		elif self.total==float(self.pagado1):
			self.ventana.destroy()
			self.cambio=Toplevel()
			self.cambio.title='ok'
			Label(self.cambio, text='Mesa pagada con éxito ').grid(row=0,column=1)
			Label(self.cambio, text='Cambio: '+'$0.00').grid(row=1,column=1)
			Button(self.cambio,text='Aceptar',command=lambda: destruir(self.cambio)).grid(row=2,column=1)
			self.bandera=1

		elif self.total<float(self.pagado1):
			self.cambio_total=float(self.pagado1)-self.total
			self.ventana.destroy()
			self.cambio=Toplevel()
			self.cambio.title='ok'
			Label(self.cambio, text='Mesa pagada con éxito ').grid(row=0,column=1)
			Label(self.cambio, text='Cambio: '+str(self.cambio_total)).grid(row=1,column=1)

			Button(self.cambio,text='Aceptar',command=lambda: destruir(self.cambio)).grid(row=2,column=1)
			self.bandera=1

		if self.bandera == 1:
			self.reiniciar_Mesa()
			self.query='SELECT Ventas FROM meseros WHERE Usuario = ? '
			self.ventas_pasadas=run_Query(self.query,(self.mesero,))
			for row in self.ventas_pasadas:
				self.ventas_ori=row[0]

			self.query='SELECT Propinas FROM meseros WHERE Usuario = ?'
			self.propinas_pasadas=run_Query(self.query,(self.mesero,))
			for row in self.propinas_pasadas:
				self.propinas_ori=row[0]

			self.total_ventas=self.ventas_ori+self.total
			self.propinas_total=self.propinas_ori+float(self.propinas1)

			self.query='UPDATE meseros SET Ventas=?, Propinas=? WHERE Usuario=?'
			self.parameters=(self.total_ventas,self.propinas_total,self.mesero)
			run_Query(self.query,self.parameters)

			self.get_Mesas()

	def reiniciar_Mesa(self):
		self.query='UPDATE mesa SET total=0,mesero="",ocupada=0,personas=0,descuento=0 WHERE num=?'
		run_Query(self.query,(self.mesa,))

		#for platillo in platillos_master:
		#	query='UPDATE mesa SET {} = 0 WHERE num = ?'.format(platillo)
		#	parameters=(mesa,)
		#	run_Query(query,parameters)

		self.query='UPDATE platillos_mesas SET {}=0'.format(self.mesa)
		run_Query(self.query)

	def get_Mesas(self):
		self.records = self.tree.get_children()
		for element in self.records:
		    self.tree.delete(element)

		self.query='SELECT * FROM mesa where ocupada = 0 or mesero = ?'
		self.db_rows=run_Query(self.query,(self.meseroahora,))
		for row in self.db_rows:
		    self.tree.insert('',END,text=row[0],values = row[3])
		print('Actualizada con extito')

class ModificarMeseros:
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

        ttk.Button(frame,text='Agregar',command = self.add_mesero).grid(row=3,columnspan=2, sticky= W + E)

        self.message=Label(text='',fg='red') ###
        self.message.grid(row=3,column=0,columnspan=2,sticky= W + E)###

        self.tree=ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Nombre',anchor=CENTER)
        self.tree.heading('#1',text='Ventas',anchor=CENTER)

        ttk.Button(text= 'Borrar',command= self.delete_mesero).grid(row = 5, column = 0, sticky= W + E )
        ttk.Button(text= 'Editar',command = self.edit_mesero).grid(row = 5, column = 1, sticky= W + E )
        ttk.Button(text= 'Regresar',command = lambda: [destruir(self.wind),crear_Gerente()]).grid(row = 6, column = 0, sticky= W + E )

        self.get_Meseros()

    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result

    def get_Meseros(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query='SELECT * FROM meseros '
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[0],values = row[1])

    def validation(self):
        return len(self.name.get())!=0

    def add_mesero(self):
        if self.validation():
            query='INSERT INTO meseros (Usuario,Ventas,Propinas) VALUES(?,0,0)'
            parameters=(self.name.get(),)
            self.run_query(query,parameters)
            self.message['text']='Mesero {} agregado'.format(self.name.get())
            self.name.delete(0,END)

        else:
            self.message['text']='Llenar nombre'

        self.get_Meseros()

    def delete_mesero(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']= 'Seleccione un registro'
            return

        self.name= self.tree.item(self.tree.selection())['text']
        self.query = 'DELETE from meseros WHERE Usuario = ?'
        self.run_query(self.query,(self.name,))
        self.message['text']= 'Mesero {} actualizado correctamente'.format(self.name)
        self.get_Meseros()

    def edit_mesero(self):
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
        self.get_Meseros()

class ModificarPlatillos:

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

        ttk.Button(frame,text='Agregar',command = self.add_platillo).grid(row=7,columnspan=2, sticky= W + E)

        self.message=Label(text='',fg='red') ###
        self.message.grid(row=3,column=0,columnspan=2,sticky= W + E)###

        self.tree = ttk.Treeview(height=15,columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Nombre',anchor=CENTER)
        self.tree.heading('#1',text='Precio',anchor=CENTER)

        ttk.Button(text= 'Borrar',command= self.delete_platillo).grid(row = 5, column = 0, sticky= W + E )
        ttk.Button(text= 'Editar',command = self.edit_platillo).grid(row = 5, column = 1, sticky= W + E )
        ttk.Button(text= 'Regresar',command = lambda: [destruir(self.wind),crear_Gerente()]).grid(row = 6, column = 0, sticky= W + E )
        ttk.Button(text= 'Actualizar',command = lambda: self.get_platillos()).grid(row = 6, column = 1, sticky= W + E )

        self.get_platillos()

    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result

    def get_platillos(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query='SELECT * FROM platillos '
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[1],values = row[0])
        print("Actualizada con exito")

    def validation1(self):
        return len(self.name.get())!=0 and len(self.precio.get())!=0 and len(self.ingrediente1.get())!=0 and len(self.ingrediente2.get())!=0 and len(self.ingrediente3.get())!=0

    def add_platillo(self):
        print(self.bebidasi.get())
        if self.validation1():
        	if self.bebidasi.get()==0:
	            query='INSERT INTO platillos (precio,nombre,disponible,ingrediente1,ingrediente2,ingrediente3,bebida) VALUES(?,?,1,?,?,?,0)'
	            nombref=self.name.get()
	            preciof=self.precio.get()
	            ingrediente1f=self.ingrediente1.get()
	            ingrediente2f=self.ingrediente2.get()
	            ingrediente3f=self.ingrediente3.get()
	            parameters=(preciof,nombref,ingrediente1f,ingrediente2f,ingrediente3f)

	            #platillos_master.append(nombref)

	            self.run_query(query,parameters)

	        #    query='ALTER TABLE mesa ADD {} text'.format(nombref)
	         #   self.run_query(query)

	          #  query='UPDATE mesa SET {} = 0'.format(nombref)
	           # self.run_query(query)

	            #query = 'UPDATE platillos SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ?'
	            query='INSERT INTO platillos_mesas (platillo,mesa1,mesa2,mesa3,mesa4,mesa5,mesa6,mesa7) VALUES(?,0,0,0,0,0,0,0)'
	            parameters=(nombref,)

	            self.run_query(query,parameters)

	            self.message['text']='Platillo {} agregado'.format(self.name.get())
	            self.name.delete(0,END)
	            self.precio.delete(0,END)
	            self.ingrediente1.delete(0,END)
	            self.ingrediente2.delete(0,END)
	            self.ingrediente3.delete(0,END)
	            #platillos_master.append(self.name.get())

	        elif self.bebidasi.get() ==1:
	            query='INSERT INTO platillos (precio,nombre,disponible,ingrediente1,ingrediente2,ingrediente3,bebida) VALUES(?,?,1,?,?,?,1)'
	            nombref=self.name.get()
	            preciof=self.precio.get()
	            ingrediente1f=self.ingrediente1.get()
	            ingrediente2f=self.ingrediente2.get()
	            ingrediente3f=self.ingrediente3.get()
	            parameters=(preciof,nombref,ingrediente1f,ingrediente2f,ingrediente3f)

	            #platillos_master.append(nombref)

	            self.run_query(query,parameters)

	        #    query='ALTER TABLE mesa ADD {} text'.format(nombref)
	         #   self.run_query(query)

	          #  query='UPDATE mesa SET {} = 0'.format(nombref)
	           # self.run_query(query)

	            #query = 'UPDATE platillos SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ?'
	            query='INSERT INTO platillos_mesas (platillo,mesa1,mesa2,mesa3,mesa4,mesa5,mesa6,mesa7) VALUES(?,0,0,0,0,0,0,0)'
	            parameters=(nombref,)

	            self.run_query(query,parameters)

	            self.message['text']='Bebida {} agregado'.format(self.name.get())
	            self.name.delete(0,END)
	            self.precio.delete(0,END)
	            self.ingrediente1.delete(0,END)
	            self.ingrediente2.delete(0,END)
	            self.ingrediente3.delete(0,END)

	            #platillos_master.append(self.name.get())

        else:
            self.message['text']='Llenar las casillas'

        self.get_platillos()

    def delete_platillo(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']= 'Seleccione un registro'
            return

        name= self.tree.item(self.tree.selection())['text']
        query = 'DELETE from platillos WHERE nombre = ?'
        self.run_query(query,(name,))

        #try:
        #	platillos_master.remove(name)
        #except:
        #	pass

        query='DELETE FROM platillos_mesas WHERE platillo = ?'
        parameters=(name,)
        self.run_query(query,parameters)

        #query='ALTER TABLE mesa DROP COLUMN {} '.format(name)

        #self.run_query(query)

        self.message['text']= 'Platillo {} borrado correctamente'.format(name)
        #platillos_master.remove(self.name.get())
        self.get_platillos()

    def edit_platillo(self):
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

        Button(self.edit_wind,text='Guardar cambios',command= lambda: self.edit_records1(new_name.get(),name,old_price,new_price.get())).grid(row=4,column=2,sticky=W)

    def edit_records1(self,new_name,name,old_price,new_price):
        o=0
        query = 'UPDATE platillos SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ?'
        parameters = (new_name,new_price,name,old_price)
        self.run_query(query,parameters)
        self.edit_wind.destroy()

        #for x in platillos_master:

            #if x == name:
        #        posicion=o
        #    o+=1

        #platillos_master[posicion] = new_name

        #query='ALTER TABLE mesa RENAME COLUMN ? TO ?'

        query = 'UPDATE platillos_mesas SET platillo = ? WHERE platillo = ?'
        parameters = (new_name,name)
        self.run_query(query,parameters)

        self.message['text'] = 'platillo {} actualizado correctamente'.format(name)
        self.get_platillos()

class WindDescuentos:
    def __init__(self,window):
        self.wind = window
        self.wind.title('GESTIONAR DESCUENTOS')
        self.wind.geometry("300x200")

        self.frame=LabelFrame(self.wind, text='Descontar a mesa: ')
        self.message=Label(self.frame,text='',fg='red')
        self.message.grid(row=0,column=0,columnspan=2,sticky=W+E)

        Label(self.frame, text='Mesa: ').grid(row=1,column=0)
        self.mesa=Entry(self.frame)
        self.mesa.grid(row=1,column=1)
        self.mesa.focus()

        Label(self.frame, text='Descuento: ').grid(row=2,column=0)
        self.descuento=Entry(self.frame)
        self.descuento.grid(row=2,column=1)

        Button(self.frame,text='Descontar',command=lambda: self.descontar_Mesa()).grid(row=3,column=0,sticky=W+E)
        Button(self.frame,text='Regresar',command=lambda: [destruir(self.wind),crear_Gerente()]).grid(row=3,column=1,sticky=W+E)
        self.frame.pack(side='top',anchor='n')

    def descontar_Mesa(self):
        self.window=self.wind
        self.bandera=0
        self.query='SELECT * FROM mesa WHERE ocupada = 1 AND num = ?'
        self.parameters=(self.mesa.get(),)

        self.mesasd=run_Query(self.query,self.parameters)

        for row in self.mesasd:
        	self.bandera = 1

        if self.bandera ==1:
        	self.query='UPDATE mesa SET descuento= ? WHERE num=?'
        	self.parameters=(self.descuento.get(),self.mesa.get())
        	run_Query(self.query,self.parameters)
        	self.message['text']='Descuento aplicado a mesa {}'.format(self.mesa.get())
        	self.mesa.delete(0,END)
        	self.descuento.delete(0,END)
        else:
        	self.message['text']='Mesa vacía o no encontrada'

class WindBloquear:
    def __init__(self,window):
        self.wind = window
        self.wind.title('GESTIONAR INGREDIENTES')
        self.wind.geometry("300x200")

        self.frame=LabelFrame(self.wind, text='Opciones: ')

        Button(self.frame,text='Bloquear platillos',command=lambda: self.bloqueo_Platillo()).grid(row=0,column=0,sticky=W+E)
        Button(self.frame,text='Desbloquear platillos',command=lambda: self.desbloqueo_Platillo()).grid(row=1,column=0,sticky=W+E,pady=10)
        Button(self.frame,text='Regresar',command=lambda: [destruir(self.wind),crear_Gerente()]).grid(row=2,column=0,sticky=W+E)
        self.frame.pack(side='top',anchor='n')

    def bloqueo_Platillo(self):
        self.bloqueo_wind=Toplevel()
        self.bloqueo_wind.title='Ingredientes'
        self.frame=LabelFrame(self.bloqueo_wind, text='Bloquear platillos con: ')

        self.message=Label(self.frame,text='',fg='red')
        self.message.grid(row=0,column=0,columnspan=2,sticky=W+E)

        Label(self.frame, text='Ingrediente: ').grid(row=1,column=0)
        self.producto=Entry(self.frame)
        self.producto.grid(row=1,column=1)
        self.producto.focus()

        Button(self.frame,text='Bloquear',command=lambda: self.bloquear_Accion()).grid(row=2,column=0,sticky=W+E)
        Button(self.frame,text='Regresar',command=lambda: destruir(self.bloqueo_wind)).grid(row=2,column=1,sticky=W+E)

        self.frame.pack(side='top',anchor='n')

    def bloquear_Accion(self):
    	self.banderab=0
    	self.productob=self.producto.get()
    	self.query='SELECT nombre from platillos WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ?'
    	self.parameters=(self.productob,self.productob,self.productob)
    	self.platos=run_Query(self.query,self.parameters)

    	for row in  self.platos:
    		#platillos_master.remove(productob)
    		self.banderab=1

    	if self.banderab==1:
    		self.query='UPDATE platillos SET disponible = 0 WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ? '
    		self.parameters=(self.productob,self.productob,self.productob)
    		run_Query(self.query,self.parameters)

    		self.message['text']='Platillos con {} bloqueados'.format(self.producto.get())
    		self.producto.delete(0,END)

    	else:
    		self.message['text']='{} no encontrado'.format(self.producto.get())
    		self.producto.delete(0,END)

    def desbloqueo_Platillo(self):
    	self.bloqueo_wind=Toplevel()
    	self.bloqueo_wind.title='Ingredientes'
    	self.frame=LabelFrame(self.bloqueo_wind, text='Desbloquear platillos con: ')

    	self.message=Label(self.frame,text='',fg='red')
    	self.message.grid(row=0,column=0,columnspan=2,sticky=W+E)

    	Label(self.frame, text='Ingrediente: ').grid(row=1,column=0)
    	self.producto=Entry(self.frame)
    	self.producto.grid(row=1,column=1)
    	self.producto.focus()

    	Button(self.frame,text='Desbloquear',command=lambda: self.desbloquear_Accion()).grid(row=2,column=0,sticky=W+E)
    	Button(self.frame,text='Regresar',command=lambda: destruir(self.bloqueo_wind)).grid(row=2,column=1,sticky=W+E)

    	self.frame.pack(side='top',anchor='n')

    def desbloquear_Accion(self):
    	self.banderab=0
    	self.productob=self.producto.get()
    	self.query='SELECT * from platillos WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ?'
    	self.parameters=(self.productob,self.productob,self.productob)
    	self.platos=run_Query(self.query,self.parameters)

    	for row in  self.platos:
    		#platillos_master.remove(productob)
    		self.banderab=1

    	if self.banderab==1:
    		self.query='UPDATE platillos SET disponible = 1 WHERE ingrediente1 = ? OR ingrediente2 = ? OR ingrediente3 = ? '
    		self.parameters=(self.productob,self.productob,self.productob)
    		run_Query(self.query,self.parameters)

    		self.message['text']='Platillos con {} desbloqueados'.format(self.producto.get())
    		self.producto.delete(0,END)

    	else:
    		self.message['text']='{} no encontrado'.format(self.producto.get())
    		self.producto.delete(0,END)

class WindVentas:
    def __init__(self,window):
        self.ventas_wind = window
        self.ventas_wind.title='Gestionar ventas'
        self.fecha=str(date.today())

        self.message=Label(self.ventas_wind,text='Ventas del día '+self.fecha)
        self.message.grid(row=0,column=0,columnspan=2,sticky=W+E)

        self.frame=LabelFrame(self.ventas_wind,text='Ventas por mesero: ')
        self.frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.tree=ttk.Treeview(self.frame,height=10,columns=2)
        self.tree.grid(row=1,column=0,pady=10,sticky=W+E)
        self.tree.heading('#0',text='Mesero',anchor=CENTER)
        self.tree.heading('#1',text='Ventas',anchor=CENTER)

        self.get_Ventas()

        self.frame2=LabelFrame(self.ventas_wind,text='Ventas totales: ')
        self.frame2.grid(row=2, column=0, columnspan=3, pady=10)

        self.query='SELECT ventas FROM meseros'
        self.db_rows=run_Query(self.query)

        self.total=0

        for row in self.db_rows:
        	self.total=self.total+row[0]

        self.total_st=str(self.total)+'0'

        Label(self.frame2,text='Efectivo: ').grid(row=0,column=0)
        Entry(self.frame2,textvariable=StringVar(self.frame2,value=self.total_st),state='readonly').grid(row=0,column=1)

        self.get_Ventas()

        Button(self.ventas_wind,text='TERMINAR  DÍA',command= lambda: self.terminar_Dia()).grid(row=3,column=0,sticky=W+E)
        Button(self.ventas_wind,text='Regresar',command=lambda: destruir(self.ventas_wind)).grid(row=3,column=1,sticky=E)

    def get_Ventas(self):
        self.records = self.tree.get_children()

        for element in self.records:
        	self.tree.delete(element)

        self.query='SELECT * FROM meseros'
        self.db_rows=run_Query(self.query)

        for row in self.db_rows:
        	self.tree.insert('',0,text=row[0],values = row[1])

        print("Actualizada con exito")

    def terminar_Dia(self):
        self.wind = self.ventas_wind
        self.bandera=0
        self.fecha=str(date.today())
        self.query='SELECT * FROM mesa WHERE ocupada=1'
        self.ocupadas=run_Query(self.query)

        for row in self.ocupadas:
        	self.bandera=1

        if self.bandera==1:
        	self.error_Terminar()

        if self.bandera==0:
        	self.query='UPDATE meseros SET Ventas=0,Propinas=0'
        	run_Query(self.query)
        	self.query='INSERT INTO ventas (dia,total) VALUES(?,?)'
        	self.parameters=(self.fecha,self.total)
        	run_Query(self.query,self.parameters)

        	self.error_wind=Toplevel()
        	self.error_wind.title='error'

        	self.frame=LabelFrame(self.error_wind,text='')
        	self.frame.grid(row=0,column=0,columnspan=3,pady=10)

        	Label(self.frame,text='Día terminado').grid(row=0,column=0)
        	Button(self.frame,text='Salir',command=lambda: quit()).grid(row=1,column=0,sticky=W+E)

    def error_Terminar(self):
        self.error_wind=Toplevel()
        self.error_wind.title='error'

        self.frame=LabelFrame(self.error_wind,text='')
        self.frame.grid(row=0,column=0,columnspan=3,pady=10)

        Label(self.frame,text='ERROR: Hay mesas ocupadas').grid(row=0,column=0)
        Button(self.frame,text='Regresar',command=lambda: destruir(self.error_wind)).grid(row=1,column=0,sticky=W+E)

class WindVentasMes:
    def __init__(self,window):
        self.ventas_wind = window
        self.ventas_wind.title='Ver ventas'

        self.message=Label(self.ventas_wind,text='Ventas ')
        self.message.grid(row=0,column=0,columnspan=2)

        self.frame=LabelFrame(self.ventas_wind,text='')
        self.frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.tree=ttk.Treeview(self.frame,height=15,columns=2)
        self.tree.grid(row=1,column=0,pady=10,sticky=W+E)
        self.tree.heading('#0',text='Día',anchor=CENTER)
        self.tree.heading('#1',text='Total',anchor=CENTER)

        self.get_Ventastotales()

        Button(self.frame,text='Generar gráfico',command=lambda: self.generar_Grafico()).grid(row=2,column=0,sticky=W+E)
        Button(self.frame,text='Regresar',command=lambda: destruir(self.ventas_wind)).grid(row=3,column=0,sticky=W+E)

    def get_Ventastotales(self):
        self.records = self.tree.get_children()

        for element in self.records:
        	self.tree.delete(element)

        self.query='SELECT * FROM ventas'
        self.db_rows=run_Query(self.query)

        for row in self.db_rows:
        	self.tree.insert('',0,text=row[0],values = row[1])

    def generar_Grafico(self):
        i=0
        lista=[]
        total=0
        root = Tk()
        root.wm_title("Gráfico de ventas")

        fig = Figure(figsize=(13,5), dpi=100)

        tabla = self.get_VentasA()

        for row in tabla:
        	total+=1

        x = np.ones(total,dtype=str)
        y = np.ones(total,dtype=float)

        tabla2 = self.get_VentasA()

        for row2 in tabla2:
        	lista.append(row2[0][5:10])
        	y[i]=row2[1]
        	i+=1
        x=np.array(lista)
        print(x)
        print(y)

        fig.add_subplot(111).bar(x, y, edgecolor='black')

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()

        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)


        canvas.mpl_connect("key_press_event", on_key_press)

        def _quit():
            root.quit()     # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = Button(master=root, text="  Regresar  ", command=_quit)
        button.pack(side=BOTTOM)

        mainloop()

    def get_VentasA(self):
        query='SELECT * FROM ventas'

        return run_Query(query)


class WindWaiter(PagarCuenta):
    def __init__(self,window,id):
        self.wind = window
        self.meseroahora=id
        self.mesero = id
        self.wind.title(nombre_Restaurante + '  || '+ self.mesero)

        self.frame=LabelFrame(self.wind, text='Mesas disponibles o asignadas:')
        self.frame.grid(row=0, column=1, columnspan=3, pady=10)

        self.message=Label(self.frame,text='',fg='red') ###
        self.message.grid(row=0,column=1,columnspan=2,sticky= W + E)###

        self.tree=ttk.Treeview(self.frame,height=11,columns=2)
        self.tree.grid(row=1,column=1,pady=10)
        self.tree.heading('#0',text='Mesa',anchor=CENTER)
        self.tree.heading('#1',text='Total',anchor=CENTER)

        self.get_Mesas()

           # ttk.Button(text='Imprimir cuenta').grid(row=2,column=0)
        ttk.Button(self.frame,text='Editar mesa',command=lambda: self.editar_Mesa()).grid(row=2,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Pagar cuenta',command=lambda: self.pagar_Cuenta(0,0)).grid(row=3,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Actualizar tabla',command=lambda: self.get_Mesas()).grid(row=4,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Salir',command=lambda:[destruir(self.wind),crear_Inicio()]).grid(row=5,column=1,sticky=W+E)

    def pagar_Cuenta(self,s,p):

        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona una mesa'
            return
        else:
            self.message['text'] = ''

        PagarCuenta.__init__(self,self.tree,s,p,self.meseroahora)

    def editar_Mesa(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona una mesa'
            return
        else:
            self.message['text'] = ''

        self.editar_wind=Toplevel()
        self.editar_wind.title = 'Editar mesa'

        self.mesa=self.tree.item(self.tree.selection())['text']

        self.query='SELECT * FROM mesa where num = ?'

        self.mesa_datos=run_Query(self.query,(self.mesa,))

        for row in self.mesa_datos:
        	self.numero_mesa=row[0]
        	self.personas=row[2]
        	self.total=row[3]
        	self.meseropasado=row[4]

        Label(self.editar_wind, text='Editar mesa No. ' + str(self.mesa)).grid(row=0,column=0)
        Label(self.editar_wind, text='Personas: ').grid(row=1,column=0)
        self.Nuevas_personas=Entry(self.editar_wind,textvariable=StringVar(self.editar_wind,value=self.personas))
        self.Nuevas_personas.grid(row=1,column=1)
        #

        Label(self.editar_wind, text='Mesero: ').grid(row=2,column=0)
        self.Nuevo_mesero=Entry(self.editar_wind,textvariable=StringVar(self.editar_wind,value=self.meseropasado))
        self.Nuevo_mesero.grid(row=2,column=1)

        #Agregar platillo
        self.frame=LabelFrame(self.editar_wind, text='Platillos')
        self.frame.grid(row=3, column=0, columnspan=3, pady=10)

        self.tree_platillos=ttk.Treeview(self.frame,height=15,columns=('Precio','Cantidad'))
        #tree_platillos['columns']=('one','two')

        self.tree_platillos.heading('#0',text='Nombre',anchor=CENTER)
        self.tree_platillos.heading('#1',text='Precio',anchor=CENTER)
        self.tree_platillos.heading('#2',text='Cantidad',anchor=CENTER)
        self.tree_platillos.grid(row=5,column=1,pady=10)

        self.get_Platillos()

        Label(self.frame,text='Total').grid(row=6,column=1,sticky=E)
        Entry(self.frame,textvariable=StringVar(self.frame,value=self.total),state='readonly').grid(row=6,column=2,sticky=W)

        Button(self.frame,text='Agregar',command=lambda: self.agregar_Plato()).grid(row=7,column=1,sticky=E)
        Button(self.frame,text='Quitar',command=lambda: self.quitar_Plato()).grid(row=7,column=2,sticky=W)

        Button(self.editar_wind,text='Aceptar',command=lambda: self.modificar_Mesa()).grid(row=6,column=0,sticky=E)
        Button(self.editar_wind,text='Regresar',command=lambda: self.editar_wind.destroy()).grid(row=6,column=2,sticky=W)

    def get_Platillos(self):
        self.lista=[]
        self.records = self.tree_platillos.get_children()

        for element in self.records:
            self.tree_platillos.delete(element)

        self.query='SELECT * FROM platillos'
        #query2='SELECT * FROM mesa WHERE num=?'
        self.query3='SELECT * FROM platillos_mesas  '

        #db_platillos=run_Query(query2,(mesa,))
        self.db_rows=run_Query(self.query)

        self.db_numerosplatillos=run_Query(self.query3,)

        self.nummesa=int(self.mesa[4])

        for row in self.db_numerosplatillos:
            self.lista.append(row[self.nummesa])

        i=0

        for row in self.db_rows:
            self.tree_platillos.insert('',END,text=row[1],values = (row[0],self.lista[i])) #lista[i]
            i+=1

        print('Actualizada con exito')

    def agregar_Plato(self):
        self.platillo=self.tree_platillos.item(self.tree_platillos.selection())['text']
        self.cantidad=self.tree_platillos.item(self.tree_platillos.selection())['values'][1]

        self.cantidad+=1

        self.query='SELECT disponible from platillos WHERE nombre = ?'
        self.disponibilidad_db=run_Query(self.query,(self.platillo,))

        for row in self.disponibilidad_db:
        	self.disponibilidad=row[0]

        if self.disponibilidad==1:
            self.query='SELECT precio from platillos Where nombre=?'
            self.precio=run_Query(self.query,(self.platillo,))
            for row in self.precio:
            	self.precio_platillo=row[0]

            self.query='SELECT total from mesa Where num=?'
            self.precio=run_Query(self.query,(self.mesa,))
            for row in self.precio:
            	self.precio_mesa=row[0]

            self.precio_total=self.precio_platillo+self.precio_mesa

            self.query='UPDATE mesa SET total=? WHERE num = ?'
            self.parameters=(self.precio_total,self.mesa)
            run_Query(self.query,self.parameters)

            self.query='UPDATE platillos_mesas SET {} = {} WHERE platillo = ? '.format(self.mesa,self.cantidad,self.platillo)

            self.platillosss=run_Query(self.query,(self.platillo,))

            for row in self.platillosss:
            	print(row)

            self.get_Platillos()

            Entry(self.frame,textvariable=StringVar(self.frame,value=self.precio_total),state='readonly').grid(row=6,column=2,sticky=W)

        else:
            self.error=Toplevel()
            self.error.title='Platillo bloqueado'
            Label(self.error, text='Platillo bloqueado ').grid(row=0,column=1)
            Button(self.error,text='Regresar',command=lambda: destruir(self.error)).grid(row=1,column=1)
            print('Platillo bloqueado')

    def quitar_Plato(self):
        self.platillo=self.tree_platillos.item(self.tree_platillos.selection())['text']
        self.cantidad=self.tree_platillos.item(self.tree_platillos.selection())['values'][1]

        self.query='SELECT precio from platillos Where nombre=?'
        self.precio=run_Query(self.query,(self.platillo,))
        for row in self.precio:
            self.precio_platillo=row[0]

        self.query='SELECT total from mesa Where num=?'
        self.precio=run_Query(self.query,(self.mesa,))
        for row in self.precio:
            self.precio_mesa=row[0]

        self.precio_total=self.precio_mesa-self.precio_platillo


        if self.cantidad>0:
            self.cantidad-=1
            #query='UPDATE mesa SET {} = ? WHERE num = ?'.format(platillo)
            #parameters=(cantidad,mesa)
            #run_Query(query,parameters)

            self.query='UPDATE platillos_mesas SET {} = {} WHERE platillo = ? '.format(self.mesa,self.cantidad,self.platillo)
            self.platillosss=run_Query(self.query,(self.platillo,))

            self.query='UPDATE mesa SET total=? WHERE num = ?'.format(self.platillo)
            self.parameters=(self.precio_total,self.mesa)
            run_Query(self.query,self.parameters)
            Entry(self.frame,textvariable=StringVar(self.frame,value=self.precio_total),state='readonly').grid(row=6,column=2,sticky=W)
            self.get_Platillos()

    def modificar_Mesa(self):
        self.num = self.mesa
        self.personas = self.Nuevas_personas.get()
        self.personas= int(self.personas)
        self.meseroactual = self.mesero
        self.mesero = self.Nuevo_mesero.get()

        if self.mesero!='' and self.personas!=0: #
            self.query= 'UPDATE mesa SET personas= ?,mesero=?,ocupada=1 WHERE num=? '
            self.parameters=(self.personas,self.mesero,self.num)
            run_Query(self.query,self.parameters)
            print('MESERO = ALGO Y PERSONAS = DIF0 ')

        elif self.mesero=='' and self.personas!=0:#
            self.mesero=self.meseroactual
            self.query= 'UPDATE mesa SET personas= ?,mesero=?,ocupada=1 WHERE num=? '
            self.parameters=(self.personas,self.meseroactual,self.num)
            run_Query(self.query,self.parameters)
            print('MESERO =NADA Y PERSONAS = DIF0 ')

        elif self.mesero!='' and self.personas==0:#
            self.personas=1
            self.query= 'UPDATE mesa SET personas= 1,mesero=?,ocupada=1 WHERE num=? '
            self.parameters=(self.mesero,self.num)
            run_Query(self.query,self.parameters)
            print('MESERO = ALGO Y PERSONAS = 0 ')

        elif self.mesero=='' and self.personas==0:#
            #self.query= 'UPDATE mesa SET personas= 0,mesero=0 ,ocupada=0 WHERE num=? '
            #run_Query(self.query,(self.num,))
            print('MESERO = NADA Y PERSONAS = 0 ')

        self.editar_wind.destroy()

        self.get_Mesas()

    def get_Mesas(self):
        self.records = self.tree.get_children()
        for element in self.records:
            self.tree.delete(element)

        self.query='SELECT * FROM mesa where ocupada = 0 or mesero = ?'
        self.db_rows=run_Query(self.query,(self.meseroahora,))
        for row in self.db_rows:
            self.tree.insert('',END,text=row[0],values = row[3])
        print('Actualizada con extito')

class WindGerente(ModificarMeseros,ModificarPlatillos,WindDescuentos,WindBloquear,WindVentas,WindVentasMes):
    def __init__(self,window,id):
        self.wind = window
        self.gerente = id

        self.wind.title(nombre_Restaurante + '  || '+ self.gerente)

        self.frame=LabelFrame(self.wind, text='Acciones: ')
        self.frame.grid(row=2, column=1, columnspan=3, pady=10)

        ttk.Button(self.frame,text='Agregar/Quitar mesero',command=lambda: self.editar_Meseros()).grid(row=2,column=1,sticky=W+E,pady=10)
        ttk.Button(self.frame,text='Descontar cuenta',command=lambda: self.descontar_Cuentas()).grid(row=3,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Modificar platillos',command=lambda: self.modificar_Platillos()).grid(row=4,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Bloquear ingredientes',command=lambda: self.bloquear_Platillos()).grid(row=5,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Modificar id',command=lambda: self.modificar_Usuario()).grid(row=6,column=1,sticky=W+E,pady=10)
        ttk.Button(self.frame,text='Gestionar día',command=lambda: self.Ventas()).grid(row=7,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Ver mesas',command=lambda: self.VerMesas()).grid(row=8,column=1,sticky=W+E)
        ttk.Button(self.frame,text='Ver ventas',command=lambda: self.ventas_Totales()).grid(row=9,column=1,sticky=W+E,pady=10)
        ttk.Button(self.frame,text='Salir',command=lambda:[destruir(self.wind),crear_Inicio()]).grid(row=10,column=1,sticky=W+E)

        self.frame.pack(side='top',anchor='n')

    def editar_Meseros(self):
        self.wind.destroy()
        self.window=Tk()
        #application=Meseros(window)
        ModificarMeseros.__init__(self,self.window)

        self.window.mainloop()

    def modificar_Platillos(self):
        self.wind.destroy()
        self.window=Tk()
        #application=Platillosn(window)
        ModificarPlatillos.__init__(self,self.window)

        self.window.mainloop()

    def descontar_Cuentas(self):
        self.wind.destroy()
        self.window2=Tk()
        #application=wind_descuentos(window2)
        WindDescuentos.__init__(self,self.window2)

        self.window2.mainloop()

    def bloquear_Platillos(self):
        self.wind.destroy()
        self.window2=Tk()
        #ventana=wind_bloquear(self.window2)
        WindBloquear.__init__(self,self.window2)

        self.window2.mainloop()

    def modificar_Usuario(self):
        self.modificar_wind=Toplevel()
        self.modificar_wind.title='Modificar usuario'

        self.message=Label(self.modificar_wind,text='',fg='red')
        self.message.grid(row=0,column=0,columnspan=2,sticky=W+E)

        Label(self.modificar_wind,text='Nuevo usuario: ').grid(row=1,column=0)
        self.nuevo_usuario=Entry(self.modificar_wind)
        self.nuevo_usuario.grid(row=1,column=1)
        self.nuevo_usuario.focus()

        Label(self.modificar_wind,text='Nueva contraseña: ').grid(row=2,column=0)
        self.nueva_contra=Entry(self.modificar_wind,show='*')
        self.nueva_contra.grid(row=2,column=1)

        Label(self.modificar_wind,text='Confirmar contraseña: ').grid(row=3,column=0)
        self.nuevo_contra2=Entry(self.modificar_wind,show='*')
        self.nuevo_contra2.grid(row=3,column=1)

        Label(self.modificar_wind,text=' ').grid(row=4,column=0)

        Button(self.modificar_wind,text='Guardar',command=lambda: self.editar_Id()).grid(row=5,column=0,sticky=E)
        Button(self.modificar_wind,text='Salir',command=lambda: destruir(self.modificar_wind)).grid(row=5,column=1,sticky=W)

    def editar_Id(self):
        self.user=self.nuevo_usuario
        self.passw = self.nueva_contra
        self.passw2 = self.nuevo_contra2
        if self.passw.get() != self.passw2.get():
            self.message['text']='Las contraseñas no coinciden'

        else:
            self.query='UPDATE gerentes SET usuario=?,contraseña=? WHERE registro = 2'
            self.parameters=(self.user.get(),self.passw.get())
            run_Query(self.query,self.parameters)
            self.message['text']='Id y contraseña actualizados'
            self.user.delete(0,END)
            self.passw.delete(0,END)
            self.passw2.delete(0,END)

    def Ventas(self):
        self.ventas_wind=Toplevel()

        WindVentas.__init__(self,self.ventas_wind)

    def VerMesas(self):

        self.window = Toplevel()
        self.window.title(nombre_Restaurante + '  ||  Mesas')

        self.frame=LabelFrame(self.window, text='Mesas: ')
        self.frame.grid(row=0, column=1, columnspan=3, pady=10)

        self.tree2=ttk.Treeview(self.frame,height=10,columns=('Mesero','Total','Descuento'))
        self.tree2.grid(row=0,column=0,pady=10)
        self.tree2.heading('#0',text='Mesa',anchor=CENTER)
        self.tree2.heading('#1',text='Mesero',anchor=CENTER)
        self.tree2.heading('#2',text='Total',anchor=CENTER)
        self.tree2.heading('#3',text='Descuento',anchor=CENTER)

        self.query = 'SELECT num,total,mesero,descuento FROM mesa '
        self.mesasn = run_Query(self.query)
        #for row in mesasn:
        #    print(row)
        self.records = self.tree2.get_children()

        for element in self.records:
            self.tree2.delete(element)

        for row in self.mesasn:
            self.tree2.insert('',END,text=row[0],values = (row[2],row[1],row[3]))
        print('Actualizada con extito')



        Button(self.frame,text='   Regresar   ',command=lambda: destruir(self.window)).grid(row=1,column=0,sticky=E)

        self.window.mainloop()

    def ventas_Totales(self):
        self.ventas_wind=Toplevel()
        WindVentasMes.__init__(self,self.ventas_wind)

class WindCheff:

	def __init__(self,window,id):
		self.wind = window
		self.wind.title('Lista de platillos || CHEFF')
		self.ID = id
		self.wind.geometry("1230x350")

		self.frame=LabelFrame(self.wind, text='Platillos Nuevos: ')
		self.frame.grid(row=0, column=0, columnspan=3, pady=10)

		self.frame1=LabelFrame(self.wind, text='Platillos en preparación: ')
		self.frame1.grid(row=0, column=4, columnspan=3, pady=10)

		self.frame2=LabelFrame(self.wind, text='Platillos listos: ')
		self.frame2.grid(row=0, column=8, columnspan=3, pady=10)

		self.tree0=ttk.Treeview(self.frame,height=10,columns=('Cantidad'))
		self.tree0.grid(row=0,column=0,pady=10)
		self.tree0.heading('#0',text='Platillo',anchor=CENTER)
		self.tree0.heading('#1',text='Cantidad',anchor=CENTER)

		self.tree3=ttk.Treeview(self.frame1,height=10,columns=('Cantidad'))
		self.tree3.grid(row=0,column=0,pady=10)
		self.tree3.heading('#0',text='Platillo',anchor=CENTER)
		self.tree3.heading('#1',text='Cantidad',anchor=CENTER)

		self.tree4=ttk.Treeview(self.frame2,height=10,columns=('Cantidad'))
		self.tree4.grid(row=0,column=0,pady=10)
		self.tree4.heading('#0',text='Platillo',anchor=CENTER)
		self.tree4.heading('#1',text='Cantidad',anchor=CENTER)

		self.cargar_Datos()

		ttk.Button(self.wind,text='Salir',command=lambda:[destruir(self.wind),crear_Inicio()]).grid(row=1,column=0,sticky=W+E)#
		ttk.Button(self.wind,text='Actualizar',command=lambda:self.actualizar_Datos()).grid(row=1,column=4,sticky=W+E)
		ttk.Button(self.wind,text='Cargar datos',command=lambda: self.cargar_Datos()).grid(row=1,column=8,sticky=W+E)

		ttk.Button(self.frame,text='Pasar a preparación',command=lambda:self.pasar_Preparacionp()).grid(row=2,column=0,sticky=W+E)

		ttk.Button(self.frame1,text='Regresar a Fila',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=W)
		ttk.Button(self.frame1,text='Marcar Listo',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=E)

		ttk.Button(self.frame2,text='Regresar a preparación',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=W)
		ttk.Button(self.frame2,text='Eliminar',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=E)

	def cargar_Datos(self):

		self.query='DELETE from controlcheffbarra WHERE bebida = 0'
		run_Query(self.query)

		self.query = 'SELECT * FROM platillos_mesas WHERE mesa1!=0 OR mesa2!=0 OR mesa3!=0 OR mesa4!=0 OR mesa5!=0 OR mesa6!=0 OR mesa7!=0  '
		self.mesasn = run_Query(self.query)
		self.records = self.tree0.get_children()

		for element in self.records:
		    self.tree0.delete(element)

		for row in self.mesasn:
			self.totalplatillo=row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+row[7]
			print('agregando ',self.totalplatillo,' ',row[0])
			self.query='SELECT bebida FROM platillos where nombre = ?'
			self.parameters = (row[0],)
			self.bebidasis=run_Query(self.query,self.parameters)
			print('seleccionado los datos de bebidas')

			for x in self.bebidasis:
				self.banderab = x[0]

			if self.banderab == 0:
				self.query='INSERT INTO controlcheffbarra (nombre,cantidad,estado,bebida) VALUES (?,?,?,?)'
				self.parameters =(row[0],self.totalplatillo,0,0)
				#run_Query(self.query,self.parameters)
				print('Insertado datos en controlcheffbarra')

				self.tree0.insert('',END,text=row[0],values = self.totalplatillo)

		print('Actualizada con extito')

	def pasar_Preparacionp(self):

		try:
		    self.tree0.item(self.tree0.selection())['text'][0]

		except IndexError as e:
			print('No se selecciono nada')
			return
		else:
			self.cantidad = self.tree0.item(self.tree0.selection())['values'][0]
			if self.cantidad > 1:
				self.platillos = self.tree0.item(self.tree0.selection())['text']
				self.tree0.insert('',END,text=self.platillos,values = self.cantidad-1)
				self.tree0.delete(self.tree0.selection())
			else:
				self.tree0.delete(self.tree0.selection())


	def actualizar_Datos(self):
		pass

class WindBar:
	def __init__(self,window,id):
		self.wind = window
		self.wind.title('Lista de bebidas || CHEFF')
		self.ID = id
		self.wind.geometry("1230x350")

		self.frame=LabelFrame(self.wind, text='Bebidas Nuevas: ')
		self.frame.grid(row=0, column=0, columnspan=3, pady=10)

		self.frame1=LabelFrame(self.wind, text='Bebidas en preparación: ')
		self.frame1.grid(row=0, column=4, columnspan=3, pady=10)

		self.frame2=LabelFrame(self.wind, text='Bebidas listos: ')
		self.frame2.grid(row=0, column=8, columnspan=3, pady=10)

		self.tree0=ttk.Treeview(self.frame,height=10,columns=('Cantidad'))
		self.tree0.grid(row=0,column=0,pady=10)
		self.tree0.heading('#0',text='Bebida',anchor=CENTER)
		self.tree0.heading('#1',text='Cantidad',anchor=CENTER)

		self.tree3=ttk.Treeview(self.frame1,height=10,columns=('Cantidad'))
		self.tree3.grid(row=0,column=0,pady=10)
		self.tree3.heading('#0',text='Bebida',anchor=CENTER)
		self.tree3.heading('#1',text='Cantidad',anchor=CENTER)

		self.tree4=ttk.Treeview(self.frame2,height=10,columns=('Cantidad'))
		self.tree4.grid(row=0,column=0,pady=10)
		self.tree4.heading('#0',text='Bebida',anchor=CENTER)
		self.tree4.heading('#1',text='Cantidad',anchor=CENTER)

		ttk.Button(self.wind,text='Salir',command=lambda:[destruir(self.wind),crear_Inicio()]).grid(row=1,column=0,sticky=W+E)#
		ttk.Button(self.wind,text='Actualizar',command=lambda:self.actualizar_Datos()).grid(row=1,column=4,sticky=W+E)
		ttk.Button(self.wind,text='Cargar datos',command=lambda: self.cargar_Datosb()).grid(row=1,column=8,sticky=W+E)

		ttk.Button(self.frame,text='Pasar a preparación',command=lambda: self.pasar_Preparacion()).grid(row=2,column=0,sticky=W+E)

		ttk.Button(self.frame1,text='Regresar a Fila',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=W)
		ttk.Button(self.frame1,text='Marcar Listo',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=E)

		ttk.Button(self.frame2,text='Regresar a preparación',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=W)
		ttk.Button(self.frame2,text='Eliminar',command=lambda:self.actualizar_Datos()).grid(row=2,column=0,sticky=E)

	def cargar_Datosb(self):

		self.query='DELETE from controlcheffbarra WHERE bebida = 1'
		run_Query(self.query)

		self.query = 'SELECT * FROM platillos_mesas WHERE mesa1!=0 OR mesa2!=0 OR mesa3!=0 OR mesa4!=0 OR mesa5!=0 OR mesa6!=0 OR mesa7!=0  '
		self.mesasn = run_Query(self.query)
		self.records = self.tree0.get_children()

		for element in self.records:
		    self.tree0.delete(element)

		for row in self.mesasn:
			self.totalplatillo=row[1]+row[2]+row[3]+row[4]+row[5]+row[6]+row[7]
			print('agregando ',self.totalplatillo,' ',row[0])
			self.query='SELECT bebida FROM platillos where nombre = ?'
			self.parameters = (row[0],)
			self.bebidasis=run_Query(self.query,self.parameters)
			print('seleccionado los datos de bebidas')

			for x in self.bebidasis:
				self.banderab = x[0]

			if self.banderab == 0:
				self.query='INSERT INTO controlcheffbarra (nombre,cantidad,estado,bebida) VALUES (?,?,?,?)'
				self.parameters =(row[0],self.totalplatillo,0,0)
				run_Query(self.query,self.parameters)
				print('Insertado datos en controlcheffbarra')

				self.tree0.insert('',END,text=row[0],values = self.totalplatillo)

		print('Actualizada con extito')

	def pasar_Preparacion(self):
		print('dentro de la funcion')
		try:
		    self.tree0.item(self.tree0.selection())['text'][0]

		except IndexError as e:
			print('No se selecciono nada')
			return

		self.tree0.delete(self.tree0.selection())

	def actualizar_Datos(self):
		pass

class VentanaPrincipal(WindWaiter,WindGerente,WindBar,WindCheff):
    def __init__(self,window):
        self.wind = window
        self.wind.title(nombre_Restaurante)

        self.frame = LabelFrame(self.wind, text = 'Inicio')
        self.frame.grid(row = 0,column = 0,columnspan = 3,pady = 20,sticky = W+E)
        self.frame.config(width = '200',height = '200')
        self.frame.pack(side = 'top',anchor = 'n')

        ttk.Button(self.frame,text = 'Iniciar sesion',command = lambda: self.meter_Id()).grid(row = 3,columnspan = 2,sticky = W+E)
        ttk.Button(self.frame,text = 'salir',command = lambda: destruir(window)).grid(row = 4,columnspan = 2,sticky = W+E)

    def meter_Id(self):

        self.introducirWind = Toplevel()
        self.introducirWind.title = 'Iniciar sesión'

        Label(self.introducirWind,text= 'ID').grid(row=0,column=1)
        self.ID = Entry(self.introducirWind)
        self.ID.focus()
        self.ID.grid(row=0,column=2)

        Button (self.introducirWind, text='Iniciar',command= lambda: self.comprobar_Id()).grid(row=1,column=2,sticky=W)

    def comprobar_Id(self):
        self.bandera = 0
        self.IDD = self.ID.get()

        self.query1 = 'SELECT usuario FROM gerentes WHERE usuario = ?'
        self.query2 = 'SELECT Usuario FROM meseros WHERE Usuario = ?'
        self.consulta = run_Query(self.query1,(self.IDD,))

        if self.IDD!='cheff' and self.IDD!='barra':

            for row in self.consulta:
                if row[0] == self.IDD:
                    self.bandera = 1
                    self.meter_Password()

            if self.bandera == 0:
                self.consulta = run_Query(self.query2,(self.IDD,))
                for row in self.consulta:
                    if row[0]==self.IDD:
                        self.bandera=1
                        self.wind.destroy()
                        self.nuevaVentana =Tk()
                        self.nuevaVentana.geometry("400x400")

                        WindWaiter.__init__(self,self.nuevaVentana,self.IDD)
    					#self.ventana = WindWaiter(self.nuevaVentana,self.ID)

                        self.nuevaVentana.mainloop()

        elif self.IDD == 'cheff':
            self.bandera=1
            self.wind.destroy()
            self.nuevaVentana =Tk()
            self.nuevaVentana.geometry("400x400")
            WindCheff.__init__(self,self.nuevaVentana,self.IDD)
            #self.ventana = Wind_cheff(self.nuevaVentana)
            self.nuevaVentana.mainloop()

        elif self.IDD == 'barra':
            self.bandera=1
            self.wind.destroy()
            self.nuevaVentana =Tk()
            self.nuevaVentana.geometry("400x400")
            WindBar.__init__(self,self.nuevaVentana,self.IDD)
            #self.ventana = Wind_bar(self.nuevaVentana)
            self.nuevaVentana.mainloop()

        if self.bandera == 0:
            self.error=Toplevel()
            self.error.title='usuario no válido'
            Label(self.error, text='Usuario no válido ').grid(row=0,column=1)
            Button(self.error,text='regresar',command=lambda: destruir(self.error)).grid(row=1,column=1)
            print('Usuario no válido')

    def meter_Password(self):
        self.usuario = self.IDD
        self.contraWind = Toplevel()
        self.contraWind.title = 'Iniciar sesión de ' +  self.usuario

        Label(self.contraWind,text= 'Contraseña:').grid(row=0,column=1)
        self.casillaPsw = Entry(self.contraWind,show="*")
        self.casillaPsw.focus()
        self.casillaPsw.grid(row=0,column=2)

        Button (self.contraWind, text='Iniciar',command= lambda: self.verificar_Password()).grid(row=1,column=2,sticky=W)
        Button (self.contraWind, text='regresar',command= lambda: self.contraWind.destroy()).grid(row=1,column=3)

    def verificar_Password(self):
    	self.bandera=0
    	self.query='SELECT contraseña FROM gerentes WHERE usuario = ?'
    	self.consulta=run_Query(self.query,(self.IDD,))

    	for row in self.consulta:
    		if row[0] == self.casillaPsw.get():
    			print('AHORA ERES GERENTE')
    			self.bandera=1

    	if self.bandera == 0:
    		print('Contraseña no válida')
    		self.error=Toplevel()
    		self.error.title='Contraseña no válida'
    		Label(self.error, text='Contraseña no válida ').grid(row=0,column=1)
    		Button(self.error,text='Regresar',command=lambda: destruir(self.error)).grid(row=1,column=1)

    	if self.bandera ==1:
            self.wind.destroy()
            self.nuevaVentana = Tk()

            self.nuevaVentana.geometry("400x400")
            WindGerente.__init__(self,self.nuevaVentana,'Gerente')
            #ventana = Wind_gerente(nuevaVentana,id)

            self.nuevaVentana.mainloop()

#crear_Inicio()
