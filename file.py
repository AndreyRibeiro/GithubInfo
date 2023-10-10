import unittest
import requests

class User:
    def __init__(self, usuario):
        self.usuario = usuario

        if not self.check_user_exists():
            print(f'O usuário "{self.usuario}" não foi encontrado no Github!')
            return
        self.save_user_data_in_file()

    def check_user_exists(self):
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

    def get_user_data(self):
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

    def get_user_repos(self):
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
        usuario = 'github'
        user = User(usuario)
        user_data = user.get_user_data()
        parameters = [
            'Nome', 'Perfil', 'Número de repositórios públicos', 'Número de seguidores', 'Número de usuários seguidos'
        ]
        for param in parameters:
            self.assertTrue(param in user_data)
if __name__ == "__main__":
    usuario = input("Digite o nome do usuário: ")
    user = User(usuario)
    unittest.main()