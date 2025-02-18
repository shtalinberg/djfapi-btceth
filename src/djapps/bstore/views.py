
from datetime import datetime, timedelta, timezone

import requests
from bstore.models import Currency, Provider
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class BlocksView(LoginRequiredMixin, TemplateView):
    """curl -X POST "http://localhost:8000/token" \
-d "username=testuser&password=testpass" \
-H "Content-Type: application/x-www-form-urlencoded"""

    template_name = "bstore/blocks_list.html"

    def _fetch_access_token(self):
        """Fetch token from FastAPI using Django session authentication"""
        response = requests.get(
            f"{settings.API_BASE_URL}/token/session",
            cookies=self.request.COOKIES,  # Send Django session cookie to FastAPI
        )
        return response.json() if response.status_code == 200 else None

    def get_context_data(self, **kwargs):
        token = self.request.session.get('auth_token')
        token_expiry = self.request.session.get('auth_token_expiry')

        # If token is missing or expired, refresh it
        if not token or datetime.now(timezone.utc) > datetime.strptime(
            token_expiry, "%Y-%m-%d %H:%M:%S"
        ):
            token_data = self._fetch_access_token()
            if token_data:
                token = token_data['access_token']
                expires_in = token_data.get('expires_in', 3600)
                expiry_time = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

                # Store token in session
                self.request.session['auth_token'] = token
                self.request.session['auth_token_expiry'] = expiry_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        context = super().get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()
        context['providers'] = Provider.objects.all()
        return context


def blocks_partial(request):
    # Get token from session or user
    token = request.session.get('auth_token')

    # Prepare API request
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'page': request.GET.get('page', 1),
        'page_size': 10,
        'currency': request.GET.get('currency', ''),
        'provider': request.GET.get('provider', ''),
    }

    # Call API
    response = requests.get(
        f'{settings.API_BASE_URL}/blocks/', headers=headers, params=params
    )
    blocks = response.json()

    return render(request, 'bstore/blocks_partial_list.html', {'blocks': blocks})


def block_detail(request, block_id):
    token = request.session.get('auth_token')
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(
        f'{settings.API_BASE_URL}/blocks/{block_id}', headers=headers
    )
    block = response.json()

    return render(request, 'bstore/blocks_detail.html', {'block': block})
