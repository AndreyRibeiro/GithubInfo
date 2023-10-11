import unittest
import requests
import os
from typing import Dict, Union, Optional

class User:
    def __init__(self, username: str):
        """
        Esta função serve para iniciar a aplicação, coletar os
        dados do usuário e armazená-los dentro do arquivo txt, fazendo isso
        através da chamada das funções do código. Caso o usuário não seja 
        encontrado no Github, o programa irá parar e retornar o código do erro.
        """
        self.username = username
        self.base_url = f'https://api.github.com/users/{self.username}'

        if not self.check_user_exists():
            print(f'O usuário "{self.username}" não foi encontrado no Github!')
            return
        self.save_user_data_in_file()

    def check_user_exists(self) -> bool:
        try:
            response = requests.get(self.base_url)
            if response.status_code == 404:
                return False
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {e}')
            return False

    def get_user_data(self) -> Optional[Dict[str, Union[str, int]]]:
        """
        Esta função serve para obter os dados do usuário, 
        os quais incluirão informações gerais URL do perfil, número de 
        repositórios públicos, número de seguidores e número de pessoas
        que o mesmo segue, realizando as solicitações pela API do Github.
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            user_info = response.json()
            # name_user = user_info['name']
            # url_user = user_info['html_url']
            # repos_user = user_info['public_repos']
            # followers_user = user_info['followers']
            # following_user = user_info['following']

            return {
                'Nome': user_info.get('name', ''),
                'Perfil': user_info.get('html_url', ''),
                'Número de repositórios públicos': user_info.get('public_repos', 0),
                'Número de seguidores': user_info.get('followers', 0),
                'Número de usuários seguidos': user_info.get('following', 0)
            }

        except requests.exceptions.RequestException as e:
            print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {e}')
            return None
        except KeyError as e:
            print(f"Ops! Erro ao analisar a resposta JSON: {e}")
            return None

    def get_user_repos(self) -> Dict[str, str]:
        """
        Esta função serve para coletar o nome dos repositórios
        públicos do usuário, o link do repositório e armazená-los
        em um dicionário.
        """
        repos_url = f'{self.base_url}/repos'
        print(repos_url)
        try:
            response = requests.get(repos_url)
            response.raise_for_status()
            repos = response.json()
            repos_dict = {}

            for repo in repos:
                name_repo = repo['name']
                url_repo = repo['html_url']
                repos_dict[name_repo] = url_repo

            return repos_dict

        except requests.exceptions.RequestException as e:
            print(f'Ops! Ocorreu um erro na solicitação à API! Erro: {e}')
            return {}
        except KeyError as e:
            print(f"Ops! Erro ao analisar a resposta JSON: {e}")
            return {}

    def save_user_data_in_file(self):
        """
        Este trecho do código servirá para coletar todos os dados do usuário,
        além de armazenar o nome dos repositórios e o link dos mesmos em conjunto
        e imprimir dentro de um arquivo .txt com o nome do usuário como título.
        """
        data_user = self.get_user_data()
        repos_user = self.get_user_repos()

        file_txt = f'{self.username}.txt'
        try:
            with open(file_txt, 'w') as file:
                if data_user:
                    for key, value in data_user.items():
                        file.write(f'{key}: {value}\n')

                file.write('Repositórios:\n')

                for name, url in repos_user.items():
                    file.write(f'{name}: {url}\n')

                print(f'As informações foram salvas em "{file_txt}".')
        except Exception as e:
            print(f'Ops! Ocorreu um erro ao salvar os dados em arquivo: {e}')

class TestMethods(unittest.TestCase):
    def test_user_has_minimal_parameters(self):
        """
        A partir daqui começam os testes unitários do código.
        Este primeiro teste serve para checar se os dados do
        usuário estão sendo devidamente coletados, fazendo uma 
        análise dos parâmetros e comparando com os que estão 
        descritos no código e no arquivo gerado.
        """
        username = 'github'
        user = User(username)
        user_data = user.get_user_data()
        parameters = [
            'Nome', 'Perfil', 'Número de repositórios públicos', 'Número de seguidores', 'Número de usuários seguidos'
        ]
        for param in parameters:
            self.assertTrue(param in user_data)

    def test_user_has_public_repos(self):
        """
        Este segundo teste serve para checar se o usuário 
        possui repositórios públicos em seu perfil. Caso 
        contrário, o teste irá falhar.
        """
        username = 'github'
        user = User(username)
        user_repos = user.get_user_repos()
        self.assertTrue(bool(user_repos))
        self.assertIsInstance(user_repos, dict)
        self.assertGreater(len(user_repos), 0)

    def test_save_user_data_in_file(self):
        """
        Este teste serve para garantir que o arquivo .txt
        está sendo gerado, e está sendo checado se possui as
        informações corretas da coleta de dados das funções
        anteriores.
        """
        username = 'github'
        user = User(username)
        user.save_user_data_in_file()

        file_txt = f'{username}.txt'

        self.assertTrue(os.path.exists(file_txt))
        with open(file_txt, 'r') as file:
            content = file.read()
        self.assertTrue(content)
    
    def test_check_user_exists(self):
        """
        Este último teste serve para garantir que 
        a função de checar se há realmente um usuário
        sendo encontrado na base de dados, ou se está identificando
        como um usuário inexistente.
        """
        parameters = [
            ('github', True),
            ('thisuserdoesnotexists', False)
        ]

        for username, expected_result in parameters:
            user = User(username)
            result = user.check_user_exists()
            self.assertEqual(result, expected_result, f'Erro para usuário: {username}')

if __name__ == "__main__":
    """
    Aqui é o trecho final do código, o qual irá coletar o 
    nome do usuário e irá realizar todo o processo do código, 
    além de realizar todos os testes de unidade sobre cada função
    da classe User.
    """
    username = input("Digite o nome do usuário: ")
    user = User(username)
    unittest.main()
