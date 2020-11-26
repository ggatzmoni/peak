class Track:
    """Track represents a piece of music."""

    def __init__(self, track_name, track_id, artists):
        """
        :param name (str): Track name
        :param id (int): Spotify track id
        :param artist (str): Artist who created the track
        """
        self.track_name = track_name
        self.track_id = track_id
        self.artists = artists

    def create_spotify_uri(self):
        return f"spotify:track:{self.track_id}"

    def __str__(self):
        return self.track_name + " by " + self.artists
