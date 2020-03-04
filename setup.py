#! usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json

from flask_script import Command

from scripts.create_json import WriteConfigJson, config_file
from application import db, app
from application.flicket_admin.models.flicket_config import FlicketConfig
from application.flicket.models.flicket_models import (
    FlicketStatus,
    FlicketPriority,
    FlicketRequesterRole,
    FlicketRequestStage,
    FlicketProcedureStage,
    FlicketInstitute,
    FlicketDomain,
)
from application.flicket.models.flicket_user import FlicketUser, FlicketGroup
from application.flicket.scripts.hash_password import hash_password

admin = "admin"

# configuration defaults for flicket
flicket_config = {
    "posts_per_page": 50,
    "allowed_extensions": [
        "txt",
        "log",
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "gif",
        "msg",
        "doc",
        "docx",
        "ppt",
        "pptx",
        "xls",
        "xlsx",
    ],
    "ticket_upload_folder": "application/flicket/static/flicket_uploads",
    "avatar_upload_folder": "application/flicket/static/flicket_avatars",
}

# Default domains
domains = [
    "Bioinformatics",
    "Database Management",
    "Image data processing",
    "Optics and biophotonics",
    "Mechatronics",
    "Software Development",
]

institutes = [
    "IBDM",
    "Institut Fresnel",
    "CIML",
    "INMED",
    "CINAM",
    "LAI",
    "IRPHE",
    "M2P2",
    "TAGC",
    "IUSTI",
    "TAGC",
    "Ciphe",
    "CPT",
    "IMM",
    "Centrale Marseille",
    "LIS",
]


procedure_stages = [
    "Consulting",
    "Maintenance",
    "First contact",
    "Short",
    "Submited",
    "Validated",
]


request_stages = ["New", "In progress", "Pending", "Ready", "Finished", "Declined"]


