import index as ind
import sqlite3

def run_Consulta(query,parameters=()):
        with sqlite3.connect('restaurante.db') as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result


def crear_db():


    queryGerentes = '''CREATE TABLE gerentes (usuario	TEXT, contraseña TEXT,registro	INTEGER );'''

    queryMesa = ''' CREATE TABLE mesa (
                num TEXT,
                ocupada INTEGER,
                personas INTEGER,
                total	REAL,
                mesero TEXT,
                descuento REAL
                );'''

    queryMeseros = '''CREATE TABLE meseros (
                    Usuario	TEXT,
                    Ventas	REAL,
                    Propinas	REAL
                    );'''

    queryPlatillos = '''CREATE TABLE platillos (
                    precio	REAL,
                    nombre	TEXT,
                    disponible	INTEGER,
                    ingrediente1	TEXT,
                    ingrediente2	TEXT,
                    ingrediente3	TEXT,
                    bebida	INTEGER
                    ); '''

    queryPlatillosMesas='''CREATE TABLE platillos_mesas (
                        platillo	TEXT,
                        mesa1	INTEGER,
                        mesa2	INTEGER,
                        mesa3	INTEGER,
                        mesa4	INTEGER,
                        mesa5	INTEGER,
                        mesa6	INTEGER,
                        mesa7   INTEGER
                        );'''

    queryVentas='''CREATE TABLE ventas (
                dia	TEXT,
                total	REAL
                ); '''

    queryIDGerente = 'INSERT INTO gerentes (usuario,contraseña,registro) VALUES (?,?,1)'
    queryIDGerente2 = 'INSERT INTO gerentes (usuario,contraseña,registro) VALUES (?,?,2)'
    run_Consulta(queryGerentes)
    run_Consulta(queryMesa)
    run_Consulta(queryMeseros)
    run_Consulta(queryPlatillos)
    run_Consulta(queryPlatillosMesas)
    run_Consulta(queryVentas)
    print('Columnas Creadas')
    run_Consulta(queryIDGerente,('admin','password'))
    run_Consulta(queryIDGerente2,('admin2','password2'))
    print('Usuario gerente creado')

    for x in range(7):
        i=str(x+1)
        nummesa='mesa'+i
        queryMesas='INSERT INTO mesa (num,ocupada,personas,total,mesero,descuento) VALUES (?,0,0,0,?,0)'
        parameters=(nummesa,'')
        run_Consulta(queryMesas,parameters)

    print('Mesas agregadas correctamente')
    print(' ')
    print('Éxito al conectarse, ejecutando programa...')

    ind.crear_Inicio()


print('***PROYECTO FINAL DE PROGRAMACIÓN***')
print('    Creadores:')
print('      Julio Hernández')
print('      Rodolfo Lagunas')
print(' ')
print(' ')
try:
    query = 'SELECT * FROM meseros'
    data = ind.run_Query(query)
except:
    print('Creando Base de datos, espera por favor...')
    crear_db()
else:
    print('Éxito al conectarse, ejecutando programa...')
    ind.crear_Inicio()
