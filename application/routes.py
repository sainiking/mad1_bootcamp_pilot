from datetime import datetime
from main import app
from flask import render_template, redirect, url_for, flash, session, request as req
from application.models import *
from main import db

@app.route("/")
def index():
    if session.get('username', None):
        categories = Categories.query.all()
        return render_template('index.html', categories=categories)
    return render_template('index.html')
  

# Sponsor Profile
@app.route("/edit_sponsor_profile", methods=["GET", "POST"])
def edit_sponsor_profile():
    if req.method == "GET":
        sponsor_profile = SponsorProfile.query.filter_by(user=session['username']).first()
        return render_template('edit_sponsor_profile.html', sponsor_profile=sponsor_profile)
    
    if req.method == "POST":
        first_name = req.form.get("first_name")
        last_name = req.form.get("last_name")
        email = req.form.get("email")
        phone = req.form.get("phone")
        company_name = req.form.get("company_name")
        company_address = req.form.get("company_address")
        industry = req.form.get("industry")
        company_website = req.form.get("company_website")
        company_description = req.form.get("company_description")
        budget = req.form.get("budget")
        user = session.get('username')
    
    # Do some validation
    if not first_name or not last_name or not phone or not company_name or not company_address or not industry or not company_website or not company_description or not budget:
        flash('All fields are required')
        return redirect(url_for('edit_sponsor_profile'))
    
    sponsor_profile = SponsorProfile.query.filter_by(user=user).first()  
   
    if sponsor_profile:
        sponsor_profile.first_name = first_name
        sponsor_profile.last_name = last_name
        sponsor_profile.email = email
        sponsor_profile.phone = phone
        sponsor_profile.company_name = company_name
        sponsor_profile.company_address = company_address
        sponsor_profile.industry = industry
        sponsor_profile.company_website = company_website
        sponsor_profile.company_description = company_description
        sponsor_profile.budget = budget
        
        try:
            db.session.commit()
            flash('Profile updated successfully')
            return redirect(url_for('view_sponsor_profile'))
        except Exception as e:
            flash(f'Error updating profile: {e}')
            return redirect(url_for('edit_sponsor_profile'))
        
    else:
        sponsor_profile = SponsorProfile(first_name=first_name, last_name=last_name, email=email, phone=phone, company_name=company_name, company_address=company_address, industry=industry, company_website=company_website, company_description=company_description, budget=budget, user=user) # type: ignore
        try:
            db.session.add(sponsor_profile)
            db.session.commit()
            flash('Profile added successfully')
            return redirect(url_for('view_sponsor_profile'))
        except Exception as e:
            flash(f'Error adding profile: {e}')
            return redirect(url_for('edit_sponsor_profile'))
    
@app.route("/view_sponsor_profile", methods=["GET", "POST"]) # type: ignore
def view_sponsor_profile():
    sponsor_profile = SponsorProfile.query.filter_by(user=session['username']).first()
    if not sponsor_profile:
        return render_template('edit_sponsor_profile.html', sponsor_profile=sponsor_profile)
    
    if req.method == "GET":
        return render_template('view_sponsor_profile.html', sponsor_profile=sponsor_profile)

# Sponsor adds, edit and delete Niche
@app.route("/add_niche", methods=["GET", "POST"]) # type: ignore
def add_niche():
    if req.method == "GET":
        categories = Categories.query.all()
        return render_template('add_niche.html', categories=categories)
    
    if req.method == "POST":
        name = req.form.get("niche_name")
        description = req.form.get("description")
        category_id = req.form.get("category_id")
        image_url = req.form.get("image_url")

        if not name or not category_id or not description:
            flash('All fields are required')
            return redirect(url_for('add_niche'))
        
        niche = Niche.query.filter_by(name=name).first()
        
        if niche:
            flash('niche already exists')
            return redirect(url_for('add_niche'))
        
        
        elif session['role'] == 'sponsor':
            niche = Niche(name=name, description=description, category_id=category_id, image_url=image_url) # type: ignore
            try:
                db.session.add(niche)
                db.session.commit()
                flash('niche added successfully')
                return redirect(url_for('add_niche'))
            except Exception as e:
                flash(f'Error adding niche: {e}')
                return redirect(url_for('add_niche'))
            
    else:
        flash('You do not have permission to add niche')
        return redirect(url_for('index'))
    
@app.route("/edit_niche/<int:niche_id>", methods=["GET", "POST"]) # type: ignore
def edit_niche(niche_id):
    niche = Niche.query.filter_by(niche_id=niche_id).first()
    if not niche:
        flash('Niche does not exist')
        return redirect(url_for('index'))
    
    if req.method == "GET":
        categories = Categories.query.all()
        return render_template('edit_niche.html', niche=niche, categories=categories)
    
    if req.method == "POST":
        name = req.form.get("niche_name")
        description = req.form.get("description")
        category_id = req.form.get("category_id")
        
        if not name or not category_id or not description:
            flash('All fields are required')
            return redirect(url_for('edit_niche', niche_id=niche_id))
        
        if (niche.name == name and niche.description == description and 
            niche.category_id == category_id):
            flash('No changes were made')
            return redirect(url_for('edit_niche', niche_id=niche_id))
        
        niche.name = name
        niche.description = description
        niche.category_id = category_id
        try:
            db.session.commit()
            flash('Niche updated successfully')
            return redirect(url_for('edit_niche', niche_id=niche_id))
        except Exception as e:
            flash(f'Error updating niche: {e}')
            return redirect(url_for('edit_niche', niche_id=niche_id))
        
