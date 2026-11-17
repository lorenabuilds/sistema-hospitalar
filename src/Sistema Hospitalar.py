import datetime
import hashlib
import json
import os

ARQUIVO_DADOS = "dados_hospital.json"

usuarios = []
pacientes = []
consultas = []
leitos = []
internacoes = []
prescricoes = []
prontuarios = []
exames = []
estoque = []
logs = []

logado = None


def carregar_dados():
    global usuarios, pacientes, consultas, leitos, internacoes
    global prescricoes, prontuarios, exames, estoque, logs
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                d = json.load(f)
            usuarios = d.get("usuarios", [])
            pacientes = d.get("pacientes", [])
            consultas = d.get("consultas", [])
            leitos = d.get("leitos", [])
            internacoes = d.get("internacoes", [])
            prescricoes = d.get("prescricoes", [])
            prontuarios = d.get("prontuarios", [])
            exames = d.get("exames", [])
            estoque = d.get("estoque", [])
            logs = d.get("logs", [])
        except (json.JSONDecodeError, OSError):
            print(">> Aviso: dados corrompidos. Iniciando vazio.")

def salvar_dados():
    d = {
        "usuarios": usuarios,
        "pacientes": pacientes,
        "consultas": consultas,
        "leitos": leitos,
        "internacoes": internacoes,
        "prescricoes": prescricoes,
        "prontuarios": prontuarios,
        "exames": exames,
        "estoque": estoque,
        "logs": logs
    }
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(">> Erro ao salvar dados:", e)

def hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

def agora():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def registrar_log(acao, detalhe):
    usuario = "sistema"
    if logado is not None:
        usuario = logado["login"]
    logs.append({
        "usuario": usuario,
        "acao": acao,
        "detalhe": detalhe,
        "data_hora": agora()
    })
    salvar_dados()

def ver_logs():
    print("\n--- LOG DE ATIVIDADES ---")
    if len(logs) == 0:
        print(">> Nenhuma atividade registrada.")
        return
    for l in logs:
        print("[" + l["data_hora"] + "]", l["usuario"], "|", l["acao"], "|", l["detalhe"])

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
    especialidade = ""
    registro = ""
    setor = ""
    if perfil in ("medico", "enfermeiro"):
        especialidade = input("Especialidade: ").strip()
        registro = input("Registro profissional (CRM/COREN): ").strip()
        setor = input("Setor de atuação: ").strip()
    usuarios.append({
        "nome": nome,
        "login": login,
        "senha_hash": hash_senha(senha),
        "perfil": perfil,
        "ativo": True,
        "especialidade": especialidade,
        "registro": registro,
        "setor": setor
    })
    registrar_log("CADASTRAR_USUARIO", "login=" + login + ", perfil=" + perfil)
    print(">> Usuário cadastrado com sucesso!")

