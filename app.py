from flask_web import create_app, db
from flask_web.models import Stand, User, StatusHistory, Product

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Stand": Stand, "StatusHistory": StatusHistory, "Product": Product}
