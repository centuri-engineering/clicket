#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField

from .flicket_forms import does_user_exist
from application.flicket.models.flicket_models import (
    FlicketInstitute,
    FlicketDomain,
    FlicketStatus,
    FlicketRequesterRole,
    FlicketRequestStage,
    FlicketProcedureStage,
)


class SearchTicketForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        form = super(SearchTicketForm, self).__init__(*args, **kwargs)

        # choices are populated via ajax query on page load. This are simply empty lists so
        # form can be loaded on page view
        self.institute.choices = [
            (d.id, d.institute)
            for d in FlicketInstitute.query.order_by(
                FlicketInstitute.institute.asc()
            ).all()
        ]
        self.institute.choices.insert(0, (0, "institute"))

        self.domain.choices = [
            (c.id, c.domain)
            for c in FlicketDomain.query.order_by(FlicketDomain.domain.asc()).all()
        ]
        self.domain.choices.insert(0, (0, "domain"))

        self.status.choices = [(s.id, s.status) for s in FlicketStatus.query.all()]
        self.status.choices.insert(0, (0, "status"))

        self.requester_role.choices = [
            (s.id, s.requester_role) for s in FlicketRequesterRole.query.all()
        ]
        self.requester_role.choices.insert(0, (0, "requester role"))

        self.request_stage.choices = [
            (s.id, s.request_stage) for s in FlicketRequestStage.query.all()
        ]
        self.request_stage.choices.insert(0, (0, "request stage"))

        self.procedure_stage.choices = [
            (s.id, s.procedure_stage) for s in FlicketProcedureStage.query.all()
        ]
        self.procedure_stage.choices.insert(0, (0, "procedure stage"))

    """ Search form. """
    institute = SelectField(lazy_gettext("institute"), coerce=int, validators=[])
    domain = SelectField(lazy_gettext("domain"), coerce=int)
    status = SelectField(lazy_gettext("status"), coerce=int)
    username = StringField(lazy_gettext("username"), validators=[does_user_exist])
    content = StringField(lazy_gettext("content"), validators=[])
    requester_role = SelectField(lazy_gettext("requester role"), coerce=int)
    request_stage = SelectField(lazy_gettext("request stage"), coerce=int)
    procedure_stage = SelectField(lazy_gettext("procedure stage"), coerce=int)

    def __repr__(self):
        return "<SearchTicketForm>"