@app.route("/delete_niche/<int:niche_id>", methods=["GET", "POST"]) # type: ignore
def delete_niche(niche_id):
    niche = Niche.query.filter_by(niche_id=niche_id).first()
    if not niche:
        flash('Niche does not exist')
        return redirect(url_for('index'))

    if req.method == "GET":
        return render_template('delete_niche.html', niche=niche) 
    try:
        db.session.delete(niche)
        db.session.commit()
        flash('Niche deleted successfully')
        return redirect(url_for('all_campaign'))
    except Exception as e:
        flash(f'Error deleting niche: {e}')
        return redirect(url_for('delete_niche', niche_id=niche_id))


# Influencer Profile
@app.route("/edit_influencer_profile", methods=["GET", "POST"])
def edit_influencer_profile():
    if req.method == "GET":
        influencer_profile = InfluencerProfile.query.filter_by(user=session['username']).first()
        return render_template('edit_influencer_profile.html', influencer_profile=influencer_profile, categories=Categories.query.all(), niche=Niche.query.all())
    
    if req.method == "POST":
        first_name = req.form.get("first_name")
        last_name = req.form.get("last_name")
        email = req.form.get("email")
        phone = req.form.get("phone")
        bio = req.form.get("bio")
        instagram_handle = req.form.get("instagram_handle")
        facebook_handle = req.form.get("facebook_handle")
        youtube_handle = req.form.get("youtube_handle")
        blog_url = req.form.get("blog_url")
        followers_count = req.form.get("followers_count")
        total_engagement = req.form.get("total_engagement")
        total_views = req.form.get("total_views")
        reach = req.form.get("reach")
        age = req.form.get("age")
        gender = req.form.get("gender")
        location = req.form.get("location")
        language = req.form.get("language")
        user = session.get('username')
        category_id = req.form.get("category")
        niche_id = req.form.get("niche")
        price = req.form.get("price")

    # Do some validation
    if not all([first_name, last_name]):
        flash('All fields are required!')
        return redirect(url_for('edit_influencer_profile'))
    
    # Fetch the niche object to validate category_id
    niche = Niche.query.get(niche_id)
    if niche and niche.category_id != int(category_id): # type: ignore
        flash('Category and Niche do not match')
        return redirect(url_for('edit_influencer_profile'))

    influencer_profile = InfluencerProfile.query.filter_by(user=user).first()
    
    if influencer_profile:
        influencer_profile.first_name = first_name
        influencer_profile.last_name = last_name
        influencer_profile.email = email
        influencer_profile.phone = phone
        influencer_profile.bio = bio
        influencer_profile.instagram_handle = instagram_handle
        influencer_profile.facebook_handle = facebook_handle
        influencer_profile.youtube_handle = youtube_handle
        influencer_profile.blog_url = blog_url
        influencer_profile.followers_count = followers_count
        influencer_profile.total_engagement = total_engagement
        influencer_profile.total_views = total_views
        influencer_profile.reach = reach
        influencer_profile.age = age
        influencer_profile.gender = gender
        influencer_profile.location = location
        influencer_profile.language = language
        influencer_profile.category_id = category_id
        influencer_profile.niche_id = niche_id
        influencer_profile.user = user
        influencer_profile.price = price
        
        try:
            db.session.commit()
            flash('Profile updated successfully')
            return redirect(url_for('view_influencer_profile'))
        except Exception as e:
            flash(f'Error updating profile: {e}')
            return redirect(url_for('edit_influencer_profile'))
        
    else:
        influencer_profile = InfluencerProfile(first_name=first_name, 
                                               last_name=last_name, 
                                               email=email, 
                                               phone=phone, 
                                               bio=bio, 
                                               instagram_handle=instagram_handle, 
                                               facebook_handle=facebook_handle, 
                                               youtube_handle=youtube_handle,
                                               blog_url=blog_url,
                                               followers_count=followers_count,
                                               total_engagement=total_engagement,
                                               total_views=total_views, 
                                               reach=reach, 
                                               age=age,
                                               gender=gender,
                                               location=location,
                                               language=language,
                                               category_id=category_id,
                                               niche_id=niche_id,
                                               user=user,
                                               price=price) # type: ignore
                                               
        try:
            db.session.add(influencer_profile)
            db.session.commit()
            flash('Profile added successfully')
            return redirect(url_for('view_influencer_profile'))
        except Exception as e:
            flash(f'Error adding profile: {e}')
            return redirect(url_for('edit_influencer_profile'))
    
@app.route("/view_influencer_profile", methods=["GET", "POST"]) # type: ignore
def view_influencer_profile():
    influencer_profile = InfluencerProfile.query.filter_by(user=session['username']).first()
    if not influencer_profile:
        return render_template('edit_influencer_profile.html', influencer_profile=influencer_profile, categories=Categories.query.all(), niche=Niche.query.all())
        
    if req.method == "GET":
        return render_template('view_influencer_profile.html', influencer_profile=influencer_profile, categories=Categories.query.all(), niche=Niche.query.all())



# Sponsor Requests to add, edit or delete categories
@app.route('/sponsor_requests')
def sponsor_requests():
    if session['role'] == 'admin':
        requests = AdRequest.query.filter_by(status='Pending').all()
        return render_template('requests.html', requests=requests)
    elif session['role'] == 'sponsor':
        requests = AdRequest.query.filter_by(username=session['username']).all()
        return render_template('requests.html', requests=requests)
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))

