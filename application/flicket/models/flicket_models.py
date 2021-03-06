#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import url_for, g
from sqlalchemy import select, join, func

from application import app, db
from application.flicket.models import Base
from application.flicket.models.flicket_user import FlicketUser
from application.flicket_api.scripts.paginated_api import PaginatedAPIMixin

# define field sizes. max are used for forms and database. min just for forms.
field_size = {
    "title_min_length": 3,
    "title_max_length": 128,
    "content_min_length": 0,
    "content_max_length": 5000,
    "status_min_length": 3,
    "status_max_length": 20,
    "institute_min_length": 3,
    "institute_max_length": 30,
    "domain_min_length": 3,
    "domain_max_length": 128,
    "filename_min_length": 3,
    "filename_max_length": 128,
    "action_max_length": 30,
}


class FlicketStatus(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_status"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(field_size["status_max_length"]))

    def to_dict(self):
        """
        Returns a dictionary object about the status
        :return:
        """
        data = {
            "id": self.id,
            "status": self.status,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_status", id=self.id),
                "statuses": app.config["base_url"] + url_for("bp_api.get_statuses"),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketStatus: id={}, status={}>".format(self.id, self.status)


class FlicketInstitute(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_institute"

    id = db.Column(db.Integer, primary_key=True)
    institute = db.Column(db.String(field_size["institute_max_length"]))

    def __init__(self, institute):
        """

        :param institute:
        """
        self.institute = institute

    def to_dict(self):
        """
        Returns a dictionary object about the institute
        :return:
        """
        data = {
            "id": self.id,
            "institute": self.institute,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_institute", id=self.id),
                "institutes": app.config["base_url"] + url_for("bp_api.get_institutes"),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketInstitute: id={}, institute={}>".format(self.id, self.institute)


class FlicketDomain(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_domain"

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(field_size["domain_max_length"]))

    def __init__(self, domain):
        """

        :param domain:
        """
        self.domain = domain

    def to_dict(self):
        """
        Returns a dictionary object about the domain and its institute
        :return:
        """
        data = {
            "id": self.id,
            "domain": self.domain,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_domain", id=self.id),
                "domains": app.config["base_url"] + url_for("bp_api.get_domains"),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketDomain: id={}, domain={}>".format(self.id, self.domain)


class FlicketRequesterRole(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_requester_roles"

    id = db.Column(db.Integer, primary_key=True)
    requester_role = db.Column(db.String(30))

    def to_dict(self):
        """
        Returns a dictionary object about the requester role
        :return:
        """
        data = {
            "id": self.id,
            "role": self.requester_role,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_requester_role", id=self.id),
                "requester_roles": app.config["base_url"]
                + url_for("bp_api.get_requester_roles"),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketRequesterRole: id={}, requester_role={}>".format(
            self.id, self.requester_role
        )


class FlicketRequestStage(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_request_stages"

    id = db.Column(db.Integer, primary_key=True)
    request_stage = db.Column(db.String(30))

    def to_dict(self):
        """
        Returns a dictionary object about the domain and its institute
        :return:
        """
        data = {
            "id": self.id,
            "role": self.request_stage,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_request_stage", id=self.id),
                "request_stages": app.config["base_url"]
                + url_for("bp_api.get_request_stages"),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketRequestStage: id={}, request_stage={}>".format(
            self.id, self.request_stage
        )


class FlicketProcedureStage(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_procedure_stages"

    id = db.Column(db.Integer, primary_key=True)
    procedure_stage = db.Column(db.String(30))

    def to_dict(self):
        """
        Returns a dictionary object about the procedure stage
        :return:
        """
        data = {
            "id": self.id,
            "role": self.procedure_stage,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_procedure_stage", id=self.id),
                "procedure_stages": app.config["base_url"]
                + url_for("bp_api.get_procedure_stages"),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketProcedureStage: id={}, procedure_stage={}>".format(
            self.id, self.procedure_stage
        )


class FlicketTicket(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_topic"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(field_size["title_max_length"]), index=True)
    requester = db.Column(db.String(field_size["title_max_length"]), index=True)
    referee = db.Column(db.String(field_size["title_max_length"]), index=True)
    content = db.Column(db.String(field_size["content_max_length"]))

    started_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser, foreign_keys="FlicketTicket.started_id")

    date_added = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())

    modified_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    modified = db.relationship(FlicketUser, foreign_keys="FlicketTicket.modified_id")

    status_id = db.Column(db.Integer, db.ForeignKey(FlicketStatus.id))
    current_status = db.relationship(FlicketStatus)

    domain_id = db.Column(db.Integer, db.ForeignKey(FlicketDomain.id))
    domain = db.relationship(FlicketDomain)

    institute_id = db.Column(db.Integer, db.ForeignKey(FlicketInstitute.id))
    institute = db.relationship(FlicketInstitute)

    assigned_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    assigned = db.relationship(FlicketUser, foreign_keys="FlicketTicket.assigned_id")

    requester_role_id = db.Column(db.Integer, db.ForeignKey(FlicketRequesterRole.id))
    requester_role = db.relationship(FlicketRequesterRole)

    request_stage_id = db.Column(db.Integer, db.ForeignKey(FlicketRequestStage.id))
    request_stage = db.relationship(FlicketRequestStage)

    procedure_stage_id = db.Column(db.Integer, db.ForeignKey(FlicketProcedureStage.id))
    procedure_stage = db.relationship(FlicketProcedureStage)

    posts = db.relationship("FlicketPost", back_populates="ticket")

    days = db.Column(db.Numeric(10, 2), server_default="0")

    # find all the images associated with the topic
    uploads = db.relationship(
        "FlicketUploads",
        primaryjoin="and_(FlicketTicket.id == FlicketUploads.topic_id)",
    )

    # finds all the users who are subscribed to the ticket.
    subscribers = db.relationship(
        "FlicketSubscription", order_by="FlicketSubscription.user_def"
    )

    # finds all the actions associated with the ticket
    actions = db.relationship(
        "FlicketAction", primaryjoin="FlicketTicket.id == FlicketAction.ticket_id"
    )

    # finds all the actions associated with the ticket and not associated with any post
    actions_nonepost = db.relationship(
        "FlicketAction",
        primaryjoin="and_(FlicketTicket.id == FlicketAction.ticket_id, "
        "FlicketAction.post_id == None)",
    )

    @property
    def num_replies(self):
        n_replies = FlicketPost.query.filter_by(ticket_id=self.id).count()
        return n_replies

    @property
    def id_zfill(self):
        return str(self.id).zfill(5)

    def is_subscribed(self, user):
        for s in self.subscribers:
            if s.user == user:
                return True
        return False

    @staticmethod
    def form_redirect(form, url="flicket_bp.tickets"):
        """

        :param form:
        :param url:
        :return:
        """

        institute = ""
        domain = ""
        status = ""
        user_id = ""
        requester_role = ""
        request_stage = ""
        procedure_stage = ""

        if form.username.data:
            user = FlicketUser.query.filter_by(id=form.username.data).first()
            if user:
                user_id = user.id

        # convert form inputs to it's table title
        if form.institute.data:
            institute = (
                FlicketInstitute.query.filter_by(id=form.institute.data)
                .first()
                .institute
            )
        if form.domain.data:
            domain = FlicketDomain.query.filter_by(id=form.domain.data).first().domain

        if form.status.data:
            status = FlicketStatus.query.filter_by(id=form.status.data).first().status

        if form.requester_role.data:
            requester_role = (
                FlicketRequesterRole.query.filter_by(id=form.requester_role.data)
                .first()
                .requester_role
            )
        if form.request_stage.data:
            request_stage = (
                FlicketRequestStage.query.filter_by(id=form.request_stage.data)
                .first()
                .request_stage
            )

        if form.procedure_stage.data:
            procedure_stage = (
                FlicketProcedureStage.query.filter_by(id=form.procedure_stage.data)
                .first()
                .procedure_stage
            )

        redirect_url = url_for(
            url,
            content=form.content.data,
            institute=institute,
            domain=domain,
            status=status,
            user_id=user_id,
            requester_role=requester_role,
            request_stage=request_stage,
            procedure_stage=procedure_stage,
        )

        return redirect_url

    @property
    def total_days(self):
        """
        Sums all days related to ticket (posts + ticket itself).
        :return:
        """

        days = (
            db.session.query(func.sum(FlicketPost.days))
            .filter_by(ticket_id=self.id)
            .scalar()
            or 0
        )

        return days + self.days

    def get_subscriber_emails(self):
        """
        Function to return a list of email addresses of subscribed users.
        :return:
        """
        emails = list()
        for user in self.subscribers:
            emails.append(user.user.email)

        return emails

    @staticmethod
    def my_tickets(ticket_query):
        """
        Function to return all tickets created by or assigned to user.
        :return:
        """
        ticket_query = ticket_query.filter(
            (FlicketTicket.started_id == g.user.id)
            | (FlicketTicket.assigned_id == g.user.id)
        )

        return ticket_query

    @staticmethod
    def query_tickets(form=None, **kwargs):
        """
        Returns a filtered query and modified form based on form submission
        :param form:
        :param kwargs:
        :return:
        """

        ticket_query = FlicketTicket.query

        # hide closed tickets by default
        # if kwargs["status"] is None:
        #     ticket_query = ticket_query.filter(
        #         FlicketTicket.current_status.has(FlicketStatus.status != "Closed")
        #     )

        for key, value in kwargs.items():

            if key == "status" and value:
                ticket_query = ticket_query.filter(
                    FlicketTicket.current_status.has(FlicketStatus.status == value)
                )
                if form:
                    form.status.data = (
                        FlicketStatus.query.filter_by(status=value).first().id
                    )
            if key == "requester_role" and value:
                ticket_query = ticket_query.filter(
                    FlicketTicket.requester_role.has(
                        FlicketRequesterRole.requester_role == value
                    )
                )
                if form:
                    form.requester_role.data = (
                        FlicketRequesterRole.query.filter_by(requester_role=value)
                        .first()
                        .id
                    )
            if key == "request_stage" and value:
                ticket_query = ticket_query.filter(
                    FlicketTicket.request_stage.has(
                        FlicketRequestStage.request_stage == value
                    )
                )
                if form:
                    form.request_stage.data = (
                        FlicketRequestStage.query.filter_by(request_stage=value)
                        .first()
                        .id
                    )
            if key == "procedure_stage" and value:
                ticket_query = ticket_query.filter(
                    FlicketTicket.procedure_stage.has(
                        FlicketProcedureStage.procedure_stage == value
                    )
                )
                if form:
                    form.procedure_stage.data = (
                        FlicketProcedureStage.query.filter_by(procedure_stage=value)
                        .first()
                        .id
                    )
            if key == "institute" and value:
                ticket_query = ticket_query.filter(
                    FlicketTicket.institute.has(FlicketInstitute.institute == value)
                )
                if form:
                    form.institute.data = (
                        FlicketInstitute.query.filter_by(institute=value).first().id
                    )
            if key == "domain" and value:
                ticket_query = ticket_query.filter(
                    FlicketTicket.domain.has(FlicketDomain.domain == value)
                )
                if form:
                    form.domain.data = (
                        FlicketDomain.query.filter_by(domain=value).first().id
                    )
            if key == "user_id" and value:
                # ticket_query = ticket_query.filter_by(assigned_id=int(value))
                ticket_query = ticket_query.filter(
                    (FlicketTicket.assigned_id == int(value))
                    | (FlicketTicket.started_id == int(value))
                )
                user = FlicketUser.query.filter_by(id=value).first()
                if form:
                    form.username.data = user.username

            if key == "content" and value:
                # search the titles
                if form:
                    form.content.data = key

                f1 = FlicketTicket.title.ilike("%" + value + "%")
                f2 = FlicketTicket.content.ilike("%" + value + "%")
                f3 = FlicketTicket.posts.any(
                    FlicketPost.content.ilike("%" + value + "%")
                )
                ticket_query = ticket_query.filter(f1 | f2 | f3)

            if key == "requester" and value:

                query_filter = FlicketTicket.requester.ilike("%" + value + "%")
                ticket_query = ticket_query.filter(query_filter)

            if key == "referee" and value:

                query_filter = FlicketTicket.referee.ilike("%" + value + "%")
                ticket_query = ticket_query.filter(query_filter)

        return ticket_query, form

    @staticmethod
    def sorted_tickets(ticket_query, sort):
        """
        Function to return sorted tickets.
        :param ticket_query:
        :param sort:
        :return:
        """
        if sort == "requester_role":
            ticket_query = ticket_query.order_by(
                FlicketTicket.requester_role_id, FlicketTicket.id
            )
        elif sort == "request_stage":
            ticket_query = ticket_query.order_by(
                FlicketTicket.request_stage_id, FlicketTicket.id
            )
        elif sort == "procedure_stage":
            ticket_query = ticket_query.order_by(
                FlicketTicket.procedure_stage_id, FlicketTicket.id
            )
        elif sort == "title":
            ticket_query = ticket_query.order_by(FlicketTicket.title, FlicketTicket.id)
        elif sort == "ticketid":
            ticket_query = ticket_query.order_by(FlicketTicket.id)
        elif sort == "ticketid_desc":
            ticket_query = ticket_query.order_by(FlicketTicket.id.desc())
        elif sort == "addedby":
            ticket_query = ticket_query.join(FlicketUser, FlicketTicket.user).order_by(
                FlicketUser.name, FlicketTicket.id
            )
        elif sort == "addedon":
            ticket_query = ticket_query.order_by(
                FlicketTicket.date_added, FlicketTicket.id
            )
        elif sort == "addedon_desc":
            ticket_query = ticket_query.order_by(
                FlicketTicket.date_added.desc(), FlicketTicket.id
            )
        elif sort == "replies":
            replies_count = func.count(FlicketPost.id).label("replies_count")
            ticket_query = (
                ticket_query.outerjoin(FlicketTicket.posts)
                .group_by(FlicketTicket.id)
                .order_by(replies_count, FlicketTicket.id)
            )
        elif sort == "replies_desc":
            replies_count = func.count(FlicketPost.id).label("replies_count")
            ticket_query = (
                ticket_query.outerjoin(FlicketTicket.posts)
                .group_by(FlicketTicket.id)
                .order_by(replies_count.desc(), FlicketTicket.id)
            )
        elif sort == "status":
            ticket_query = ticket_query.order_by(
                FlicketTicket.status_id, FlicketTicket.id
            )
        elif sort == "status_desc":
            ticket_query = ticket_query.order_by(
                FlicketTicket.status_id.desc(), FlicketTicket.id
            )
        elif sort == "assigned":
            ticket_query = ticket_query.outerjoin(
                FlicketUser, FlicketTicket.assigned
            ).order_by(FlicketUser.name, FlicketTicket.id)
        elif sort == "time":
            total_days = (FlicketTicket.days + func.sum(FlicketPost.days)).label(
                "total_days"
            )
            ticket_query = (
                ticket_query.outerjoin(FlicketTicket.posts)
                .group_by(FlicketTicket.id)
                .order_by(total_days, FlicketTicket.id)
            )
        elif sort == "time_desc":
            total_days = (FlicketTicket.days + func.sum(FlicketPost.days)).label(
                "total_days"
            )
            ticket_query = (
                ticket_query.outerjoin(FlicketTicket.posts)
                .group_by(FlicketTicket.id)
                .order_by(total_days.desc(), FlicketTicket.id)
            )

        return ticket_query

    def from_dict(self, data):
        """

        :param data:
        :return:
        """
        for field in [
            "title",
            "content",
            "requester",
            "referee",
            "domain_id",
            "institute_id",
            "requester_role_id",
            "request_stage_id",
            "procedure_stage_id",
        ]:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        """

        :return: dict()
        """

        modified_by = None
        assigned = None

        if self.modified_id:
            modified_by = app.config["base_url"] + url_for(
                "bp_api.get_user", id=self.modified_id
            )

        if self.assigned_id:
            assigned = app.config["base_url"] + url_for(
                "bp_api.get_user", id=self.assigned_id
            )

        data = {
            "id": self.id,
            "assigned_id": self.assigned_id,
            "domain_id": self.domain_id,
            "institute_id": self.institute_id,
            "content": self.content,
            "requester": self.requester,
            "referee": self.referee,
            "date_added": self.date_added,
            "date_modified": self.date_modified,
            "modified_id": self.modified_id,
            "started_id": self.started_id,
            "status_id": self.status_id,
            "title": self.title,
            "requester_role_id": self.requester_role_id,
            "request_stage_id": self.request_stage_id,
            "procedure_stage_id": self.procedure_stage_id,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_ticket", id=self.id),
                "assigned": assigned,
                "requester_role": app.config["base_url"]
                + url_for("bp_api.get_requester_role", id=self.requester_role_id),
                "request_stage": app.config["base_url"]
                + url_for("bp_api.get_request_stage", id=self.request_stage_id),
                "procedure_stage": app.config["base_url"]
                + url_for("bp_api.get_procedure_stage", id=self.procedure_stage_id),
                "started_ny": app.config["base_url"]
                + url_for("bp_api.get_user", id=self.started_id),
                "modified_by": modified_by,
                "domain": app.config["base_url"]
                + url_for("bp_api.get_domain", id=self.domain_id),
                "institute": app.config["base_url"]
                + url_for("bp_api.get_institute", id=self.institute_id),
                "status": app.config["base_url"]
                + url_for("bp_api.get_status", id=self.status_id),
                "subscribers": app.config["base_url"]
                + url_for("bp_api.get_subscriptions", ticket_id=self.id),
                "tickets": app.config["base_url"] + url_for("bp_api.get_tickets"),
                "histories": app.config["base_url"]
                + url_for("bp_api.get_histories", topic_id=self.id),
            },
        }

        return data

    @staticmethod
    def carousel_query():
        """
        Return all 'open' 'high priority' tickets for carousel.
        :return:
        """

        tickets = (
            FlicketTicket.query.filter(FlicketTicket.procedure_stage_id == 3)
            .filter(FlicketTicket.status_id == 1)
            .limit(100)
        )

        return tickets

    def __repr__(self):
        return (
            f"<FlicketTicket: "
            f"id={self.id}, "
            f'title="{self.title}", '
            f"created_by={self.user}, "
            f"domain={self.domain}"
            f"institute={self.institute}"
            f"status={self.current_status}"
            f"assigned={self.assigned}>"
        )


class FlicketPost(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_post"

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket, back_populates="posts")

    content = db.Column(db.String(field_size["content_max_length"]))

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser, foreign_keys="FlicketPost.user_id")

    date_added = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())

    modified_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    modified = db.relationship(FlicketUser, foreign_keys="FlicketPost.modified_id")

    days = db.Column(db.Numeric(10, 2), server_default="0")

    # finds all the images associated with the post
    uploads = db.relationship(
        "FlicketUploads", primaryjoin="and_(FlicketPost.id == FlicketUploads.posts_id)"
    )

    # finds all the actions associated with the post
    actions = db.relationship(
        "FlicketAction", primaryjoin="FlicketPost.id == FlicketAction.post_id"
    )

    def to_dict(self):
        """

        :return: dict()
        """

        data = {
            "id": self.id,
            "content": self.content,
            "data_added": self.date_added,
            "date_modified": self.date_modified,
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "links": {
                "self": app.config["base_url"] + url_for("bp_api.get_post", id=self.id),
                "created_by": app.config["base_url"]
                + url_for("bp_api.get_user", id=self.user_id),
                "posts": app.config["base_url"]
                + url_for("bp_api.get_posts", ticket_id=self.ticket_id),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketPost: id={}, ticket_id={}, content={}>".format(
            self.id, self.ticket_id, self.content
        )


class FlicketUploads(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_uploads"

    id = db.Column(db.Integer, primary_key=True)

    posts_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    topic_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    topic = db.relationship(FlicketTicket)

    filename = db.Column(db.String(field_size["filename_max_length"]))
    original_filename = db.Column(db.String(field_size["filename_max_length"]))

    def to_dict(self):
        """

        :return: dict()
        """

        ticket_url, post_url = None, None

        if self.topic_id:
            ticket_url = app.config["base_url"] + url_for(
                "bp_api.get_ticket", id=self.topic_id
            )

        if self.posts_id:
            post_url = app.config["base_url"] + url_for(
                "bp_api.get_post", id=self.posts_id
            )

        data = {
            "id": self.id,
            "filename": self.filename,
            "image": app.config["base_url"] + "/flicket_uploads/" + self.filename,
            "original_filename": self.original_filename,
            "post_id": self.posts_id,
            "topic_id": self.topic_id,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_upload", id=self.id),
                "post": post_url,
                "ticket": ticket_url,
                "uploads": app.config["base_url"] + url_for("bp_api.get_uploads"),
            },
        }

        return data

    def __repr__(self):
        return (
            "<FlicketUploads: id={}, "
            "post_id={}, topic_id={}, filename={}, original_filename={}>"
        ).format(
            self.id, self.posts_id, self.topic_id, self.filename, self.original_filename
        )


class FlicketHistory(PaginatedAPIMixin, Base):
    """
    A database to track the editing of tickets and posts.
    """

    __tablename__ = "flicket_history"

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    topic_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    topic = db.relationship(FlicketTicket)

    date_modified = db.Column(db.DateTime())

    original_content = db.Column(db.String(field_size["content_max_length"]))

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser)

    def to_dict(self):
        """

        :return: dict()
        """

        ticket_url, post_url = None, None

        if self.topic_id:
            ticket_url = app.config["base_url"] + url_for(
                "bp_api.get_ticket", id=self.topic_id
            )

        if self.post_id:
            post_url = app.config["base_url"] + url_for(
                "bp_api.get_post", id=self.post_id
            )

        data = {
            "id": self.id,
            "date_modified": self.date_modified,
            "original_content": self.original_content,
            "post_id": self.post_id,
            "topic_id": self.topic_id,
            "user_id": self.user_id,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_history", id=self.id),
                "histories": app.config["base_url"] + url_for("bp_api.get_histories"),
                "post": post_url,
                "ticket": ticket_url,
                "user": app.config["base_url"]
                + url_for("bp_api.get_user", id=self.user_id),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketHistory: id={}, post_id={}, topic_id={}>".format(
            self.id, self.posts_id, self.topic_id
        )


class FlicketSubscription(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_ticket_subscription"

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket)

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser)

    user_def = db.deferred(
        db.select([FlicketUser.name]).where(FlicketUser.id == user_id)
    )

    def to_dict(self):
        """

        :return: dict()
        """

        data = {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "user_def": self.user_def,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_subscription", id=self.id),
                "subscriptions": app.config["base_url"]
                + url_for("bp_api.get_subscriptions"),
                "ticket": app.config["base_url"]
                + url_for("bp_api.get_ticket", id=self.ticket_id),
                "user": app.config["base_url"]
                + url_for("bp_api.get_user", id=self.user_id),
            },
        }

        return data

    def __repr__(self):
        return "<Class FlicketSubscription: ticket_id={}, user_id={}>".format(
            self.ticket_id, self.user_id
        )


class FlicketAction(PaginatedAPIMixin, Base):
    """
    SQL table that stores the action history of a ticket.
    For example, if a user claims a ticket that action is stored here.
    The action is associated with ticket_id and latest post_id (if exists).
    """

    __tablename__ = "flicket_ticket_action"

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket)

    post_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    action = db.Column(db.String(field_size["action_max_length"]))
    data = db.Column(db.JSON(none_as_null=True))

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser, foreign_keys=[user_id])

    recipient_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    recipient = db.relationship(FlicketUser, foreign_keys=[recipient_id])

    date = db.Column(db.DateTime)

    def output_action(self):
        """
        Method used in ticket view to show what action has taken place in ticket.
        :return:
        """

        _date = self.date.strftime("%d-%m-%Y %H:%M")

        if self.action == "open":
            return (
                f"Ticket opened"
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

        if self.action == "assign":
            return (
                f'Ticket assigned to <a href="mailto:{self.recipient.email}">{self.recipient.name}</a>'
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

        if self.action == "claim":
            return (
                f"Ticked claimed"
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

        if self.action == "status":
            return (
                f'Ticket status has been changed to "{self.data["status"]}"'
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

        if self.action == "request_stage":
            return (
                f'Ticket request stage  has been changed to "{self.data["request_stage"]}"'
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

        if self.action == "procedure_stage":
            return (
                f'Ticket procedure stage has been changed to "{self.data["procedure_stage"]}"'
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

        if self.action == "release":
            return (
                f"Ticket released"
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

        if self.action == "close":
            return (
                f"Ticked closed"
                f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}'
            )

    def to_dict(self):
        """

        :return: dict()
        """

        data = {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "post_id": self.post_id,
            "action": self.action,
            "data": self.data,
            "user_id": self.user_id,
            "recipient_id": self.recipient_id,
            "date": self.date,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_action", id=self.id),
                "actions": app.config["base_url"]
                + url_for("bp_api.get_actions", ticket_id=self.ticket_id),
            },
        }

        return data

    def __repr__(self):
        return (
            f"<Class FlicketAction: ticket_id={self.ticket_id}, post_id={self.ticket_id}, action={self.action!r}, "
            f"data={self.data}, user_id={self.user_id}, recipient_id={self.recipient_id}, date={self.date}>"
        )
