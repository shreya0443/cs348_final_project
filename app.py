from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Spirit, Location, Exorcist, ExorcismRequest
from datetime import datetime
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spirits.db'
app.secret_key = "your_super_secret_key_here"  # Add this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Flag to track if the database has been initialized
db_initialized = False

@app.route("/")
def index():
    global db_initialized
    if not db_initialized:
        with app.app_context():
            db.create_all()
        db_initialized = True
    spirits = Spirit.query.all()
    return render_template("index.html", spirits=spirits)

@app.route("/request_exorcism", methods=["GET", "POST"])
def request_exorcism():
    with app.app_context():
        spirits = Spirit.query.all()
        exorcists = Exorcist.query.all()

        if request.method == "POST":
            customer_name = request.form["customer_name"]
            email = request.form["email"]
            spirit_id = request.form["spirit_id"]
            exorcist_id = request.form.get("exorcist_id") or None
            preferred_datetime = request.form.get("preferred_datetime")
            notes = request.form.get("notes", "")
            
            # Convert datetime string to Python datetime object
            request_date = None
            if preferred_datetime:
                try:
                    request_date = datetime.strptime(preferred_datetime, "%Y-%m-%dT%H:%M")
                except ValueError:
                    flash("Invalid date format", "danger")
                    return render_template("request_exorcism.html", spirits=spirits, exorcists=exorcists)

            new_request = ExorcismRequest(
                customer_name=customer_name,
                email=email,
                spirit_id=spirit_id,
                exorcist_id=exorcist_id,
                request_date=request_date,
                notes=notes
            )

            db.session.add(new_request)
            db.session.commit()

            flash("Exorcism request submitted successfully!", "success")
            return redirect(url_for("confirmation", request_id=new_request.id))

    return render_template("request_exorcism.html", spirits=spirits, exorcists=exorcists)


@app.route('/view_requests')
def view_requests():
    requests = ExorcismRequest.query.all()  # Retrieve all requests
    return render_template('view_requests.html', requests=requests)

@app.route("/add_spirit", methods=["GET", "POST"])
def add_spirit():
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["type"]
        location_id = request.form["location"]
        threat_level = request.form["threat_level"]
        new_spirit = Spirit(name=name, type=type, location_id=location_id, threat_level=threat_level)
        db.session.add(new_spirit)
        db.session.commit()
        return redirect(url_for("index"))
    locations = Location.query.all()
    return render_template("add_spirit.html", locations=locations)

@app.route("/delete_spirit/<int:id>")
def delete_spirit(id):
    spirit = Spirit.query.get(id)
    db.session.delete(spirit)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/manage_exorcisms')
def manage_exorcisms():
    requests = ExorcismRequest.query.all()
    return render_template('edit_request.html', requests=requests)

@app.route('/edit_request/<int:request_id>', methods=['GET', 'POST'])
def edit_request(request_id):
    exorcism_request = ExorcismRequest.query.get_or_404(request_id)
    spirits = Spirit.query.all()
    exorcists = Exorcist.query.all()
    if request.method == 'POST':
        exorcism_request.customer_name = request.form['customer_name']
        exorcism_request.email = request.form['email']
        exorcism_request.spirit_id = request.form['spirit_id']
        exorcism_request.exorcist_id = request.form.get('exorcist_id')
        exorcism_request.preferred_date = request.form['preferred_date']
        db.session.commit()
        flash('Exorcism request updated successfully!', 'success')
        return redirect(url_for('manage_exorcisms'))
    return render_template('edit_request.html', request=exorcism_request, spirits=spirits, exorcists=exorcists)

@app.route('/delete_request/<int:request_id>', methods=['POST'])
def delete_request(request_id):
    exorcism_request = ExorcismRequest.query.get_or_404(request_id)
    db.session.delete(exorcism_request)
    db.session.commit()
    flash('Exorcism request deleted!', 'danger')
    return redirect(url_for('manage_exorcisms'))

@app.route("/confirmation/<int:request_id>")
def confirmation(request_id):
    request_details = ExorcismRequest.query.get(request_id)
    if not request_details:
        flash("Invalid request ID!", "danger")
        return redirect(url_for("request_exorcism"))
    
    return render_template("confirmation.html", request=request_details)


