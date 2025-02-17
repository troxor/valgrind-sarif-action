FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
	uv sync --frozen --no-install-project --no-dev

COPY vgxml-to-sarif.py .

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT [ "uv", "run", "/app/vgxml-to-sarif.py" ]
