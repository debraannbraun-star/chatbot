Secrets and deployment notes

- Do NOT commit `.streamlit/secrets.toml` containing real secret values.
- Use the template file `.streamlit/secrets.toml.example` as a starting point.

Local setup

1. Copy the example to the real secrets file:

```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit `.streamlit/secrets.toml` and set real values
```

2. Export any environment variables needed during local development (optional):

```bash
export OPENAI_API_KEY="sk-..."
```

Streamlit Community Cloud

- When you deploy on https://share.streamlit.io you can add secrets in the app's "Secrets" section in the UI. These map to the same keys as in `.streamlit/secrets.toml`.
- Example: add `OPENAI_API_KEY` in the Secrets UI instead of committing it.

Best practices

- Keep secrets out of version control (add `.streamlit/secrets.toml` to `.gitignore` if not present).
- Use environment variables or cloud secret managers for production deployments.
