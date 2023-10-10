import unittest
import requests

class User:
    def __init__(self, nome, url_usuario, repos_usuario, seguidores_usuario, seguindo_usuario):
        """ 
        Esta função servirá para iniciar a aplicação, coletar os
        dados do usuário e armazená-los em variáveis referentes
        ao usuário.
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

        return {
            'Nome de Usuário': nome,
            'URL do Usuário': url_usuario,
            'Número de repositórios públicos': repos_usuario,
            'Número de seguidores do usuário': seguidores_usuario,
            'Número de pessoas seguindo': seguindo_usuario
        }
    
    except requests.exceptions.RequestException as e:
        print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {e}')
        return None
    except KeyError as e:
        print(f"Ops! Erro ao analisar a reposta JSON: {e}")
        return None

def get_user_repos(usuario):
    """
    Esta função serve para coletar o nome dos repositórios
    públicos do usuário, o link do repositório e 
    """
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

        return repos_dict

    except requests.exceptions.RequestException as e:
        print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {e}')
        return {}
    except KeyError as e:
        print(f"Ops! Erro ao analisar a reposta JSON: {e}")
        return {}
        
def save_user_data_in_file(usuario):
    """
    Este trecho do código servirá para coletar todos os dados do usuário,
    além de armazenar o nome dos repositórios e o link dos mesmos em conjunto
    """
    dados_usuario = get_user_data(usuario)
    repos_usuario = get_user_repos(usuario)

    arquivo_txt = f'{usuario}.txt'
    try:
        with open(arquivo_txt, 'w') as arquivo:
            arquivo.write(f'Dados do usuário: {usuario}\n\n')
            
            if dados_usuario:
                for chave, valor in dados_usuario.items():
                    arquivo.write(f'{chave}: {valor}\n')
                    
            arquivo.write('\nRepositórios do usuário:\n')
            
            for nome, url in repos_usuario.items():
                arquivo.write(f'Nome do repositório: {nome}\n')
                arquivo.write(f'URL do repositório: {url}\n\n')
                
            print(f'As informações foram salvas em "{arquivo_txt}".')
    
    except Exception as e:
        print(f'Ops! Ocorreu um erro ao salvar os dados em arquivo: {e}') 
        

class TestMethods(unittest.TestCase):
    def test_user_has_minimal_parameters(self):
        parameters = [
            'name', 'html_url', 'public_repos', 'followers', 'following'
        ]
        user = get_user_data(usuario)
        for param in parameters:
            self.assertTrue(hasattr(user, param))

usuario = input("Digite o nome do usuário: ")
# dados_usuario = get_user_data(usuario)
# get_user_data(usuario)
save_user_data_in_file(usuario)
# get_user_repos(usuario)