def listar_usuarios():
    print("\n--- LISTA DE USUÁRIOS ---")
    if len(usuarios) == 0:
        print(">> Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        status = "ativo" if u.get("ativo", True) else "inativo"
        print(u["nome"], "|", u["login"], "|", u["perfil"], "|", status)
        if u.get("especialidade", "") != "":
            print("  Especialidade:", u["especialidade"], "| Registro:", u.get("registro", ""), "| Setor:", u.get("setor", ""))

def alternar_status_usuario():
    print("\n--- ATIVAR/DESATIVAR USUÁRIO ---")
    listar_usuarios()
    login = input("\nLogin do usuário: ").strip()
    for u in usuarios:
        if u["login"] == login:
            if logado is not None and u["login"] == logado["login"]:
                print(">> Você não pode desativar seu próprio usuário.")
                return
            u["ativo"] = not u.get("ativo", True)
            registrar_log("ALTERAR_STATUS_USUARIO", "login=" + login + ", ativo=" + str(u["ativo"]))
            print(">> Usuário agora está", "ativo" if u["ativo"] else "inativo")
            return
    print(">> Usuário não encontrado.")

def fazer_login():
    global logado
    print("\n--- LOGIN ---")
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    senha_hash = hash_senha(senha)
    for u in usuarios:
        if u["login"] == login and u.get("senha_hash") == senha_hash:
            if not u.get("ativo", True):
                print(">> Usuário inativo. Procure o administrador.")
                return
            logado = u
            registrar_log("LOGIN", "login=" + login)
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
    cpf = input("CPF (somente números): ").strip()
    telefone = input("Telefone: ").strip()
    endereco = input("Endereço: ").strip()
    contato_emergencia = input("Contato de emergência: ").strip()
    alergias = input("Alergias (Enter se não tiver): ").strip()
    convenio = input("Convênio (Enter se não tiver): ").strip()
    if nome == "" or cpf == "" or telefone == "":
        print(">> Nome, CPF e telefone são obrigatórios!")
        return
    for p in pacientes:
        if p["cpf"] == cpf:
            print(">> Já existe paciente com esse CPF!")
            return
    pacientes.append({
        "id": len(pacientes) + 1,
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "endereco": endereco,
        "contato_emergencia": contato_emergencia,
        "alergias": alergias,
        "convenio": convenio
    })
    registrar_log("CADASTRAR_PACIENTE", "id=" + str(len(pacientes)) + ", nome=" + nome + ", cpf=" + cpf)
    print(">> Paciente cadastrado! Código:", len(pacientes))

def listar_pacientes():
    print("\n--- LISTA DE PACIENTES ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    for p in pacientes:
        print("Código:", p["id"])
        print("  Nome:", p["nome"])
        print("  CPF:", p["cpf"])
        print("  Telefone:", p["telefone"])
        print("  Endereço:", p.get("endereco", "") if p.get("endereco", "") != "" else "não informado")
        print("  Contato de emergência:", p.get("contato_emergencia", "") if p.get("contato_emergencia", "") != "" else "não informado")
        print("  Alergias:", p["alergias"] if p["alergias"] != "" else "nenhuma")
        print("  Convênio:", p["convenio"] if p["convenio"] != "" else "particular")
        print("")

def achar_paciente(codigo):
    for p in pacientes:
        if str(p["id"]) == str(codigo):
            return p
    return None

def atualizar_paciente():
    print("\n--- ATUALIZAR PACIENTE ---")
    if len(pacientes) == 0:
        print(">> Nenhum paciente cadastrado.")
        return
    listar_pacientes()
    codigo = input("Código do paciente: ").strip()
    paciente = achar_paciente(codigo)
    if paciente is None:
        print(">> Paciente não encontrado.")
        return
    print("\nPressione Enter para manter o valor atual.")
    nome = input("Novo nome: ").strip()
    telefone = input("Novo telefone: ").strip()
    endereco = input("Novo endereço: ").strip()
    contato = input("Novo contato de emergência: ").strip()
    alergias = input("Novas alergias (LIMPAR para apagar): ").strip()
    convenio = input("Novo convênio (LIMPAR para apagar): ").strip()
    alterou = False
    if nome:
        paciente["nome"] = nome
        alterou = True
    if telefone:
        paciente["telefone"] = telefone
        alterou = True
    if endereco:
        paciente["endereco"] = endereco
        alterou = True
    if contato:
        paciente["contato_emergencia"] = contato
        alterou = True
    if alergias.upper() == "LIMPAR":
        paciente["alergias"] = ""
        alterou = True
    elif alergias:
        paciente["alergias"] = alergias
        alterou = True
    if convenio.upper() == "LIMPAR":
        paciente["convenio"] = ""
        alterou = True
    elif convenio:
        paciente["convenio"] = convenio
        alterou = True
    if alterou:
        registrar_log("ATUALIZAR_PACIENTE", "id=" + str(paciente["id"]))
        salvar_dados()
        print(">> Dados atualizados com sucesso!")
    else:
        print(">> Nenhuma alteração realizada.")

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
        if u["perfil"] == "medico" and u.get("ativo", True):
            medicos.append(u)
    if len(medicos) == 0:
        print(">> Nenhum médico ativo cadastrado.")
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
    emergencia = input("É emergência? (s/N): ").strip().upper()
    if emergencia == "S":
        emergencia = True
    else:
        emergencia = False
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
        "emergencia": emergencia,
        "status": "agendada"
    })
    registrar_log("AGENDAR_CONSULTA", "paciente=" + paciente["nome"] + ", medico=" + medico["nome"] + ", " + data + " " + hora)
    print(">> Consulta agendada! Código:", len(consultas))

