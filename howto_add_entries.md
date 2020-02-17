
# How to add entries to the database

## Free form entry (no DB entry)




## Multiple choice type entry

Here we assume the entry is called "request_type". It has a set of descrete values:

1. N/A
2. First Contact
3. Submited
4. Validated
5. Declined



### Add or edit migration file

Add the following to the last migration file

```py
def upgrade():

    op.create_table(
        "flicket_request_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_type", sa.String(length=12), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "flicket_topic", sa.Column("request_type", sa.Integer(), nullable=True,),
    )
    op.add_column(
        "flicket_topic",
        sa.Column(
            "request_type_id",
            sa.Integer(),
            sa.ForeignKey("flicket_request_types.id"),
            nullable=True,
        ),
    )

```

### Create the model

* In `/application/flicket/models/flicket_models.py` - eventually add an entry to `field_size` or use an existing one.

* create the class

```py
class FlicketRequestType(PaginatedAPIMixin, Base):
    __tablename__ = "flicket_request_types"

    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(field_size["priority_max_length"]))

    def to_dict(self):
        """
        Returns a dictionary object about the domain and its institute
        :return:
        """
        data = {
            "id": self.id,
            "role": self.request_type,
            "links": {
                "self": app.config["base_url"]
                + url_for("bp_api.get_request_type", id=self.id),
                "request_types": app.config["base_url"]
                + url_for("bp_api.get_request_types"),
            },
        }

        return data

    def __repr__(self):
        return "<FlicketRequestType: id={}, request_type={}>".format(
            self.id, self.request_type
        )
```

* Add class attributes to `FlicketTicket`:

```py
request_type_id = db.Column(db.Integer, db.ForeignKey(FlicketRequestType.id))
    request_type = db.relationship(FlicketRequestType)

```

* Add entries to the `form_redirect` method


```py
# at function beginning
        request_type = ""
...

# if blocks
        if form.request_type.data:
            request_type = (
                FlicketRequesterRole.query.filter_by(id=form.request_type.data)
                .first()
                .request_type
            )
...
# redirect_url argument
        request_type=request_type,

```

* Edit `query_tickets`

```py
            if key == "request_type" and value:
                ticket_query = ticket_query.filter(
                    FlicketTicket.request_type.has(
                        FlicketRequestType.request_type == value
                    )
                )
                if form:
                    form.request_type.data = (
                        FlicketRequestType.query.filter_by(request_type=value)
                        .first()
                        .id
                    )
```
* Edit `sorted_tickets`

```py
        elif sort == "request_type":
            ticket_query = ticket_query.order_by(
                FlicketTicket.request_type_id, FlicketTicket.id
            )
```

* Edit lists in `from_dict` and `to_dict` (you got it by now: copy, paste, replace)

#### Extended model

In `application/flicket/models/flicket_models_ext.py` - search, copy and replace for the model and the attributes


## Edit `setup.py`

* Import `FlicketRequestType` from `flicket_models`

* Create the list of values as a module variable:
```py
request_types = [
    " Consulting",
    " Short project",
    " Long project",
    " Maintenance",
]
```



* Write the corrsponding `create_default_` method for the `RunSetUP` class

```py
    @staticmethod
    def create_default_request_type_levels(silent=False):
        """ set up default request_type levels """

        for level in request_types:
            request_type = FlicketRequestType.query.filter_by(request_type=level).first()
            if not request_type:
                add_request_type = FlicketRequestType(request_type=level)
                db.session.add(add_request_type)

                if not silent:
                    print("Added request type level {}".format(level))
```

And call it in the `run` method.

## Forms

### Edit `application/flicket/forms/search.py`

* import the model
* standard search / copy / replace

### Edit `/application/flicket/forms/flicket_forms.py`

* same (you can copy the `.choices` lines from `search.py`)

## Views

### `application/flicket/views/create.py`

Just the one function call

### `/application/flicket/views/edit.py`

You now the drill

### `application/flicket/views/tickets.py`

### Create `application/flicket_api/views/request_types.py`

Copy from an existing similar entry and search / replace all

### `application/__init__.py`

Add the import

```py
# noinspection PyPep8
from .flicket_api.views import request_types
```

## Templates


### create `application/flicket/templates/flicket_apijson_request_type.html`




### `application/flicket/templates/flicket_post_box.html`

Just one column to add:
```html
        <div class="col">
            <label class="control-label mb-0">{{ _('Request Type) }}</label>
            {{ form.request_type(class="form-control form-control-sm m-0") }}
        </div>
```

### `application/flicket/templates/flicket_tickets.html`




## Recreate / update the db (make sure to dump it before)


## TODO: emails (?), csv export


<!-- ./setup.py -->
<!-- ./migrations/versions/13b0fec5b6ac_adds_centuri_specific_fields.py -->
<!-- ./application/flicket/models/flicket_models_ext.py -->
<!-- ./application/flicket/models/flicket_models.py -->
<!-- ./application/flicket/forms/search.py -->
<!-- ./application/flicket/forms/flicket_forms.py -->
<!-- ./application/flicket/views/create.py -->
<!-- ./application/flicket/views/edit.py -->
<!-- ./application/flicket/views/tickets.py -->
<!-- ./application/__init__.py -->
<!-- ./application/flicket_api/views/requester_roles.py -->
<!-- ./application/flicket/templates/flicket_post_box.html -->
<!-- ./application/flicket/templates/flicket_apijson_requester_roles.html -->
<!-- ./application/flicket/templates/flicket_tickets.html -->
