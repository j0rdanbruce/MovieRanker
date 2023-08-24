from secret import SECRET_API_KEY
import requests, json

class TMDB_API():
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
        self.tmdb_api_key = SECRET_API_KEY
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4ODExZGM1NWVjYzg4YzEwY2M2NjFkYjNkNDliNWFmZSIsInN1YiI6IjYzY2FhNWNkMDM5OGFiMDBhZjA2NWY0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._PG6E7GO285kY8arZVu5MWCj4_wHEGvZcFMbPypukgU"
        }

    def get_movie_data(self, movie_id: int) -> dict:
        movie_search_url = self.base_url + "/movie/{}".format(movie_id)
        response = requests.get(movie_search_url, headers=self.headers)
        return json.loads(response.text)
    
    def find_streaming_service_for(self, movie_id: int) -> dict:
        '''returns dictionary of streaming services to watch a given movie'''
        stream_url = "https://api.themoviedb.org/3/movie/348/watch/providers"
        response = requests.get(stream_url, headers=self.headers)
        return json.loads(response.text)