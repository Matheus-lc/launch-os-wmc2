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
- Não usar a meta antiga como gatilho, milestone ou referência principal do grupo WMC 2.

## Regra de metas do grupo WMC 2

O assistente e qualquer agente do repositório devem considerar:

- Grupo de WhatsApp abre em 22/05/2026.
- Carrinho abre em 05/06/2026.
- Expectativa realista do grupo até 05/06: 300 integrantes qualificados.
- Meta operacional do grupo até 05/06: 500 integrantes qualificados.
- Se o grupo estiver abaixo de 300, recomendar plano de compensação.
- Se o grupo estiver entre 300 e 500, tratar como cenário esperado, não como fracasso.
- Se o grupo passar de 500, tratar como cenário positivo, mas não abrir carrinho antes de 05/06 apenas por isso.

## Regra sem fechamento planejado

O assistente e qualquer agente do repositório devem considerar:

- Grupo de WhatsApp abre em 22/05/2026.
- Carrinho abre em 05/06/2026.
- Não existe fechamento planejado.
- Não existe fechamento automático por queda de vendas.
- Não usar escassez falsa.
- Não sugerir “fechar carrinho” como ação padrão.
- Se vendas caírem, recomendar otimização, prova, remarketing, recuperação de checkout e resposta a objeções.
- Só falar em fechamento se o usuário informar explicitamente uma decisão manual futura.

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

Não sobre-engenheirar. Manter pt-BR. Preservar coerência com a marca Mr.Saizen e com a abertura oficial via WhatsApp.