def alterar_consulta():
    print("\n--- ALTERAR CONSULTA ---")
    agendadas = []
    for c in consultas:
        if c["status"] == "agendada" or c["status"] == "confirmada":
            agendadas.append(c)
    if len(agendadas) == 0:
        print(">> Nenhuma consulta para alterar.")
        return
    for c in agendadas:
        print("Código:", c["id"], "|", c["paciente"], "|", c["medico"], "|", c["data"], c["hora"], "|", c["status"])
    codigo = input("Código da consulta: ").strip()
    for c in agendadas:
        if str(c["id"]) == codigo:
            nova_data = input("Nova data (" + c["data"] + "): ").strip()
            nova_hora = input("Nova hora (" + c["hora"] + "): ").strip()
            if nova_data == "":
                nova_data = c["data"]
            if nova_hora == "":
                nova_hora = c["hora"]
            if c["emergencia"] == False:
                if nova_hora < "07:00" or nova_hora >= "18:00":
                    print(">> Fora do horário de atendimento (07:00 às 18:00).")
                    return
            for outra in consultas:
                if outra["id"] != c["id"] and outra["medico"] == c["medico"] and outra["data"] == nova_data and outra["hora"] == nova_hora and outra["status"] != "cancelada":
                    print(">> Esse médico já tem consulta nesse horário!")
                    return
            c["data"] = nova_data
            c["hora"] = nova_hora
            c["status"] = "agendada"
            registrar_log("ALTERAR_CONSULTA", "id=" + str(c["id"]) + ", nova data=" + nova_data + " " + nova_hora)
            print(">> Consulta alterada com sucesso!")
            return
    print(">> Consulta não encontrada.")

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
        if c["emergencia"] == True:
            print("  Emergência: sim")
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
            registrar_log("CONFIRMAR_CONSULTA", "id=" + str(c["id"]))
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
            registrar_log("CANCELAR_CONSULTA", "id=" + str(c["id"]))
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
            registrar_log("REGISTRAR_ATENDIMENTO", "paciente=" + c["paciente"] + ", consulta=" + str(c["id"]))
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
    registrar_log("VER_PRONTUARIO", "paciente=" + paciente["nome"])
    print("\n=== PRONTUÁRIO DE", paciente["nome"], "===")
    print("CPF:", paciente["cpf"])
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
    print("\n--- Internações ---")
    encontrou_int = False
    for i in internacoes:
        if i["paciente"] == paciente["nome"]:
            encontrou_int = True
            print("  Leito:", i["leito"], "| Status:", i["status"])
            if "historico" in i:
                for h in i["historico"]:
                    print("    Transferência: do leito", h["de"], "para", h["para"], "em", h["data_hora"])
    if not encontrou_int:
        print(">> Nenhuma internação registrada.")

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
            registrar_log("ALERTA_ALERGIA", "paciente=" + paciente["nome"] + ", medicamento=" + medicamento)
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
        registrar_log("PRESCREVER", "paciente=" + paciente["nome"] + ", medicamento=" + medicamento)
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
    registrar_log("SOLICITAR_EXAME", "paciente=" + paciente["nome"] + ", exame=" + tipo)
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
            registrar_log("RESULTADO_EXAME", "exame=" + str(e["id"]) + ", paciente=" + e["paciente"])
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
    registrar_log("CADASTRAR_LEITO", setor + "-" + numero)
    print(">> Leito cadastrado! Código:", len(leitos))

def listar_leitos():
    print("\n--- LISTA DE LEITOS ---")
    if len(leitos) == 0:
        print(">> Nenhum leito cadastrado.")
        return
    for l in leitos:
        print("Código:", l["id"], "| Setor:", l["setor"], "| Número:", l["numero"], "| Status:", l["status"])

