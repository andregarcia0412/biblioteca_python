import bcrypt

def cadastrar_usuario(nome_arquivo, usuario, senha):
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"{usuario}:{senha.decode()}:False\n")
        print("Usuário cadastrado com sucesso.")

def verificar_login(nome_arquivo, usuario, senha):
    try:
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                usuario_salvo, senha_salva, admin = linha.strip().split(":")
                if usuario == usuario_salvo and bcrypt.checkpw(senha.encode(), senha_salva.encode()):
                    return True
        return False
    except:
        return False
    
def verificar_usuario_existente(nome_arquivo, usuario):
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            usuario_salvo, senha_salva, admin = linha.strip().split(":")
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

def adicionar_administrador(nome_arquivo, usuario_tornar_adm):
    novas_linhas = []
    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            usuario_salvo, senha, admin = linha.strip().split(":")
            if usuario_salvo == usuario_tornar_adm:
                if admin != "True":
                    novas_linhas.append(f"{usuario_tornar_adm}:{senha}:True\n")
                    print("Esse usuario agora é administrador")
                else:
                    novas_linhas.append(linha)
                    print("Esse usuário já é administrador")
            else:
                novas_linhas.append(linha)
    
    with open(nome_arquivo, "w") as arquivo:
        arquivo.writelines(novas_linhas)

def remover_administrador(nome_arquivo, usuario_remover_adm):
    novas_linhas = []
    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            usuario_salvo, senha, admin = linha.strip().split(":")
            if usuario_salvo == usuario_remover_adm:
                if admin == "True":
                    novas_linhas.append(f"{usuario_remover_adm}:{senha}:False\n")
                    print("Esse usuario não é mais administrador")
                else:
                    novas_linhas.append(linha)
                    print("Esse usuário já não é administrador")
            else:
                novas_linhas.append(linha)
    
    with open(nome_arquivo, "w") as arquivo:
        arquivo.writelines(novas_linhas)


def verificar_administrador(nome_arquivo, usuario):
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            usuario_salvo, senha, admin = linha.strip().split(":")
            if usuario_salvo == usuario:
                if admin == "True":
                    return True
    return False

def adicionar_livro(nome_arquivo, nome_livro, disponibilidade, forma, quantidade):
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"{nome_livro}: {disponibilidade}: {forma}: {quantidade}\n")
        print("O livro foi adicionado com sucesso")

def criptografar_senha(senha):
    salt = bcrypt.gensalt()
    senha_bytes = senha.encode()
    hash = bcrypt.hashpw(senha_bytes, salt)
    return hash

def conferir_senha(senha, hash):
    if bcrypt.checkpw(senha.encode(), hash):
        return True
    else:
        return False
    
def remover_livro(nome_arquivo, livro_removido):
    novas_linhas = []
    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            livro, disponibilidade, forma, quantidade = linha.strip().split(": ")
            if livro_removido.lower() != livro.lower():
                novas_linhas.append(linha)
    
    with open(nome_arquivo, "w") as arquivo:
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
            hash = criptografar_senha(senha_usuario)
            cadastrar_usuario(arquivo_usuarios, nome_usuario, hash)
        else:
            print("As senhas digitadas não são iguais ")

elif escolha_login == "2":
    nome_usuario = input("Digite o nome de usuário ")
    senha_usuario = input("Digite sua senha ")
    if verificar_usuario_existente(arquivo_usuarios, nome_usuario):
        if verificar_login(arquivo_usuarios, nome_usuario, senha_usuario):
            escolha_livro = input(f"Bem vindo, {nome_usuario}, oque deseja fazer?\n1. Alugar Livro\n2. Devolver Livro\n3. Ver livros em posse\n4. Opções de administrador\n5. Cancelar\n")
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
                with open(arquivo_livros_emprestados, "r") as arquivo:
                    existe_livro_posse = False
                    for linha in arquivo:
                        usuario_salvo, livro_alugado = linha.strip().split(":")
                        if usuario_salvo == nome_usuario:
                            existe_livro_posse = True
                            print(livro_alugado)
                    if not existe_livro_posse:
                        print("Esse usuario não tem livros em posse")

            elif escolha_livro == "4":
                if verificar_administrador(arquivo_usuarios, nome_usuario):
                    escolha_adm = input("Bem vindo administrador, o que deseja fazer?\n1. Adicionar administrador\n2. Adicionar livro\n3. Remover administrador\n4. Remover livro\n5. Remover usuário\n")
                    if escolha_adm == "1":
                        nome_usuario_admin = input("Digite o nome do usuario que quer tornar administrador:\n").strip()
                        adicionar_administrador(arquivo_usuarios, nome_usuario_admin)
                    elif escolha_adm == "2":
                        nome_livro = input("Digite o nome do livro:\n")
                        disponibilidade = input("Digite a disponibilidade do livro (Disponivel/Indisponivel)\n")
                        forma = input("Digite a forma do livro (Digital/Fisico)\n")
                        quantidade = int(input("Digite a quantidade de livros\n"))
                        adicionar_livro(arquivo_livros, nome_livro, disponibilidade, forma, quantidade)
                    elif escolha_adm == "3":
                        nome_usuario_remover_admin = input("Digite o nome do usuario que quer remover o cargo de administrador\n")
                        remover_administrador(arquivo_usuarios, nome_usuario_remover_admin)
                    elif escolha_adm == "4":
                        nome_livro_removido = input("Qual o nome do livro que deseja remover?\n")
                        if verificar_livro_existente(arquivo_livros, nome_livro_removido):
                            remover_livro(arquivo_livros, nome_livro_removido)
                            print(f"O livro {nome_livro_removido} foi removido")
                        else:
                            print("Esse livro não está no banco de dados")
                else:
                    print("Você não tem permissões de administrador")
            elif escolha_livro == "5":
                print("Volte sempre!")
            else:
                print("Opção Inválida")
        else:
            print("Senha Incorreta")
    else:
        print("Usuário não existe ")
else:
    print("Opção Inválida")

#continuar as opções de administrador
