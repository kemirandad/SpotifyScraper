import requests
import base64
from pprint import pprint


class SpotifyScrapy:

    
    def get_token(self, client_id, client_secret):
        encoded = base64.b64encode(bytes(client_id+':'+client_secret, 'utf-8'))
        params = {'grant_type':'client_credentials'}
        header = {'Authorization': 'Basic {}'.format(str(encoded, 'utf-8'))}
        r = requests.post('https://accounts.spotify.com/api/token', headers=header, data=params)
        if r.status_code != 200:
            print('Error en la request. ', r.json())
            return None
        else:
            print('Token válido por {} segundos.'.format(r.json()['expires_in']))
            return r.json()['access_token']
        
    def _buscar(func):
        def inner_func(self, name, token, *args):
            types = args[0]
            url_busqueda = 'https://api.spotify.com/v1/search'
            header = {'Authorization': 'Bearer {}'.format(token)}
            search_params = {'q':f'{name}'.replace(' ', '+'), 'type':types, 'market': 'US'}
            
            busqueda = requests.get(url_busqueda, headers=header, params=search_params)
            if busqueda.status_code != 200:
                print('Error... No he encontrado ese artista...')
                return busqueda.status_code
            else:
                print('Hecho!')
                return func(self, busqueda.json()[types+'s']['items'][0]['id'], token)
        return inner_func

    
    @_buscar
    def _buscar_artista(self, name, token, *args):
        
        info = list()
        
        url_artist = 'https://api.spotify.com/v1/artists/{artist_id}'.format(artist_id=name)
        print(url_artist)
        header = {'Authorization': 'Bearer {}'.format(token)}
        art = requests.get(url=url_artist, headers=header)
        
        artist = art.json()
        
        id_ = artist['id'] 
        name = artist['name']
        popularity = artist['popularity']
        url = artist['external_urls']['spotify']
        followers = artist['followers']['total']
        genres = artist['genres']
        img = artist['images'][0]['url']

        ret_dict = {name:{'id':id_,
                        'url':url,
                        'followers':followers,
                        'genres':genres,
                        'popularity':popularity,
                            }}
        info.append(img)
        info.append(ret_dict)
                    
        return info

    
    @_buscar
    def _buscar_albums_artist(self, name, token, *args):
        url_album = 'https://api.spotify.com/v1/artists/{artist_id}/albums'.format(artist_id=name)
        print(url_album)

        albums_list = list()
        
        header = {'Authorization': 'Bearer {}'.format(token)}
        r = requests.get(url=url_album, headers=header, params={'limit':50})
        
        if r.status_code != 200:
            print('Error en la requests.', r.json())
            return None
        
        albums = r.json()['items']
        
        for album in albums:
            id_ = album['id']
            name = album['name']
            
            ret_dict = {'name':name, 'id':id_}
            
            albums_list.append(ret_dict)
        
        while r.json()['next']:
            r = requests.get(r.json()['next'], headers=header)
            
            if r.status_code != 200:
                print('Error en la requests.', r.json())
                return None
        
        
            albums = r.json()['items']
        
            for album in albums:
                id_ = album['id']
                name = album['name']

                ret_dict = {'name':name, 'id':id_}

                albums_list.append(ret_dict)
            

        return albums_list 
    

    @_buscar
    def _obtener_tracks_album(self, name, token, *args):
        
        url_album = 'https://api.spotify.com/v1/albums/{album_id}/tracks'.format(album_id=name)
        print(url_album)

        track_list = list()
        
        header = {'Authorization': 'Bearer {}'.format(token)}
        album = requests.get(url=url_album, headers=header)
        
        tracks = album.json()['items']
        
        for track in tracks:
            id_ = track['id']
            name = track['name']
            preview = track['preview_url']
            
            ret_dict = {'name':name, 'id':id_, 'preview': preview}
            
            track_list.append(ret_dict)
            
        return track_list 