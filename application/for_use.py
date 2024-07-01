# @app.route("/add_category", methods=["GET", "POST"])
# def add_category():
#     if req.method == "GET":
#         return render_template('add_category.html')
    
#     if req.method == "POST":
#         name = req.form.get("title")
#         description = req.form.get("content")
        
#         if not name:
#             flash('category name is required')
#             return redirect(url_for('add_category'))
        
#         category = Categories.query.filter_by(name=name).first()
        
#         if category:
#             flash('category already exists')
#             return redirect(url_for('add_category'))
        
#         if session['role'] == 'admin':
#             try:
#                 category = Categories(name=name, description=description)
#                 db.session.add(category)
#                 db.session.commit()
#                 flash('category added successfully')
#                 return redirect(url_for('add_category'))
#             except Exception as e:
#                 flash(f'Error adding category: {e}')
#                 return redirect(url_for('add_category'))
            
#         elif session['role'] == 'sponsor' or session['role'] == 'influencer':
#             request = AdRequest.query.filter_by(username=session['username'], 
#                                                 category_id=category.category_id, 
#                                                 request_type='category',
#                                                 status='Pending',
#                                                 new_category_name=name).first()
#             if request:
#                 flash('Request already exists')
#                 return redirect(url_for('add_category'))
            
#             request = AdRequest(username=session['username'], 
#                                 category_id=category.category_id, 
#                                 request_type='category',
#                                 request_date=datetime.now(),
#                                 status='Pending',
#                                 terms='Please add this category',
#                                 new_category_name=name,
#                                 new_category_description=description
#                                 )
#             try:
#                 db.session.add(request)
#                 db.session.commit()
#                 flash('Request added successfully')
#                 return redirect(url_for('index'))
#             except Exception as e:
#                 flash(f'Error adding request: {e}')
#                 return redirect(url_for('add_category'))
#         else:
#             flash('You do not have permission to add category')
#             return redirect(url_for('index'))