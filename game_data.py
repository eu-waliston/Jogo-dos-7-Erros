"""Dados estáticos: trilhas, temas, perguntas, perfis narrativos e níveis."""
import copy

TRAILS = {
    "iniciante": {
        "id": "iniciante", "name": "Iniciante", "icon": "Iniciante",
        "description": "Para quem esta comecando do zero. Muitas dicas e passo a passo!",
        "color": (37, 99, 235),
    },
    "explorador": {
        "id": "explorador", "name": "Explorador", "icon": "Explorador",
        "description": "Para aprendizes curiosos. Puzzles moderados e recompensas por exploracao.",
        "color": (249, 115, 22),
    },
    "hacker": {
        "id": "hacker", "name": "Hacker", "icon": "Hacker",
        "description": "Para programadores intermediarios. Bugs, logica e missoes tecnicas.",
        "color": (34, 197, 94),
    },
    "mestre": {
        "id": "mestre", "name": "Mestre", "icon": "Mestre",
        "description": "Para especialistas. Maxima dificuldade, pouquissimas dicas.",
        "color": (139, 92, 246),
    },
}

TRAIL_TO_PROFILE = {
    "iniciante": "mago",
    "explorador": "detetive",
    "hacker": "hacker",
    "mestre": "detetive",
}

THEMES = {
    "fantasia":    {"id": "fantasia",    "name": "Fantasia e Magia",        "setting": "Grimorio Antigo"},
    "tecnologia":  {"id": "tecnologia",  "name": "Tecnologia e Hackers",    "setting": "Rede Digital"},
    "misterio":    {"id": "misterio",    "name": "Misterio e Investigacao",  "setting": "Cena do Crime Digital"},
    "competicao":  {"id": "competicao",  "name": "Competicao e Desafio",    "setting": "Arena Digital"},
}

QUESTIONS = [
    {
        "id": 1, "question": "Voce ja teve contato com programacao?",
        "options": [
            {"text": "Nunca",    "scores": {"iniciante": 3,  "explorador": 1, "hacker": -2, "mestre": -5}},
            {"text": "Um pouco", "scores": {"iniciante": 1,  "explorador": 3, "hacker": 1,  "mestre": -2}},
            {"text": "Bastante", "scores": {"iniciante": -1, "explorador": 1, "hacker": 3,  "mestre": 1}},
            {"text": "Avancado", "scores": {"iniciante": -3, "explorador": 0, "hacker": 2,  "mestre": 3}},
        ],
    },
    {
        "id": 2, "question": "Como voce prefere aprender?",
        "options": [
            {"text": "Praticando devagar",      "scores": {"iniciante": 3, "explorador": 1, "hacker": 0, "mestre": -2}},
            {"text": "Explorando livremente",   "scores": {"iniciante": 0, "explorador": 3, "hacker": 1, "mestre": 0}},
            {"text": "Resolvendo problemas",    "scores": {"iniciante": -1, "explorador": 1, "hacker": 3, "mestre": 2}},
            {"text": "Desafios extremos",       "scores": {"iniciante": -3, "explorador": 0, "hacker": 1, "mestre": 3}},
        ],
    },
    {
        "id": 3, "question": "Qual tema voce prefere?",
        "options": [
            {"text": "Fantasia e Magia",       "theme": "fantasia"},
            {"text": "Tecnologia e Hackers",   "theme": "tecnologia"},
            {"text": "Misterio",               "theme": "misterio"},
            {"text": "Competicao",             "theme": "competicao"},
        ],
    },
]

PROFILES = {
    "hacker": {
        "name": "Hacker de Elite",
        "enemy_name": "Virus Glitch",
        "enemy_color": (34, 197, 94),
        "enemy_eye_color": (0, 200, 50),
        "enemy_shape": "square",
        "level_names": [
            "MISSAO 1: Saudacao do Servidor Oculto",
            "MISSAO 2: Quebra do Firewall",
            "MISSAO 3: Loop do Nucleo do Sistema",
            "MISSAO 4: Interface de Login",
            "MISSAO 5: Backdoor do Painel de Controle",
        ],
        "level_intros": [
            "O Virus Glitch foi detectado tentando alterar a mensagem de boas-vindas do servidor oculto.",
            "O Glitch esta corrompendo a logica do firewall. Proteja o banco de dados!",
            "Um loop infinito foi inserido no nucleo. Prepare-se para interceptar!",
            "O virus esta desfigurando a pagina principal da intranet.",
            "Backdoor detectado! O Glitch adulterou o formulario para vazar senhas.",
        ],
        "steal_msg": "MALWARE EXECUTADO! Clique nos circulos para debugar o codigo!",
        "win_msg": "DEBUG CONCLUIDO! O codigo esta limpo.",
    },
    "mago": {
        "name": "Mago do Codigo",
        "enemy_name": "Goblin Ladrao",
        "enemy_color": (139, 92, 246),
        "enemy_eye_color": (251, 191, 36),
        "enemy_shape": "triangle",
        "level_names": [
            "CAPITULO 1: Feitico de Invocacao",
            "CAPITULO 2: Encantamento de Barreira",
            "CAPITULO 3: Ritual de Repeticao Astral",
            "CAPITULO 4: Pergaminho de Ilusao",
            "CAPITULO 5: Contrato de Pacto Magico",
        ],
        "level_intros": [
            "O grimorio foi aberto. Um Goblin sorrateiro se aproxima do feitico de invocacao...",
            "O Goblin quer quebrar a magia de barreira que protege os aprendizes!",
            "O ritual astral esta instavel! O Goblin tenta sabotar as linhas de repeticao.",
            "As antigas escrituras estao sendo reescritas pela criatura!",
            "O ritual final: o Goblin quer adulterar as assinaturas do Pacto Magico!",
        ],
        "steal_msg": "ZAP! O Goblin sugou as runas! Conserte os nos magicos!",
        "win_msg": "FEITICO RESTAURADO! A magia flui perfeitamente.",
    },
    "detetive": {
        "name": "Detetive Cibernetico",
        "enemy_name": "Falsificador",
        "enemy_color": (249, 115, 22),
        "enemy_eye_color": (255, 255, 255),
        "enemy_shape": "square_eyes",
        "level_names": [
            "CASO 1: O Registro de Ponto Falso",
            "CASO 2: Sabotagem na Camera de Seguranca",
            "CASO 3: Rastreamento de Pegadas Digitais",
            "CASO 4: O Site de Phishing",
            "CASO 5: Formulario de Extorsao",
        ],
        "level_intros": [
            "Detetive, o Falsificador esta tentando alterar os registros de entrada do suspeito.",
            "Ele esta na sala das cameras! Tentando mudar a logica de autorizacao.",
            "Estamos seguindo as pegadas dele num loop de dados, mas ele tenta apagar rastros.",
            "Uma pagina falsa foi encontrada. Ele esta alterando a estrutura para enganar vitimas.",
            "A peca final: o formulario usado para roubar credenciais.",
        ],
        "steal_msg": "CENA DO CRIME ADULTERADA! Encontre as contradicoes na sintaxe!",
        "win_msg": "MISTERIO RESOLVIDO! Voce encontrou as falhas do criminoso.",
    },
}

