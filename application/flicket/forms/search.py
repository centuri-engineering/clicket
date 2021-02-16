#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField

from .flicket_forms import does_user_exist

from application.flicket.models.flicket_models import (
    FlicketTeam,
    FlicketRequestType,
    FlicketStatus,
    FlicketInstrument,
    FlicketRequestStage,
)
from application.flicket.models.flicket_user import FlicketUser


class SearchTicketForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        form = super(SearchTicketForm, self).__init__(*args, **kwargs)

        # choices are populated via ajax query on page load. This are simply empty lists so
        # form can be loaded on page view
        self.team.choices = [
            (d.id, d.team)
            for d in FlicketTeam.query.order_by(FlicketTeam.team.asc()).all()
        ]
        self.team.choices.insert(0, (0, "team"))

        self.request_type.choices = [
            (c.id, c.request_type)
            for c in FlicketRequestType.query.order_by(
                FlicketRequestType.request_type.asc()
            ).all()
        ]
        self.request_type.choices.insert(0, (0, "request"))

        self.username.choices = [
            (u.id, u.username)
            for u in FlicketUser.query.all()
            if not u.username in ["admin", "notification"]
        ]
        self.username.choices.insert(0, (0, "username"))

        self.status.choices = [(s.id, s.status) for s in FlicketStatus.query.all()]
        self.status.choices.insert(0, (0, "status"))

        self.instrument.choices = [
            (s.id, s.instrument) for s in FlicketInstrument.query.all()
        ]
        self.instrument.choices.insert(0, (0, "requester role"))

        self.request_stage.choices = [
            (s.id, s.request_stage) for s in FlicketRequestStage.query.all()
        ]
        self.request_stage.choices.insert(0, (0, "request stage"))

    """ Search form. """
    team = SelectField(lazy_gettext("team"), coerce=int, validators=[])
    request_type = SelectField(lazy_gettext("request type"), coerce=int)
    status = SelectField(lazy_gettext("status"), coerce=int)
    username = SelectField(lazy_gettext("username"), coerce=int, validators=[])
    content = StringField(lazy_gettext("content"), validators=[])
    instrument = SelectField(lazy_gettext("requester role"), coerce=int)
    request_stage = SelectField(lazy_gettext("request stage"), coerce=int)

    def __repr__(self):
        return "<SearchTicketForm>"
