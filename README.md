# Gestão de Squad - CRUD

Este projeto é um sistema de gerenciamento de jogadores de futebol (Squad), desenvolvido como trabalho final de Desenvolvimento de Sistemas. O sistema permite realizar operações de CRUD (Criar, Ler, Atualizar e Deletar) através de uma interface desktop ou via API REST.

## Tecnologias Utilizadas

  * **Linguagem:** Python 3
  * **Interface Gráfica (GUI):** Tkinter (Nativo do Python)
  * **API:** Flask
  * **Banco de Dados:** SQLite3

## Funcionalidades

O sistema gerencia duas entidades principais no banco de dados: **Jogadores** (`squad`) e **Times** (`times`).

### Interface Gráfica (GUI)

Ao executar o módulo visual, você pode:

  * **Adicionar Jogadores:** Cadastro completo com Nome, Idade, Posição, Nacionalidade e Time.
      * *Nota:* Se o time informado não existir, o sistema o cria automaticamente.
  * **Listar Jogadores:** Visualização dos dados em uma tabela (Treeview).
  * **Atualizar:** Selecionar um jogador na lista para editar seus dados.
  * **Excluir:** Remover registros do banco de dados.

### API REST

A aplicação também expõe endpoints para integração com outros sistemas:

| Método | Endpoint          | Descrição                          |
| ------ | ----------------- | ---------------------------------- |
| `GET`  | `/jogadores`      | Retorna a lista de todos jogadores |
| `POST` | `/jogadores`      | Cria um novo jogador               |
| `PUT`  | `/jogadores/<id>` | Atualiza um jogador existente      |
| `DELETE`| `/jogadores/<id>`| Remove um jogador pelo ID          |

## Instalação e Dependências

O projeto utiliza bibliotecas nativas do Python, com exceção do **Flask**.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/victorbalencar/ceub-devsistemascrudgui.git
    cd Ceub-DevSistemasCrudGUI
    ```

2.  **Instale as dependências:**

    ```bash
    pip install flask
    ```

    *(Nota: O `tkinter` e `sqlite3` geralmente já vêm instalados com o Python).*

## Como Executar

### 1\. Executando a Interface Gráfica

Para abrir o gerenciador visual (Janela Desktop):

```bash
python main.py
```

Isso iniciará a classe `App` e conectará ao banco de dados `banco.db`.

### 2\. Executando a API

Para iniciar o servidor web localmente (na porta 5000):

```bash
python api.py
```

#### Exemplos de Requisições (JSON)

**Criar Jogador (`POST /jogadores`):**

```json
{
    "nome": "Neymar Jr",
    "idade": 31,
    "posicao": "ATA",
    "nacionalidade": "Brasil",
    "time": "Al-Hilal"
}
```

**Atualizar Jogador (`PUT /jogadores/1`):**

```json
{
    "nome": "Neymar Jr",
    "idade": 32,
    "posicao": "MEI",
    "nacionalidade": "Brasil",
    "time": "Santos"
}
```

## Estrutura do Projeto

  * `main.py`: Ponto de entrada para rodar a aplicação visual.
  * `gui.py`: Contém a lógica da interface gráfica (Janela, Botões, Tabela) usando Tkinter.
  * `api.py`: Servidor Flask que provê os endpoints JSON.
  * `db.py`: Camada de acesso a dados (DAO). Gerencia a conexão com o SQLite e as queries SQL.
  * `banco.db`: Arquivo do banco de dados gerado automaticamente na primeira execução.

-----

*Este README foi gerado com o auxílio do Gemini.*