LEVELS = [
    {
        "language": "Python",
        "correct_code": 'def saudacao(nome):\n    print("Ola, " + nome + "!")\n    return True',
        "wrong_code":   'def saudacao(nome)\n    print("Ola, " + nome + "!)\n    return Truw',
        "errors": [
            {"line": 0, "char_pos": 17, "explanation": "Faltou ':' apos 'def saudacao(nome)'"},
            {"line": 1, "char_pos": 26, "explanation": "String sem fechamento de aspas"},
            {"line": 2, "char_pos": 11, "explanation": "'Truw' nao existe — deveria ser 'True'"},
        ],
    },
    {
        "language": "Python",
        "correct_code": 'idade = 18\nif idade >= 18:\n    print("Maior de idade")\nelse:\n    print("Menor de idade")',
        "wrong_code":   'idade = 18\nif idade > 18:\n    print("Maior de idade")\nelse\n    print("Menor de idade")',
        "errors": [
            {"line": 1, "char_pos": 9,  "explanation": "Operador incorreto: deveria ser '>=' nao '>'"},
            {"line": 3, "char_pos": 4,  "explanation": "Faltou ':' apos 'else'"},
        ],
    },
    {
        "language": "Python",
        "correct_code": 'for i in range(3):\n    print("Valor: " + str(i))\n    if i == 1:\n        break',
        "wrong_code":   'for i in range(3)\n    print("Valor: " + i)\n    if i = 1:\n        break',
        "errors": [
            {"line": 0, "char_pos": 17, "explanation": "Faltou ':' no final do for"},
            {"line": 1, "char_pos": 20, "explanation": "Concatenacao invalida: int com string sem str()"},
            {"line": 2, "char_pos": 9,  "explanation": "Atribuicao '=' ao inves de comparacao '=='"},
        ],
    },
    {
        "language": "HTML",
        "correct_code": '<div class="container">\n    <h1>Bem-vindo</h1>\n    <p>Paragrafo</p>\n    <img src="foto.jpg" alt="Foto">\n</div>',
        "wrong_code":   '<div class="container">\n    <h1>Bem-vindo</h2>\n    <p>Paragrafo\n    <img src="foto.jpg">\n</div>',
        "errors": [
            {"line": 1, "char_pos": 19, "explanation": "Tag h1 fechada com /h2"},
            {"line": 2, "char_pos": 15, "explanation": "Tag <p> nao fechada"},
            {"line": 3, "char_pos": 20, "explanation": "Imagem sem atributo alt"},
        ],
    },
    {
        "language": "HTML",
        "correct_code": '<form action="/enviar" method="POST">\n    <label for="nome">Nome:</label>\n    <input type="text" name="nome">\n    <button type="submit">Enviar</button>\n</form>',
        "wrong_code":   '<form action="/enviar" method=POST>\n    <label>Nome:</label>\n    <input type="text" nome="nome">\n    <button type="submit">Enviar</button>\n</from>',
        "errors": [
            {"line": 0, "char_pos": 29, "explanation": "Atributo method sem aspas"},
            {"line": 1, "char_pos": 10, "explanation": "Label sem atributo for"},
            {"line": 2, "char_pos": 22, "explanation": "'nome' invalido — deveria ser 'name'"},
            {"line": 4, "char_pos": 2,  "explanation": "Tag de fechamento </from> invalida"},
        ],
    },
]


def apply_theme_to_profile(profile, theme):
    """Retorna cópia do perfil com level_names prefixados pelo setting do tema."""
    p = copy.deepcopy(profile)
    setting = theme["setting"]
    p["level_names"] = [f"{setting} - {n}" for n in profile["level_names"]]
    return p
