import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from tkinter.tix import Select
from flask import Flask, redirect
from flask import render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from flask import send_from_directory
from flask_login import LoginManager
from datetime import datetime
from werkzeug.urls import url_parse  # prueba login
...

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'liammateo18'
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA


@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)


@app.route("/")
def index():
    sql = "SELECT * FROM `empleados`;"  # CONSULTA BASE DE DATOS
    # conección a base de datos y envio de datos!
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()  # selecciona todolos datos.
    print(empleados)  # imprime en consola
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)


@app.route('/destroy/<int:id>')  # <int:id> recibe un entero!!!
def destroy(id):
    # Funcion para borrar un empleado a travez de un ID.
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()
    return redirect('/')  # redirecciona


@app.route('/edit/<int:id>')  # para editar usuarios
def edit(id):
    conn = mysql.connect()  # conecta base de datos
    cursor = conn.cursor()  # almacena datos de consulta
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados = cursor.fetchall()  # selecciona todolos datos.
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)


@app.route('/update', methods=['POST'])
def update():  # Función para actualizar datos de un usuario con el EDIT
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _tipoUser = request.form['txtTipoUsuario']
    # _foto=request.files['txtFoto']
    id = request.form['txtID']
    # aca agregamos a la BD lo que agregamos en el formulario
    # sin 'empleados' no funciona, tener en cuenta!!!
    sql = "UPDATE empleados SET nombre=%s, correo=%s, tipoUsuario=%s WHERE `empleados`.`id` =%s ;"
    # introducción de datos
    datos = (_nombre, _correo, _tipoUser, id)
    # conección a base de datos y envio de datos!
    conn = mysql.connect()
    cursor = conn.cursor()
    now = datetime.now()  # tiempo actual
    tiempo = now.strftime("%Y%M%d%H%M%S")

    # consultamos si hay foto mismo nombre, guardamos por fecha.
    # if _foto.filename!='':
    #   nuevoNombreFoto=tiempo+_foto.filename
    #  _foto.save("uploads/"+nuevoNombreFoto)
    # cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    # fila=cursor.fetchall()
    # os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    #cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
    # conn.commit()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')


@app.route('/login_inicio')  # para ir a pantalla iniciar sesión
def login_inicio():
    return render_template('login_inicio.html')


@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/createClientes')
def createClientes():
    return render_template('empleados/createClientes.html')


@app.route('/empl')
def empl():
    sql = "SELECT * FROM `empleados`;"  # CONSULTA BASE DE DATOS
    # conección a base de datos y envio de datos!
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()  # selecciona todolos datos.
    conn.commit()
    return render_template('empleados/empl.html', empleados=empleados)


@app.route('/clientes')
def clientes():
    sql = "SELECT * FROM `empleados`;"  # CONSULTA BASE DE DATOS
    # conección a base de datos y envio de datos!
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()  # selecciona todolos datos.
    conn.commit()
    return render_template('empleados/clientes.html', empleados=empleados)


@app.route('/store', methods=['POST'])
# para ingresar desde el formulario "create.html"
def storage():
    # variables
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _tipoUser = request.form['txtTipoUsuario']
    # _foto=request.files['txtFoto']
    # para evitar sobre escribir fotos con el mismo nombre
    # now=datetime.now() #tiempo actual
    # tiempo=now.strftime("%Y%M%d%H%M%S")
    # consultamos si hay foto mismo nombre, guardamos por fecha.
    # if _foto.filename!='':
    #   nuevoNombreFoto=tiempo+_foto.filename
    #    _foto.save("uploads/"+nuevoNombreFoto)
    # aca agregamos a la BD lo que agregamos en el formulario
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `tipoUsuario`) VALUES (NULL, %s, %s, %s) ;"
    # introducción de datos
    datos = (_nombre, _correo, _tipoUser)
    # conección a base de datos y envio de datos!
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
