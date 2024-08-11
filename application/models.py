from application.database import db
from datetime import datetime
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
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
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    # Relationships
    niches = db.relationship('Niche', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
    
def add_default_categories():
    default_categories = [
        {"name": "Fashion & Beauty", "description": "Everything about fashion and beauty."},
        {"name": "Technology & Gadgets", "description": "Latest in tech and gadgets."},
        {"name": "Health & Fitness", "description": "Health, fitness, and wellness tips."},
        {"name": "Food & Beverage", "description": "Delicious recipes and food reviews."},
        {"name": "Travel & Adventure", "description": "Travel destinations and adventure sports."},
        {"name": "Lifestyle & Home", "description": "Home decor, parenting, and DIY projects."},
        {"name": "Entertainment", "description": "Movies, music, and celebrity news."},
        {"name": "Finance & Business", "description": "Personal finance and business advice."},
        {"name": "Education & Learning", "description": "Educational content and learning tips."},
        {"name": "Automotive", "description": "Car reviews and automotive news."},
        {"name": "Art & Design", "description": "Graphic design and art tutorials."},
        {"name": "Pets & Animals", "description": "Pet care and animal training."},
        {"name": "Gaming", "description": "Game reviews and live streaming."},
        {"name": "Politics & Social Issues", "description": "Political commentary and social activism."},
    ]

    for category in default_categories:
        existing_category = Categories.query.filter_by(name=category["name"]).first()
        if not existing_category:
            new_category = Categories(name=category["name"], description=category["description"])
            db.session.add(new_category)
    db.session.commit()

class Niche(db.Model):
    niche_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    
    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id
    
    def __str__(self):
        return f'<Niche {self.name}>'

def add_default_niches():
    niches = [
        {"name": "Women's Fashion", "category_id": 1},
        {"name": "Men's Fashion", "category_id": 1},
        {"name": "Streetwear", "category_id": 1},
        {"name": "Skincare", "category_id": 1}, 
        {"name": "Makeup", "category_id": 1},
        {"name": "Unboxing", "category_id": 2},
        {"name": "Gadget Reviews", "category_id": 2},
        {"name": "Smart Home", "category_id": 2},
        {"name": "Tech News", "category_id": 2},
        {"name": "Mobile Apps", "category_id": 2},
        {"name": "Fitness Tips", "category_id": 3},
        {"name": "Yoga", "category_id": 3},
        {"name": "Running", "category_id": 3},
        {"name": "Crossfit", "category_id": 3},
        {"name": "Nutrition", "category_id": 3},
        {"name": "Weight Loss", "category_id": 3},
        {"name": "Weightlifting", "category_id": 3},
        {"name": "Recipes", "category_id": 4},
        {"name": "Cooking Tips", "category_id": 4},
        {"name": "Baking", "category_id": 4},
        {"name": "Food Reviews", "category_id": 4},
        {"name": "Healthy Eating", "category_id": 4},
        {"name": "Beverage Reviews", "category_id": 4},
        {"name": "Wine and Spirits", "category_id": 4},
        {"name": "Food Photography", "category_id": 4},
        {"name": "Restaurant Reviews", "category_id": 4},
        {"name": "Vegetarian/Vegan", "category_id": 4},
        {"name": "Adventure Travel", "category_id": 5},
        {"name": "Luxury Travel", "category_id": 5},
        {"name": "Budget Travel", "category_id": 5},
        {"name": "Travel Tips", "category_id": 5},
        {"name": "Destination Guides", "category_id": 5},
        {"name": "Backpacking", "category_id": 5},
        {"name": "Cultural Experiences", "category_id": 5},
        {"name": "Road Trips", "category_id": 5},
        {"name": "Travel Photography", "category_id": 5},
        {"name": "Solo Travel", "category_id": 5},
        {"name": "Home Decor", "category_id": 6},
        {"name": "DIY Projects", "category_id": 6},
        {"name": "Gardening", "category_id": 6},
        {"name": "Personal Development", "category_id": 6},
        {"name": "Minimalism", "category_id": 6},
        {"name": "Organization Tips", "category_id": 6},
        {"name": "Sustainable Living", "category_id": 6},
        {"name": "Parenting", "category_id": 6},
        {"name": "Life Hacks", "category_id": 6},
        {"name": "Home Improvement", "category_id": 6},
        {"name": "Movies", "category_id": 7},
        {"name": "TV Shows", "category_id": 7},
        {"name": "Music", "category_id": 7},
        {"name": "Celebrity News", "category_id": 7},
        {"name": "Event Coverage", "category_id": 7},
        {"name": "Book Reviews", "category_id": 7},
        {"name": "Theatre", "category_id": 7},
        {"name": "Stand-up Comedy", "category_id": 7},
        {"name": "Concert Reviews", "category_id": 7},
        {"name": "Pop Culture", "category_id": 7},
        {"name": "Personal Finance", "category_id": 8},
        {"name": "Investing", "category_id": 8},
        {"name": "Entrepreneurship", "category_id": 8},
        {"name": "Marketing", "category_id": 8},
        {"name": "Real Estate", "category_id": 8},
        {"name": "E-commerce", "category_id": 8},
        {"name": "Startups", "category_id": 8},
        {"name": "Business News", "category_id": 8},
        {"name": "Financial Planning", "category_id": 8},
        {"name": "Cryptocurrency", "category_id": 8},
        {"name": "Online Learning", "category_id": 9},
        {"name": "Study Tips", "category_id": 9},
        {"name": "Language Learning", "category_id": 9},
        {"name": "Educational Resources", "category_id": 9},
        {"name": "EdTech Reviews", "category_id": 9},
        {"name": "Science", "category_id": 9},
        {"name": "History", "category_id": 9},
        {"name": "Mathematics", "category_id": 9},
        {"name": "Literature", "category_id": 9},
        {"name": "Exam Preparation", "category_id": 9},
        {"name": "Car Reviews", "category_id": 10},
        {"name": "Motorcycle Reviews", "category_id": 10},
        {"name": "Automotive News", "category_id": 10},
        {"name": "Car Maintenance Tips", "category_id": 10},
        {"name": "Custom Builds", "category_id": 10},
        {"name": "Electric Vehicles", "category_id": 10},
        {"name": "Classic Cars", "category_id": 10},
        {"name": "Car Shows", "category_id": 10},
        {"name": "Automotive Accessories", "category_id": 10},
        {"name": "Off-Roading", "category_id": 10},
        {"name": "Graphic Design", "category_id": 11},
        {"name": "Photography", "category_id": 11},
        {"name": "Painting", "category_id": 11},
        {"name": "Digital Art", "category_id": 11},
        {"name": "Crafting", "category_id": 11},
        {"name": "Interior Design", "category_id": 11},
        {"name": "Fashion Design", "category_id": 11},
        {"name": "Architecture", "category_id": 11},
        {"name": "Illustration", "category_id": 11},
        {"name": "Art Tutorials", "category_id": 11},
        {"name": "Pet Care", "category_id": 12},
        {"name": "Pet Training", "category_id": 12},
        {"name": "Pet Nutrition", "category_id": 12},
        {"name": "Pet Accessories", "category_id": 12},
        {"name": "Animal Rescue", "category_id": 12},
        {"name": "Wildlife", "category_id": 12},
        {"name": "Pet Photography", "category_id": 12},
        {"name": "Exotic Pets", "category_id": 12},
        {"name": "Pet Behavior", "category_id": 12},
        {"name": "Veterinarian Advice", "category_id": 12},
        {"name": "Game Reviews", "category_id": 13},
        {"name": "Live Streaming", "category_id": 13},
        {"name": "E-sports", "category_id": 13},
        {"name": "Gaming News", "category_id": 13},
        {"name": "Game Tutorials", "category_id": 13},
        {"name": "Indie Games", "category_id": 13},
        {"name": "Mobile Games", "category_id": 13},
        {"name": "PC Games", "category_id": 13},
        {"name": "Console Games", "category_id": 13},
        {"name": "Virtual Reality Gaming", "category_id": 13},
        {"name": "Political News", "category_id": 14},
        {"name": "Social Justice", "category_id": 14},
        {"name": "Environmental Issues", "category_id": 14},
        {"name": "Human Rights", "category_id": 14},
        {"name": "Policy Analysis", "category_id": 14},
        {"name": "Activism", "category_id": 14},
        {"name": "Public Health", "category_id": 14},
        {"name": "Global Affairs", "category_id": 14},
        {"name": "Community Development", "category_id": 14},
        {"name": "Legal Issues", "category_id": 14}
    ]

    for niche in niches:
        existing_niche = Niche.query.filter_by(name=niche["name"]).first()
        if not existing_niche:
            new_niche = Niche(name=niche["name"], category_id=niche["category_id"])
            db.session.add(new_niche)
    db.session.commit()

class InfluencerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), db.ForeignKey('user.username'))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    bio = db.Column(db.String(256), nullable=False)
    # social media details
    instagram_handle = db.Column(db.String(64), nullable=False)
    facebook_handle = db.Column(db.String(64), nullable=False)
    youtube_handle = db.Column(db.String(64), nullable=False)
    blog_url = db.Column(db.String(100), nullable=False)
    # metrics
    followers_count = db.Column(db.Integer)
    total_engagement = db.Column(db.Integer)
    total_views = db.Column(db.Integer)
    reach = db.Column(db.Integer)
    # demographics
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    location = db.Column(db.String(30))
    language = db.Column(db.String(20))
    # category and niche
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    niche_id = db.Column(db.Integer, db.ForeignKey('niche.niche_id'))
    # pricing
    price = db.Column(db.Float)
    # status
    flagged = db.Column(db.Boolean, default=False)
    # relationships
    category = db.relationship('Categories', backref='influencers', lazy=True)
    niche = db.relationship('Niche', backref='influencers', lazy=True)
    # campaigns = relationship('Campaign', foreign_keys=[campaign_id], backref='influencer')
    def __repr__(self):
        return f'<InfluencerProfile {self.user}>'

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
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor_profile.id'))
    user = db.Column(db.String(20), db.ForeignKey('user.username'))
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    status = db.Column(db.String(23), default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    niche_id = db.Column(db.Integer, db.ForeignKey('niche.niche_id'))
    flagged = db.Column(db.Boolean, default=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer_profile.id'))
    # Relationships
    category = db.relationship('Categories', backref='campaigns', lazy=True)
    niche = db.relationship('Niche', backref='campaigns', lazy=True)
    sponsor = db.relationship('SponsorProfile', backref='campaigns', lazy=True)
    influencer = relationship('InfluencerProfile', foreign_keys=[influencer_id], backref='campaigns')
    def __repr__(self):
        return f'<Campaign {self.name}>'

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('user.username'))
    # campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    # influencer_id = db.Column(db.Integer, db.ForeignKey('influencer_profile.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)
    request_type = db.Column(db.String(20), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(64), nullable=False)  # e.g., 'Pending', 'Accepted', 'Rejected', 'Negotiating'
    #terms = db.Column(db.String(256), nullable=False)
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

    def __repr__(self):
        return f'<TransactionHistory {self.niche_id} - {self.username}>'
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer_profile.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    niche_id = db.Column(db.Integer, db.ForeignKey('niche.niche_id'))

    #Relationships
    category = db.relationship('Categories', backref='messages', lazy=True)
    niche = db.relationship('Niche', backref='messages', lazy=True)
    campaign = db.relationship('Campaign', backref='messages', lazy=True)
    influencer = db.relationship('InfluencerProfile', backref='messages', lazy=True)

    def __repr__(self):
        return f'<Message {self.id} from {self.sender} to {self.receiver}>'

class RequestToInfluencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor_profile.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer_profile.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    campaign = db.relationship('Campaign', backref='requests', lazy=True)
    sponsor = db.relationship('SponsorProfile', backref='requests', lazy=True)
    influencer = db.relationship('InfluencerProfile', backref='requests', lazy=True)
    
    def __init__(self, campaign_id, sponsor_id, influencer_id, message=None):
        self.campaign_id = campaign_id
        self.sponsor_id = sponsor_id
        self.influencer_id = influencer_id
        self.message = message

    

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign = db.Column(db.Integer)
    sender = db.Column(db.Integer)
    receiver = db.Column(db.Integer)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    
    def __repr__(self):
        return f'<Notification {self.id} from {self.sender} to {self.receiver}>'