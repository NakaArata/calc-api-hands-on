# 非機能要件（non-requirements / non-functional requirements）

## 1. 実行環境（Azure）
- 実行基盤: Azure Functions
- プラン: Consumption Plan
- リージョン: Japan East（東日本）

## 2. 実装技術
- 開発言語: Python 3.11
- トリガー: HTTP Trigger

## 3. セキュリティ（POCとしての最適解）
### 3.1. 認証・認可
- 既定は Azure Functions の Function Key を利用する（`authLevel=function` 相当）。
  - 理由: POC での導入が軽く、Anonymous より安全。
  - 期待される利用方法: クエリ `code=<function_key>` を付与して呼び出す。

### 3.2. 通信
- HTTPS のみを前提とする（HTTP は利用しない/無効化できる場合は無効化する）。

### 3.3. 入力の取り扱い
- 受け取る値は `A`/`B` のみとし、数値以外は `400` で拒否する。
- 個人情報や機微情報は扱わない（想定しない）。

### 3.4. CORS
- ブラウザでの利用は「URL を直接開く（ナビゲーション）」を想定し、JavaScript からのクロスオリジン呼び出しは要件外。
- そのため CORS 設定は最小（必要になった時点で追加要件として扱う）。

## 4. 運用
- 監視: 不要（Application Insights 等の監視は要件外）
- ログ: 追加の運用要件が無い前提で、最小限（エラー時の簡易ログ）に留める。

## 5. 可用性・性能
- Consumption Plan の特性（コールドスタート、スケールアウト）を許容する。
- 目標値（SLA/SLO、レスポンスタイム、スループット）は POC のため定義しない。

## 6. 保守性
- API は 2 本（掛け算/割り算）に限定し、追加機能は要件追加がない限り行わない。

## 7. 非対象（明示的にやらないこと）
- 監視ダッシュボード/アラートの整備
- 認証基盤（Entra ID/OAuth 等）を用いた厳格な認証・認可
- API 管理（API Management）の導入
- DB など永続化
- レート制限/WAF 等の高度な防御（必要になった時点で追加検討）
