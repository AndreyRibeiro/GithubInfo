import requests

# Nome do usuário do GitHub que você deseja consultar
usuario = "yuzu-emu"

# URL da API pública do GitHub para obter informações do usuário
url = f"https://api.github.com/users/{usuario}"

# Faça a solicitação GET para a API pública do GitHub (sem autenticação)
response = requests.get(url)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Parseie a resposta JSON
    usuario_info = response.json()

    # Extraia as informações desejadas
    nome_de_usuario = usuario_info["login"]
    url_do_usuario = usuario_info["html_url"]
    num_repositorios_publicos = usuario_info["public_repos"]
    num_seguidores = usuario_info["followers"]
    num_seguindo = usuario_info["following"]

    # Imprima as informações no console
    print(f"Nome de usuário: {nome_de_usuario}")
    print(f"URL do usuário: {url_do_usuario}")
    print(f"Número de repositórios públicos: {num_repositorios_publicos}")
    print(f"Número de seguidores: {num_seguidores}")
    print(f"Número de pessoas que o usuário segue: {num_seguindo}")

else:
    print(f"Erro na solicitação à API: {response.status_code}")
