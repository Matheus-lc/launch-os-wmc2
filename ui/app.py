from __future__ import annotations

import base64
import json
import os
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
OPS_CSV = ROOT / "operations" / "cronograma-dia-a-dia.csv"
STYLE_PATH = ROOT / "ui" / "styles.css"
LOGO_PATH = ROOT / "ui" / "assets" / "saizen-squad-logo.png"
GROUP_OPEN_FALLBACK = date(2026, 5, 22)
CART_OPEN_FALLBACK = date(2026, 6, 5)
REALISTIC_GROUP_FALLBACK = 300
OPERATIONAL_GROUP_FALLBACK = 500


st.set_page_config(
    page_title="Launch OS WMC 2",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "WMC2",
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


def load_css() -> None:
    if STYLE_PATH.exists():
        st.markdown(f"<style>{STYLE_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def system_notice(message: str, tone: str = "neutral") -> None:
    st.markdown(f'<div class="system-notice notice-{tone}">{message}</div>', unsafe_allow_html=True)


def image_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def md_file_picker(label: str, folder: str, pattern: str = "*.md") -> Path | None:
    files = sorted((ROOT / folder).glob(pattern))
    if not files:
        system_notice("Nenhum arquivo encontrado.", "warning")
        return None
    names = [f"{folder}/{file.name}" for file in files]
    selected = st.selectbox(label, names)
    return ROOT / selected


def fmt_number(value) -> str:
    try:
        return f"{int(float(value)):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "0"


def fmt_money(value) -> str:
    try:
        return f"R${float(value):,.0f}".replace(",", ".")
    except (TypeError, ValueError):
        return "R$0"


def latest_row(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    return df.iloc[-1].to_dict()


def parse_date(value, fallback: date) -> date:
    if not value:
        return fallback
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return fallback


def int_seed(seed: dict, key: str, fallback: int) -> int:
    try:
        return int(seed.get(key, fallback))
    except (TypeError, ValueError, AttributeError):
        return fallback


def current_group_members(row: dict) -> int:
    try:
        return int(float(row.get("grupo_total", 0) or 0))
    except (TypeError, ValueError):
        return 0


def days_left_until_cart(as_of: date, cart_open: date) -> int:
    if as_of >= cart_open:
        return 1
    return max((cart_open - as_of).days, 1)


def daily_needed(current: int, target: int, as_of: date, cart_open: date) -> float:
    missing = max(target - current, 0)
    return missing / days_left_until_cart(as_of, cart_open)


def group_projection(current: int, as_of: date, group_open: date, cart_open: date) -> float:
    if as_of >= cart_open:
        return float(current)
    if as_of < group_open:
        elapsed = 1
        remaining = max((cart_open - group_open).days, 1)
    else:
        elapsed = max((as_of - group_open).days, 1)
        remaining = max((cart_open - as_of).days, 0)
    pace = current / elapsed if elapsed else 0
    return current + (pace * remaining)


def group_status(current: int, projection: float, realistic: int, operational: int) -> tuple[str, str]:
    if current >= operational:
        return "ACIMA DA META OPERACIONAL", "ok"
    if projection >= operational:
        return "CAMINHANDO PARA META OPERACIONAL", "ok"
    if current >= realistic or projection >= realistic:
        return "DENTRO DO CENÁRIO REALISTA", "warning"
    if projection < 200:
        return "ABAIXO DA PROJEÇÃO REALISTA", "critical"
    return "ABAIXO DA PROJEÇÃO REALISTA", "critical"


def projection_band(projection: float, realistic: int, operational: int) -> tuple[str, str]:
    if projection >= operational:
        return "VERDE · 500 OU MAIS", "ok"
    if projection >= realistic:
        return "AMARELO · entre 300 e 500", "warning"
    if projection < 200:
        return "CRÍTICO · abaixo de 200", "critical"
    return "VERMELHO · abaixo de 300", "critical"


def marker(label: str) -> None:
    st.markdown(f'<div class="protocol-marker">&gt;&gt;&gt; {label} &lt;&lt;&lt;</div>', unsafe_allow_html=True)


def badge(label: str, tone: str = "neutral") -> str:
    return f'<span class="badge badge-{tone}">{label}</span>'


def command_card(index: str, label: str, value: str, tone: str = "neutral", note: str = "") -> None:
    st.markdown(
        f"""
        <div class="command-card command-{tone}">
            <div class="card-index">{index}</div>
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="card-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, status: str = "OK", tone: str = "ok") -> None:
    st.markdown(
        f"""
        <div class="kpi-card kpi-{tone}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-status">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def quick_command(text: str) -> None:
    st.markdown(f'<div class="quick-command">[ {text} ]</div>', unsafe_allow_html=True)


def infer_gargalo(row: dict) -> tuple[str, str]:
    entradas = float(row.get("novas_entradas", 0) or 0)
    cpl = float(row.get("cpl_grupo", 0) or 0)
    cliques = float(row.get("cliques_checkout", 0) or 0)
    vendas = float(row.get("vendas", 0) or 0)

    if cliques > 50 and vendas == 0:
        return "CHECKOUT / OFERTA", "crítico"
    if cpl > 8:
        return "CAPTAÇÃO CARA", "crítico"
    if entradas < 20:
        return "ENTRADAS NO GRUPO", "atenção"
    return "SEM GARGALO CRÍTICO", "ok"


def metric_tone(metric: str, value) -> tuple[str, str]:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = 0

    if metric == "cpl":
        if numeric > 8:
            return "CRÍTICO", "critical"
        if numeric > 5:
            return "ATENÇÃO", "warning"
        return "OK", "ok"
    if metric == "vendas":
        if numeric == 0:
            return "ATENÇÃO", "warning"
        return "OK", "ok"
    if metric == "entradas":
        if numeric < 20:
            return "ATENÇÃO", "warning"
        return "OK", "ok"
    return "OK", "ok"


load_css()

schedule = read_csv(str(OPS_CSV))
dashboard = read_csv(str(ROOT / "metrics" / "dashboard_base.csv"))
latest_metrics = latest_row(dashboard)
kpis_seed = read_json(str(ROOT / "data" / "seed_kpis.json"))
if not isinstance(kpis_seed, dict):
    kpis_seed = {}
group_open_date = parse_date(kpis_seed.get("group_open_date"), GROUP_OPEN_FALLBACK)
cart_open_date = parse_date(kpis_seed.get("cart_open_date"), CART_OPEN_FALLBACK)
realistic_group_target = int_seed(kpis_seed, "group_members_realistic_target", REALISTIC_GROUP_FALLBACK)
operational_group_target = int_seed(kpis_seed, "group_members_operational_target", OPERATIONAL_GROUP_FALLBACK)
group_members_now = current_group_members(latest_metrics)
metrics_as_of = parse_date(latest_metrics.get("date"), date.today())
projected_group_members = group_projection(group_members_now, metrics_as_of, group_open_date, cart_open_date)
group_status_label, group_status_tone = group_status(
    group_members_now,
    projected_group_members,
    realistic_group_target,
    operational_group_target,
)
gargalo, gargalo_tone = infer_gargalo(latest_metrics)
logo_uri = image_data_uri(LOGO_PATH)
logo_html = f'<img class="hero-logo" src="{logo_uri}" alt="GH15 Approved Saizen Squad">' if logo_uri else ""

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=190)
    st.markdown(
        """
        <div class="sidebar-title">LAUNCH OS · WMC 2</div>
        <div class="sidebar-subtitle">Sistema operacional de lançamento do Método Saizen</div>
        <div class="sidebar-code">ID://WMC2-001</div>
        <div class="sidebar-rule"></div>
        <div class="sidebar-menu">
            <div>HOJE</div>
            <div>CALENDÁRIO</div>
            <div>CONTEÚDO</div>
            <div>MÉTRICAS</div>
            <div>CHECKLISTS</div>
            <div>COMPLIANCE</div>
            <div>ASSISTENTE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <section class="hero">
        <div>
            <div class="hero-kicker">MR.SAIZEN · PROTOCOLO DE LANÇAMENTO</div>
            <h1>LAUNCH OS · WMC 2</h1>
            <p>Sistema operacional de lançamento do Método Saizen. Nada entra por acaso.</p>
        </div>
        <div class="hero-side">
            {logo_html}
            <div class="hero-stamp">
                <span>ID://WMC2-001</span>
                <strong>PROTOCOLO · EXECUÇÃO</strong>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "HOJE",
        "CALENDÁRIO",
        "CONTEÚDO",
        "MÉTRICAS",
        "CHECKLISTS",
        "COMPLIANCE",
        "ASSISTENTE",
    ]
)

with tabs[0]:
    marker("PROTOCOLO · EXECUÇÃO")
    st.markdown('<div class="microcopy">O gargalo do dia precisa ser visível.</div>', unsafe_allow_html=True)

    selected_date = st.date_input("DATA DE TRABALHO", value=date.today())
    selected_iso = selected_date.isoformat()

    if schedule.empty:
        system_notice("Cronograma não encontrado.", "critical")
        day_tasks = pd.DataFrame()
    else:
        day_tasks = schedule[schedule["date"] == selected_iso].copy()
        if day_tasks.empty:
            system_notice("Sem tarefas datadas para hoje. Mostrando próximas pendências críticas do cronograma.", "warning")
            day_tasks = schedule[schedule["status"].str.lower() != "concluído"].head(8).copy()

    priority_task = "Revisar cronograma e escolher o gargalo do dia."
    next_action = "Atualizar status, publicar peça crítica e medir resposta."
    if not day_tasks.empty:
        sorted_tasks = day_tasks.sort_values(
            by="priority",
            key=lambda col: col.map({"crítica": 0, "alta": 1, "média": 2, "baixa": 3}).fillna(4),
        )
        priority_task = str(sorted_tasks.iloc[0].get("task", priority_task))
        next_action = str(sorted_tasks.iloc[0].get("notes", next_action)) or next_action

    col_a, col_b, col_c = st.columns([1.35, 1, 1])
    with col_a:
        command_card("01", "PRIORIDADE DO DIA", priority_task, "critical", "Sem achismo. Sem dogma. Sem planilha decorativa.")
    with col_b:
        command_card("02", "GARGALO ATUAL", gargalo, gargalo_tone, "Se não está medido, está sendo imaginado.")
    with col_c:
        command_card("03", "PRÓXIMA AÇÃO EM 2 HORAS", next_action, "warning", "Comando curto. Execução visível.")

    kpi_cols = st.columns(6)
    kpi_values = [
        ("ENTRADAS NO GRUPO", fmt_number(latest_metrics.get("novas_entradas", 0)), "entradas"),
        ("CPL", fmt_money(latest_metrics.get("cpl_grupo", 0)), "cpl"),
        ("VISITAS NA PÁGINA", fmt_number(latest_metrics.get("visitas_pagina_vendas", 0)), "neutral"),
        ("CHECKOUT INICIADO", fmt_number(latest_metrics.get("cliques_checkout", 0)), "neutral"),
        ("VENDAS", fmt_number(latest_metrics.get("vendas", 0)), "vendas"),
        ("RECEITA", fmt_money(latest_metrics.get("faturamento_bruto", 0)), "neutral"),
    ]
    for idx, (label, value, metric_key) in enumerate(kpi_values):
        with kpi_cols[idx]:
            status, tone = metric_tone(metric_key, latest_metrics.get("novas_entradas" if metric_key == "entradas" else "cpl_grupo" if metric_key == "cpl" else "vendas", 0))
            if metric_key == "neutral":
                status, tone = "CAMPO", "neutral"
            kpi_card(label, value, status, tone)

    marker("GRUPO · 300/500")
    st.markdown(
        f'<div class="microcopy">Status: {group_status_label}. Base lida em {metrics_as_of.isoformat()}.</div>',
        unsafe_allow_html=True,
    )
    group_cols = st.columns(2)
    with group_cols[0]:
        kpi_card(
            f"EXPECTATIVA REALISTA · {realistic_group_target}",
            f"{fmt_number(group_members_now)} / {fmt_number(realistic_group_target)}",
            "BASE",
            group_status_tone if group_members_now < realistic_group_target else "ok",
        )
        st.progress(min(group_members_now / realistic_group_target, 1.0))
    with group_cols[1]:
        kpi_card(
            f"META OPERACIONAL · {operational_group_target}",
            f"{fmt_number(group_members_now)} / {fmt_number(operational_group_target)}",
            "ESFORÇO",
            group_status_tone,
        )
        st.progress(min(group_members_now / operational_group_target, 1.0))

    marker("CHECKLIST · CRÍTICO")
    if not day_tasks.empty:
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

        if st.button("[ SALVAR STATUS NO CSV ]", type="primary"):
            updated = schedule.copy()
            for idx, row in editable.iterrows():
                if idx in updated.index:
                    updated.loc[idx, :] = row
            save_schedule(updated)
            system_notice("Cronograma atualizado em operations/cronograma-dia-a-dia.csv.", "ok")

    marker("ROTINA · OPERAÇÃO")
    st.markdown(read_text(ROOT / "docs" / "guia-de-uso-diario.md"))

with tabs[1]:
    marker("CALENDÁRIO · CAMPO")
    st.markdown('<div class="microcopy">Datas reais. Entregas visíveis. Sem operação imaginária.</div>', unsafe_allow_html=True)

    calendar_seed = read_json(str(ROOT / "data" / "seed_calendar.json"))
    if calendar_seed:
        st.dataframe(pd.DataFrame(calendar_seed), width="stretch", hide_index=True)

    if not schedule.empty:
        st.subheader("CRONOGRAMA COMPLETO")
        st.dataframe(schedule, width="stretch", hide_index=True)

    marker("PLANO · JUNHO 2026")
    st.markdown(read_text(ROOT / "strategy" / "calendario-junho-2026.md"))

with tabs[2]:
    marker("CONTEÚDO · PROTOCOLO")
    st.markdown('<div class="microcopy">Não é achismo. Não é dogma. Não é planilha pronta.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("PLANO E SEQUÊNCIAS")
        content_file = md_file_picker("ARQUIVO DE CONTEÚDO", "content")
        if content_file:
            st.markdown(read_text(content_file))

    with col2:
        st.subheader("TEMPLATES PARA COPIAR")
        template_file = md_file_picker("TEMPLATE OPERACIONAL", "templates")
        if template_file:
            template_text = read_text(template_file)
            st.code(template_text, language="markdown")

with tabs[3]:
    marker("MÉTRICAS · CAMPO")
    st.markdown('<div class="microcopy">Se não está medido, está sendo imaginado.</div>', unsafe_allow_html=True)

    price = int_seed(kpis_seed, "price", 247)
    band_label, band_tone = projection_band(projected_group_members, realistic_group_target, operational_group_target)
    missing_realistic = max(realistic_group_target - group_members_now, 0)
    missing_operational = max(operational_group_target - group_members_now, 0)
    needed_realistic = daily_needed(group_members_now, realistic_group_target, metrics_as_of, cart_open_date)
    needed_operational = daily_needed(group_members_now, operational_group_target, metrics_as_of, cart_open_date)

    marker("CAPTAÇÃO DO GRUPO")
    group_metric_cols = st.columns(4)
    with group_metric_cols[0]:
        kpi_card("INTEGRANTES ATUAIS", fmt_number(group_members_now), band_label, band_tone)
    with group_metric_cols[1]:
        kpi_card("EXPECTATIVA REALISTA", fmt_number(realistic_group_target), f"FALTAM {fmt_number(missing_realistic)}", "warning" if missing_realistic else "ok")
    with group_metric_cols[2]:
        kpi_card("META OPERACIONAL", fmt_number(operational_group_target), f"FALTAM {fmt_number(missing_operational)}", "warning" if missing_operational else "ok")
    with group_metric_cols[3]:
        kpi_card("PROJEÇÃO ATÉ 05/06", fmt_number(projected_group_members), band_label, band_tone)

    needed_cols = st.columns(4)
    with needed_cols[0]:
        kpi_card("MÉDIA P/ 300", f"{needed_realistic:.1f}/dia", "ATÉ 05/06", "ok" if needed_realistic <= 22 else "warning")
    with needed_cols[1]:
        kpi_card("MÉDIA P/ 500", f"{needed_operational:.1f}/dia", "ATÉ 05/06", "ok" if needed_operational <= 40 else "warning")
    with needed_cols[2]:
        kpi_card("PREÇO", fmt_money(price), "OFERTA", "neutral")
    with needed_cols[3]:
        healthy_ranges = kpis_seed.get("healthy_ranges", {}) if isinstance(kpis_seed, dict) else {}
        kpi_card("CONVERSÃO GRUPO", healthy_ranges.get("conversao_grupo", "8% a 12%"), "REFERÊNCIA", "neutral")

    st.markdown(
        """
        <div class="legend-row">
            <span class="legend legend-ok">OK</span>
            <span class="legend legend-warning">ATENÇÃO</span>
            <span class="legend legend-critical">CRÍTICO</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_files = [
        "dashboard_base.csv",
        "metas.csv",
        "criativos.csv",
        "scorecard-page.csv",
        "scorecard-grupo.csv",
        "scorecard-ads.csv",
        "daily_log.csv",
        "sales_velocity.csv",
        "open_close_decision_rules.csv",
    ]
    selected_metric = st.selectbox("ARQUIVO DE MÉTRICA", metric_files)
    metric_df = read_csv(str(ROOT / "metrics" / selected_metric))
    st.dataframe(metric_df, width="stretch", hide_index=True)

    marker("DICIONÁRIO · DECISÃO")
    st.markdown(read_text(ROOT / "metrics" / "dicionario-de-metricas.md"))

with tabs[4]:
    marker("CHECKLISTS · ABERTURA")
    st.markdown('<div class="microcopy">Checklist bom deixa a próxima ação impossível de ignorar.</div>', unsafe_allow_html=True)

    checklist_file = md_file_picker("CHECKLIST OPERACIONAL", "operations", "checklist*.md")
    if checklist_file:
        st.markdown(read_text(checklist_file))

    marker("EQUIPE · RITUAIS")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(read_text(ROOT / "operations" / "responsabilidades-da-equipe.md"))
    with col2:
        st.markdown(read_text(ROOT / "operations" / "rituais-diarios.md"))

with tabs[5]:
    marker("COMPLIANCE · RISCO")
    st.markdown(
        """
        <div class="risk-grid">
            <div class="risk-card">NÃO INVENTAR PROVA.</div>
            <div class="risk-card">NÃO PROMETER RESULTADO GARANTIDO.</div>
            <div class="risk-card">NÃO TRANSFORMAR MÉTODO EM MILAGRE.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    compliance_file = md_file_picker("ARQUIVO DE COMPLIANCE", "compliance")
    if compliance_file:
        st.markdown(read_text(compliance_file))

    faq = read_json(str(ROOT / "data" / "faq.json"))
    if faq:
        st.subheader("FAQ RÁPIDO")
        for item in faq:
            with st.expander(item["question"]):
                st.write(item["answer"])

with tabs[6]:
    marker("ASSISTENTE · HEAD DE LANÇAMENTO")
    st.markdown('<div class="microcopy">Sala de comando. Diagnóstico, decisão, próxima ação.</div>', unsafe_allow_html=True)

    prompt = read_text(ROOT / "assistant" / "prompt-head-lancamento.md")
    commands = read_text(ROOT / "assistant" / "comandos-de-uso.md")

    st.subheader("COMANDOS RÁPIDOS")
    cmd_cols = st.columns(3)
    commands_fast = [
        "O QUE FAZEMOS HOJE?",
        "REVISE ESTA COPY.",
        "ESTAMOS ABAIXO DA PROJEÇÃO DE 300. O QUE FAZER?",
        "ESTAMOS ENTRE 300 E 500. COMO SEGUIR?",
        "BATEMOS 500 ANTES DE 05/06. O QUE FAZER?",
        "COM ESSE TAMANHO DE GRUPO, QUAL CENÁRIO DE VENDAS É REALISTA?",
    ]
    for index, command in enumerate(commands_fast):
        with cmd_cols[index % 3]:
            quick_command(command)

    st.subheader("PROMPT MESTRE")
    st.code(prompt, language="markdown")

    st.subheader("COMANDOS DE USO")
    st.markdown(commands)

    st.subheader("MONTADOR DE CONSULTA")
    user_context = st.text_area(
        "COLE O CONTEXTO PARA O ASSISTENTE",
        placeholder="Exemplo: o grupo tem 280 pessoas, interação caiu para 4%, tivemos 12 vendas e muitas dúvidas sobre WMC1.",
        height=140,
    )
    if user_context:
        composed = f"{prompt}\n\nContexto atual:\n{user_context}\n\nResponda no formato obrigatório."
        st.code(composed, language="markdown")

    if os.getenv("OPENAI_API_KEY"):
        system_notice("OPENAI_API_KEY detectada. Use o prompt acima em um cliente de chat ou conecte uma integração local se desejar.", "ok")
    else:
        system_notice("Sem OPENAI_API_KEY. A aba funciona como área de prompt e cópia, sem chamada externa.", "neutral")
