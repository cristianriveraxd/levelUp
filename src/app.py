from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash

from config import config #importar clase config.py
#models
from models.modelUser import ModelUser
#entities
from models.entities.user import User

#se instancia flask
app=Flask(__name__)
app.static_folder = 'static'
csrf=CSRFProtect()
db=MySQL(app)#conexiónadb

loginManagerapp=LoginManager(app)
@loginManagerapp.user_loader 

def load_user(id):
    return ModelUser.getId(db, id)

@app.route('/')#nos redireccióna hacia login. Como accede en Get ingreso a login pero cuando realice un POST 
#se procedera a la siguiente
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])#definimos ruta para app y permitimos acceso a ambos metodos
#vista
def login():
    #print(app.config['SECRET_KEY'])
    if request.method=='POST':
        #print(request.form['user'])validaciones
        #print(request.form['password'])
        user = User(0,request.form['user'],request.form['password'])
        loggedUser=ModelUser.login(db,user)
        if loggedUser != None:
            if loggedUser.password:
                login_user(loggedUser)
                return redirect(url_for("home"))
            else:
                flash("Contraseña incorrecta")
        else:
            flash("Usuario no encontrado") 
            return render_template('login.html')#si se envie un post
    
    else:    
        return render_template('login.html')


@app.route('/registro', methods=['GET','POST'])
def checkin():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['contrasena']
        hashed_password = generate_password_hash(password, method='sha256')
        name = request.form['nombre']
        lastname = request.form['apellido']
        email = request.form['correo']
        age = request.form['edad']
        region = request.form['region']
        try:
            cursor = db.connection.cursor()
            sql = ("INSERT INTO user (username, password, name, lastname, email, age, region) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (username, hashed_password, name, lastname, email, age, region)) #tupla
            db.connection.commit()
            cursor.close()
        except Exception as e:
            raise Exception(e)
    return render_template('registro.html')    

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
        return render_template('home.html')
    
@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada!!</h1>", 404 

    
if __name__== '__main__':
    app.config.from_object(config['development'])#inicia configuración, se pasa dicciónario en llave development
    app.register_error_handler(401, status_401)
    app.register_error_handler(401, status_404)
    csrf.init_app(app)
    app.run()#inicia la aplicación
    


