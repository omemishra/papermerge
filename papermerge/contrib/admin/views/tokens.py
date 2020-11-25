from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from knox.models import AuthToken

from papermerge.contrib.admin.forms import AuthTokenForm
from papermerge.contrib.admin.views import mixins as mix


class TokensView(
    LoginRequiredMixin,
    mix.CommonListMixin
):
    model = AuthToken
    form_class = AuthTokenForm
    success_url = action_url = reverse_lazy('admin:tokens')
    new_object_url = reverse_lazy('admin:token-add')


class TokensListView(
    TokensView,
    mix.PaginationMixin,
    mix.DeleteEntriesMixin,
    generic.ListView
):
    title = _("Tokens")
    action_url = reverse_lazy('admin:tokens')

    table_header_row = [
        _('Digest'),
        _('Created At'),
        _('Expires At'),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_header_row'] = self.table_header_row
        return context


class TokenCreateView(TokensView, generic.CreateView):

    title = _("New")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('New')
        context['action_url'] = reverse_lazy('admin:token-add')

        return context


class TokenUpdateView(TokensView, generic.UpdateView):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit')
        context['action_url'] = reverse_lazy(
            'admin:token-update',
            args=(self.object.pk,)
        )

        return context