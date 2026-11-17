usuarios = []
pacientes = []
consultas = []
leitos = []
internacoes = []
prescricoes = []

logado = None


def cadastrar_usuario():
    print("\n--- CADASTRAR USUÁRIO ---")
    nome = input("Nome: ").strip()
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    if nome == "" or login == "" or senha == "":
        print(">> Preencha todos os campos!")
        return
    for u in usuarios:
        if u["login"] == login:
            print(">> Esse login já existe!")
            return
    if len(usuarios) == 0:
        perfil = "administrador"
        print(">> Primeiro usuário será administrador.")
    else:
        print("\nEscolha o perfil:")
        print("1 - Administrador")
        print("2 - Médico")
        print("3 - Enfermeiro")
        print("4 - Recepcionista")
        op = input("Opção: ").strip()
        if op == "1":
            perfil = "administrador"
        elif op == "2":
            perfil = "medico"
        elif op == "3":
            perfil = "enfermeiro"
        elif op == "4":
            perfil = "recepcionista"
        else:
            print(">> Perfil inválido!")
            return
    usuarios.append({"nome": nome, "login": login, "senha": senha, "perfil": perfil})
    print(">> Usuário cadastrado com sucesso!")


def fazer_login():
    global logado
    print("\n--- LOGIN ---")
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    for u in usuarios:
        if u["login"] == login and u["senha"] == senha:
            logado = u
            print("\n>> Bem-vindo(a),", u["nome"], "(", u["perfil"], ")")
            abrir_menu_do_perfil(u["perfil"])
            return
    print(">> Login ou senha incorretos!")


def abrir_menu_do_perfil(perfil):
    if perfil == "administrador":
        menu_administrador()
    elif perfil == "medico":
        menu_medico()
    elif perfil == "enfermeiro":
        menu_enfermeiro()
    else:
        menu_recepcionista()


def cadastrar_paciente():
    print("\n--- CADASTRAR PACIENTE ---")
    nome = input("Nome completo: ").strip()
    telefone = input("Telefone: ").strip()
    alergias = input("Alergias (Enter se não tiver): ").strip()
    if nome == "" or telefone == "":
        print(">> Nome e telefone são obrigatórios!")
        return
    pacientes.append({"id": len(pacientes) + 1, "nome": nome, "telefone": telefone, "alergias": alergias})
    print(">> Paciente cadastrado! Código:", len(pacientes))


