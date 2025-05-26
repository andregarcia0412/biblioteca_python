def cadastrar_usuario(nome_arquivo, usuario, senha):
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"{usuario}:{senha}\n")
        print("Usuário cadastrado com sucesso.")

def verificar_login(nome_arquivo, usuario, senha):
    try:
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                usuario_salvo, senha_salva = linha.strip().split(":")
                if usuario == usuario_salvo and senha == senha_salva:
                    return True
        return False
    except:
        return False
    
def verificar_usuario_existente(nome_arquivo, usuario):
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            usuario_salvo, senha_salva = linha.strip().split(":")
            if usuario == usuario_salvo:
                return True
    return False

def verificar_livro_existente(nome_arquivo, livro):
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            livro_salvo, disponibilidade, forma, quantidade = linha.strip().split(": ")
            if livro.lower() == livro_salvo.lower():
                return True
    return False

def alugar_livro(nome_arquivo, usuario, livro):
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"{usuario}:{livro.lower()}\n")
        print("O livro foi alugado")
    
def reescrever_livros(nome_arquivo, livro_escolhido):

    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    for linha in linhas:
        livro, disponibilidade, forma, quantidade = linha.strip().split(": ")
        if livro.lower() == livro_escolhido.lower():
            quantidade = int(quantidade) - 1
            if quantidade == 0:
                disponibilidade = "Indisponivel"
            if quantidade < 0:
                quantidade = 0
            novas_linhas.append(f"{livro}: {disponibilidade}: {forma}: {quantidade}\n")
        else:
            novas_linhas.append(linha)

    with open(nome_arquivo, "w") as arquivo:
        arquivo.writelines(novas_linhas)

def verificar_alugado(nome_arquivo, usuario, livro):
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            usuario_salvo, livro_salvo = linha.strip().split(":")
            if usuario == usuario_salvo:
                if livro == livro_salvo:
                    return True
                else:
                    pass
    return False

def retornar_livro(nome_arquivo_emprestimo, nome_arquivo_livros, livro_escolhido, nome_usuario):
    
    with open(nome_arquivo_livros, "r") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    for linha in linhas:
        livro, disponibilidade, forma, quantidade = linha.strip().split(": ")
        if livro.lower() == livro_escolhido.lower():
            quantidade = int(quantidade) + 1
            novas_linhas.append(f"{livro}: {disponibilidade}: {forma}: {quantidade}\n")
        else:
            novas_linhas.append(linha)

    with open(nome_arquivo_livros, "w") as arquivo:
        arquivo.writelines(novas_linhas)

    with open (nome_arquivo_emprestimo, "r") as arquivo:
        linhas = arquivo.readlines()

    novas_linhas = []
    for linha in linhas:
        usuario_salvo, livro_salvo = linha.strip().split(":")
        if livro_salvo.lower() == livro_escolhido.lower() and usuario_salvo == nome_usuario:
            novas_linhas.append("")
        else:
            novas_linhas.append(linha)

    with open(nome_arquivo_emprestimo, "w") as arquivo:
        arquivo.writelines(novas_linhas)

arquivo_usuarios = "loginPython/usuarios.txt"

print("=== Biblioteca Virtual ===")
print("=== Faça seu login ===")

escolha_login = input("1. Realizar Cadastro\n2. Fazer Login\n")

if escolha_login == "1":
    nome_usuario = input("Digite o nome de usuário ")
    if verificar_usuario_existente(arquivo_usuarios, nome_usuario):
        print("Ja existe um usuário com esse nome ")
    else:
        senha_usuario = input("Crie uma senha ")
        confirmar_senha = input("Confirme a senha ")
        if(senha_usuario == confirmar_senha):
            cadastrar_usuario(arquivo_usuarios, nome_usuario, senha_usuario)
        else:
            print("As senhas digitadas não são iguais ")

elif escolha_login == "2":
    nome_usuario = input("Digite o nome de usuário ")
    senha_usuario = input("Digite sua senha ")
    if verificar_usuario_existente(arquivo_usuarios, nome_usuario):
        if verificar_login(arquivo_usuarios, nome_usuario, senha_usuario):
            escolha_livro = input(f"Bem vindo, {nome_usuario}, oque deseja fazer?\n1. Alugar Livro\n2. Devolver Livro\n3. Cancelar\n")
            arquivo_livros = "loginPython/livros.txt"
            arquivo_livros_emprestados = "loginPython/livros_emprestados.txt"

            if escolha_livro == "1":
                livro = input("Digite o nome do livro que quer alugar ").strip().lower()
                if verificar_livro_existente(arquivo_livros, livro):
                    with open(arquivo_livros, "r") as arquivo:
                        for linha in arquivo:
                            livro_salvo, disponibilidade, forma, quantidade = linha.strip().split(": ")
                            if livro == livro_salvo.lower():
                                break

                    if verificar_alugado(arquivo_livros_emprestados, nome_usuario, livro):
                        print("Você já alugou esse livro")
                    else:
                        if forma.lower() == "digital":
                            alugar_livro(arquivo_livros_emprestados, nome_usuario, livro)
                        elif disponibilidade.lower() == "disponivel":
                            alugar_livro(arquivo_livros_emprestados, nome_usuario, livro)
                            reescrever_livros(arquivo_livros, livro)
                        else:
                            print("O livro está Indisponível")
                else:
                    print("Livro não encontrado")
            elif escolha_livro == "2":
                livro = input("Digite o nome do livro que quer retornar ").strip().lower()
                if verificar_alugado(arquivo_livros_emprestados, nome_usuario, livro):
                    retornar_livro(arquivo_livros_emprestados, arquivo_livros, livro, nome_usuario)
                    print("O livro foi devolvido")
                else:
                    print("Você não está com o livro")
            elif escolha_livro == "3":
                print("Volte sempre!")
            else:
                print("Opção Inválida")
        else:
            print("Senha Incorreta")
    else:
        print("Usuário não existe ")
else:
    print("Opção Inválida")

#fazer opções de administrador (adicionar ou remover livros e outras funcionalidades)
#fazer criptografia de senhas