@app.route("/add_category", methods=["GET", "POST"]) # type: ignore
def add_category():
    if req.method == "GET":
        return render_template('add_category.html', categories=Categories.query.all())
    
    if req.method == "POST":
        name = req.form.get("title")
        description = req.form.get("content")
    
        category = Categories.query.filter_by(name=name).first()
        if category:
            flash('Category already exists')
            return redirect(url_for('add_category'))
        
        if session['role'] == 'admin':
            try:
                category = Categories(name=name, description=description) # type: ignore
                db.session.add(category)
                db.session.commit()
                flash('category added successfully')
                return redirect(url_for('add_category'))
            except Exception as e:
                flash(f'Error adding category: {e}')
                return redirect(url_for('add_category'))
            
        if session['role'] == 'sponsor':
            existing_category = Categories.query.filter_by(name=name).first()
            if existing_category:
                flash('Category already exists')
                return redirect(url_for('add_category'))
            
            request = AdRequest.query.filter_by(username=session['username'],  
                                                request_type='add_category',
                                                status='Pending',
                                                new_category_name=name).first()
            if request:
                flash('Request already exists')
                return redirect(url_for('add_category'))
            
            request = AdRequest(username=session['username'], 
                                request_type='add_category',
                                request_date=datetime.now(),
                                status='Pending',
                                new_category_name=name,
                                new_category_description=description
                                ) # type: ignore
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request added successfully to admin.')
                return redirect(url_for('add_category'))
            except Exception as e:
                flash(f'Error adding request: {e}')
                return redirect(url_for('add_category'))
        else:
            flash('You do not have permission to add category')
            return redirect(url_for('index'))

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"]) # type: ignore
def edit_category(category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        flash('Category does not exist')
        return redirect(url_for('all_campaign'))
    
    if req.method == "GET":
        return render_template('edit_category.html', category=category)
    
    if req.method == "POST":
        name = req.form.get("title")
        description = req.form.get("content")
        
        if session['role'] == 'admin':
            try:
                existing_category = Categories.query.filter_by(name=name).first()
                if existing_category and existing_category.category_id != category_id:
                    flash('Category already exists')
                    return redirect(url_for('edit_category', category_id=category_id))
                category.name = name
                category.description = description
                db.session.commit()
                flash('category edited successfully')
                return redirect(url_for('edit_category', category_id=category_id))
            except Exception as e:
                flash(f'Error adding category: {e}')
                return redirect(url_for('edit_category', category_id=category_id))
            
        elif session['role'] == 'sponsor':
            if category.name == name and category.description == description:
                flash('No changes made')
                return redirect(url_for('edit_category', category_id=category_id))
            
            request = AdRequest.query.filter_by(username=session['username'], 
                                                category_id=category.category_id, 
                                                request_type='edit_category',
                                                status='Pending',
                                                new_category_name=name).first()
            if request:
                flash('Request already exists')
                return redirect(url_for('edit_category', category_id=category_id))
            
            request = AdRequest(username=session['username'], 
                                category_id=category.category_id, 
                                request_type='edit_category',
                                request_date=datetime.now(),
                                status='Pending',
                                new_category_name=name,
                                new_category_description=description
                                ) # type: ignore
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request added successfully')
                return redirect(url_for('edit_category', category_id=category_id))
            except Exception as e:
                flash(f'Error adding request: {e}')
                return redirect(url_for('add_category'))
            
    else:
        flash('You do not have permission to edit category')
        return redirect(url_for('all_campaign'))
    
@app.route("/delete_category/<int:category_id>", methods=["GET", "POST"]) # type: ignore
def delete_category(category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        flash('Category does not exist')
        return redirect(url_for('all_campaign'))
    
    if req.method == "GET":
            return render_template('delete_category.html', category=category)
    
    if req.method == "POST":
        if session['role'] == 'sponsor':
            request = AdRequest.query.filter_by(username=session['username'], 
                                                category_id=category.category_id, 
                                                request_type='delete_category',
                                                status='Pending').first()
            if request:
                flash('Request already exists')
                return redirect(url_for('delete_category', category_id=category_id  ))
            
            request = AdRequest(username=session['username'], 
                                category_id=category.category_id, 
                                request_type='delete_category',         
                                request_date=datetime.now(),
                                status='Pending',
                                ) # type: ignore
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request added successfully')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error adding request: {e}')
                return redirect(url_for('delete_category', category_id=category_id))
            
        elif session['role'] == 'admin':
            try:
                db.session.delete(category)
                db.session.commit()
                flash('Category deleted successfully')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error deleting category: {e}')
                return redirect(url_for('delete_category', category_id=category_id))
        else:
            flash('You do not have permission to delete category')
            return redirect(url_for('all_campaign'))


# Admin approves or rejects requests
@app.route('/approve_request/<int:id>', methods=['GET', 'POST']) # type: ignore
def approve_request(id):
    request= AdRequest.query.filter_by(id=id).first()

    if not request:
        flash('Request not found', 'danger')
        return redirect(url_for('index'))
    
    if session['role']=='admin':
        if request.request_type == 'add_category':
            category = Categories.query.filter_by(name=request.new_category_name).first()
            if category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category already exists - Request Rejected', 'danger')
                return redirect(url_for('sponsor_requests'))
            
            category = Categories(name=request.new_category_name, description=request.new_category_description) # type: ignore
            try:
                db.session.add(category)
                db.session.commit()
                request.status = 'approved'
                db.session.commit()
                flash('Category added successfully', 'success')
                return redirect(url_for('sponsor_requests'))
            except Exception as e:
                flash(f'Error adding category!! Error: {e}', 'danger')
                return redirect(url_for('sponsor_requests'))
        
        if request.request_type == 'edit_category':
            category = Categories.query.filter_by(name=request.new_category_name).first()
            if category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category with same name already exits - Request Rejected', 'danger')
                return redirect(url_for('sponsor_requests'))
            
            category = Categories.query.filter_by(category_id=request.category_id).first()
            if not category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category not found - Request Rejected', 'danger')
                return redirect(url_for('sponsor_requests'))
            
            category.name = request.new_category_name
            category.description = request.new_category_description
            try:
                db.session.commit()
                request.status = 'approved'
                db.session.commit()
                flash('Category updated successfully', 'success')
                return redirect(url_for('sponsor_requests'))
            except Exception as e:
                flash(f'Error updating category!! Error: {e}', 'danger')
                return redirect(url_for('sponsor_requests'))
            
        if request.request_type == 'delete_category':
            category = Categories.query.filter_by(category_id=request.category_id).first()
            if not category:
                request.status = 'rejected'
                db.session.commit()
                flash('Category not found - Request Rejected', 'danger')
                return redirect(url_for('sponsor_requests'))
            
            try:
                db.session.delete(category)
                # db.session.commit()
                request.status = 'approved'
                db.session.commit()
                flash('Category deleted successfully', 'success')
                return redirect(url_for('sponsor_requests'))
            except Exception as e:
                flash(f'Error deleting category!! Error: {e}', 'danger')
                return redirect(url_for('sponsor_requests'))
            

@app.route('/reject_request/<int:id>', methods=['GET', 'POST']) # type: ignore
def reject_request(id):
    request = AdRequest.query.filter_by(id=id).first()

    if not request:
        flash('Request not found', 'danger')
        return redirect(url_for('index'))
    
    if session['role']=='admin':
        request.status = 'rejected'
        db.session.commit()
        flash('Request rejected successfully', 'success')
        return redirect(url_for('sponsor_requests'))


# Search for campaigns and influencers
@app.route('/search_campaign', methods=['GET', 'POST'])
def search_campaign():
    campaigns = []
    if req.method == 'POST':
        search_term = req.form.get('search')
        campaigns = Campaign.query.join(Categories, Campaign.category_id == Categories.category_id).join(Niche, Campaign.niche_id == Niche.niche_id).filter((Campaign.name.ilike(f'%{search_term}%')) | (Categories.name.ilike(f'%{search_term}%')) | (Niche.name.ilike(f'%{search_term}%'))).filter(Campaign.flagged == False).all()
        return render_template('search_campaign.html', campaigns=campaigns)
    return render_template('search_campaign.html', campaigns=campaigns)

@app.route('/search_influencer', methods=['GET', 'POST'])
def search_influencer():
    influencers = []
    if req.method == 'POST':
        search_term = req.form.get('search')
        influencers = InfluencerProfile.query.join(Categories, InfluencerProfile.category_id == Categories.category_id).join(Niche, InfluencerProfile.niche_id == Niche.niche_id).filter((InfluencerProfile.location.ilike(f'%{search_term}%')) | (InfluencerProfile.youtube_handle.ilike(f'%{search_term}%')) | (Categories.name.ilike(f'%{search_term}%')) | (Niche.name.ilike(f'%{search_term}%'))).all()
        return render_template('search_influencer.html', influencers=influencers)
    return render_template('search_influencer.html', influencers=influencers)


# Summary of all influencers and sponsors
@app.route('/summary_influencers')  
def summary_influencer():
    influencers = InfluencerProfile.query.filter_by(flagged=False).all()
    campaign = Campaign.query.all()

    return render_template('summary_influencer.html', influencers=influencers, campaign=campaign)


# Influencer Attributes
@app.route('/profile_view_influencer/<user>')
def profile_view_influencer(user):
    influencer_profile = InfluencerProfile.query.filter_by(user=user).first()
    return render_template('profile_view_influencer.html', influencer_profile=influencer_profile)


# Create Campaigns
@app.route("/create_campaign", methods=["GET", "POST"]) # type: ignore
def create_campaign():
    if req.method == "GET":
        campaign = Campaign.query.filter_by(user=session['username']).first()
        return render_template('create_campaign.html', campaign=campaign, categories=Categories.query.all(), niches=Niche.query.all())

    if req.method == "POST":
        name = req.form.get("name")
        user = session.get('username')
        description = req.form.get("description")
        budget = req.form.get("budget")
        category_id = req.form.get("category")
        niche_id = req.form.get("niche")
        start_date = datetime.strptime(req.form.get("start_date"), '%Y-%m-%d') # type: ignore
        end_date = datetime.strptime(req.form.get("end_date"), '%Y-%m-%d') # type: ignore
        status = req.form.get("status")
        
        #print(name, description, budget, category_id, niche_id, start_date, end_date, status)
        sponsor = SponsorProfile.query.filter_by(user=session['username']).first()
        influencer = InfluencerProfile.query.filter_by(user=session['username']).first()
        sponsor_id = sponsor.id if sponsor else None
        if sponsor_id is None:
            flash('You need to complete your profile first.')
            return redirect(url_for('view_sponsor_profile'))
        
        influencer_id = influencer.id if influencer else None

        if not name or not description or not budget  or not start_date or not end_date or not status:
            flash('All fields are required')
            return redirect(url_for('create_campaign'))
        
        # Fetch the niche object to validate category_id
        niche = Niche.query.get(niche_id)
        if niche and niche.category_id != int(category_id): # type: ignore
            flash('Category and Niche do not match')
            return redirect(url_for('create_campaign'))
        
        
        campaign = Campaign(name=name, description=description, budget=budget, category_id=category_id, niche_id=niche_id, start_date=start_date, end_date=end_date, status=status, user=user, sponsor_id=sponsor_id, influencer_id=influencer_id) # type: ignore
        try:
            db.session.add(campaign)
            db.session.commit()
            flash('Campaign added successfully')
            return redirect(url_for('create_campaign'))
        except Exception as e:
            flash(f'Error adding campaign: {e}')
            return redirect(url_for('create_campaign'))

@app.route("/edit_campaign/<int:campaign_id>", methods=["GET", "POST"]) # type: ignore
def edit_campaign(campaign_id):
    if req.method == "GET":
        campaign = Campaign.query.get(campaign_id)
        return render_template('edit_campaign.html', campaign=campaign, categories=Categories.query.all(), niches=Niche.query.all())
    
    if req.method == "POST":
        campaign_id = req.form.get("campaign_id")
        name = req.form.get("name")
        user = session.get('username')
        description = req.form.get("description")
        budget = req.form.get("budget")
        category_id = req.form.get("category")
        niche_id = req.form.get("niche")
        sponsor_id = session.get("sponsor")
        start_date = datetime.strptime(req.form.get("start_date"), '%Y-%m-%d') # type: ignore
        end_date = datetime.strptime(req.form.get("end_date"), '%Y-%m-%d') # type: ignore
        status = req.form.get("status")
        influencer_id = session.get("influencer")

        #print(name, description, budget, category_id, niche_id, start_date, end_date, status)

        if not name or not description or not budget  or not start_date or not end_date or not status:
            flash('All fields are required')
            return redirect(url_for('edit_campaign'))
        
            # Fetch the niche object to validate category_id
        niche = Niche.query.get(niche_id)
        if niche and niche.category_id != int(category_id): # type: ignore
            flash('Category and Niche do not match')
            return redirect(url_for('edit_campaign'))
        
        campaign = Campaign.query.get(campaign_id)
        if campaign and campaign.user == session['username']:
            campaign.name = name
            campaign.description = description
            campaign.budget = budget
            campaign.category_id = category_id
            campaign.niche_id = niche_id
            campaign.start_date = start_date
            campaign.end_date = end_date
            campaign.status = status
            campaign.user = user
            campaign.sponsor_id = sponsor_id if sponsor_id else campaign.sponsor_id
            campaign.influencer_id = influencer_id

            try:
                db.session.commit()
                flash('Campaign updated successfully')
                return redirect(url_for('all_campaign', campaign_id=campaign_id))
            except Exception as e:
                flash(f'Error updating campaign: {e}')
                return redirect(url_for('edit_campaign', campaign_id=campaign_id))

        else:
            flash('No existing campaign found to update')
            return redirect(url_for('edit_campaign'))



# View all campaigns
@app.route('/all_campaign')
def all_campaign():
    campaigns = Campaign.query.filter_by(flagged=False).all()
    # for campaign in campaigns:
    #     print(campaign.influencer_id)
    return render_template('all_campaign.html', campaigns=campaigns)


# Campaign Attributes
@app.route('/profile_view_sponsor/<user>')
def profile_view_sponsor(user):
    sponsor_profile = SponsorProfile.query.filter_by(user=user).first()
    return render_template('profile_view_sponsor.html', sponsor_profile=sponsor_profile)

@app.route('/accept_campaign/<int:campaign_id>', methods=['GET'])
def accept_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    user = session.get('username')
    influencer = InfluencerProfile.query.filter_by(user=user).first()
    influencer.campaign_id = campaign_id
    influencer_id = influencer.id if influencer else None
    print(influencer_id)  
    if not influencer_id:
        flash('You need to complete your profile first.')
        return redirect(url_for('view_influencer_profile'))
    
    campaign.status = 'pending approval'
    campaign.influencer_id = influencer_id

    db.session.commit()
    flash('Campaign acceptance request sent for approval.')
    return redirect(url_for('all_campaign'))

@app.route('/approve_campaign_sponsor/<int:campaign_id>', methods=['POST'])
def approve_campaign_sponsor(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign and campaign.user == session['username']:
        campaign.status = 'accepted'
        db.session.commit()
        flash('Campaign approved successfully')
    else:
        flash('You do not have permission to approve this campaign')
    return redirect(url_for('all_campaign'))

@app.route('/reject_campaign_sponsor/<int:campaign_id>', methods=['POST'])
def reject_campaign_sponsor(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign and campaign.user == session['username']:
        campaign.status = 'Active'
        campaign.influencer_id = None
        db.session.commit()
        flash('Campaign rejected successfully')
    else:
        flash('You do not have permission to reject this campaign')
    return redirect(url_for('all_campaign'))

@app.route("/delete_campaign/<int:campaign_id>", methods=["POST"])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign and campaign.user == session['username']:
        try:
            InfluencerProfile.query.filter_by(campaign_id = campaign_id).update({'campaign_id': None})
            db.session.delete(campaign)
            db.session.commit()
            flash('Campaign deleted successfully')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting campaign: {e}')
    else:
        flash('You do not have permission to delete this campaign')
    return redirect(url_for('all_campaign'))

@app.route("/negotiate_campaign/<int:campaign_id>", methods=["GET", "POST"])
def negotiate_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    influencer = InfluencerProfile.query.filter_by(user=session['username']).first()
    if not influencer:
        flash('You need to complete your profile first.')
        return redirect(url_for('view_influencer_profile'))
    if req.method == "POST":
        message_content = req.form.get("message")
        sender = session.get('username')
        campaign_id = campaign.id
        influencer_id = influencer.id
        category_id = campaign.category_id
        niche_id = campaign.niche_id
        receiver = campaign.user  # Assuming campaign.user is the sponsor's username
        
        if not message_content:
            flash('Message content is required')
            return redirect(url_for('negotiate_campaign', campaign_id=campaign_id))
        
        # Create a new message
        message = Message(sender=sender, campaign_id=campaign_id, influencer_id=influencer_id, category_id=category_id, niche_id=niche_id, receiver=receiver, content=message_content) # type: ignore
        
        try:
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully')
            return redirect(url_for('all_campaign', campaign_id=campaign_id))
        except Exception as e:
            flash(f'Error sending message: {e}')
            return redirect(url_for('negotiate_campaign', campaign_id=campaign_id))
        
    return render_template('negotiate_campaign.html', campaign=campaign)


# Flagged Campaigns, Sponsors and Influencers.
@app.route('/flag_campaign/<int:campaign_id>', methods=['GET'])
def flag_campaign(campaign_id):
    if 'username' not in session or session['role'] != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('all_campaign'))

    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.flagged = True
        db.session.commit()
        flash('Campaign has been flagged as inappropriate.', 'success')
    else:
        flash('Campaign not found.', 'danger')

    return redirect(url_for('all_campaign'))

@app.route('/flagged_campaign_sponsor')
def flagged_campaign_sponsor():
    user = session.get('username')  
    if 'role' in session and session['role'] == 'sponsor':
        campaigns = Campaign.query.filter_by(user=user, flagged=True).all()
        return render_template('flagged_campaign_sponsor.html', campaigns=campaigns)
        
    else:
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('all_campaign'))



@app.route('/flag_influencer/<int:influencer_id>', methods=['GET'])
def flag_influencer(influencer_id):
    if 'username' not in session or session['role'] != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('all_campaign'))

    influencer = InfluencerProfile.query.get(influencer_id)
    if influencer:
        influencer.flagged = True
        db.session.commit()
        flash('Influencer has been flagged as inappropriate.', 'success')
    else:
        flash('Influencer not found.', 'danger')

    return redirect(url_for('summary_influencer'))


