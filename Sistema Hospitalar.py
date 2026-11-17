pacientes = []


def cadastrar_paciente():
    print("\n--- Cadastro de paciente ---")

    nome = input("Nome completo: ").strip()
    telefone = input("Telefone: ").strip()
    alergias = input("Alergias (deixe vazio se não houver): ").strip()

    if not nome or not telefone:
        print("Nome e telefone são obrigatórios!")
        return

    paciente = {
        "id": len(pacientes) + 1,
        "nome": nome,
        "telefone": telefone,
        "alergias": alergias
    }

    pacientes.append(paciente)
    print("Paciente cadastrado com sucesso!")


def listar_pacientes():
    print("\n--- Pacientes cadastrados ---")

    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return

    for paciente in pacientes:
        print(f"\nCódigo: {paciente['id']}")
        print(f"Nome: {paciente['nome']}")
        print(f"Telefone: {paciente['telefone']}")
        print(f"Alergias: {paciente['alergias'] or 'Nenhuma informada'}")


def menu():
    while True:
        print("\n=== SISTEMA HOSPITALAR ===")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_paciente()
        elif opcao == "2":
            listar_pacientes()
        elif opcao == "0":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()