class RunSetUP(Command):
    def run(self):
        WriteConfigJson().json_exists()
        username, password, email = self.get_admin_details()
        self.set_db_config_defaults()
        self.set_email_config()
        self.create_admin(
            username=username, password=password, email=email, job_title="admin"
        )
        self.create_notifier()
        self.create_admin_group()
        self.create_default_ticket_status()
        self.create_default_priority_levels()
        self.create_default_requester_role_levels()
        self.create_default_request_stage_levels()
        self.create_default_procedure_stage_levels()
        self.create_default_depts()
        # commit changes to the database
        db.session.commit()

    @staticmethod
    def set_db_config_defaults(silent=False):

        with open(config_file, "r") as f:
            config_data = json.load(f)

        base_url = config_data["base_url"]

        count = FlicketConfig.query.count()
        if count > 0:
            if not silent:
                print(
                    "Flicket Config database seems to already be populated. Check values via application."
                )
            return

        set_config = FlicketConfig(
            posts_per_page=flicket_config["posts_per_page"],
            allowed_extensions=", ".join(flicket_config["allowed_extensions"]),
            ticket_upload_folder=flicket_config["ticket_upload_folder"],
            avatar_upload_folder=flicket_config["avatar_upload_folder"],
            base_url=base_url,
            application_title="Clicket",
            mail_max_emails=10,
            mail_port=465,
        )

        if not silent:
            print("Adding config values to database.")

        db.session.add(set_config)
        db.session.commit()

    @staticmethod
    def get_admin_details():

        # todo: add some password validation to prevent easy passwords being entered
        _username = admin
        with open(config_file, "r") as f:
            config_data = json.load(f)

        email = config_data["admin_email"]
        password = config_data["admin_password"]
        return _username, password, email

    @staticmethod
    def create_admin(username, password, email, job_title, silent=False):
        """ creates flicket_admin user. """

        query = FlicketUser.query.filter_by(username=username)
        if query.count() == 0:
            add_user = FlicketUser(
                username=username,
                name=username,
                password=hash_password(password),
                email=email,
                job_title=job_title,
                date_added=datetime.datetime.now(),
            )
            db.session.add(add_user)

            if not silent:
                print("Admin user added.")
        else:
            print("Admin user is already added.")

    @staticmethod
    def create_notifier():
        """ creates user for notifications """

        query = FlicketUser.query.filter_by(
            username=app.config["NOTIFICATION"]["username"]
        )
        if query.count() == 0:
            add_user = FlicketUser(
                username=app.config["NOTIFICATION"]["username"],
                name=app.config["NOTIFICATION"]["name"],
                password=hash_password(app.config["NOTIFICATION"]["password"]),
                email=app.config["NOTIFICATION"]["email"],
                date_added=datetime.datetime.now(),
            )
            db.session.add(add_user)
            print("Notification user added.")
        else:
            print("Notification user already added.")

    @staticmethod
    def create_admin_group(silent=False):
        """ creates flicket_admin and super_user group and assigns flicket_admin to group admin. """

        query = FlicketGroup.query.filter_by(group_name=app.config["ADMIN_GROUP_NAME"])
        if query.count() == 0:
            add_group = FlicketGroup(group_name=app.config["ADMIN_GROUP_NAME"])
            db.session.add(add_group)
            if not silent:
                print("Admin group added")

        user = FlicketUser.query.filter_by(username=admin).first()
        group = FlicketGroup.query.filter_by(
            group_name=app.config["ADMIN_GROUP_NAME"]
        ).first()
        in_group = False
        # see if user flicket_admin is already in flicket_admin group.
        for g in group.users:
            if g.username == admin:
                in_group = True
                break
        if not in_group:
            group.users.append(user)
            if not silent:
                print("Added flicket_admin user to flicket_admin group.")

        #  create the super_user group
        query = FlicketGroup.query.filter_by(
            group_name=app.config["SUPER_USER_GROUP_NAME"]
        )
        if query.count() == 0:
            add_group = FlicketGroup(group_name=app.config["SUPER_USER_GROUP_NAME"])
            db.session.add(add_group)
            if not silent:
                print("super_user group added")

    # noinspection PyArgumentList
    @staticmethod
    def create_default_ticket_status(silent=False):
        """ set up default status levels """

        sl = ["Open", "Closed"]
        for s in sl:
            status = FlicketStatus.query.filter_by(status=s).first()

            if not status:
                add_status = FlicketStatus(status=s)
                db.session.add(add_status)
                if not silent:
                    print("Added status level {}".format(s))

    @staticmethod
    def create_default_priority_levels(silent=False):
        """ set up default priority levels """

        pl = ["low", "medium", "high"]
        for p in pl:
            priority = FlicketPriority.query.filter_by(priority=p).first()

            if not priority:
                add_priority = FlicketPriority(priority=p)
                db.session.add(add_priority)

                if not silent:
                    print("Added priority level {}".format(p))

    @staticmethod
    def create_default_requester_role_levels(silent=False):
        """ set up default requester_role levels """

        pl = ["PhD", "PostDoc", "Engineer", "Researcher"]
        for p in pl:
            requester_role = FlicketRequesterRole.query.filter_by(
                requester_role=p
            ).first()

            if not requester_role:
                add_requester_role = FlicketRequesterRole(requester_role=p)
                db.session.add(add_requester_role)

                if not silent:
                    print("Added requester role level {}".format(p))

    @staticmethod
    def create_default_request_stage_levels(silent=False):
        """ set up default request_stage levels """

        for level in request_stages:
            request_stage = FlicketRequestStage.query.filter_by(
                request_stage=level
            ).first()
            if not request_stage:
                add_request_stage = FlicketRequestStage(request_stage=level)
                db.session.add(add_request_stage)

                if not silent:
                    print("Added request stage level {}".format(level))

    @staticmethod
    def create_default_procedure_stage_levels(silent=False):
        """ set up default procedure_stage levels """

        for level in procedure_stages:
            procedure_stage = FlicketProcedureStage.query.filter_by(
                procedure_stage=level
            ).first()
            if not procedure_stage:
                add_procedure_stage = FlicketProcedureStage(procedure_stage=level)
                db.session.add(add_procedure_stage)

                if not silent:
                    print("Added procedure stage level {}".format(level))

    @staticmethod
    def create_default_depts(silent=False):
        """ creates default institutes and domains. """

        for institute in institutes:
            query = FlicketInstitute.query.filter_by(institute=institute).first()
            if not query:
                add_institute = FlicketInstitute(institute=institute)
                db.session.add(add_institute)

                if not silent:
                    print("institute {} added.".format(institute))

        for domain in domains:
            query = FlicketDomain.query.filter_by(domain=domain).first()
            if not query:
                add_domain = FlicketDomain(domain=domain)
                db.session.add(add_domain)

                if silent is False:
                    print("domain {} added.".format(domain))

    @staticmethod
    def set_email_config(silent=False):
        """
        To stop mail send errors after initial set-up set the email configuration value for suppress
        send will be set to True
        :return:
        """

        query = FlicketConfig.query.first()
        if query.mail_server is None:
            query.mail_debug = True
            query.mail_suppress_send = True
            db.session.commit()
            if not silent:
                print(
                    "Setting email settings to suppress sending. Change values via administration panel with in "
                    "Flicket."
                )


class TestingSetUp:
    @staticmethod
    def set_db_config_defaults_testing(silent=False):
        """
        Set config defaults. Only used for unit testing
        :param silent:
        :return:
        """

        set_config = FlicketConfig(
            posts_per_page=10,
            allowed_extensions="txt,  jpg",
            ticket_upload_folder="tmp/uploads",
            base_url="",
            mail_debug=True,
            mail_suppress_send=True,
        )

        if not silent:
            print("Adding config values to database.")

        db.session.add(set_config)
        db.session.commit()
