from application.database import db

class User(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64))
    
    # Relationships
    #role = db.relationship('Role', lazy=True, uselist=False, primaryjoin="User.role == Role.name")
    roles = db.relationship('Role', secondary='role_user', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<Role {self.role_name}>'
    
class RoleUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('user.username'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    def __repr__(self):
        return f'<RoleUser username={self.username} role_id={self.role_id}>'

class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    # Relationships
    niches = db.relationship('Niche', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Niche(db.Model):
    niche_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)

    def __str__(self):
        return f'<Niche {self.name}>'
    
class InfluencerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'))
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    niche = db.Column(db.String(64))
    reach = db.Column(db.Integer)

class SponsorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), db.ForeignKey('user.username'))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    # company details
    company_name = db.Column(db.String(64))
    company_address = db.Column(db.String(100), nullable=False)
    company_website = db.Column(db.String(100), nullable=False)
    company_description = db.Column(db.String(256), nullable=False)
    industry = db.Column(db.String(64))
    budget = db.Column(db.Float)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor_profile.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    niche_id = db.Column(db.Integer, db.ForeignKey('niche.niche_id'))
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    status = db.Column(db.String(23), default=True)

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('user.username'))
    # campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    # influencer_id = db.Column(db.Integer, db.ForeignKey('influencer_profile.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    request_type = db.Column(db.String(20), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(64), nullable=False)  # e.g., 'Pending', 'Accepted', 'Rejected', 'Negotiating'
    terms = db.Column(db.String(256), nullable=False)
    new_category_name = db.Column(db.String(40), nullable=True)
    new_category_description = db.Column(db.String(100), nullable=True)

    # Relationships
    category = db.relationship('Categories', backref='adrequests', lazy=True)

    def __repr__(self):
        return f'<AdRequest {self.category_id} - {self.request_type}>'
    
class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    niche_id = db.Column(db.Integer, db.ForeignKey('niche.niche_id'))
    username = db.Column(db.String(30), db.ForeignKey('user.username'))
    purchase_date = db.Column(db.Date, nullable=False)

    # Relationships
    niche = db.relationship('Niche', backref='TransactionHistory', lazy=True)
