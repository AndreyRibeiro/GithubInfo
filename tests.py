import requests

class User:
    def __init__(self, usuario):
        """ 
        Esta função serve para iniciar a aplicação, coletar os
        dados do usuário e armazená-los dentro do arquivo txt, fazendo isso
        através da captação do nome do usuário e chamada das funções do código.
        Caso o usuário não seja encontrado no Github, o programa irá parar e 
        retornar o código do erro.
        """
        self.usuario = input("Digite o nome de usuário: ")

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
            print(f"Ops! Erro ao analisar a reposta JSON: {e}")
            return None

    def get_user_repos(self):
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
            print(f"Ops! Erro ao analisar a reposta JSON: {e}")
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

