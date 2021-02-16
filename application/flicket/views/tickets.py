#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from datetime import datetime

from flask import redirect
from flask import request as rq
from flask import make_response
from flask import render_template
from flask import Response
from flask import url_for
from flask_babel import gettext
from flask_login import login_required

from application import app
from application.flicket.forms.search import SearchTicketForm
from application.flicket.models.flicket_models import FlicketTicket
from . import flicket_bp


def clean_csv_data(input_text):

    output_text = input_text.replace('"', "'")

    return output_text


def tickets_view(page, is_my_view=False):
    """
    Function common to 'tickets' and 'my_tickets' expect where query is filtered for users own tickets.
    """

    form = SearchTicketForm()

    # get request arguments from the url
    status = rq.args.get("status")
    team = rq.args.get("team")
    request_type = rq.args.get("request_type")
    content = rq.args.get("content")
    requester = rq.args.get("requester")
    referee = rq.args.get("referee")
    user_id = rq.args.get("user_id")
    instrument = rq.args.get("instrument")
    request_stage = rq.args.get("request_stage")

    if form.validate_on_submit():
        redirect_url = FlicketTicket.form_redirect(form, url="flicket_bp.tickets")

        return redirect(redirect_url)

    arg_sort = rq.args.get("sort")
    if arg_sort:
        print(arg_sort)
        args = rq.args.copy()
        del args["sort"]

        response = make_response(redirect(url_for("flicket_bp.tickets", **args)))
        response.set_cookie(
            "tickets_sort",
            arg_sort,
            max_age=2419200,
            path=url_for("flicket_bp.tickets", **args),
        )

        return response

    sort = rq.cookies.get("tickets_sort")
    if sort:
        set_cookie = True
    else:
        sort = "date_desc"
        set_cookie = False

    ticket_query, form = FlicketTicket.query_tickets(
        form,
        team=team,
        request_type=request_type,
        status=status,
        user_id=user_id,
        content=content,
        requester=requester,
        referee=referee,
        instrument=instrument,
        request_stage=request_stage,
    )
    if is_my_view:
        ticket_query = FlicketTicket.my_tickets(ticket_query)
    ticket_query = FlicketTicket.sorted_tickets(ticket_query, sort)
    number_results = ticket_query.count()

    ticket_query = ticket_query.paginate(page, app.config["posts_per_page"])

    title = gettext("Tickets")
    if is_my_view:
        title = gettext("My Tickets")

    if content:
        form.content.data = content
    if requester:
        form.requester.data = requester
    if referee:
        form.referee.data = referee

    response = make_response(
        render_template(
            "flicket_tickets.html",
            title=title,
            form=form,
            tickets=ticket_query,
            page=page,
            number_results=number_results,
            status=status,
            team=team,
            request_type=request_type,
            instrument=instrument,
            request_stage=request_stage,
            user_id=user_id,
            sort=sort,
            base_url="flicket_bp.tickets",
        )
    )

    if set_cookie:
        response.set_cookie(
            "tickets_sort", sort, max_age=2419200, path=url_for("flicket_bp.tickets")
        )

    return response


# tickets main
@flicket_bp.route(app.config["FLICKET"] + "tickets/", methods=["GET", "POST"])
@flicket_bp.route(
    app.config["FLICKET"] + "tickets/<int:page>/", methods=["GET", "POST"]
)
@login_required
def tickets(page=1):
    response = tickets_view(page)

    return response


@flicket_bp.route(app.config["FLICKET"] + "tickets_csv/", methods=["GET", "POST"])
@login_required
def tickets_csv():
    # get request arguments from the url
    status = rq.args.get("status")
    team = rq.args.get("team")
    request_type = rq.args.get("request_type")
    content = rq.args.get("content")
    requester = rq.args.get("requester")
    referee = rq.args.get("referee")
    user_id = rq.args.get("user_id")

    ticket_query, form = FlicketTicket.query_tickets(
        team=team,
        request_type=request_type,
        status=status,
        user_id=user_id,
        content=content,
        requester=requester,
        referee=referee,
    )
    ticket_query = ticket_query.limit(app.config["csv_dump_limit"])

    date_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = date_stamp + "ticketdump.csv"

    csv_contents = (
        "Ticket_ID,Title,Submitted By,Date,Replies,Request,Status,Assigned,URL\n"
    )
    for ticket in ticket_query:

        if hasattr(ticket.assigned, "name"):
            _name = ticket.assigned.name
        else:
            _name = "Not assigned"

        csv_contents += '{},{},"{}",{},{},{},{} - {},{},{},{}{}\n'.format(
            ticket.id_zfill,
            clean_csv_data(ticket.title),
            ticket.user.name,
            ticket.date_added.strftime("%Y-%m-%d"),
            ticket.num_replies,
            clean_csv_data(ticket.request_type.team.team),
            clean_csv_data(ticket.request_type.request_type),
            ticket.current_status.status,
            _name,
            app.config["base_url"],
            url_for("flicket_bp.ticket_view", ticket_id=ticket.id),
        )

    return Response(
        csv_contents,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={file_name}"},
    )


@flicket_bp.route(app.config["FLICKET"] + "my_tickets/", methods=["GET", "POST"])
@flicket_bp.route(
    app.config["FLICKET"] + "my_tickets/<int:page>/", methods=["GET", "POST"]
)
@login_required
def my_tickets(page=1):
    response = tickets_view(page, is_my_view=True)

    return response
