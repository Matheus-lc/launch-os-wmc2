# Launch OS WMC 2

Este repositório é o sistema operacional do lançamento do **WMC 2 - Weapons of Mass Construction 2**, do **Mr.Saizen**. Ele reúne estratégia, operação diária, templates, métricas, compliance, prompt de assistência e uma interface local simples para consulta pela equipe.

O objetivo é transformar o lançamento em uma rotina executável: poucas ferramentas, decisões claras, conteúdo técnico, venda indireta e controle diário do que precisa acontecer.

## Estrutura de pastas

```text
/
  README.md
  AGENTS.md
  .gitignore
  /docs          Visão geral, plano imediato, uso diário e perguntas em aberto
  /strategy      Estratégia do lançamento, canais, oferta, calendário e contingências
  /operations    Checklists, responsabilidades, rituais e cronograma
  /content       Plano editorial, WhatsApp, YouTube, provas e briefings
  /copy          Promessas, anúncios, roteiros, WhatsApp, FAQ e revisão
  /offer         Oferta final, order bump, garantia, urgência e FAQ
  /templates     Modelos prontos para preencher e copiar
  /metrics       Dicionário, metas, scorecards e logs em CSV
  /compliance    Regras de claims, provas, depoimentos e revisão
  /assistant     Prompt mestre, playbooks e comandos para o time
  /ui            Interface interna opcional em Streamlit
  /data          Seeds em JSON para tarefas, calendário, KPIs e FAQ
```

## Como usar no dia a dia

A equipe deve abrir este repositório no início do dia, olhar as tarefas do calendário, revisar as métricas do dia anterior e decidir o que precisa ser produzido, publicado, ajustado ou respondido. O Launch OS não substitui julgamento humano; ele reduz ruído operacional.

Arquivos fonte de verdade:

- Estratégia: `strategy/diagnostico.md`, `strategy/funil-e-canais.md`, `strategy/calendario-junho-2026.md`
- Operação: `operations/cronograma-dia-a-dia.csv`, `operations/checklist-geral.md`, `operations/rituais-diarios.md`
- Oferta: `offer/oferta-principal.md`, `offer/order-bump-wmc1.md`
- Métricas: `metrics/dashboard_base.csv`, `metrics/daily_log.csv`, `metrics/metas.csv`
- Compliance: `compliance/guia-compliance.md`, `compliance/biblioteca-de-claims.md`
- Assistente: `assistant/prompt-head-lancamento.md`

## Fluxo de uso em 5 passos

1. Abrir `docs/guia-de-uso-diario.md` e executar o ritual da manhã.
2. Conferir `operations/cronograma-dia-a-dia.csv` e marcar o status das tarefas.
3. Produzir conteúdo usando `content/sequencia-de-conteudo.md` e os templates em `templates/`.
4. Revisar qualquer peça com `copy/checklist-revisao-de-copy.md` e `compliance/checklist-compliance.md`.
5. Fechar o dia preenchendo `metrics/daily_log.csv` e usando `assistant/playbooks.md` se houver gargalo.

## Como abrir a UI Streamlit

A interface é opcional e roda localmente, sem backend obrigatório.

```bash
cd launch-os-wmc2
python -m venv .venv
.venv\Scripts\activate
pip install -r ui/requirements.txt
streamlit run ui/app.py
```

Se `OPENAI_API_KEY` existir no ambiente, a aba Assistente mostra um modo opcional de chat simples. Sem chave, a UI continua funcionando como painel de consulta e cópia de prompt.

## Deploy no Streamlit Community Cloud

O projeto já está organizado para deploy no Streamlit Cloud:

- Repositório GitHub: `Matheus-lc/launch-os-wmc2`
- Branch: `main`
- Main file path: `ui/app.py`
- Dependências: `requirements.txt` na raiz
- Configuração visual: `.streamlit/config.toml`

No Streamlit Community Cloud:

1. Clique em `Create app`.
2. Escolha `Yup, I have an app`.
3. Informe o repositório `Matheus-lc/launch-os-wmc2`.
4. Informe a branch `main`.
5. Informe o arquivo principal `ui/app.py`.
6. Em `Advanced settings`, use Python `3.12` se a opção aparecer.
7. Não é necessário configurar secrets para o uso básico.
8. Clique em `Deploy`.

## Decisão estratégica resumida

O modelo recomendado é um pré-lançamento orgânico curto com aquecimento em WhatsApp, abertura primeiro no WhatsApp, liberação pública depois no Instagram e carrinho de 48 a 60 horas. A venda é técnica, indireta e baseada em autoridade, prova e clareza de aplicação.

Datas principais:

- Pré-lançamento até **02/06/2026**
- Abertura no WhatsApp em **03/06/2026**
- Fechamento em **05/06/2026**
- Preço recomendado: **R$247**