# View flagged campaigns and influencers
@app.route('/admin_view_flagged_campaign')
def admin_view_flagged_campaign():
    if 'role' in session and session['role'] == 'admin':
        campaigns = Campaign.query.filter_by(flagged=True).all()
        return render_template('admin_view_flagged_campaign.html', campaigns=campaigns)
        
    else:
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('all_campaign'))
    
@app.route('/admin_view_flagged_influencer')
def admin_view_flagged_influencer():
    if 'role' in session and session['role'] == 'admin':
        influencers = InfluencerProfile.query.filter_by(flagged=True).all()
        return render_template('admin_view_flagged_influencer.html', influencers=influencers)
    else:
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('summary_influencer'))
    
@app.route('/flagged_influencer_view')
def flagged_influencer_view():
    if 'role' in session and session['role'] == 'influencer':
        influencers = InfluencerProfile.query.filter_by(flagged=True).all()
        if influencers:
            return render_template('flagged_influencer_view.html', influencers=influencers)
        
        else:
            flash('Lucky you! You are not flagged.', 'danger')
            return redirect(url_for('summary_influencer'))
    else:
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('summary_influencer'))
      

# Request to unflag
@app.route("/request_to_unflag_campaign/<int:campaign_id>", methods=["GET", "POST"])
def request_to_unflag_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    if req.method == "POST":
        message_content = req.form.get("message")
        sender = session.get('username')
        category_id = campaign.category_id
        niche_id = campaign.niche_id
        receiver = 'admin'
        campaign_id = campaign.id  # Assuming campaign.user is the sponsor's username
        
        if not message_content:
            flash('Message content is required')
            return redirect(url_for('request_to_unflag_campaign', campaign_id=campaign_id))
        
        # Create a new message
        message = Message(sender=sender, category_id=category_id, niche_id=niche_id, receiver=receiver, content=message_content, campaign_id=campaign_id) # type: ignore
        
        try:
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully')
            return redirect(url_for('all_campaign', campaign_id=campaign_id))
        except Exception as e:
            flash(f'Error sending message: {e}')
            return redirect(url_for('request_to_unflag_campaign', campaign_id=campaign_id))
        
    return render_template('request_to_unflag_campaign.html', campaign=campaign)

