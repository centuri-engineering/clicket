#! usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
from application import app

from application.flicket.models.flicket_user import FlicketUser as User

json_user_file = "users.json"


@app.cli.command("export_users_to_json")
def export_users_to_json(self):
    """
    Command used by manage.py to export all the users from the database to a json file.
    Useful if we need a list of users to import into other applications.
    """
    db_user_list = self.db_users()
    self.dump_json(db_user_list)


def db_users():
    """
    Create queries flicket database and returns list of users.
    :return:         [
        { username, name, email, password.
    ]
    """
    # query database.
    users = User.query.all()
    output_list = []

    for u in users:
        loop_dict = dict()
        loop_dict["username"] = u.username
        loop_dict["name"] = u.name
        loop_dict["email"] = u.email
        loop_dict["password"] = u.password.decode("utf-8")
        output_list.append(loop_dict)

    return output_list


def dump_json(json_list):
    """
    Takes list of users and writes to a file
    :param json_list:
    :return: writes to json_user_file
    """

    # check existence of json file.
    if os.path.isfile(json_user_file):

        while True:
            over_write = input("json user file already exists. Over write? (Y/n)> ")
            if over_write == "Y":
                return False
            else:
                print("You have opted to not over write. Exiting ....")
                exit()

    file_text = json.dumps(json_list)

    with open(json_user_file, "w") as f:
        f.write(file_text)
