# Feishu Setup

## Purpose

This document defines the v1 Feishu/Lark setup for `Intellectual Tutor`.

The supported integration mode is:

- official Hermes `Feishu / Lark` adapter in `websocket` mode

This repo does not implement a custom Feishu gateway.

## Integration Mode

Use the official Hermes Feishu/Lark adapter instead of a community bridge or custom webhook service.

Why:

- It is first-party Hermes functionality.
- It matches the PRD.
- It supports Hermes `gateway setup` scan-based bot creation.
- It keeps messaging and agent execution in one runtime.

## Official Flow

The official Hermes Feishu bring-up flow is:

1. Run `hermes gateway setup`
2. Choose `Feishu / Lark`
3. Scan the QR code and authorize bot creation
4. Hermes stores the app credentials locally
5. Hermes uses `websocket` mode to receive inbound messages
5. The agent runs
6. Hermes replies on the same Feishu channel

## Preferred Setup Path

Use the official setup wizard when possible:

```bash
hermes gateway setup
```

This is the preferred path because Hermes can create the bot application and persist the credentials for you.

## Manual Credentials

If you need manual configuration instead of the setup wizard, collect these values:

- `App ID`
- `App Secret`
- optional allowlisted user IDs for bring-up
- optional home-channel chat ID for notifications

## Required Hermes Environment Variables

Store these in `$HERMES_HOME/.env`:

```env
FEISHU_APP_ID=your-app-id
FEISHU_APP_SECRET=your-app-secret
```

Optional:

```env
FEISHU_ALLOWED_USERS=user1,user2
FEISHU_HOME_CHANNEL=chat_id
FEISHU_DOMAIN=feishu
FEISHU_CONNECTION_MODE=websocket
```

## Config Template

If you prefer `config.yaml` instead of environment variables, use `platforms.feishu.extra`:

```yaml
platforms:
  feishu:
    enabled: true
    extra:
      domain: "feishu"
      connection_mode: "websocket"
      # Prefer `hermes gateway setup` and keep secrets in $HERMES_HOME/.env:
      # app_id: "cli_a1b2c3"
      # app_secret: "secret"
```

This follows the official Hermes Feishu adapter in `websocket` mode and does not require a public callback path.

## Recommended v1 Constraints

For v1, keep the integration narrow:

- one Feishu bot application
- one subject entry
- one course-focused Hermes instance
- an explicit user allowlist during bring-up

Recommended setting during early testing:

```env
FEISHU_ALLOWED_USERS=your_feishu_user_id
```

## Runtime Expectations

The Feishu websocket model has these bring-up expectations:

- no public endpoint is required
- WebSocket connectivity must succeed from the Hermes runtime
- access policy should stay narrow during first bring-up
- long-running tasks may still take minutes before final reply delivery

Because of that, the course app must keep these message stages explicit:

- accepted
- running
- waiting for confirmation
- completed
- blocked

## Verification Checklist

- `hermes gateway setup` completes and persists the Feishu credentials
- `hermes gateway` or `hermes gateway start` authenticates successfully
- a test text message reaches the Hermes instance
- the correct dedicated course instance handles the message
- replies return to the same Feishu user or chat

## Security Notes

- Keep all Feishu secrets in `$HERMES_HOME/.env`
- Do not commit secrets into this repo
- Start with `FEISHU_ALLOWED_USERS`
- Expand to broader access only after e2e validation
