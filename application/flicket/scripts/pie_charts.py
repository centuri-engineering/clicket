#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import json

import plotly

from application.flicket.models.flicket_models import FlicketRequestType
from application.flicket.models.flicket_models import FlicketTeam
from application.flicket.models.flicket_models import FlicketStatus, FlicketRequestStage


from application.flicket.models.flicket_models import FlicketTicket


def count_request_tickets(request_type, stage):
    query = (
        FlicketTicket.query.join(FlicketRequestType)
        .join(FlicketRequestStage)
        .filter(FlicketRequestType.request_type == request_type)
        .filter(FlicketRequestStage.request_stage == stage)
    )

    return query.count()


def create_pie_chart_dict():
    """

    :return:
    """

    stages = FlicketRequestStage.query
    request_types = FlicketRequestType.query

    graphs = []

    for request_type in request_types:

        graph_title = request_type.request_type
        graph_labels = []
        graph_values = []
        for stage in stages:
            graph_labels.append(stage.request_stage)
            graph_values.append(count_request_tickets(graph_title, stage.request_stage))

        # append graphs if have values.
        if any(graph_values):
            graphs.append(
                dict(
                    data=[
                        dict(
                            labels=graph_labels,
                            values=graph_values,
                            type="pie",
                            marker=dict(
                                colors=[
                                    "darkorange",
                                    "darkgreen",
                                    "green",
                                    "lightgreen",
                                ]
                            ),
                            sort=False,
                        )
                    ],
                    layout=dict(
                        title=graph_title,
                        autosize=True,
                        margin=dict(b=0, t=40, l=0, r=0),
                        height=400,
                    ),
                )
            )

    ids = [f"Graph {i}" for i, _ in enumerate(graphs)]
    graph_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return ids, graph_json
