# christmas-tree-stand-monitor-service
Service for tracking water levels in your Christmas tree stand.

from flask_web import db
from flask_web.models import Product
from flask_web import create_app
app = create_app()
app.app_context().push()
p = Product(model_number="TS1-PROTOTYPE")
print(f"registration id: {p.registration_id}")
db.session.add(p)
db.session.commit()


from flask_web import db
from flask_web.models import Stand
from flask_web import create_app
app = create_app()
app.app_context().push()
db.session.query(Stand).delete()
db.session.commit()

http://127.0.0.1:5000/manage/36a281ef-03b3-4c99-a5b8-bd8ea88e90ef/edit