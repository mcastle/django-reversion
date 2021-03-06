from __future__ import unicode_literals
from django.apps import apps
from django.contrib import admin
from django.core.management.base import BaseCommand, CommandError
from reversion.revisions import is_registered


class BaseRevisionCommand(BaseCommand):

    def add_arguments(self, parser):
        super(BaseRevisionCommand, self).add_arguments(parser)
        parser.add_argument(
            "app_label",
            metavar="app_label",
            nargs="*",
            help="Optional app_label or app_label.model_name list.",
        )
        parser.add_argument(
            "--using",
            default=None,
            help="The database to query for revision data.",
        )
        parser.add_argument(
            "--model-db",
            default=None,
            help="The database to query for model data.",
        )

    def get_models(self, options):
        # Load admin classes.
        admin.autodiscover()
        # Get options.
        app_labels = options["app_label"]
        # Parse model classes.
        if len(app_labels) == 0:
            selected_models = apps.get_models()
        else:
            selected_models = set()
            for label in app_labels:
                if "." in label:
                    # This is an app.Model specifier.
                    app_label, model_label = label.split(".")
                    try:
                        app = apps.get_app_config(app_label)
                    except LookupError:
                        raise CommandError("Unknown app: {}".format(app_label))
                    try:
                        model = app.get_model(model_label)
                    except LookupError:
                        raise CommandError("Unknown model: {}.{}".format(app_label, model_label))
                    selected_models.add(model)
                else:
                    # This is just an app - no model qualifier.
                    app_label = label
                    try:
                        app = apps.get_app_config(app_label)
                    except LookupError:
                        raise CommandError("Unknown app: {}".format(app_label))
                    selected_models.update(app.get_models())
        for model in selected_models:
            if is_registered(model):
                yield model
