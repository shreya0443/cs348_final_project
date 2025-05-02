from app import db, Exorcist, Spirit, ExorcismRequest, app

with app.app_context():
    requests = ExorcismRequest.query.all()
    for request in requests:
     print(request.id, request.customer_name, request.spirit_id, request.exorcist_id)



    spirits = Spirit.query.all()
    print("Spirits in database:", spirits)

    exorcists = Exorcist.query.all()
    print("Exorcists in database:", exorcists)