def alterar_status_leito():
    print("\n--- ALTERAR STATUS DE LEITO ---")
    listar_leitos()
    if len(leitos) == 0:
        return
    codigo = input("Código do leito: ").strip()
    for l in leitos:
        if str(l["id"]) == codigo:
            print("Status atual:", l["status"])
            print("1 - disponivel")
            print("2 - ocupado")
            print("3 - reservado")
            print("4 - manutencao")
            op = input("Novo status: ").strip()
            mapa = {"1": "disponivel", "2": "ocupado", "3": "reservado", "4": "manutencao"}
            if op in mapa:
                l["status"] = mapa[op]
                registrar_log("ALTERAR_STATUS_LEITO", "id=" + str(l["id"]) + ", status=" + l["status"])
                print(">> Status alterado para", l["status"])
            else:
                print(">> Opção inválida.")
            return
    print(">> Leito não encontrado.")

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
            internacoes.append({
                "id": len(internacoes) + 1,
                "paciente": paciente["nome"],
                "leito": l["id"],
                "status": "ativa",
                "historico": []
            })
            registrar_log("INTERNAR", "paciente=" + paciente["nome"] + ", leito=" + str(l["id"]))
            print(">> Paciente internado no leito", l["numero"], "do setor", l["setor"])
            return
    print(">> Leito inválido ou já ocupado.")

def transferir_leito():
    print("\n--- TRANSFERIR PACIENTE ---")
    ativas = []
    for i in internacoes:
        if i["status"] == "ativa":
            ativas.append(i)
    if len(ativas) == 0:
        print(">> Nenhuma internação ativa.")
        return
    for i in ativas:
        print("Paciente:", i["paciente"], "| Leito atual:", i["leito"])
    nome = input("Nome do paciente: ").strip()
    for i in internacoes:
        if i["paciente"] == nome and i["status"] == "ativa":
            disponiveis = []
            for l in leitos:
                if l["status"] == "disponivel":
                    disponiveis.append(l)
            if len(disponiveis) == 0:
                print(">> Nenhum leito disponível para transferência.")
                return
            print("\nLeitos disponíveis:")
            for l in disponiveis:
                print("  Código:", l["id"], "| Setor:", l["setor"], "| Número:", l["numero"])
            codigo_leito = input("Código do novo leito: ").strip()
            for l in leitos:
                if str(l["id"]) == codigo_leito and l["status"] == "disponivel":
                    leito_antigo = i["leito"]
                    for l2 in leitos:
                        if l2["id"] == leito_antigo:
                            l2["status"] = "disponivel"
                    l["status"] = "ocupado"
                    i["leito"] = l["id"]
                    i["historico"].append({
                        "de": leito_antigo,
                        "para": l["id"],
                        "data_hora": agora()
                    })
                    registrar_log("TRANSFERIR", "paciente=" + nome + ", de=" + str(leito_antigo) + " para=" + str(l["id"]))
                    print(">> Transferência registrada! Novo leito:", l["numero"], "do setor", l["setor"])
                    return
            print(">> Leito inválido ou indisponível.")
            return
    print(">> Internação ativa não encontrada.")

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
            registrar_log("ALTA", "paciente=" + i["paciente"])
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
    hoje = datetime.date.today()
    validade = datetime.date(ano, mes, dia)
    return (validade - hoje).days

def cadastrar_medicamento():
    print("\n--- CADASTRAR MEDICAMENTO ---")
    nome = input("Nome do medicamento: ").strip()
    lote = input("Lote: ").strip()
    fornecedor = input("Fornecedor: ").strip()
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
        "fornecedor": fornecedor,
        "quantidade": quantidade,
        "validade": validade,
        "minimo": minimo
    })
    registrar_log("CADASTRAR_MEDICAMENTO", nome + ", lote=" + lote)
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
            registrar_log("ENTRADA_ESTOQUE", m["nome"] + ", +" + str(qtd))
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
            registrar_log("SAIDA_ESTOQUE", m["nome"] + ", -" + str(qtd))
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
        print("Código:", m["id"], "|", m["nome"], "| Lote:", m["lote"], "| Fornecedor:", m.get("fornecedor", ""))
        print("  Quantidade:", m["quantidade"], "| Mínimo:", m["minimo"], "| Validade:", m["validade"])
        print("  Status:", status)
        print("")

