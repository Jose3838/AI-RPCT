# Provider Fallback Policy

If a real provider API fails:

1. Log the error.
2. Do not break the full pipeline.
3. Continue with other providers.
4. Mark provider as failed.
5. Never silently invent real data.

Placeholder data is allowed only for local development and must be clearly marked.
