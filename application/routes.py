# from flask import current_app as app, redirect, render_template, url_for

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

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if req.method == "GET":
        return render_template('add_category.html')
    
    if req.method == "POST":
        name = req.form.get("title")
        description = req.form.get("content")
        
        if not name:
            flash('category name is required')
            return redirect(url_for('add_category'))
        
        category = Categories.query.filter_by(name=name).first()
        
        if category:
            flash('category already exists')
            return redirect(url_for('add_category'))
        
        if session['role'] == 'admin':
            try:
                category = Categories(name=name, description=description)
                db.session.add(category)
                db.session.commit()
                flash('category added successfully')
                return redirect(url_for('add_category'))
            except Exception as e:
                flash(f'Error adding category: {e}')
                return redirect(url_for('add_category'))
            
        elif session['role'] == 'sponsor':
            request = AdRequest.query.filter_by(username=session['username'], 
                                                category_id=category.category_id, 
                                                request_type='category',
                                                status='Pending',
                                                new_category_name=name).first()
            if request:
                flash('Request already exists')
                return redirect(url_for('add_category'))
            
            request = AdRequest(username=session['username'], 
                                category_id=category.category_id, 
                                request_type='category',
                                request_date=datetime.now(),
                                status='Pending',
                                terms='Please add this category',
                                new_category_name=name,
                                new_category_description=description
                                )
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request added successfully')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error adding request: {e}')
                return redirect(url_for('add_category'))
        else:
            flash('You do not have permission to add category')
            return redirect(url_for('index'))

 
@app.route("/add_niche", methods=["GET", "POST"])
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
        
        # if session['role'] == 'admin':
        #     flash('You do not have permission to add niche')
        #     return redirect(url_for('index'))
        
        elif session['role'] == 'sponsor': #'sponsor' or session['role'] == 'influencer':
            niche = Niche(name=name, description=description, category_id=category_id, image_url=image_url)
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
    
@app.route("/edit_niche/<int:niche_id>", methods=["GET", "POST"])
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
        image_url = req.form.get("image_url")
        
        if not name or not category_id or not description:
            flash('All fields are required')
            return redirect(url_for('edit_niche', niche_id=niche_id))
        
        niche.name = name
        niche.description = description
        niche.category_id = category_id
        niche.image_url = image_url
        try:
            db.session.commit()
            flash('Niche updated successfully')
            return redirect(url_for('edit_niche', niche_id=niche_id))
        except Exception as e:
            flash(f'Error updating niche: {e}')
            return redirect(url_for('edit_niche', niche_id=niche_id))
        
@app.route("/delete_niche/<int:niche_id>", methods=["GET", "POST"])
def delete_niche(niche_id):
    niche = Niche.query.filter_by(niche_id=niche_id).first()
    if not niche:
        flash('Niche does not exist')
        return redirect(url_for('index'))

    if req.method == "GET":
        return render_template('delete_niche.html', niche=niche) 
    # try:
    #     db.session.delete(niche)
    #     db.session.commit()
    #     flash('Niche deleted successfully')
    #     return redirect(url_for('index'))
    # except Exception as e:
    #     flash(f'Error deleting niche: {e}')
    #     return redirect(url_for('index'))
        
