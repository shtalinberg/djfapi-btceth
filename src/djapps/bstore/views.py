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

    def get(self, request, *args, **kwargs):
        # If it's an HTMX request, render partial list
        if request.headers.get('HX-Request') == 'true':
            return self.blocks_partial(request)
        return super().get(request, *args, **kwargs)

    def blocks_partial(self, request):
        # Get token from session or user session cookie
        token = self.get_token()

        # Prepare API request
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'page': request.GET.get('page', 1),
            'page_size': 10,
            'currency': request.GET.get('currency', ''),
            'provider': request.GET.get('provider', ''),
        }

        # Call API to fetch blocks
        response = requests.get(
            f'{settings.API_BASE_URL}/blocks/', headers=headers, params=params
        )
        blocks_data = response.json()

        # Extract blocks and pagination data
        blocks = blocks_data.get('results', [])
        total = blocks_data.get('total', 0)
        page = int(params.get('page', 1))
        page_size = params.get('page_size', 10)

        # Calculate total pages based on total count and page_size
        total_pages = (total // page_size) + (1 if total % page_size else 0)

        return render(
            request,
            'bstore/blocks_partial_list.html',
            {
                'blocks': blocks,
                'total': total,
                'total_pages': total_pages,
                'page': page,
                'page_size': page_size,
            },
        )

    def _fetch_access_token(self):
        """Fetch token from FastAPI using Django session authentication"""
        response = requests.get(
            f"{settings.API_BASE_URL}/token/session",
            cookies=self.request.COOKIES,  # Ensure session cookie is sent
        )
        return response.json() if response.status_code == 200 else None

    def get_token(self):
        """Fetch token from FastAPI using Django session authentication"""
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
        return self.request.session.get('auth_token')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()
        context['providers'] = Provider.objects.all()
        context['selected_currency'] = self.request.GET.get('currency')
        context['selected_provider'] = self.request.GET.get('provider')
        return context


def block_detail(request, block_id):
    token = request.session.get('auth_token')
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(
        f'{settings.API_BASE_URL}/blocks/{block_id}', headers=headers
    )
    block = response.json()

    return render(request, 'bstore/blocks_detail.html', {'block': block})
