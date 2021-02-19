from flask_script import Manager, Server, Shell
from covid19 import create_app, db
from config import CovidWeb
from flask_migrate import Migrate, MigrateCommand


app = create_app()
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

migrate = Migrate(app, db)

manager.add_command("runserver", Server(host=CovidWeb.HOST, port=CovidWeb.PORT))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
    app.run(host=CovidWeb.HOST, port=CovidWeb.PORT)

from covid19 import routes