@app.route("/create_campaign", methods=["GET", "POST"])
def create_campaign():
    if req.method == "GET":
        categories = Categories.query.all()
        niches = Niche.query.all()
        return render_template('create_campaign.html', categories=categories, niches=niches)
    
    if req.method == "POST":
        name = req.form.get("campaign_name")
        description = req.form.get("description")
        budget = req.form.get("budget")
        category_id = req.form.get("category")
        niche_id = req.form.get("niche")
        start_date = datetime.strptime(req.form.get("start_date"), '%Y-%m-%d')
        end_date = datetime.strptime(req.form.get("end_date"), '%Y-%m-%d')
        status = req.form.get("status")
        #print(name, description, budget, category_id, niche_id, start_date, end_date, status)
        
        if not name or not description or not budget  or not start_date or not end_date or not status:
            flash('All fields are required')
            return redirect(url_for('create_campaign'))
        
        if session['role'] == 'sponsor':
            try:
                campaign = Campaign(name=name, 
                                    description=description, 
                                    budget=budget, 
                                    category_id=category_id, 
                                    niche_id=niche_id, 
                                    start_date=start_date, 
                                    end_date=end_date, 
                                    status=status)
                db.session.add(campaign)
                db.session.commit()
                flash('Campaign added successfully')
                return redirect(url_for('create_campaign'))
            except Exception as e:
                flash(f'Error adding campaign: {e}')
                return redirect(url_for('create_campaign'))
            
        # elif session['role'] == 'sponsor':
            # request = AdRequest.query.filter_by(username=session['username'], 
            #                                     category_id=category_id, 
            #                                     niche_id=niche_id, 
            #                                     request_type='campaign',
            #                                     status='Pending',
            #                                     new_category_name=name).first()
            # if request:
            #     flash('Request already exists')
            #     return redirect(url_for('create_campaign'))
            
            # request = AdRequest(username=session['username'], 
            #                     category_id=category_id, 
            #                     #niche_id=niche_id, 
            #                     request_type='campaign',
            #                     request_date=datetime.now(),
            #                     status='Pending',
            #                     terms='Please add this campaign',
            #                     new_category_name=name,
            #                     new_category_description=description,
            #                     #new_campaign_budget=budget,
            #                     # new_campaign_start_date=start_date,
            #                     # new_campaign_end_date=end_date,
            #                     # new_campaign_status=status
            #                     )
            # try:
            #     db.session.add(request)
            #     db.session.commit()
            #     flash('Request added successfully')
            #     return redirect(url_for('index'))
            # except Exception as e:
            #     flash(f'Error adding request: {e}')
            #     return redirect(url_for('create_campaign'))
        else:
            flash('You do not have permission to add campaign')
            return redirect(url_for('index'))
        
@app.route("/sponsor_profile", methods=["GET", "POST"])
def sponsor_profile():
    if req.method == "GET":
        sponsor_profile = SponsorProfile.query.all()
        return render_template('sponsor_profile.html', sponsor_profile=sponsor_profile)
    
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
        return redirect(url_for('sponsor_profile'))
    
    if sponsor_profile:
        flash('Profile already exists')
        return redirect(url_for('sponsor_profile'))
       
    if session['role'] == 'sponsor':
        sponsor_profile = SponsorProfile(first_name=first_name, last_name=last_name, email=email, phone=phone, company_name=company_name, company_address=company_address, industry=industry, company_website=company_website, company_description=company_description, budget=budget, user=user)
        try:
            db.session.add(sponsor_profile)
            db.session.commit()
            flash('Profile added successfully')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding profile: {e}')
            return redirect(url_for('sponsor_profile'))
    else:
        flash('You do not have permission to add profile')
        return redirect(url_for('index'))
    
@app.route("/view_sponsor_profile", methods=["GET", "POST"])
def view_sponsor_profile():
    sponsor_profile = SponsorProfile.query.filter_by(user=session['username']).first()
    if not sponsor_profile:
        flash('Sponsor does not exist')
        return redirect(url_for('index'))
    
    if req.method == "GET":
        return render_template('view_sponsor_profile.html', sponsor_profile=sponsor_profile)
    
    # if req.method == "POST":
    #     first_name = req.form.get("first_name")
    #     last_name = req.form.get("last_name")
    #     email = req.form.get("email")
    #     phone = req.form.get("phone")
    #     company_name = req.form.get("company_name")
    #     company_address = req.form.get("company_address")
    #     industry = req.form.get("industry")
    #     company_website = req.form.get("company_website")
    #     company_description = req.form.get("company_description")
    #     budget = req.form.get("budget")

    #     if not first_name or not last_name or not phone or not company_name or not company_address or not industry or not company_website or not company_description or not budget:
    #         flash('All fields are required')
    #         return redirect(url_for('view_sponsor_profile', id=id))
        
    #     if session['role'] == 'sponsor':
    #         sponsor_profile.user = session['username']
    #         sponsor_profile.first_name = first_name
    #         sponsor_profile.last_name = last_name
    #         sponsor_profile.email = email
    #         sponsor_profile.phone = phone
    #         sponsor_profile.company_name = company_name
    #         sponsor_profile.company_address = company_address
    #         sponsor_profile.industry = industry
    #         sponsor_profile.company_website = company_website
    #         sponsor_profile.company_description = company_description
    #         sponsor_profile.budget = budget

    #         try:
    #             db.session.commit()
    #             flash('Profile updated successfully')
    #             return redirect(url_for('view_sponsor_profile', id=id))
    #         except Exception as e:
    #             flash(f'Error updating profile: {e}')
    #             return redirect(url_for('view_sponsor_profile', id=id))
    #     else:
    #         flash('You do not have permission to update profile')
    #         return redirect(url_for('index'))
        
        # sponsor_profile.first_name = first_name
        # sponsor_profile.last_name = last_name
        # sponsor_profile.email = email
        # sponsor_profile.phone = phone
        # sponsor_profile.company_name = company_name
        # sponsor_profile.company_address = company_address
        # sponsor_profile.industry = industry
        # sponsor_profile.company_website = company_website
        # sponsor_profile.company_description = company_description
        # sponsor_profile.budget = budget
        # try:
        #     db.session.commit()
        #     flash('Profile updated successfully')
        #     return redirect(url_for('view_sponsor_profile', id=id))
        # except Exception as e:
        #     flash(f'Error updating profile: {e}')
        #     return redirect(url_for('view_sponsor_profile', id=id))
        
    # if req.method == "POST":
    #     username = req.form.get("username")
    #     user = User.query.filter_by(username=username).first()
    #     if not user:
    #         flash('User does not exist')
    #         return redirect(url_for('view_profile'))
        
    #     return render_template('view_profile.html', user=user)
