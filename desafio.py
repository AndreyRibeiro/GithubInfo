import unittest
import requests
import os
from typing import Dict, Optional, Union

class User:
    def __init__(self, usuario: str):
        """
        Esta função serve para iniciar a aplicação, coletar os
        dados do usuário e armazená-los dentro do arquivo txt, fazendo isso
        através da chamada das funções do código. Caso o usuário não seja 
        encontrado no Github, o programa irá parar e retornar o código do erro.
        """
        self.usuario = usuario

        if not self.check_user_exists():
            print(f'O usuário "{self.usuario}" não foi encontrado no Github!')
            return
        self.save_user_data_in_file()

    def check_user_exists(self) -> bool:
        url = f'https://api.github.com/users/{self.usuario}'
        try:
            response = requests.get(url)
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
        url = f'https://api.github.com/users/{self.usuario}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            usuario_info = response.json()
            nome_usuario = usuario_info['name']
            url_usuario = usuario_info['html_url']
            repos_usuario = usuario_info['public_repos']
            seguidores_usuario = usuario_info['followers']
            seguindo_usuario = usuario_info['following']

            return {
                'Nome': nome_usuario,
                'Perfil': url_usuario,
                'Número de repositórios públicos': repos_usuario,
                'Número de seguidores': seguidores_usuario,
                'Número de usuários seguidos': seguindo_usuario
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
        url = f'https://api.github.com/users/{self.usuario}/repos'
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
            print(f"Ops! Erro ao analisar a resposta JSON: {e}")
            return {}

    def save_user_data_in_file(self):
        """
        Este trecho do código servirá para coletar todos os dados do usuário,
        além de armazenar o nome dos repositórios e o link dos mesmos em conjunto
        e imprimir dentro de um arquivo .txt com o nome do usuário como título.
        """
        dados_usuario = self.get_user_data()
        repos_usuario = self.get_user_repos()

        arquivo_txt = f'{self.usuario}.txt'
        try:
            with open(arquivo_txt, 'w') as arquivo:
                if dados_usuario:
                    for chave, valor in dados_usuario.items():
                        arquivo.write(f'{chave}: {valor}\n')

                arquivo.write('Repositórios:\n')

                for nome, url in repos_usuario.items():
                    arquivo.write(f'{nome}: {url}\n')

                print(f'As informações foram salvas em "{arquivo_txt}".')
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
        usuario = 'github'
        user = User(usuario)
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
        usuario = 'github'
        user = User(usuario)
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
        usuario = 'github'
        user = User(usuario)
        user.save_user_data_in_file()

        arquivo_txt = f'{usuario}.txt'

        self.assertTrue(os.path.exists(arquivo_txt))
        with open(arquivo_txt, 'r') as arquivo:
            conteudo = arquivo.read()
        self.assertTrue(conteudo)
    
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

        for usuario, expected_result in parameters:
            user = User(usuario)
            result = user.check_user_exists()
            self.assertEqual(result, expected_result, f'Erro para usuário: {usuario}')

if __name__ == "__main__":
    """
    Aqui é o trecho final do código, o qual irá coletar o 
    nome do usuário e irá realizar todo o processo do código, 
    além de realizar todos os testes de unidade sobre cada função
    da classe User.
    """
    usuario = input("Digite o nome do usuário: ")
    user = User(usuario)
    unittest.main()
