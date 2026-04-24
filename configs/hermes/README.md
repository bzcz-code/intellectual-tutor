# Hermes Config Templates

This directory stores tracked templates for the dedicated `Intellectual Tutor` Hermes instance.

These files are not the live Hermes home.

Live runtime files belong under:

```text
$HERMES_HOME/
```

Typical usage:

- copy `SOUL.template.md` to `$HERMES_HOME/SOUL.md`
- merge `config.template.yaml` into `$HERMES_HOME/config.yaml`
- copy `env.template` to `$HERMES_HOME/.env` and fill secrets locally
- copy `inference_policy.template.yaml` to `$HERMES_HOME/intellectual_tutor_inference_policy.yaml`

The tracked inference-policy template records which request classes may use the local
`Ollama + gemma4` lane and where local-miss fallback logs should be written.
