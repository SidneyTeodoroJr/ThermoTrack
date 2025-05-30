<h1 align="center">ThermoTrack</h1>

<div align="center">
  <img src="https://github.com/SidneyTeodoroJr/ThermoTrack/blob/main/src/assets/print/print2.png" alt="GUI"/>
</div>
</br>
</br>

**ThermoTrack** é uma aplicação interativa desenvolvida com [Flet](https://flet.dev/) e [FastAPI](https://fastapi.tiangolo.com/) que permite monitorar e visualizar dados de temperatura e eficiência de diferentes cidades em tempo real. A aplicação oferece uma interface gráfica intuitiva para busca de dados, exibição de gráficos e atualização contínua das informações.

## 🧰 Tecnologias Utilizadas

- [Flet](https://flet.dev/): Framework para criação de interfaces gráficas em Python.
- [FastAPI](https://fastapi.tiangolo.com/): Framework web moderno e rápido para APIs.
- [SQLite](https://www.sqlite.org/index.html): Banco de dados leve e embutido.

<div align="center">
  <img height=200 width=300 src="https://logosmarcas.net/wp-content/uploads/2021/10/Python-Logo.png" alt="Python"/>
  <img height=200 width=300 src="https://raw.githubusercontent.com/flet-dev/flet/main/media/logo/flet-logo.svg" alt="Flet"/>
</div>
</br>
</br>

## 🚀 Funcionalidades

- 🔍 Busca de dados de temperatura e eficiência por cidade.
- 📊 Exibição de gráficos interativos com os dados históricos.
- 🔄 Atualização automática dos dados em tempo real.
- 🖥️ Interface amigável e responsiva.

## 📦 Estrutura do Projeto

```bash
ThermoTrack/
├── assets/
│ └── data/
│ └── data-base.db
├── back/
│ └── init.py
├── module/
│ └── utils.py
├── api.py
├── main.py
├── requirements.txt
└── README.md
```

- `assets/data/data-base.db`: Banco de dados SQLite contendo os registros.
- `back.py`: Módulo responsável pela atualização e obtenção dos dados.
- `module/utils.py`: Funções utilitárias para criação de gráficos, validação de entrada, etc.
- `api.py`: API FastAPI para acesso aos dados.
- `main.py`: Interface gráfica construída com Flet.
- `requirements.txt`: Lista de dependências do projeto.

## ⚙️ Instalação e Execução

1. **Clone o repositório:**

```bash
git clone https://github.com/SidneyTeodoroJr/ThermoTrack.git
```
```bash
cd ThermoTrack
```


```bash
cd src
```

Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
```

# Linux/macOS:
```bash
source venv/bin/activate
```

# Windows:
```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
flet run
```
```bash
flet run -w
```

<div align="center">
  <img src="https://github.com/SidneyTeodoroJr/ThermoTrack/blob/main/src/assets/print/print1.png" alt="GUI"/>
</div>
</br>
</br>

A interface gráfica será aberta, permitindo que você interaja com a aplicação.

📝 Observações
Certifique-se de que a porta 8000 esteja disponível, pois a API FastAPI será executada nela.

Os dados são armazenados localmente no banco de dados SQLite localizado em assets/data/data-base.db.

Para adicionar ou visualizar novos dados manualmente, você pode utilizar ferramentas como DB Browser for SQLite.

<h2>Contributions</h2>
</br>

<p>
Contributions are welcome! If you want to improve the project, add new features or fix bugs, feel free to do so.
</p>
<hr>
</br>

<div align="center">
<a href="https://sidney-personal-portfolio.netlify.app/"><img src="https://img.shields.io/badge/-Portifolio-%230077B5?style=for-the-badge&logo=portifolio&logoColor=white" style="border-radius: 30px" target="_blank" /></a>
<a href="https://www.instagram.com/sidneyteodoroaraujo" target="_blank"><img src="https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/sidey-teodoro-a-jr/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" style="border-radius: 30px" target="_blank" /></a>
</div>
