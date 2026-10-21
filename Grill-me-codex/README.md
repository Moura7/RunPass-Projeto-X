# grill-me-codex

Small Codex skills for better planning with `request_user_input`.

This is a tiny adaptation of the `grill-me` workflow for Codex.

The goal is simple: make Codex ask better planning questions before writing code, without forcing you into a heavier workflow like a full spec system.

## Why

I liked the original `grill-me` idea because it is short, practical, and does not lock me into a complex architecture.

But in Codex, I wanted two changes:

1. Ask 1–3 questions at a time instead of only one.
2. Use `request_user_input` so the questions appear in Codex’s native UI.

## Codex config

In my setup, I use the following config to enable the ask tool outside Plan Mode:

```toml
[features]
default_mode_request_user_input = true
```

## Notes

This is not meant to replace every planning workflow.

For me, it replaces most of the value I wanted from Plan Mode when I need Codex to challenge my idea before building.