#stage3
@app.route('/report', methods=['GET', 'POST'])
def report():
    locations = Location.query.all()
    
    if request.method == 'POST':
        # Get filter parameters from form
        location_id = request.form.get('location_id')
        threat_level = request.form.get('threat_level')
        status = request.form.get('status')
        
        # Build query with filters
        query = Spirit.query
        if location_id:
            query = query.filter(Spirit.location_id == location_id)
        if threat_level:
            query = query.filter(Spirit.threat_level == threat_level)
        if status:
            query = query.filter(Spirit.status == status)
            
        spirits = query.all()
        
        # Calculate statistics
        total_spirits = len(spirits)
        high_threat = sum(1 for s in spirits if s.threat_level == 'High')
        exorcised = sum(1 for s in spirits if s.status == 'Exorcised')
        
        return render_template('report.html', 
                            locations=locations,
                            spirits=spirits,
                            total_spirits=total_spirits,
                            high_threat=high_threat,
                            exorcised=exorcised,
                            selected_location=location_id,
                            selected_threat=threat_level,
                            selected_status=status)
    
    return render_template('report.html', locations=locations)

@app.route('/active_spirits', methods=['GET', 'POST'])
def active_spirits():
    locations = Location.query.all()
    query = Spirit.query.filter(Spirit.status == 'Active')
    
    # Initialize selected filters
    selected_location = 'all'
    selected_threat = 'all'
    selected_type = 'all'
    
    if request.method == 'POST':
        selected_location = request.form.get('location_id', 'all')
        selected_threat = request.form.get('threat_level', 'all')
        selected_type = request.form.get('type', 'all')
        
        if selected_location and selected_location != 'all':
            query = query.filter(Spirit.location_id == selected_location)
        if selected_threat and selected_threat != 'all':
            query = query.filter(Spirit.threat_level == selected_threat)
        if selected_type and selected_type != 'all':
            query = query.filter(Spirit.type == selected_type)
    
    spirits = query.order_by(Spirit.threat_level.desc(), Spirit.reported_at.asc()).all()
    
    # Enhanced Statistics
    stats = {
        'total': len(spirits),
        'by_threat': {
            'High': sum(1 for s in spirits if s.threat_level == 'High'),
            'Medium': sum(1 for s in spirits if s.threat_level == 'Medium'),
            'Low': sum(1 for s in spirits if s.threat_level == 'Low')
        },
        'by_type': {},
        'avg_days_active': 0,
        'most_dangerous_location': None,
        'exorcism_priority': []
    }
    
    # Calculate days active and type distribution
    type_counts = {}
    location_danger = {}
    total_days = 0
    
    for spirit in spirits:
        days_active = (datetime.utcnow() - spirit.reported_at).days
        total_days += days_active
        
        # Count by type
        type_counts[spirit.type] = type_counts.get(spirit.type, 0) + 1
        
        # Calculate location danger
        if spirit.location_id not in location_danger:
            location_danger[spirit.location_id] = {
                'name': spirit.location.name,
                'count': 0,
                'high_threat': 0
            }
        location_danger[spirit.location_id]['count'] += 1
        if spirit.threat_level == 'High':
            location_danger[spirit.location_id]['high_threat'] += 1
    
    # Calculate averages and percentages
    stats['avg_days_active'] = round(total_days / len(spirits), 1) if spirits else 0
    stats['by_type'] = {t: {'count': c, 'percent': round(c/stats['total']*100, 1)} 
                       for t, c in type_counts.items()}
    
    # Determine most dangerous location
    if location_danger:
        stats['most_dangerous_location'] = max(
            location_danger.values(), 
            key=lambda x: (x['high_threat'], x['count'])
        )
    
    # Create exorcism priority list
    priority_list = sorted(
        spirits,
        key=lambda x: (
            x.threat_level == 'High',
            x.threat_level == 'Medium',
            (datetime.utcnow() - x.reported_at).days
        ),
        reverse=True
    )
    stats['exorcism_priority'] = priority_list[:5]  # Top 5 priorities
    
    return render_template('active_spirits.html',
                         locations=locations,
                         spirits=spirits,
                         stats=stats,
                         datetime=datetime,
                         selected_location=selected_location,
                         selected_threat=selected_threat,
                         selected_type=selected_type)

if __name__ == "__main__":
    app.run(debug=True)