def listar_pacientes():
    print("\n--- LISTA DE PACIENTES ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    for p in pacientes:
        print("Código:", p["id"])
        print("  Nome:", p["nome"])
        print("  Telefone:", p["telefone"])
        print("  Alergias:", p["alergias"] if p["alergias"] != "" else "nenhuma")
        print("")


def achar_paciente(codigo):
    for p in pacientes:
        if str(p["id"]) == str(codigo):
            return p
    return None


def agendar_consulta():
    print("\n--- AGENDAR CONSULTA ---")
    if len(pacientes) == 0:
        print(">> Cadastre um paciente primeiro.")
        return
    listar_pacientes()
    codigo = input("Código do paciente: ").strip()
    paciente = achar_paciente(codigo)
    if paciente is None:
        print(">> Paciente não encontrado.")
        return
    data = input("Data (ex: 20/11/2026): ").strip()
    hora = input("Hora (07:00 até 18:00, ex: 09:00): ").strip()
    if hora < "07:00" or hora >= "18:00":
        print(">> Fora do horário de atendimento (07:00 às 18:00).")
        return
    for c in consultas:
        if c["data"] == data and c["hora"] == hora:
            print(">> Já existe consulta nesse horário!")
            return
    consultas.append({"id": len(consultas) + 1, "paciente": paciente["nome"], "data": data, "hora": hora, "status": "agendada"})
    print(">> Consulta agendada com sucesso! Código:", len(consultas))


def listar_consultas():
    print("\n--- LISTA DE CONSULTAS ---")
    if len(consultas) == 0:
        print(">> Nenhuma consulta agendada.")
        return
    for c in consultas:
        print("Código:", c["id"])
        print("  Paciente:", c["paciente"])
        print("  Data:", c["data"], "às", c["hora"])
        print("  Status:", c["status"])
        print("")


def cancelar_consulta():
    print("\n--- CANCELAR CONSULTA ---")
    listar_consultas()
    if len(consultas) == 0:
        return
    codigo = input("Código da consulta: ").strip()
    for c in consultas:
        if str(c["id"]) == codigo:
            c["status"] = "cancelada"
            print(">> Consulta cancelada (histórico mantido).")
            return
    print(">> Consulta não encontrada.")


def prescrever():
    print("\n--- PRESCREVER MEDICAMENTO ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    listar_pacientes()
    codigo = input("Código do paciente: ").strip()
    paciente = achar_paciente(codigo)
    if paciente is None:
        print(">> Paciente não encontrado.")
        return
    medicamento = input("Medicamento: ").strip()
    if paciente["alergias"] != "" and medicamento.lower() in paciente["alergias"].lower():
        print("\n>> ALERTA DE ALERGIA!")
        print(">> O paciente é alérgico a:", paciente["alergias"])
        print(">> Prescrição NÃO registrada.")
        return
    prescricoes.append({"paciente": paciente["nome"], "medicamento": medicamento})
    print(">> Prescrição registrada com sucesso!")


def listar_prescricoes():
    print("\n--- LISTA DE PRESCRIÇÕES ---")
    if len(prescricoes) == 0:
        print(">> Nenhuma prescrição registrada.")
        return
    for p in prescricoes:
        print("Paciente:", p["paciente"], "-> Medicamento:", p["medicamento"])


def cadastrar_leito():
    print("\n--- CADASTRAR LEITO ---")
    setor = input("Setor: ").strip()
    numero = input("Número do leito: ").strip()
    if setor == "" or numero == "":
        print(">> Preencha setor e número!")
        return
    leitos.append({"id": len(leitos) + 1, "setor": setor, "numero": numero, "status": "disponivel"})
    print(">> Leito cadastrado! Código:", len(leitos))


def listar_leitos():
    print("\n--- LISTA DE LEITOS ---")
    if len(leitos) == 0:
        print(">> Nenhum leito cadastrado.")
        return
    for l in leitos:
        print("Código:", l["id"], "| Setor:", l["setor"], "| Número:", l["numero"], "| Status:", l["status"])


def internar():
    print("\n--- INTERNAR PACIENTE ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    listar_pacientes()
    codigo = input("Código do paciente: ").strip()
    paciente = achar_paciente(codigo)
    if paciente is None:
        print(">> Paciente não encontrado.")
        return
    for i in internacoes:
        if i["paciente"] == paciente["nome"] and i["status"] == "ativa":
            print(">> Esse paciente já está internado!")
            return
    disponiveis = []
    for l in leitos:
        if l["status"] == "disponivel":
            disponiveis.append(l)
    if len(disponiveis) == 0:
        print(">> Nenhum leito disponível.")
        return
    print("\nLeitos disponíveis:")
    for l in disponiveis:
        print("  Código:", l["id"], "| Setor:", l["setor"], "| Número:", l["numero"])
    codigo_leito = input("Código do leito: ").strip()
    for l in leitos:
        if str(l["id"]) == codigo_leito and l["status"] == "disponivel":
            l["status"] = "ocupado"
            internacoes.append({"paciente": paciente["nome"], "leito": l["id"], "status": "ativa"})
            print(">> Paciente internado no leito", l["numero"], "do setor", l["setor"])
            return
    print(">> Leito inválido ou já ocupado.")


def dar_alta():
    print("\n--- DAR ALTA ---")
    ativas = []
    for i in internacoes:
        if i["status"] == "ativa":
            ativas.append(i)
    if len(ativas) == 0:
        print(">> Nenhuma internação ativa.")
        return
    print("Internações ativas:")
    for i in ativas:
        print("  Paciente:", i["paciente"], "| Leito:", i["leito"])
    nome = input("Nome do paciente para alta: ").strip()
    for i in internacoes:
        if i["paciente"] == nome and i["status"] == "ativa":
            i["status"] = "encerrada"
            for l in leitos:
                if l["id"] == i["leito"]:
                    l["status"] = "disponivel"
            print(">> Alta registrada. Leito liberado.")
            return
    print(">> Internação não encontrada.")


def menu_administrador():
    while True:
        print("\n=== MENU ADMINISTRADOR ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Cadastrar leito")
        print("4 - Listar leitos")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            cadastrar_usuario()
        elif op == "2":
            print("\n--- LISTA DE USUÁRIOS ---")
            for u in usuarios:
                print(u["nome"], "|", u["login"], "|", u["perfil"])
        elif op == "3":
            cadastrar_leito()
        elif op == "4":
            listar_leitos()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")


def menu_recepcionista():
    while True:
        print("\n=== MENU RECEPCIONISTA ===")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes")
        print("3 - Agendar consulta")
        print("4 - Listar consultas")
        print("5 - Cancelar consulta")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            cadastrar_paciente()
        elif op == "2":
            listar_pacientes()
        elif op == "3":
            agendar_consulta()
        elif op == "4":
            listar_consultas()
        elif op == "5":
            cancelar_consulta()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")


def menu_medico():
    while True:
        print("\n=== MENU MÉDICO ===")
        print("1 - Listar pacientes")
        print("2 - Agendar consulta")
        print("3 - Listar consultas")
        print("4 - Prescrever medicamento")
        print("5 - Listar prescrições")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            listar_pacientes()
        elif op == "2":
            agendar_consulta()
        elif op == "3":
            listar_consultas()
        elif op == "4":
            prescrever()
        elif op == "5":
            listar_prescricoes()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")


def menu_enfermeiro():
    while True:
        print("\n=== MENU ENFERMEIRO ===")
        print("1 - Listar pacientes")
        print("2 - Listar leitos")
        print("3 - Internar paciente")
        print("4 - Dar alta")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            listar_pacientes()
        elif op == "2":
            listar_leitos()
        elif op == "3":
            internar()
        elif op == "4":
            dar_alta()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")

def menu():
    while True:
        print("\n=== SISTEMA HOSPITALAR ===")
        if len(usuarios) == 0:
            print("1 - Cadastrar primeiro administrador")
        else:
            print("1 - Fazer login")
        print("0 - Encerrar")
        op = input("Opção: ").strip()
        if op == "1":
            if len(usuarios) == 0:
                cadastrar_usuario()
            else:
                fazer_login()
        elif op == "0":
            print(">> Sistema encerrado.")
            break
        else:
            print(">> Opção inválida.")

menu()