@app.route("/request_to_unflag_influencer/<int:influencer_id>", methods=["GET", "POST"])
def request_to_unflag_influencer(influencer_id):
    influencer = InfluencerProfile.query.get_or_404(influencer_id)

    if req.method == "POST":
        message_content = req.form.get("message")
        sender = session.get('username')
        category_id = influencer.category_id
        niche_id = influencer.niche_id
        receiver = 'admin'
        influencer_id = influencer.id  # Assuming campaign.user is the sponsor's username

        if not message_content:
            flash('Message content is required')
            return redirect(url_for('request_to_unflag_influencer', influencer_id=influencer_id))
        
        # Create a new message
        message = Message(sender=sender, category_id=category_id, niche_id=niche_id, receiver=receiver, content=message_content, influencer_id=influencer_id) # type: ignore

        try:
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully')
            return redirect(url_for('all_campaign', influencer_id=influencer_id))
        except Exception as e:
            flash(f'Error sending message: {e}')
            return redirect(url_for('request_to_unflag_influencer', influencer_id=influencer_id))
        
    return render_template('request_to_unflag_influencer.html', influencer=influencer)

# Unflag Campaign, Sponsor and Influencer
@app.route('/unflag_influencer/<int:influencer_id>', methods=['POST'])
def unflag_influencer(influencer_id):
    if 'username' not in session or session['role'] != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('all_campaign'))

    influencer = InfluencerProfile.query.get(influencer_id)
    if influencer:
        influencer.flagged = False
        db.session.commit()
        flash('Influencer has been unflagged and re-enabled.', 'success')
    else:
        flash('Influencer not found.', 'danger')

    return redirect(url_for('all_campaign'))

