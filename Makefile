HOST ?= 0.0.0.0
PORT ?= 8000

run:
	uv run uvicorn app.main:app --reload --host ${HOST} --port ${PORT}

depends:
	uv sync