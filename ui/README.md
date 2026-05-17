# UI Streamlit

Esta interface é opcional. Ela serve para consulta rápida do Launch OS, visualização de tarefas, calendário, métricas, checklists, compliance e prompt do assistente.

A fonte de verdade continua sendo os arquivos Markdown, CSV e JSON do repositório. A UI apenas lê esses arquivos e permite editar o status das tarefas no CSV local `operations/cronograma-dia-a-dia.csv`.

## Como rodar

```bash
cd launch-os-wmc2
python -m venv .venv
.venv\Scripts\activate
pip install -r ui/requirements.txt
streamlit run ui/app.py
```

## Sem API externa

A UI funciona sem API externa. Se `OPENAI_API_KEY` existir no ambiente, a aba Assistente mostra um espaço opcional para montar uma mensagem de chat, mas o uso do prompt mestre continua manual e local.

## Deploy no Streamlit Community Cloud

Configurações:

- Repository: `Matheus-lc/launch-os-wmc2`
- Branch: `main`
- Main file path: `ui/app.py`
- Python version: `3.12`

Não configure secrets no primeiro deploy. A UI funciona lendo apenas arquivos Markdown, CSV e JSON do repositório.
