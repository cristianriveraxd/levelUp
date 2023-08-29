class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^' #llave para manejar datos de sesión utilzando flahs

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST='127.0.0.1' #conexión a db
    MYSQL_USER='root'
    MYSQL_PASSWORD=''
    MYSQL_DB ='levelup'

#diccionario que incluye clase
config= {
    'development':DevelopmentConfig
}