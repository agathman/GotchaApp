from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy

  
app = Flask(__name__, template_folder="templates", instance_relative_config=False)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pymssql://gotchadata:Got1234!@COT-CIS4375-08:1433/GotchaData'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
    
db.init_app(app)
    #app.config.from_object('config.config')

with app.app_context():
    from .views import my_view  # Import routess
    app.register_blueprint(my_view)
    
     
    if __name__ == '__main__':
         
         app.run(debug = True)




