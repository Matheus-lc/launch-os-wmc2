from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
OPS_CSV = ROOT / "operations" / "cronograma-dia-a-dia.csv"


st.set_page_config(
    page_title="Launch OS WMC 2",
    page_icon="WMC2",
    layout="wide",
)


def read_text(path: Path) -> str:
    if not path.exists():
        return f"Arquivo não encontrado: {path}"
    return path.read_text(encoding="utf-8")


@st.cache_data(show_spinner=False)
def read_csv(path: str) -> pd.DataFrame:
    file_path = Path(path)
    if not file_path.exists():
        return pd.DataFrame()
    return pd.read_csv(file_path)


@st.cache_data(show_spinner=False)
def read_json(path: str):
    file_path = Path(path)
    if not file_path.exists():
        return [] if file_path.suffix == ".json" else {}
    return json.loads(file_path.read_text(encoding="utf-8"))


def save_schedule(df: pd.DataFrame) -> None:
    df.to_csv(OPS_CSV, index=False, encoding="utf-8")
    st.cache_data.clear()


def md_file_picker(label: str, folder: str, pattern: str = "*.md") -> Path | None:
    files = sorted((ROOT / folder).glob(pattern))
    if not files:
        st.info("Nenhum arquivo encontrado.")
        return None
    names = [f"{folder}/{file.name}" for file in files]
    selected = st.selectbox(label, names)
    return ROOT / selected


def metric_card(title: str, value: str, help_text: str = "") -> None:
    st.metric(title, value, help=help_text or None)


st.title("Launch OS WMC 2")
st.caption("Sistema operacional local para o lançamento do WMC 2, do Mr.Saizen.")

tabs = st.tabs(
    [
        "Hoje",
        "Calendário",
        "Conteúdo",
        "Métricas",
        "Checklists",
        "Compliance",
        "Assistente",
    ]
)

schedule = read_csv(str(OPS_CSV))

with tabs[0]:
    st.header("Hoje")

    selected_date = st.date_input("Data de trabalho", value=date.today())
    selected_iso = selected_date.isoformat()

    if schedule.empty:
        st.warning("Cronograma não encontrado.")
    else:
        day_tasks = schedule[schedule["date"] == selected_iso].copy()

        if day_tasks.empty:
            st.info("Não há tarefas para esta data. Mostrando as próximas tarefas pendentes.")
            day_tasks = schedule[schedule["status"].str.lower() != "concluído"].head(8).copy()

        st.subheader("Tarefas")
        editable = st.data_editor(
            day_tasks,
            width="stretch",
            hide_index=True,
            column_config={
                "status": st.column_config.SelectboxColumn(
                    "status",
                    options=["pendente", "em andamento", "concluído", "bloqueado"],
                    required=True,
                ),
                "priority": st.column_config.SelectboxColumn(
                    "priority",
                    options=["baixa", "média", "alta", "crítica"],
                ),
            },
        )

        if st.button("Salvar status no CSV", type="primary"):
            updated = schedule.copy()
            for idx, row in editable.iterrows():
                if idx in updated.index:
                    updated.loc[idx, :] = row
            save_schedule(updated)
            st.success("Cronograma atualizado em operations/cronograma-dia-a-dia.csv.")

    st.subheader("Prioridade operacional")
    st.markdown(read_text(ROOT / "docs" / "guia-de-uso-diario.md"))

with tabs[1]:
    st.header("Calendário")

    calendar_seed = read_json(str(ROOT / "data" / "seed_calendar.json"))
    if calendar_seed:
        st.dataframe(pd.DataFrame(calendar_seed), width="stretch", hide_index=True)

    if not schedule.empty:
        st.subheader("Cronograma completo")
        st.dataframe(schedule, width="stretch", hide_index=True)

    st.subheader("Plano detalhado")
    st.markdown(read_text(ROOT / "strategy" / "calendario-junho-2026.md"))

with tabs[2]:
    st.header("Conteúdo")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Plano e sequências")
        content_file = md_file_picker("Escolha um arquivo de conteúdo", "content")
        if content_file:
            st.markdown(read_text(content_file))

    with col2:
        st.subheader("Templates para copiar")
        template_file = md_file_picker("Escolha um template", "templates")
        if template_file:
            template_text = read_text(template_file)
            st.code(template_text, language="markdown")

with tabs[3]:
    st.header("Métricas")

    kpis = read_json(str(ROOT / "data" / "seed_kpis.json"))
    targets = kpis.get("targets", {}) if isinstance(kpis, dict) else {}

    cols = st.columns(4)
    if targets:
        cols[0].metric("Preço", "R$247")
        cols[1].metric("Meta realista", f"R${targets['realista']['faturamento']:,}".replace(",", "."))
        cols[2].metric("Vendas realistas", targets["realista"]["vendas"])
        cols[3].metric("Conversão grupo saudável", kpis["healthy_ranges"]["conversao_grupo"])

    metric_files = [
        "dashboard_base.csv",
        "metas.csv",
        "criativos.csv",
        "scorecard-page.csv",
        "scorecard-grupo.csv",
        "scorecard-ads.csv",
        "daily_log.csv",
    ]
    selected_metric = st.selectbox("Arquivo de métrica", metric_files)
    metric_df = read_csv(str(ROOT / "metrics" / selected_metric))
    st.dataframe(metric_df, width="stretch", hide_index=True)

    st.subheader("Dicionário")
    st.markdown(read_text(ROOT / "metrics" / "dicionario-de-metricas.md"))

with tabs[4]:
    st.header("Checklists")
    checklist_file = md_file_picker("Escolha um checklist", "operations", "checklist*.md")
    if checklist_file:
        st.markdown(read_text(checklist_file))

    st.subheader("Responsabilidades e rituais")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(read_text(ROOT / "operations" / "responsabilidades-da-equipe.md"))
    with col2:
        st.markdown(read_text(ROOT / "operations" / "rituais-diarios.md"))

with tabs[5]:
    st.header("Compliance")

    compliance_file = md_file_picker("Escolha um arquivo de compliance", "compliance")
    if compliance_file:
        st.markdown(read_text(compliance_file))

    faq = read_json(str(ROOT / "data" / "faq.json"))
    if faq:
        st.subheader("FAQ rápido")
        for item in faq:
            with st.expander(item["question"]):
                st.write(item["answer"])

with tabs[6]:
    st.header("Assistente")

    prompt = read_text(ROOT / "assistant" / "prompt-head-lancamento.md")
    commands = read_text(ROOT / "assistant" / "comandos-de-uso.md")

    st.subheader("Prompt mestre")
    st.code(prompt, language="markdown")

    st.subheader("Comandos úteis")
    st.markdown(commands)

    st.subheader("Montador de consulta")
    user_context = st.text_area(
        "Cole aqui o contexto para o assistente",
        placeholder="Exemplo: o grupo tem 820 pessoas, interação caiu para 4%, tivemos 12 vendas e muitas dúvidas sobre WMC1.",
        height=140,
    )
    if user_context:
        composed = f"{prompt}\n\nContexto atual:\n{user_context}\n\nResponda no formato obrigatório."
        st.code(composed, language="markdown")

    if os.getenv("OPENAI_API_KEY"):
        st.success("OPENAI_API_KEY detectada. Use o prompt acima em um cliente de chat ou conecte uma integração local se desejar.")
    else:
        st.info("Sem OPENAI_API_KEY. A aba funciona como área de prompt e cópia, sem chamada externa.")
