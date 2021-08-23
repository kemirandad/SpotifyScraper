import argparse
from pprint import pprint
from config import config
import logging
from spotify_scrap import SpotifyScrapy

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

conf = config('access.json')

def main(query, name, type_):
    logger.info('Inicia el programa...')
    spotify = SpotifyScrapy()

    token = spotify.get_token(conf['credentials']['id'], conf['credentials']['password'])
    logger.info('Se genera un nuevo token...')

    if type_ == 'album':
        logger.info('Se retorna las canciones del album...')
        tracks = spotify._obtener_tracks_album(name, token, type_)
        pprint(tracks) 
    
    elif type_ == 'artist':
        if query == 'art':
            logger.info('Se retorna los artistas con ese nombre...')
            artistas = spotify._buscar_artista(name, token, type_)
            pprint(artistas) 
        else:
            logger.info('Se retorna los albumes de ese artista...')
            albumes = spotify._buscar_albums_artist(name, token, type_)
            pprint(albumes) 
    else:
        return None




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    querys_spotify_choices = list(conf["url_requests"].keys())

    parser.add_argument('querys_spotify',
                        help="Las peticiones que deseas realizar",
                        type=str,
                        choices=querys_spotify_choices)
  

    type_choices = ('artist', 'album')

    parser.add_argument('name',
                        help="Nombre del album o el artista",
                        type=str)
    
    parser.add_argument('type',
                        help="Elige si es un artista o album lo que deseas buscar",
                        type=str,
                        choices=type_choices)
       

    args = parser.parse_args()

    main(args.querys_spotify, args.name, args.type)