@app.route('/unflag_campaign/<int:campaign_id>', methods=['POST'])
def unflag_campaign(campaign_id):
    if 'username' not in session or session['role'] != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('all_campaign'))

    campaign = Campaign.query.get(campaign_id)
    if campaign is None:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('all_campaign'))
    campaign.flagged = False
    db.session.commit()
    flash('Campaign has been unflagged and re-enabled.', 'success')
    return redirect(url_for('all_campaign'))


# View messages
@app.route("/view_message", methods=["GET"])
def view_message():
    user = session.get('username')
    messages = Message.query.filter_by(receiver=user).order_by(Message.timestamp.desc()).all()
    if messages:
        return render_template('view_message.html',messages=messages)
    flash('No messages to display.')
    return redirect(url_for('all_campaign'))

@app.route("/view_message_admin", methods=["GET"])
def view_message_admin():
    user = session.get('username')
    messages = Message.query.filter_by(receiver=user).order_by(Message.timestamp.desc()).all()
    if messages:
        return render_template('view_message_admin.html',messages=messages)
    flash('No messages to display.')
    return redirect(url_for('all_campaign'))
    
@app.route("/view_message_for_influencer", methods=["GET"])
def view_message_for_influencer():
    user = session.get('username')

    messages = Message.query.filter_by(receiver=user).order_by(Message.timestamp.desc()).all()
    message_count = len(messages)
    if messages:
        return render_template('view_message_for_influencer.html',messages=messages, message_count=message_count)
    flash('No messages to display.')
    return redirect(url_for('all_campaign'))


