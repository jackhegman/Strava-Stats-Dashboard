import time
from urllib.parse import urlencode

import requests
from requests import HTTPError
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from strava_stats_dashboard import settings


class StravaStatsView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        strava_token = request.user.strava
        client = StravaClient(strava_token)
        rides = client.get_activities(request.GET.get('page'))
        return Response(rides)


class StravaClient:
    API_URL = 'https://www.strava.com/api/v3'
    ACTIVITY_URL = 'https://www.strava.com/activities/'
    TOKEN_URL = 'https://www.strava.com/oauth/token'

    def __init__(self, strava_token):
        self.strava_token = strava_token
        self.uid = strava_token.uid

    def load_token(self):
        if time.time() > self.strava_token.expires_at:
            return self.refresh_token()
        else:
            return self.strava_token.access_token

    def refresh_token(self):
        data = {
            'client_id': settings.STRAVA_CLIENT_ID,
            'client_secret': settings.STRAVA_SECRET_KEY,
            'grant_type': 'refresh_token',
            'refresh_token': self.strava_token.refresh_token}
        response = requests.post(self.TOKEN_URL, data=data)
        if 'errors' in response.json():
            raise Exception(response.json().errors)
        else:
            updated_token = response.json()
            fields = ['refresh_token', 'access_token', 'expires_at']
            for field in fields:
                setattr(self.strava_token, field, updated_token[field])
            self.strava_token.save(update_fields=fields)
        return self.strava_token.access_token

    def _api_request(self, endpoint):
        token = self.load_token()
        headers = {
            "Authorization": 'Bearer {}'.format(token)}
        url = f'{self.API_URL}/{endpoint}'
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
        except HTTPError:
            raise Exception("Bad api request", {"response_status": response.status_code})
        return response.json()

    def get_activities(self, page=None):
        endpoint = '/athlete/activities'
        endpoint += '?page={}'.format(page) if page else ''
        return self._api_request(endpoint)
