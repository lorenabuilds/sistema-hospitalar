usuarios = []
pacientes = []
consultas = []
leitos = []
internacoes = []
prescricoes = []
prontuarios = []
exames = []
estoque = []

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
    convenio = input("Convênio (Enter se não tiver): ").strip()
    if nome == "" or telefone == "":
        print(">> Nome e telefone são obrigatórios!")
        return
    pacientes.append({
        "id": len(pacientes) + 1,
        "nome": nome,
        "telefone": telefone,
        "alergias": alergias,
        "convenio": convenio
    })
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
        print("  Convênio:", p["convenio"] if p["convenio"] != "" else "particular")
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
    medicos = []
    for u in usuarios:
        if u["perfil"] == "medico":
            medicos.append(u)
    if len(medicos) == 0:
        print(">> Nenhum médico cadastrado.")
        return
    print("\nMédicos disponíveis:")
    for m in medicos:
        print("  ", m["nome"])
    nome_medico = input("Nome do médico: ").strip()
    medico = None
    for m in medicos:
        if m["nome"] == nome_medico:
            medico = m
    if medico is None:
        print(">> Médico não encontrado.")
        return
    data = input("Data (ex: 20/11/2026): ").strip()
    hora = input("Hora (07:00 até 18:00, ex: 09:00): ").strip()
    if hora < "07:00" or hora >= "18:00":
        print(">> Fora do horário de atendimento (07:00 às 18:00).")
        return
    for c in consultas:
        if c["medico"] == medico["nome"] and c["data"] == data and c["hora"] == hora and c["status"] != "cancelada":
            print(">> Esse médico já tem consulta nesse horário!")
            return
    consultas.append({
        "id": len(consultas) + 1,
        "paciente": paciente["nome"],
        "medico": medico["nome"],
        "data": data,
        "hora": hora,
        "status": "agendada"
    })
    print(">> Consulta agendada! Código:", len(consultas))

def listar_consultas():
    print("\n--- LISTA DE CONSULTAS ---")
    if len(consultas) == 0:
        print(">> Nenhuma consulta agendada.")
        return
    for c in consultas:
        print("Código:", c["id"])
        print("  Paciente:", c["paciente"])
        print("  Médico:", c["medico"])
        print("  Data:", c["data"], "às", c["hora"])
        print("  Status:", c["status"])
        print("")

def confirmar_consulta():
    print("\n--- CONFIRMAR CONSULTA ---")
    agendadas = []
    for c in consultas:
        if c["status"] == "agendada":
            agendadas.append(c)
    if len(agendadas) == 0:
        print(">> Nenhuma consulta agendada.")
        return
    for c in agendadas:
        print("Código:", c["id"], "|", c["paciente"], "|", c["medico"], "|", c["data"], c["hora"])
    codigo = input("Código da consulta: ").strip()
    for c in agendadas:
        if str(c["id"]) == codigo:
            paciente = None
            for p in pacientes:
                if p["nome"] == c["paciente"]:
                    paciente = p
            if paciente is not None and paciente["convenio"] != "":
                print(">> Verificando cobertura do convênio", paciente["convenio"], "... OK")
            else:
                print(">> Paciente particular (sem convênio).")
            c["status"] = "confirmada"
            print(">> Consulta confirmada!")
            return
    print(">> Consulta não encontrada.")

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

def registrar_atendimento():
    print("\n--- REGISTRAR ATENDIMENTO ---")
    confirmadas = []
    for c in consultas:
        if c["status"] == "confirmada":
            confirmadas.append(c)
    if len(confirmadas) == 0:
        print(">> Nenhuma consulta confirmada.")
        return
    for c in confirmadas:
        print("Código:", c["id"], "|", c["paciente"], "|", c["medico"], "|", c["data"], c["hora"])
    codigo = input("Código da consulta: ").strip()
    for c in confirmadas:
        if str(c["id"]) == codigo:
            if c["medico"] != logado["nome"]:
                print(">> Essa consulta não é sua.")
                return
            queixa = input("Queixa principal: ").strip()
            evolucao = input("Evolução clínica: ").strip()
            prontuarios.append({
                "paciente": c["paciente"],
                "medico": c["medico"],
                "data": c["data"],
                "queixa": queixa,
                "evolucao": evolucao
            })
            c["status"] = "realizada"
            print(">> Atendimento registrado no prontuário!")
            return
    print(">> Consulta não encontrada.")