# Reply to messages
@app.route("/reply_from_sponsor/<int:message_id>", methods=["GET", "POST"])
def reply_from_sponsor(message_id):
    message = Message.query.get_or_404(message_id)

    if req.method == "POST":
        reply_content = req.form.get("message")
        sender = session.get('username')
        category_id = message.category_id
        niche_id = message.niche_id
        receiver = message.sender
        campaign_id = message.campaign_id
        influencer_id = message.influencer_id
        if not reply_content:
            flash('Reply content is required')
            return redirect(url_for('reply_from_sponsor', message_id=message_id))
        
        # Create a new message
        message = Message(sender=sender, campaign_id=campaign_id, influencer_id=influencer_id, category_id=category_id, niche_id=niche_id, receiver=receiver, content=reply_content) # type: ignore

        try:
            db.session.add(message)
            db.session.commit()
            flash('Reply sent successfully')
            return redirect(url_for('all_campaign'))
        except Exception as e:
            flash(f'Error sending reply: {e}')
            return redirect(url_for('reply_from_sponsor', message_id=message_id))
        
    return render_template('reply_from_sponsor.html', message=message)

@app.route("/reply_from_influencer/<int:message_id>", methods=["GET", "POST"])
def reply_from_influencer(message_id):
    message = Message.query.get_or_404(message_id)

    if req.method == "POST":
        reply_content = req.form.get("message")
        sender = session.get('username')
        category_id = message.category_id
        niche_id = message.niche_id
        receiver = message.sender
        campaign_id = message.campaign_id
        influencer_id = message.influencer_id
        if not reply_content:
            flash('Reply content is required')
            return redirect(url_for('reply_from_influencer', message_id=message_id))
        
        # Create a new message
        message = Message(sender=sender, influencer_id=influencer_id, campaign_id=campaign_id, category_id=category_id, niche_id=niche_id, receiver=receiver, content=reply_content) # type: ignore

        try:
            db.session.add(message)
            db.session.commit()
            flash('Reply sent successfully')
            return redirect(url_for('all_campaign'))
        except Exception as e:
            flash(f'Error sending reply: {e}')
            return redirect(url_for('reply_from_influencer', message_id=message_id))
        
    return render_template('reply_from_influencer.html', message=message)

@app.route("/reply_from_admin/<int:message_id>", methods=["GET", "POST"])
def reply_from_admin(message_id):
    message = Message.query.get_or_404(message_id)

    if req.method == "POST":
        reply_content = req.form.get("message")
        sender = session.get('username')
        influencer_id = message.influencer_id
        campaign_id = message.campaign_id
        category_id = message.category_id
        niche_id = message.niche_id
        receiver = message.sender
        
        if not reply_content:
            flash('Reply content is required')
            return redirect(url_for('reply_from_admin', message_id=message_id))
        
        # Create a new message
        message = Message(sender=sender, campaign_id=campaign_id, influencer_id=influencer_id, category_id=category_id, niche_id=niche_id, receiver=receiver, content=reply_content) # type: ignore

        try:
            db.session.add(message)
            db.session.commit()
            flash('Reply sent successfully')
            return redirect(url_for('all_campaign'))
        except Exception as e:
            flash(f'Error sending reply: {e}')
            return redirect(url_for('reply_from_admin', message_id=message_id))
        
    return render_template('reply_from_admin.html', message=message)




# Sponsor routes for sending requests to influencers
@app.route("/send_request/<int:influencer_id>", methods=["GET", "POST"])
def send_request(influencer_id):
    sponsor = SponsorProfile.query.filter_by(user=session['username']).first()
    sponsor_id = sponsor.id if sponsor else None
    influencer = InfluencerProfile.query.get_or_404(influencer_id)
    ongoing_campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id, status='Active', flagged=0).all()

    if ongoing_campaigns:    
        if req.method == "POST":
            campaign_id = req.form.get('campaign_id')
            request_message = req.form.get("message")
            
            # Create a new request
            new_request = RequestToInfluencer(campaign_id=campaign_id, sponsor_id=sponsor_id, influencer_id=influencer_id, message=request_message)
            
            try:
                db.session.add(new_request)
                db.session.commit()
                flash('Request sent successfully')
                return redirect(url_for('all_campaign'))
            except Exception as e:
                flash(f'Error sending request: {e}')
                return redirect(url_for('all_campaign'))
        
        return render_template('send_request.html', sponsor=sponsor,influencer=influencer, ongoing_campaigns=ongoing_campaigns)
    else:
        flash('You do not have any ongoing campaigns.')
        return redirect(url_for('create_campaign'))
    
