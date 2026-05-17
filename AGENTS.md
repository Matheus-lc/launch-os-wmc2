# AGENTS.md

## Propósito

Este repositório é o Launch OS do WMC 2, do Mr.Saizen. Ele deve funcionar como documento estratégico, rotina operacional, base de templates, centro de métricas, guia de compliance e interface interna simples.

## Mapa rápido

- `docs/`: visão executiva e uso diário.
- `strategy/`: decisões estratégicas e plano do lançamento.
- `operations/`: checklists, responsáveis, rituais e cronograma.
- `content/`: plano editorial, WhatsApp, YouTube, provas e briefings.
- `copy/`: promessas, roteiros, anúncios, mensagens e revisão.
- `offer/`: oferta, order bump, garantia e FAQ.
- `templates/`: modelos prontos para preencher.
- `metrics/`: CSVs e dicionário de métricas.
- `compliance/`: regras de segurança jurídica e editorial.
- `assistant/`: prompt mestre e playbooks.
- `ui/`: Streamlit local opcional.
- `data/`: seeds JSON usados pela UI.

## Regras de simplicidade

- Preferir Markdown, CSV e JSON antes de qualquer ferramenta nova.
- Não criar automação complexa.
- Não depender de live, e-mail ou backend para o plano funcionar.
- Toda recomendação precisa caber em uma equipe pequena e inexperiente.

## Padrão de linguagem

Português do Brasil, técnico, didático, premium, provocativo na medida e sem tom de guru. Preservar a voz professoral do Mr.Saizen: clareza, critério, precisão e venda sem pressão artificial.

## Do nots

- Não inventar prova, depoimento, número ou resultado.
- Não prometer ganho físico garantido, renda garantida ou transformação inevitável.
- Não usar escassez falsa.
- Não empilhar ferramentas.
- Não trocar o plano por funil complexo.
- Não usar inglês como idioma principal.

## O que significa pronto

Um arquivo está pronto quando a equipe consegue executar uma próxima ação sem pedir contexto adicional. Um checklist está pronto quando contém itens marcáveis e responsáveis sugeridos. Uma copy está pronta quando tem CTA, contexto, promessa segura e revisão de compliance possível.

## Validação da UI

Rodar:

```bash
pip install -r ui/requirements.txt
streamlit run ui/app.py
```

Confirmar que as abas Hoje, Calendário, Conteúdo, Métricas, Checklists, Compliance e Assistente abrem sem erro.

## Validação de CSV e Markdown

- CSVs devem abrir em planilha, ter cabeçalhos e exemplos realistas.
- Datas devem usar formato `YYYY-MM-DD`.
- Markdown deve ter títulos claros, listas acionáveis e links relativos coerentes.

## Instrução final

Não sobre-engenheirar. Manter pt-BR. Preservar coerência com a marca Mr.Saizen e com o lançamento curto via WhatsApp.

