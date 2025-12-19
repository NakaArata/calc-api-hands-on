# calc-api-hands-on

Azure Functions (Python 3.11) で動作する簡単な計算 API です。

## APIs
- `GET /mul?A=<number>&B=<number>`: `A * B`
- `GET /div?A=<number>&B=<number>`: `A / B`

成功時は `text/plain; charset=utf-8` で結果を返します。入力不正・ゼロ除算は `400` を返します。

## Local dev (tests)
```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements-dev.txt
pytest -q
```

## Notes
- デプロイ対象は `src/` を想定しています。
