import os
import json

from collector_base import CollectorService
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from datetime import date


class SpotifyService(CollectorService):
    def __init__(self):
        scope_needed_for_recent = "user-read-recently-played"
        self.auth_manager: SpotifyOAuth = SpotifyOAuth(
            cache_path=os.path.join(os.path.expanduser('~'), 'spotify_auth_cache'),
            scope=scope_needed_for_recent)
        self.spotify_instance: Spotify = Spotify(auth_manager=self.auth_manager)

    def disconnect_from_service(self) -> bool:
        """
        Disconnects from the service
        :return: If the disconnection was successful or not
        """
        del self.spotify_instance
        self.spotify_instance = None
        return True

    def is_service_active(self) -> bool:
        """
        Checks if the service is alive or not
        :return: if the service is alive or not
        """
        return self.spotify_instance is not None

    def collect_data(self) -> str:
        """
        Collects data from a services
        :return: Data from the service in a json form
        """
        assert self.is_service_active(), 'The spotify service is closed!'

        today_date = date.today()
        today_time_in_ms = int(float(date(year=today_date.year, month=today_date.month,
                                          day=today_date.day).strftime('%s.%f'))*1000)
        today_music_with = self.spotify_instance.current_user_recently_played(
            after=today_time_in_ms, limit=50).get('items', [])
        return json.dumps(today_music_with)


def init_data_collection_service() -> CollectorService:
    return SpotifyService()
