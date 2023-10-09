import unittest
import requests

class User:
    def __init__(self, nome, url_usuario, repos_usuario, seguidores_usuario, seguindo_usuario):
        """ 
        Esta função servirá para iniciar a aplicação e declarar
        as variáveis globais do projeto, facilitando na localização
        dos dados.
        """
        self.name = nome
        self.user_url = url_usuario
        self.user_repos = repos_usuario
        self.user_followers = seguidores_usuario
        self.user_following = seguindo_usuario

def get_user_data(username):
    """
    Esta função serve para obter os dados do usuário, 
    os quais incluirão informações gerais como nome de usuário,
    URL do perfil, número de repositórios públicos, número de seguidores
    e número de pessoas que o mesmo segue, realizando as solicitações
    pela API do Github.
    """
    usuario = input("Digite o nome do usuário: ")
    url = f'https://api.github.com/users/{usuario}'
    response = requests.get(url)
    if response.status_code == 200:
        usuario_info = response.json()
        nome_usuario = usuario_info['login']
        url_usuario = usuario_info['html_url']
        repos_pubs_usuario = usuario_info['public_repos']
        seguidores_usuario = usuario_info['followers']
        seguindo_usuario = usuario_info['following']

        print(f'Nome de usuário: {nome_usuario}')
        print(f'URL do usuário: {url_usuario}')
        print(f'Número de repositórios públicos do usuário: {repos_pubs_usuario}')
        print(f'Número de seguidores do usuário: {seguidores_usuario}')
        print(f'Número de pessoas que o usuário segue: {seguindo_usuario}')

    else:
        print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {response.status_code}')
