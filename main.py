from flask import Flask, render_template, url_for, request, redirect
from application.config import Config
# from flask_login import LoginManager, current_user, login_required, logout_user, login_user
from application.models import *

def create_app():
    app = Flask(__name__, template_folder = "templates")
    # next we need to config our application. make a config.py file

    app.config.from_object(Config)
    # we need to tell our database which app to refer for that we initialize init_.app
    db.init_app(app)

    # next we need to create_all models from the models.py with the help of with app.app_context
    with app.app_context():
        db.create_all()

        add_default_categories()

        add_default_niches()

        admin_role = Role.query.filter_by(role_name='admin').first()
        if not admin_role:       
            admin_role = Role(role_name='admin', description='Administration') # type: ignore
            db.session.add(admin_role)
        
        sponsor_role = Role.query.filter_by(role_name='sponsor').first()
        if not sponsor_role:   
            sponsor_role = Role(role_name='sponsor', description='Sponsor Profile') # type: ignore
            db.session.add(sponsor_role)
        
        influencer_role = Role.query.filter_by(role_name='influencer').first()
        if not influencer_role:
            influencer_role = Role(role_name='influencer', description='Influencer Profile') # type: ignore
            db.session.add(influencer_role)


        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@gmail.com', password='admin', role='admin', roles = [admin_role]) # type: ignore
        db.session.add(admin)
        db.session.commit()
    return app

app = create_app()


from application.auth_routes import *
from application.routes import *

if __name__ == '__main__':
    app.run(debug=True) # type: ignore