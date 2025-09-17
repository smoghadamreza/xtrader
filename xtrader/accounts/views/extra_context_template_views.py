from django.views.generic import TemplateView


class ExtraContextTemplateView(TemplateView):
    """Add extra context to a simple template view."""

    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.extra_context:
            context.update(self.extra_context)
        return context

    # this view is used in POST requests,
    # e.g. signup when the form is not valid
    post = TemplateView.get
