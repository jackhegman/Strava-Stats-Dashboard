import requests
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.http import urlencode
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from strava_auth.models import StravaToken
from strava_auth.serializers import UserSerializer
from strava_stats_dashboard import settings


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=401)
        data = UserSerializer(request.user).data
        return Response(data)


class UserLogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user:
            logout(request)
            return Response()
        else:
            return Response(status=400)


class StravaAuthView(APIView):
    AUTHORIZE_URL = 'https://www.strava.com/oauth/authorize'
    TOKEN_URL = 'https://www.strava.com/oauth/token'
    REDIRECT_URL = 'http://localhost:8000/api/auth/login/'
    SCOPE = 'profile:read_all,activity:read'
    TOKEN_ATTR = ['token_type', 'expires_in', 'expires_at', 'access_token', 'refresh_token']

    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        if auth_code:
            token_info = self._perform_auth_callback(auth_code)
            self._login_user(request, token_info)
            return redirect(settings.FRONT_END_URL)
        else:
            redirect_url = self._get_redirect_url()
            return Response({"redirect_url": redirect_url})

    def _get_redirect_url(self):
        data = {
            'client_id': settings.STRAVA_CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'scope': self.SCOPE,
            'response_type': 'code'}
        return f'{self.AUTHORIZE_URL}?{urlencode(data)}'

    def _perform_auth_callback(self, auth_code):
        data = {
            'client_id': settings.STRAVA_CLIENT_ID,
            'client_secret': settings.STRAVA_SECRET_KEY,
            'code': auth_code,
            'grant_type': 'authorization_code'}
        response = requests.post(self.TOKEN_URL, data=data)
        if 'errors' in response.json():
            raise Exception(response.json().errors)
        return response.json()

    def _login_user(self, request, token_info):
        athlete = token_info.pop('athlete')
        try:
            user = User.objects.get(username=athlete.get('id'))
        except User.DoesNotExist:
            password = User.objects.make_random_password()
            user = User.objects.create_user(
                username=athlete.get('id'),
                email=athlete.get('email', ''),
                first_name=athlete.get('firstname'),
                last_name=athlete.get('lastname'),
                password=password
            )
        self._create_strava_token(athlete.get('id'), user, token_info)
        if request.user:
            logout(request)
        login(request, user)

    def _create_strava_token(self, athlete_id, user, token_info):
        token_dict = {attr: token_info.get(attr) for attr in self.TOKEN_ATTR}
        if not all(token_dict.values()):
            raise Exception("Missing token info")

        StravaToken.objects.update_or_create(
            uid=athlete_id,
            user=user,
            defaults=token_dict
        )