def relatorio_pacientes():
    print("\n=== RELATÓRIO DE PACIENTES ===")
    total = len(pacientes)
    com_alergia = 0
    com_convenio = 0
    for p in pacientes:
        if p["alergias"] != "":
            com_alergia = com_alergia + 1
        if p["convenio"] != "":
            com_convenio = com_convenio + 1
    print("Total de pacientes:", total)
    print("Com alergia registrada:", com_alergia)
    print("Com convênio:", com_convenio)
    print("Particulares:", total - com_convenio)

def relatorio_consultas():
    print("\n=== RELATÓRIO DE CONSULTAS ===")
    agendadas = 0
    confirmadas = 0
    realizadas = 0
    canceladas = 0
    for c in consultas:
        if c["status"] == "agendada":
            agendadas = agendadas + 1
        elif c["status"] == "confirmada":
            confirmadas = confirmadas + 1
        elif c["status"] == "realizada":
            realizadas = realizadas + 1
        elif c["status"] == "cancelada":
            canceladas = canceladas + 1
    print("Total de consultas:", len(consultas))
    print("Agendadas:", agendadas)
    print("Confirmadas:", confirmadas)
    print("Realizadas:", realizadas)
    print("Canceladas:", canceladas)

def relatorio_internacoes():
    print("\n=== RELATÓRIO DE INTERNAÇÕES ===")
    ativas = 0
    encerradas = 0
    for i in internacoes:
        if i["status"] == "ativa":
            ativas = ativas + 1
        else:
            encerradas = encerradas + 1
    total_leitos = len(leitos)
    ocupados = 0
    for l in leitos:
        if l["status"] == "ocupado":
            ocupados = ocupados + 1
    taxa = 0
    if total_leitos > 0:
        taxa = (ocupados * 100) / total_leitos
    print("Internações ativas:", ativas)
    print("Internações encerradas:", encerradas)
    print("Leitos totais:", total_leitos)
    print("Leitos ocupados:", ocupados)
    print("Taxa de ocupação:", round(taxa, 1), "%")

def relatorio_exames():
    print("\n=== RELATÓRIO DE EXAMES ===")
    solicitados = 0
    concluidos = 0
    for e in exames:
        if e["status"] == "solicitado":
            solicitados = solicitados + 1
        else:
            concluidos = concluidos + 1
    print("Total de exames:", len(exames))
    print("Pendentes:", solicitados)
    print("Concluídos:", concluidos)

def relatorio_estoque():
    print("\n=== RELATÓRIO DE ESTOQUE ===")
    total = len(estoque)
    vencidos = 0
    vencendo = 0
    abaixo_minimo = 0
    for m in estoque:
        data = converter_data(m["validade"])
        if data is not None:
            dias = dias_para_vencer(data[0], data[1], data[2])
            if dias < 0:
                vencidos = vencidos + 1
            elif dias <= 30:
                vencendo = vencendo + 1
        if m["quantidade"] < m["minimo"]:
            abaixo_minimo = abaixo_minimo + 1
    print("Total de itens:", total)
    print("Vencidos:", vencidos)
    print("Vencendo em até 30 dias:", vencendo)
    print("Abaixo do estoque mínimo:", abaixo_minimo)

def relatorio_prescricoes():
    print("\n=== RELATÓRIO DE PRESCRIÇÕES ===")
    if len(prescricoes) == 0:
        print(">> Nenhuma prescrição registrada.")
        return
    print("Total de prescrições:", len(prescricoes))
    for p in prescricoes:
        print("  ", p["paciente"], "->", p["medicamento"])

