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

def get_user_data(usuario):
    """
    Esta função serve para obter os dados do usuário, 
    os quais incluirão informações gerais como nome de usuário,
    URL do perfil, número de repositórios públicos, número de seguidores
    e número de pessoas que o mesmo segue, realizando as solicitações
    pela API do Github.
    """
    url = f'https://api.github.com/users/{usuario}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        usuario_info = response.json()
        nome = usuario_info['login']
        url_usuario = usuario_info['html_url']
        repos_usuario = usuario_info['public_repos']
        seguidores_usuario = usuario_info['followers']
        seguindo_usuario = usuario_info['following']

        return User(nome, url_usuario, repos_usuario, seguidores_usuario, seguindo_usuario)

        # print(f'Nome de usuário: {nome_usuario}')
        # print(f'URL do usuário: {url_usuario}')
        # print(f'Número de repositórios públicos do usuário: {repos_pubs_usuario}')
        # print(f'Número de seguidores do usuário: {seguidores_usuario}')
        # print(f'Número de pessoas que o usuário segue: {seguindo_usuario}')

    except requests.exceptions.RequestException as e:
        print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {e}')
    except KeyError as e:
        print(f"Ops! Erro ao analisar a reposta JSON: {e}")


def get_user_repos(usuario):
    url = f'https://api.github.com/users/{usuario}/repos'
    try:
        response = requests.get(url)
        response.raise_for_status()
        repositorios = response.json()
        repos_dict = {}

        for repo in repositorios:
            nome_repo = repo['name']
            url_repo = repo['html_url']
            repos_dict[nome_repo] = url_repo

        for nome, url in repos_dict.items():
            print(f'Nome do repositório: {nome}')
            print(f'Link do repositório: {url}')
            print()

    except requests.exceptions.RequestException as e:
        print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {e}')
    except KeyError as e:
        print(f"Ops! Erro ao analisar a reposta JSON: {e}")


usuario = input("Digite o nome do usuário: ")
# get_user_data(usuario)
get_user_repos(usuario)