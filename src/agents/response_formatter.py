from typing import Any

from src.config.llm_settings import load_agent_runtime_settings


def _format_top_attackers(tool_result: dict[str, Any]) -> str:
    attackers = tool_result.get("result", [])

    lines = ["Os principais IPs suspeitos são:"]

    for index, item in enumerate(attackers[:5], start=1):
        lines.append(
            f"{index}. `{item.get('ip')}` — "
            f"risco {item.get('risk_level')}, "
            f"score {item.get('risk_score'):.2f}, "
            f"{item.get('total_requests')} requests e "
            f"{item.get('unique_invoice_ids')} invoices únicos."
        )

    lines.append(
        "\nTodos os principais IPs apresentam sinais compatíveis com enumeração IDOR: "
        "alto volume, grande diversidade de invoices e sequential_access_ratio elevado."
    )

    lines.append(
        "\nNenhuma ação foi executada. O sistema está em modo dry-run."
    )

    return "\n".join(lines)


def _format_attack_window(tool_result: dict[str, Any]) -> str:
    result = tool_result.get("result", {})

    return (
        "A atividade suspeita dos principais IPs ocorreu entre "
        f"`{result.get('first_seen')}` e `{result.get('last_seen')}`.\n\n"
        f"Nesse período foram observados `{result.get('total_attack_events')}` eventos, "
        f"envolvendo `{result.get('unique_invoices_accessed')}` invoices únicos, "
        f"`{result.get('unique_tokens_seen')}` tokens e "
        f"`{result.get('unique_attack_ips')}` IPs suspeitos.\n\n"
        "Isso sugere uma campanha prolongada e distribuída, não um evento isolado.\n\n"
        "Nenhuma ação foi executada. O sistema está em modo dry-run."
    )


def _format_idor_explanation(rag_context: dict[str, Any]) -> str:
    return (
        "IDOR, ou Insecure Direct Object Reference, é uma falha de Broken Access Control "
        "em que a aplicação expõe um identificador direto, como `invoice_id`, mas não valida "
        "corretamente se o usuário tem permissão para acessar aquele objeto.\n\n"
        "No dataset analisado, os sinais compatíveis são:\n"
        "- milhares de invoices únicos acessados por um mesmo IP;\n"
        "- acesso sequencial a IDs de invoices;\n"
        "- alto volume de requests;\n"
        "- convergência entre risk scoring, bot detection e anomaly detection.\n\n"
        "A recomendação é validar autorização server-side por invoice, aplicar rate limiting "
        "e manter ações de contenção em dry-run até aprovação humana."
    )


def _fallback_format_response(
    question: str,
    rag_context: dict[str, Any],
    tool_result: dict[str, Any] | None,
) -> str:
    normalized = question.lower()

    if tool_result and tool_result.get("status") == "ok":
        result = tool_result.get("result")

        if isinstance(result, list):
            return _format_top_attackers(tool_result)

        if isinstance(result, dict):
            return _format_attack_window(tool_result)

    if "idor" in normalized or "broken access" in normalized:
        return _format_idor_explanation(rag_context)

    if tool_result and tool_result.get("status") == "approval_required":
        return (
            "A ação solicitada exige aprovação humana antes de qualquer execução real.\n\n"
            "Como o sistema está em modo dry-run, nenhuma ação externa foi executada. "
            "O pedido foi tratado como simulação segura e registrado nos logs."
        )

    docs = rag_context.get("retrieved_documents", [])

    if docs:
        titles = ", ".join(
            doc.get("title", "documento")
            for doc in docs
        )

        return (
            "Encontrei contexto relevante na base RAG para apoiar a análise.\n\n"
            f"Documentos consultados: {titles}.\n\n"
            "A resposta foi gerada em modo determinístico, sem executar ações externas."
        )

    return (
        "Não encontrei uma tool específica ou contexto RAG suficiente para responder com precisão. "
        "Você pode perguntar sobre top IPs atacantes, janela do ataque, IDOR, IOCs ou contenção."
    )


def format_soc_response(
    *,
    question: str,
    rag_context: dict[str, Any],
    tool_result: dict[str, Any] | None,
) -> dict[str, Any]:
    settings = load_agent_runtime_settings()

    fallback_answer = _fallback_format_response(
        question=question,
        rag_context=rag_context,
        tool_result=tool_result,
    )

    if not settings.agents_use_llm:
        return {
            "answer": fallback_answer,
            "mode": "deterministic_natural_language",
            "used_llm": False,
    }

    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        return {
            "answer": fallback_answer,
            "mode": "llm_requested_but_dependency_missing",
            "used_llm": False,
        }

    if not settings.llm_api_key:
        return {
            "answer": fallback_answer,
            "mode": "llm_requested_but_api_key_missing",
            "used_llm": False,
        }

    llm_kwargs = {
        "model": settings.llm_model,
        "api_key": settings.llm_api_key,
        "temperature": 0,
    }

    if settings.llm_base_url:
        llm_kwargs["base_url"] = settings.llm_base_url

    llm = ChatOpenAI(
        **llm_kwargs
    )

    prompt = f"""
Você é um analista DFIR conversacional.

Responda em português, de forma clara, objetiva e investigativa.

Regras:
- Use apenas as evidências fornecidas.
- Não invente fatos.
- Separe fatos de inferências.
- Reforce que o sistema está em dry-run.
- Não diga que executou ações reais.

Pergunta:
{question}

Contexto RAG:
{rag_context}

Resultado de tool:
{tool_result}

Resposta base determinística:
{fallback_answer}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "mode": "llm_natural_language",
        "used_llm": True,
        "model": settings.llm_model,
    }