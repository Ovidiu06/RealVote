from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from election_manager.models import ElectionEvent


class ElectionEventsView(LoginRequiredMixin, ListView):
    model = ElectionEvent
    context_object_name = 'object_list'

    def get_template_names(self):
        if self.request.path == '/my_elections/':
            return ['election_manager/my_elections.html']
        return ['election_manager/voting_list.html']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.path == '/my_elections/':
            return queryset.filter(creator=self.request.user)
        return queryset

class AddElectionView(LoginRequiredMixin, CreateView):
    model = ElectionEvent
    template_name = 'election_manager/add_election.html'
    fields = ['name', 'description', 'start_time', 'end_time', 'is_public']
    success_url = reverse_lazy('voting:dashboard')

    def form_invalid(self, form):
        print(form.errors)
        return super(AddElectionView, self).form_invalid(form)

    def form_valid(self, form):
        if form.is_valid() and not form.errors:
            instance = form.save(commit=False)
            instance.save()
        return redirect('voting:dashboard')