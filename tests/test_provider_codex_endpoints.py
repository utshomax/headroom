from headroom.providers.codex.endpoints import (
    chatgpt_backend_url,
    codex_backend_url,
    codex_backend_ws_url,
)


def test_chatgpt_backend_url_appends_optional_query() -> None:
    assert chatgpt_backend_url("/backend-api/me") == "https://chatgpt.com/backend-api/me"
    assert (
        chatgpt_backend_url("/backend-api/me", "client_version=1")
        == "https://chatgpt.com/backend-api/me?client_version=1"
    )


def test_codex_backend_url_normalizes_path_prefix() -> None:
    assert codex_backend_url("models") == "https://chatgpt.com/backend-api/codex/models"
    assert (
        codex_backend_url("/responses/compact", "trace=1")
        == "https://chatgpt.com/backend-api/codex/responses/compact?trace=1"
    )


def test_codex_backend_ws_url_normalizes_path_prefix() -> None:
    assert codex_backend_ws_url() == "wss://chatgpt.com/backend-api/codex"
    assert codex_backend_ws_url("responses") == "wss://chatgpt.com/backend-api/codex/responses"
    assert codex_backend_ws_url("/responses") == "wss://chatgpt.com/backend-api/codex/responses"


def test_chatgpt_target_api_url_moves_http_and_websocket_urls(monkeypatch) -> None:
    import importlib

    from headroom.providers.codex import endpoints

    monkeypatch.setenv("CHATGPT_TARGET_API_URL", "http://127.0.0.1:8095/chatgpt_passthrough/")
    try:
        importlib.reload(endpoints)
        assert endpoints.codex_backend_url("responses") == (
            "http://127.0.0.1:8095/chatgpt_passthrough/backend-api/codex/responses"
        )
        assert endpoints.codex_backend_ws_url("responses") == (
            "ws://127.0.0.1:8095/chatgpt_passthrough/backend-api/codex/responses"
        )
        monkeypatch.setenv("CHATGPT_TARGET_API_URL", "https://gw.example")
        importlib.reload(endpoints)
        assert endpoints.codex_backend_ws_url() == "wss://gw.example/backend-api/codex"
    finally:
        monkeypatch.delenv("CHATGPT_TARGET_API_URL")
        importlib.reload(endpoints)
    assert endpoints.codex_backend_url("models") == "https://chatgpt.com/backend-api/codex/models"