def relatorio_profissionais():
    print("\n=== RELATÓRIO DE PROFISSIONAIS ===")
    total = 0
    for u in usuarios:
        if u["perfil"] in ("medico", "enfermeiro"):
            total = total + 1
            status = "ativo" if u.get("ativo", True) else "inativo"
            print(u["nome"], "|", u["perfil"], "|", status)
            print("  Especialidade:", u.get("especialidade", "não informada"))
            print("  Registro:", u.get("registro", "não informado"))
            print("  Setor:", u.get("setor", "não informado"))
    if total == 0:
        print(">> Nenhum profissional cadastrado.")

def menu_relatorios():
    while True:
        print("\n=== RELATÓRIOS ===")
        print("1 - Pacientes")
        print("2 - Consultas")
        print("3 - Internações")
        print("4 - Exames")
        print("5 - Estoque")
        print("6 - Prescrições")
        print("7 - Profissionais")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            relatorio_pacientes()
        elif op == "2":
            relatorio_consultas()
        elif op == "3":
            relatorio_internacoes()
        elif op == "4":
            relatorio_exames()
        elif op == "5":
            relatorio_estoque()
        elif op == "6":
            relatorio_prescricoes()
        elif op == "7":
            relatorio_profissionais()
        elif op == "0":
            break
        else:
            print(">> Opção inválida.")

def ver_indicadores():
    print("\n=== INDICADORES HOSPITALARES ===")
    realizadas = 0
    for c in consultas:
        if c["status"] == "realizada":
            realizadas = realizadas + 1
    internacoes_ativas = 0
    for i in internacoes:
        if i["status"] == "ativa":
            internacoes_ativas = internacoes_ativas + 1
    altas = 0
    for i in internacoes:
        if i["status"] == "encerrada":
            altas = altas + 1
    total_leitos = len(leitos)
    ocupados = 0
    for l in leitos:
        if l["status"] == "ocupado":
            ocupados = ocupados + 1
    taxa = 0
    if total_leitos > 0:
        taxa = (ocupados * 100) / total_leitos
    exames_pendentes = 0
    for e in exames:
        if e["status"] == "solicitado":
            exames_pendentes = exames_pendentes + 1
    estoque_baixo = 0
    for m in estoque:
        if m["quantidade"] < m["minimo"]:
            estoque_baixo = estoque_baixo + 1
    print("Pacientes cadastrados:", len(pacientes))
    print("Consultas realizadas:", realizadas)
    print("Internações ativas:", internacoes_ativas)
    print("Altas registradas:", altas)
    print("Leitos totais:", total_leitos)
    print("Leitos ocupados:", ocupados)
    print("Taxa de ocupação:", round(taxa, 1), "%")
    print("Exames pendentes:", exames_pendentes)
    print("Itens de estoque abaixo do mínimo:", estoque_baixo)

def central_notificacoes():
    print("\n=== CENTRAL DE NOTIFICAÇÕES ===")
    encontrou = False
    for m in estoque:
        data = converter_data(m["validade"])
        if data is not None:
            dias = dias_para_vencer(data[0], data[1], data[2])
            if dias < 0:
                print(">> VENCIDO:", m["nome"], "(lote", m["lote"], ")")
                encontrou = True
            elif dias <= 30:
                print(">> VENCE EM", dias, "DIAS:", m["nome"], "(lote", m["lote"], ")")
                encontrou = True
        if m["quantidade"] < m["minimo"]:
            print(">> ESTOQUE BAIXO:", m["nome"], "(qtd", m["quantidade"], "de mínimo", m["minimo"], ")")
            encontrou = True
    for e in exames:
        if e["status"] == "solicitado":
            print(">> EXAME PENDENTE:", e["tipo"], "do paciente", e["paciente"])
            encontrou = True
    for c in consultas:
        if c["status"] == "confirmada":
            print(">> CONSULTA CONFIRMADA:", c["paciente"], "com", c["medico"], "em", c["data"], "às", c["hora"])
            encontrou = True
    if not encontrou:
        print(">> Nenhuma notificação no momento.")

