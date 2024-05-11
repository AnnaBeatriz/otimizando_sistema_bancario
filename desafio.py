import textwrap

def menu():
    menu = """\n
    -----------MENU-----------
    [1] \tDepositar
    [2] \tSacar
    [3] \tSaldo e Limite Diário
    [4] \tExtrato
    [5] \tNovo usuário
    [6] \tNova conta
    [7] \tLista contas
    [8] \tEncerrar conta
    [9] \tSair
    --------------------------
    => """
    return int(input(textwrap.dedent(menu)))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \tR$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
  
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def consultar_saldo_e_limite(saldo, limite, numero_saques, LIMITE_SAQUES):
    valor_maximo_saque = min(limite, saldo)

    print("\n------- Saldo e Limite Diário -------")
    print(f"Saldo: R$ {saldo:.2f}")
    print(f"Limite Diário: R$ {limite * LIMITE_SAQUES:.2f}")
    print(f"Valor Máximo por Saque: R$ {valor_maximo_saque:.2f}")
    print("-----------------------------------")

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

  
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    if not contas:
        print("Não existe nenhum conta cadastrada no momento, cadastre uma conta caso desejar!")
    else:
        for conta in contas:
            linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

def encerrar_conta(cpf, usuarios, contas):
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = encontrar_conta_por_usuario(usuario, contas)

        if conta:
            contas.remove(conta)
            print(f"Conta encerrada com sucesso para o CPF {cpf}.")
        else:
            print(f"Conta não encontrada para o CPF {cpf}.")
    else:
        print(f"Usuário não encontrado com o CPF {cpf}.")

def encontrar_conta_por_usuario(usuario, contas):
    for conta in contas:
        if conta["usuario"] == usuario:
            return conta
    return None




def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 1:
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 2:
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
        
        elif opcao == 3:
           consultar_saldo_e_limite(saldo, limite, numero_saques, LIMITE_SAQUES)

        elif opcao == 4:
            exibir_extrato(saldo, extrato=extrato)
        

        elif opcao == 5:
            criar_usuario(usuarios)

        elif opcao == 6:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 7:
            listar_contas(contas)
        
        elif opcao == 8:
            cpf = input("Informe o CPF para encerrar a conta: ")
            encerrar_conta(cpf, usuarios, contas)

        elif opcao == 9:
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()

