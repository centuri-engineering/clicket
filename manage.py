#! usr/bin/python3
# -*- coding: utf-8 -*-

# from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from setup import run_set_up
from application import app, db

# from scripts.email_batch_notifications import EmailOutStandingTickets
# from scripts.users_export_to_json import ExportUsersToJson
# from scripts.users_import_from_json import ImportUsersFromJson
# from scripts.update_user_details import TotalUserPosts, TotalUserAssigned

migrate = Migrate(app, db, compare_type=True)

# manager.add_command("export_users", ExportUsersToJson)
# manager.add_command("import_users", ImportUsersFromJson)
# manager.add_command("update_user_posts", TotalUserPosts)
# manager.add_command("update_user_assigned", TotalUserAssigned)
# manager.add_command("email_outstanding_tickets", EmailOutStandingTickets)

# manager.add_command(
#     "runserver",
#     Server(host="0.0.0.0", port=5001, use_reloader=False, use_debugger=False),
# )


@app.cli.command("runserver")
def runserver():
    app.run(host="0.0.0.0", port=5001, use_reloader=False, use_debugger=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, use_reloader=False, use_debugger=False)