@app.route("/accept_request/<int:request_id>", methods=["POST"])
def accept_request(request_id):
    request = RequestToInfluencer.query.get_or_404(request_id)
    request.status = 'accepted'
    db.session.commit()

    # Add campaign to influencer profile
    influencer = InfluencerProfile.query.get(request.influencer_id)
    influencer_username = influencer.user.capitalize() if influencer else None

    # Change campaign status to accepted
    campaign = Campaign.query.get(request.campaign_id)
    campaign_name = campaign.name if campaign else None
    if campaign:
        campaign.influencer_id = request.influencer_id
        campaign.status = 'accepted'
        db.session.commit()
    else:
        flash('Campaign not found', 'danger')

    # Send a notification to the sponsor
    sponsor = SponsorProfile.query.get(request.sponsor_id)
    if sponsor:
        message = f'Your request for campaign "{campaign_name}" has been accepted by the influencer "{influencer_username}"'
        notification = Notification(sender=request.influencer_id,campaign=campaign_name, receiver=request.sponsor_id, message=message) # type: ignore
        db.session.add(notification)
        db.session.commit()
    else:
        flash('Sponsor not found', 'danger')

    flash('Request accepted')
    return redirect(url_for('view_request'))

@app.route("/view_notification", methods=["GET"])
def view_notification():
    influencer = InfluencerProfile.query.filter_by(user=session['username']).first()
    sponsor = SponsorProfile.query.filter_by(user=session['username']).first()
    sponsor_id = sponsor.id if sponsor else None
    notifications = Notification.query.filter_by(receiver=sponsor_id).order_by(Notification.timestamp.desc()).all()
    notification_count = len(notifications)
    return render_template('view_notification.html',influencer=influencer, notifications=notifications, notification_count=notification_count)


@app.route("/view_request", methods=["GET"])
def view_request():
    influencer = InfluencerProfile.query.filter_by(user=session['username']).first()
    if influencer:
        influencer_id = influencer.id  # Retrieve influencer_id from the influencer object
        requests = RequestToInfluencer.query.filter_by(influencer_id=influencer_id).all()
    else:
        requests = []
    return render_template('view_request.html', requests=requests, influencer=influencer)

@app.route("/reject_request_/<int:request_id>", methods=["GET","POST"])
def reject_request_(request_id):
    request = RequestToInfluencer.query.get_or_404(request_id)
    
    if req.method == "POST":
        request.status = 'rejected'
        db.session.commit()

        campaign = Campaign.query.get(request.campaign_id)
        campaign_name = campaign.name if campaign else None

        influencer = InfluencerProfile.query.get(request.influencer_id)
        influencer_username = influencer.user if influencer else None

        # Send a notification to the sponsor
        sponsor = SponsorProfile.query.get(request.sponsor_id)
        if sponsor:
            message = f'Your request for campaign "{campaign_name}" has been rejected by the influencer{influencer_username}'
            notification = Notification(sender=request.influencer_id, campaign=campaign_name, receiver=request.sponsor_id, message=message) # type: ignore
            db.session.add(notification)
            db.session.commit()
        else:
            flash('Sponsor not found', 'danger')

        flash('Reject message sent')
        return redirect(url_for('view_request'))
    
    return render_template('reject_request.html', request=request)

@app.route("/negotiate_request/<int:request_id>", methods=["GET", "POST"])
def negotiate_request(request_id):
    request = RequestToInfluencer.query.get_or_404(request_id)
    
    if req.method == "POST":
        negotiation_message = req.form.get("message")
        request.status = 'negotiating'
        request.message = negotiation_message
        db.session.commit()

        campaign = Campaign.query.get(request.campaign_id)
        campaign_name = campaign.name if campaign else None
        
        influencer = InfluencerProfile.query.get(request.influencer_id)
        influencer_username = influencer.user.capitalize() if influencer else None
        
        # Send a notification to the sponsor
        sponsor = SponsorProfile.query.get(request.sponsor_id)
        if sponsor:
            message = f'Your request for campaign "{campaign_name}" has been negotiated by the influencer "{influencer_username}". Negotiation message: {negotiation_message} Reply to accept or reject the negotiation from messages.'
            notification = Notification(sender=request.influencer_id, campaign=campaign_name, receiver=request.sponsor_id, message=message) # type: ignore
            db.session.add(notification)
            new_message = Message(sender=influencer.user, receiver=sponsor.user, content=negotiation_message, timestamp=datetime.now(), campaign_id=request.campaign_id, influencer_id=request.influencer_id, category_id=campaign.category_id, niche_id=campaign.niche_id) # type: ignore
            db.session.add(new_message)
            db.session.commit()
        else:
            flash('Sponsor not found', 'danger')

        flash('Negotiation Sent!')
        return redirect(url_for('view_request'))
    
    return render_template('negotiate_request.html', request=request)


# Statistics
@app.route('/statistics')
def statistics():
    if 'username' not in session or session['role'] != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))

    total_sponsors = SponsorProfile.query.count()
    average_spend_per_sponsor = db.session.query(db.func.avg(Campaign.budget)).scalar()
    top_sponsors = SponsorProfile.query.order_by(SponsorProfile.budget.desc()).limit(5).all()

    total_influencers = InfluencerProfile.query.count()
    costly_influencers = InfluencerProfile.query.order_by(InfluencerProfile.price.desc()).limit(5).all()
    top_influencers = InfluencerProfile.query.order_by(InfluencerProfile.total_engagement.desc()).limit(5).all()

    total_campaigns = Campaign.query.count()
    active_campaigns = Campaign.query.filter(Campaign.status == 'Active').count()
    top_campaigns = Campaign.query.order_by(Campaign.budget.desc()).limit(5).all()

    return render_template('statistics.html',
                           total_sponsors=total_sponsors,
                           average_spend_per_sponsor=average_spend_per_sponsor,
                           top_sponsors=top_sponsors,
                           total_influencers=total_influencers,
                           costly_influencers=costly_influencers,
                           top_influencers=top_influencers,
                           total_campaigns=total_campaigns,
                           active_campaigns=active_campaigns,
                           top_campaigns=top_campaigns)