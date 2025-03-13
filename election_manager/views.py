from django.views.generic import ListView
from election_manager.models import ElectionEvent


class ElectionEventsView(ListView):
    model = ElectionEvent
    template_name = 'election_manager/voting_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return ElectionEvent.objects.filter(is_active=True)