def menu_administrador():
    while True:
        print("\n=== MENU ADMINISTRADOR ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Ativar/Desativar usuário")
        print("4 - Cadastrar leito")
        print("5 - Listar leitos")
        print("6 - Alterar status de leito")
        print("7 - Cadastrar medicamento")
        print("8 - Listar estoque")
        print("9 - Entrada de estoque")
        print("10 - Saída de estoque")
        print("11 - Relatórios")
        print("12 - Indicadores")
        print("13 - Ver logs de atividades")
        print("14 - Central de notificações")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            cadastrar_usuario()
        elif op == "2":
            listar_usuarios()
        elif op == "3":
            alternar_status_usuario()
        elif op == "4":
            cadastrar_leito()
        elif op == "5":
            listar_leitos()
        elif op == "6":
            alterar_status_leito()
        elif op == "7":
            cadastrar_medicamento()
        elif op == "8":
            listar_estoque()
        elif op == "9":
            entrada_estoque()
        elif op == "10":
            saida_estoque()
        elif op == "11":
            menu_relatorios()
        elif op == "12":
            ver_indicadores()
        elif op == "13":
            ver_logs()
        elif op == "14":
            central_notificacoes()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")
        salvar_dados()

def menu_recepcionista():
    while True:
        print("\n=== MENU RECEPCIONISTA ===")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes")
        print("3 - Atualizar paciente")
        print("4 - Agendar consulta")
        print("5 - Alterar consulta")
        print("6 - Listar consultas")
        print("7 - Confirmar consulta")
        print("8 - Cancelar consulta")
        print("9 - Central de notificações")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            cadastrar_paciente()
        elif op == "2":
            listar_pacientes()
        elif op == "3":
            atualizar_paciente()
        elif op == "4":
            agendar_consulta()
        elif op == "5":
            alterar_consulta()
        elif op == "6":
            listar_consultas()
        elif op == "7":
            confirmar_consulta()
        elif op == "8":
            cancelar_consulta()
        elif op == "9":
            central_notificacoes()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")
        salvar_dados()

def menu_medico():
    while True:
        print("\n=== MENU MÉDICO ===")
        print("1 - Listar pacientes")
        print("2 - Agendar consulta")
        print("3 - Alterar consulta")
        print("4 - Listar consultas")
        print("5 - Registrar atendimento")
        print("6 - Ver prontuário")
        print("7 - Prescrever medicamentos")
        print("8 - Listar prescrições")
        print("9 - Solicitar exame")
        print("10 - Registrar resultado de exame")
        print("11 - Listar exames")
        print("12 - Central de notificações")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            listar_pacientes()
        elif op == "2":
            agendar_consulta()
        elif op == "3":
            alterar_consulta()
        elif op == "4":
            listar_consultas()
        elif op == "5":
            registrar_atendimento()
        elif op == "6":
            ver_prontuario()
        elif op == "7":
            prescrever()
        elif op == "8":
            listar_prescricoes()
        elif op == "9":
            solicitar_exame()
        elif op == "10":
            registrar_resultado_exame()
        elif op == "11":
            listar_exames()
        elif op == "12":
            central_notificacoes()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")
        salvar_dados()

def menu_enfermeiro():
    while True:
        print("\n=== MENU ENFERMEIRO ===")
        print("1 - Listar pacientes")
        print("2 - Listar leitos")
        print("3 - Internar paciente")
        print("4 - Transferir paciente")
        print("5 - Dar alta")
        print("6 - Ver prontuário")
        print("7 - Listar exames")
        print("8 - Central de notificações")
        print("0 - Sair")
        op = input("Opção: ").strip()
        if op == "1":
            listar_pacientes()
        elif op == "2":
            listar_leitos()
        elif op == "3":
            internar()
        elif op == "4":
            transferir_leito()
        elif op == "5":
            dar_alta()
        elif op == "6":
            ver_prontuario()
        elif op == "7":
            listar_exames()
        elif op == "8":
            central_notificacoes()
        elif op == "0":
            print(">> Você saiu da conta.")
            break
        else:
            print(">> Opção inválida.")
        salvar_dados()

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


carregar_dados()
menu()