def ver_prontuario():
    print("\n--- PRONTUÁRIO DO PACIENTE ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    listar_pacientes()
    codigo = input("Código do paciente: ").strip()
    paciente = achar_paciente(codigo)
    if paciente is None:
        print(">> Paciente não encontrado.")
        return
    print("\n=== PRONTUÁRIO DE", paciente["nome"], "===")
    encontrou = False
    for p in prontuarios:
        if p["paciente"] == paciente["nome"]:
            encontrou = True
            print("\nData:", p["data"], "| Médico:", p["medico"])
            print("  Queixa:", p["queixa"])
            print("  Evolução:", p["evolucao"])
    if not encontrou:
        print(">> Nenhum atendimento registrado.")
    print("\n--- Prescrições ---")
    for pr in prescricoes:
        if pr["paciente"] == paciente["nome"]:
            print("  ", pr["medicamento"], "|", pr["dose"], "|", pr["frequencia"], "|", pr["duracao"])
    print("\n--- Exames ---")
    for e in exames:
        if e["paciente"] == paciente["nome"]:
            print("  ", e["tipo"], "| status:", e["status"], "| resultado:", e["resultado"] if e["resultado"] != "" else "pendente")

def prescrever():
    print("\n--- PRESCREVER MEDICAMENTOS ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    listar_pacientes()
    codigo = input("Código do paciente: ").strip()
    paciente = achar_paciente(codigo)
    if paciente is None:
        print(">> Paciente não encontrado.")
        return
    while True:
        print("\nMedicamento", len(prescricoes) + 1, "(Enter vazio para encerrar)")
        medicamento = input("Medicamento: ").strip()
        if medicamento == "":
            break
        if paciente["alergias"] != "" and medicamento.lower() in paciente["alergias"].lower():
            print("\n>> ALERTA DE ALERGIA! Paciente é alérgico a:", paciente["alergias"])
            print("1 - Substituir medicamento")
            print("2 - Descartar esta prescrição")
            op = input("Opção: ").strip()
            if op == "1":
                continue
            else:
                print(">> Medicamento descartado.")
                continue
        dose = input("Dose: ").strip()
        frequencia = input("Frequência: ").strip()
        duracao = input("Duração: ").strip()
        prescricoes.append({
            "paciente": paciente["nome"],
            "medicamento": medicamento,
            "dose": dose,
            "frequencia": frequencia,
            "duracao": duracao
        })
        print(">> Prescrição registrada!")

def listar_prescricoes():
    print("\n--- LISTA DE PRESCRIÇÕES ---")
    if len(prescricoes) == 0:
        print(">> Nenhuma prescrição registrada.")
        return
    for p in prescricoes:
        print(p["paciente"], "->", p["medicamento"], "|", p["dose"], "|", p["frequencia"], "|", p["duracao"])

def solicitar_exame():
    print("\n--- SOLICITAR EXAME ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    listar_pacientes()
    codigo = input("Código do paciente: ").strip()
    paciente = achar_paciente(codigo)
    if paciente is None:
        print(">> Paciente não encontrado.")
        return
    tipo = input("Tipo de exame: ").strip()
    if tipo == "":
        print(">> Informe o tipo de exame!")
        return
    exames.append({
        "id": len(exames) + 1,
        "paciente": paciente["nome"],
        "tipo": tipo,
        "status": "solicitado",
        "resultado": ""
    })
    print(">> Exame solicitado! Código:", len(exames))

def registrar_resultado_exame():
    print("\n--- REGISTRAR RESULTADO DE EXAME ---")
    pendentes = []
    for e in exames:
        if e["status"] == "solicitado":
            pendentes.append(e)
    if len(pendentes) == 0:
        print(">> Nenhum exame pendente.")
        return
    for e in pendentes:
        print("Código:", e["id"], "|", e["paciente"], "|", e["tipo"])
    codigo = input("Código do exame: ").strip()
    for e in pendentes:
        if str(e["id"]) == codigo:
            resultado = input("Resultado: ").strip()
            e["resultado"] = resultado
            e["status"] = "concluido"
            print(">> Resultado registrado no prontuário!")
            return
    print(">> Exame não encontrado.")

def listar_exames():
    print("\n--- LISTA DE EXAMES ---")
    if len(exames) == 0:
        print(">> Nenhum exame solicitado.")
        return
    for e in exames:
        print("Código:", e["id"], "|", e["paciente"], "|", e["tipo"], "| status:", e["status"], "| resultado:", e["resultado"] if e["resultado"] != "" else "pendente")

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

def converter_data(data):
    partes = data.split("/")
    if len(partes) != 3:
        return None
    try:
        dia = int(partes[0])
        mes = int(partes[1])
        ano = int(partes[2])
    except ValueError:
        return None
    return (ano, mes, dia)

def dias_para_vencer(ano, mes, dia):
    import datetime
    hoje = datetime.date.today()
    validade = datetime.date(ano, mes, dia)
    return (validade - hoje).days

def cadastrar_medicamento():
    print("\n--- CADASTRAR MEDICAMENTO ---")
    nome = input("Nome do medicamento: ").strip()
    lote = input("Lote: ").strip()
    quantidade = input("Quantidade: ").strip()
    validade = input("Validade (DD/MM/AAAA): ").strip()
    minimo = input("Estoque mínimo: ").strip()

    if nome == "" or lote == "" or quantidade == "" or validade == "" or minimo == "":
        print(">> Preencha todos os campos!")
        return

    if converter_data(validade) is None:
        print(">> Data inválida! Use DD/MM/AAAA.")
        return

    try:
        quantidade = int(quantidade)
        minimo = int(minimo)
    except ValueError:
        print(">> Quantidade e mínimo devem ser números!")
        return

    estoque.append({
        "id": len(estoque) + 1,
        "nome": nome,
        "lote": lote,
        "quantidade": quantidade,
        "validade": validade,
        "minimo": minimo
    })
    print(">> Medicamento cadastrado! Código:", len(estoque))

def entrada_estoque():
    print("\n--- ENTRADA DE ESTOQUE ---")
    if len(estoque) == 0:
        print(">> Nenhum medicamento cadastrado.")
        return
    listar_estoque()
    codigo = input("Código do medicamento: ").strip()
    for m in estoque:
        if str(m["id"]) == codigo:
            qtd = input("Quantidade a adicionar: ").strip()
            try:
                qtd = int(qtd)
            except ValueError:
                print(">> Quantidade inválida!")
                return
            if qtd <= 0:
                print(">> A quantidade deve ser positiva!")
                return
            m["quantidade"] = m["quantidade"] + qtd
            print(">> Entrada registrada! Nova quantidade:", m["quantidade"])
            return
    print(">> Medicamento não encontrado.")

def saida_estoque():
    print("\n--- SAÍDA DE ESTOQUE (DISPENSAÇÃO) ---")
    if len(estoque) == 0:
        print(">> Nenhum medicamento cadastrado.")
        return
    listar_estoque()
    codigo = input("Código do medicamento: ").strip()
    for m in estoque:
        if str(m["id"]) == codigo:
            # RN.19 - bloqueia vencido
            data = converter_data(m["validade"])
            if data is not None:
                dias = dias_para_vencer(data[0], data[1], data[2])
                if dias < 0:
                    print(">> BLOQUEADO: medicamento vencido em", m["validade"], "!")
                    return
            qtd = input("Quantidade a dispensar: ").strip()
            try:
                qtd = int(qtd)
            except ValueError:
                print(">> Quantidade inválida!")
                return
            if qtd <= 0:
                print(">> A quantidade deve ser positiva!")
                return
            if qtd > m["quantidade"]:
                print(">> Estoque insuficiente! Disponível:", m["quantidade"])
                return
            m["quantidade"] = m["quantidade"] - qtd
            print(">> Saída registrada! Restante:", m["quantidade"])
            if m["quantidade"] < m["minimo"]:
                print(">> ALERTA: estoque abaixo do mínimo (", m["minimo"], ")!")
            return
    print(">> Medicamento não encontrado.")

def listar_estoque():
    print("\n--- ESTOQUE DE MEDICAMENTOS ---")
    if len(estoque) == 0:
        print(">> Nenhum medicamento cadastrado.")
        return
    for m in estoque:
        data = converter_data(m["validade"])
        status = ""
        if data is not None:
            dias = dias_para_vencer(data[0], data[1], data[2])
            if dias < 0:
                status = "VENCIDO"
            elif dias <= 30:
                status = "VENCE EM " + str(dias) + " DIAS"
            elif m["quantidade"] < m["minimo"]:
                status = "ESTOQUE BAIXO"
            else:
                status = "OK"
        else:
            status = "VALIDADE INVÁLIDA"
        print("Código:", m["id"], "|", m["nome"], "| Lote:", m["lote"])
        print("  Quantidade:", m["quantidade"], "| Mínimo:", m["minimo"], "| Validade:", m["validade"])
        print("  Status:", status)
        print("")

def verificar_alertas():
    print("\n=== ALERTAS DE ESTOQUE ===")
    encontrou = False
    for m in estoque:
        data = converter_data(m["validade"])
        if data is not None:
            dias = dias_para_vencer(data[0], data[1], data[2])
            if dias < 0:
                print(">> VENCIDO:", m["nome"], "(lote", m["lote"], ", validade", m["validade"], ")")
                encontrou = True
            elif dias <= 30:
                print(">> VENCE EM", dias, "DIAS:", m["nome"], "(lote", m["lote"], ")")
                encontrou = True
        if m["quantidade"] < m["minimo"]:
            print(">> ESTOQUE BAIXO:", m["nome"], "(qtd", m["quantidade"], "de mínimo", m["minimo"], ")")
            encontrou = True
    if not encontrou:
        print(">> Nenhum alerta. Estoque em ordem.")

def menu_administrador():
    while True:
        verificar_alertas()
        print("\n=== MENU ADMINISTRADOR ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Cadastrar leito")
        print("4 - Listar leitos")
        print("5 - Cadastrar medicamento")
        print("6 - Listar estoque")
        print("7 - Entrada de estoque")
        print("8 - Saída de estoque")
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
        elif op == "5":
            cadastrar_medicamento()
        elif op == "6":
            listar_estoque()
        elif op == "7":
            entrada_estoque()
        elif op == "8":
            saida_estoque()
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
        print("5 - Confirmar consulta")
        print("6 - Cancelar consulta")
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
            confirmar_consulta()
        elif op == "6":
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
        print("4 - Registrar atendimento")
        print("5 - Ver prontuário")
        print("6 - Prescrever medicamentos")
        print("7 - Listar prescrições")
        print("8 - Solicitar exame")
        print("9 - Registrar resultado de exame")
        print("10 - Listar exames")
        print("11 - Verificar alertas de estoque")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            listar_pacientes()
        elif op == "2":
            agendar_consulta()
        elif op == "3":
            listar_consultas()
        elif op == "4":
            registrar_atendimento()
        elif op == "5":
            ver_prontuario()
        elif op == "6":
            prescrever()
        elif op == "7":
            listar_prescricoes()
        elif op == "8":
            solicitar_exame()
        elif op == "9":
            registrar_resultado_exame()
        elif op == "10":
            listar_exames()
        elif op == "11":
            verificar_alertas()
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
        print("5 - Ver prontuário")
        print("6 - Listar exames")
        print("7 - Verificar alertas de estoque")
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
        elif op == "5":
            ver_prontuario()
        elif op == "6":
            listar_exames()
        elif op == "7":
            verificar_alertas()
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