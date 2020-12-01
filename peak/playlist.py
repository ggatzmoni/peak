class Playlist:
    """Playlist represents a Spotify playlist."""

    def __init__(self, playlist_name, playlist_id):
        """
        :param name (str): Playlist name
        :param id (int): Spotify playlist id
        """
        self.playlist_name = playlist_name
        self.playlist_id = playlist_id

    def __str__(self):
        return f"Playlist: {self.playlist_name}"