# @app.route("/add_campaign", methods=["GET", "POST"])
# def add_campaign():
#     if req.method == "GET":
#         return render_template('add_campaign.html')
    
#     if req.method == "POST":
#         name = req.form.get["campaign_name"]
#         description = req.form.get["campaign_description"]
#         budget = req.form.get["campaign_budget"]
#         sponsor_id = req.form.get["sponsor_id"]
        
#         if not name or not description or not budget or not sponsor_id:
#             flash('All fields are required')
#             return redirect(url_for('add_campaign'))
        
#         sponsor = SponsorProfile.query.filter_by(id=sponsor_id).first()
#         if not sponsor:
#             flash('Sponsor does not exist')
#             return redirect(url_for('add_campaign'))
        
#         campaign = Campaign(name=name, description=description, budget=budget, sponsor_id=sponsor_id)
#         try:
#             db.session.add(campaign)
#             db.session.commit()
#             flash('Campaign added successfully')
#             return redirect(url_for('add_campaign'))
#         except Exception as e:
#             flash(f'Error adding campaign: {e}')
#             return redirect(url_for('add_campaign'))

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        flash('Category does not exist')
        return redirect(url_for('index'))
    
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
                category = Categories(name=name, description=description)
                db.session.add(category)
                db.session.commit()
                flash('category edited successfully')
                return redirect(url_for('edit_category'))
            except Exception as e:
                flash(f'Error adding category: {e}')
                return redirect(url_for('edit_category'))
            
        elif session['role'] == 'sponsor':
            request = AdRequest.query.filter_by(username=session['username'], 
                                                category_id=category.category_id, 
                                                request_type='edit_category',
                                                status='Pending',
                                                new_category_name=name).first()
            if request:
                flash('Request already exists')
                return redirect(url_for('edit_category'))
            
            request = AdRequest(username=session['username'], 
                                category_id=category.category_id, 
                                request_type='edit_category',
                                request_date=datetime.now(),
                                status='Pending',
                                terms='Please add this category',
                                new_category_name=name,
                                new_category_description=description
                                )
            try:
                db.session.add(request)
                db.session.commit()
                flash('Request added successfully')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error adding request: {e}')
                return redirect(url_for('add_category'))
            
    else:
        flash('You do not have permission to edit category')
        return redirect(url_for('index'))
    

@app.route("/delete_category/<int:category_id>", methods=["GET", "POST"])
def delete_category(category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        flash('Category does not exist')
        return redirect(url_for('index'))
    
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
                                terms='Please add this category'
                                )
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
            return redirect(url_for('index'))
        
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
    
@app.route('/approve_request/<int:id>', methods=['GET', 'POST'])
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
            
            category = Categories(name=request.new_category_name, description=request.new_category_description)
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
            

@app.route('/reject_request/<int:id>', methods=['GET', 'POST'])
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
    
@app.route('/search')
def search():
    query = req.args.get('search')
    categories, niches = None, None
    if query:
        categories = Categories.query.filter(Categories.name.ilike(f'%{query}%')).all()
        niches = Niche.query.filter(Niche.name.ilike(f'%{query}%')).all()
    return render_template('search.html', query=query, categories=categories, niches=niches)

