from urllib import request
import requests

kakao_token_api = 'https://kauth/kakao.com/oauth/token'
data = {
            'grant_type':'authorization_code',
            'client_id': '7dd7ce5b55fbc3add10a9445a8992a50',
            'redirection_uri' : 'http://127.0.0.1:8000/users/signin/kakao/callback',
            'code':'4HDrY1sGZQIf2SOAb5nLsE88UbyqTEiINwIjpqaHHUtDJdXBg6kPXVOoZhc99Pgqul4Sawo9dZwAAAF_UJmdVA',
        }

result = requests.post('https://www.naver.com', data=data)
