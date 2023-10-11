# Informações de Usuário do Github

Este código possui o intuito de coletar informações do usuário, como nome de usuário, URL de perfil, dentre outras informações e armazená-las dentro de um arquivo .txt, além de realizar testes para garantir que as informações estejam sendo devidamente coletadas.

# Como utilizar

1. Clone ou faça um download do repositório.
2. Faça o download e instale a versão mais recente do Python pelo site https://www.python.org.
3. Após a instalação, abra um terminal, copie o caminho onde foi clonado a pasta do repositório através do comando cd. Ex.: "cd C:\Users\{usuario}\Documents\Python\Githubuserinfo".
4. Execute o comando pip install requests.
5. Execute o comando "python desafio.py".

# Resultado esperado

Após este passo a passo, é esperado que seja criado um arquivo .txt com o nome de usuário, e dentro deste arquivo seja reunido todas as informaões principais do usuário.

O código começa a partir da classe User, a qual é utilizada para armazenar as informações do usuário através da API do Github. 

Dentro dessa classe, há 4 funções: uma que reúne informações como: nome de usuário, URL de perfil, número de repositórios públicos, número de seguidores e número de pessoas seguindo. 

Após isso, a próxima função serve para coletar os nomes e os links do repositórios públicos do usuário e armazená-los dentro de um dicionário.

A penúltima função serve para juntar todos esses dados coletados do funcionário e escrevê-los dentro de um arquivo .txt, em que possuirá o nome do usuário como arquivo. Então por exemplo, se o usuário inserido for o 'github', o nome do arquivo será 'github.txt'.

E a última função serve para checar se o usuário existe na base de dados do Github. Caso não exista, o código irá parar.

Após a classe User, há a classe de teste unitário, que serve para garantir que todo o passo a passo esteja sendo realizado devidamente. Depois do código ser chamado, os testes serão realizados em conjunto com o programa e irá mostrar no console se todos os testes passaram. E caso algum não tenha passado, será mostrado qual parte falhou e apresentará um erro.