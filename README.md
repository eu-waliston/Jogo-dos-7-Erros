# 🐛 Caça aos Bugs!

Um jogo educacional de programação onde você encontra e corrige erros de sintaxe antes que o inimigo fuja com o código. Disponível em duas versões: **JavaScript (navegador)** e **Python (Pygame)**.

---

## 🎮 Como Jogar

1. Responda o questionário para descobrir seu perfil de jogador (ou escolha uma trilha diretamente)
2. Um inimigo vai **roubar** o código e introduzir erros de sintaxe
3. **Clique nos círculos vermelhos piscantes** para encontrar os erros no código da esquerda
4. Compare com o **código correto** exibido à direita
5. Encontre todos os erros antes de passar para o próximo nível!

---

## 🗂️ Estrutura do Projeto

```
/
├── 7-erros/                    # Versão JavaScript (navegador)
│   ├── index.html
│   ├── script.js               # Lógica principal do jogo
│   ├── questionnaire.js        # Sistema de questionário e perfis
│   └── background-music.js    # Música de fundo (Web Audio API)
│
└── jogo_erros/                 # Versão Python (Pygame)
    ├── main.py                 # Ponto de entrada
    ├── constants.py            # Cores, fontes e dimensões
    ├── game_data.py            # Dados: trilhas, temas, níveis e erros
    ├── questionnaire.py        # Telas de questionário e seleção
    ├── minigame.py             # Gameplay: círculos, inimigo, animações
    ├── music.py                # Música sintetizada em tempo real
    └── widgets.py              # Botões e helpers de UI
```

---

## 🚀 Rodando a Versão Python

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/caca-aos-bugs.git
cd caca-aos-bugs/jogo_erros

# Instale as dependências
pip install pygame numpy
```

### Execução

```bash
python main.py
```

> **Dica:** `numpy` é opcional — sem ele a música de fundo é desabilitada, mas o jogo funciona normalmente.

---

## 🌐 Rodando a Versão JavaScript

Basta abrir o arquivo `7-erros/index.html` num servidor local. Se tiver o VS Code com a extensão **Live Server**, clique com o botão direito no `index.html` → *Open with Live Server*.

Ou via terminal:

```bash
cd 7-erros
npx serve .
# acesse http://localhost:3000
```

---

## 🧩 Trilhas e Perfis

O questionário inicial determina qual dos quatro perfis você vai jogar:

| Trilha | Perfil Narrativo | Inimigo | Dificuldade |
|---|---|---|---|
| 🎓 Iniciante | Mago do Código | Goblin Ladrão | Fácil |
| 🧭 Explorador | Detetive Cibernético | Falsificador | Médio |
| 🎯 Hacker | Hacker de Elite | Vírus Glitch | Intermediário |
| ⚡ Mestre | Detetive Cibernético | Falsificador | Difícil |

Cada perfil tem **narrativa própria**, inimigo com visual diferente e nomes de fases temáticos.

---

## 🗺️ Temas Narrativos

Após definir a trilha, você escolhe o tema que "colore" os nomes das fases:

| Tema | Cenário |
|---|---|
| 🧙 Fantasia e Magia | Grimório Antigo |
| 💻 Tecnologia e Hackers | Rede Digital |
| 🕵️ Mistério e Investigação | Cena do Crime Digital |
| 🏆 Competição e Desafio | Arena Digital |

---

## 📚 Linguagens dos Níveis

O jogo tem **5 níveis** com erros em:

- **Python** — erros de sintaxe clássicos: `:` faltando, operadores errados, tipos incompatíveis
- **HTML** — tags mal fechadas, atributos inválidos, falta de `alt`

---

## 🏗️ Arquitetura (Versão Python)

```
main.py
  └── QuestionnaireScreen   →  coleta perfil do jogador
        └── Minigame        →  loop principal do jogo
              ├── Enemy          animação do inimigo
              ├── draw_panels    canvas de código (correto é estático!)
              ├── error_circles  círculos pulsantes clicáveis
              └── music          thread de áudio em background
```

### Decisões de design

- **Canvas correto renderizado uma só vez** — a `Surface` do código de referência é gerada ao carregar o nível e apenas colada (`blit`) a cada frame, sem redesenho. Isso elimina o gargalo de performance que existia na versão JS original.
- **Perfis clonados com `deepcopy`** — corrige o bug da versão JS onde o nome das fases acumulava o prefixo do tema a cada vez que o jogador refazia o questionário.
- **Música em thread separada** — usa `threading.Thread` + `pygame.sndarray` para gerar a melodia chiptune sem travar o loop principal.
- **`localStorage` → arquivo JSON** — o perfil salvo fica em `player_profile.json` na mesma pasta, com `try/except` em todas as operações de leitura e escrita.

---

## ➕ Como Adicionar Novos Níveis

Abra `game_data.py` e adicione um novo item na lista `LEVELS`:

```python
{
    "language": "Python",           # exibido no HUD
    "correct_code": "...",          # código sem erros (painel direito)
    "wrong_code": "...",            # código com erros (painel esquerdo)
    "errors": [
        {
            "line": 0,              # índice da linha (começa em 0)
            "char_pos": 10,         # posição do caractere na linha
            "explanation": "Faltou ':' após o def",
        },
    ],
},
```

> **Dica:** `char_pos` define onde o círculo vermelho aparece. Conte os caracteres da linha até o erro (começa em 0).

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit: `git commit -m 'Adiciona novo nivel de JavaScript'`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

Sugestões bem-vindas:
- Novos níveis (JavaScript, CSS, SQL...)
- Novos temas narrativos
- Sistema de pontuação e ranking
- Suporte a teclado/acessibilidade

---

## 📄 Licença

MIT — sinta-se livre para usar, modificar e distribuir.
