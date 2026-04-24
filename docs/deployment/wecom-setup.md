# WeCom Setup

## Purpose

This document defines the v1 WeCom setup for `Intellectual Tutor`.

The supported integration mode is:

- official Hermes `WeCom Callback (Self-Built App)`

This repo does not implement a custom WeCom gateway.

## Integration Mode

Use the official Hermes callback adapter instead of a community bridge or custom webhook service.

Why:

- It is first-party Hermes functionality.
- It matches the PRD.
- It supports self-built enterprise apps.
- It keeps messaging and agent execution in one runtime.

## Official Flow

The official Hermes WeCom callback flow is:

1. Register a self-built app in WeCom
2. WeCom pushes encrypted XML to the Hermes callback endpoint
3. Hermes decrypts and queues the message
4. Hermes acknowledges immediately
5. The agent runs
6. Hermes sends the reply proactively with `message/send`

## Required WeCom Values

Collect these values from the WeCom admin console:

- `Corp ID`
- `Corp Secret`
- `Agent ID`
- `Token`
- `EncodingAESKey`

## Required Hermes Environment Variables

Store these in `$HERMES_HOME/.env`:

```env
WECOM_CALLBACK_CORP_ID=your-corp-id
WECOM_CALLBACK_CORP_SECRET=your-corp-secret
WECOM_CALLBACK_AGENT_ID=1000002
WECOM_CALLBACK_TOKEN=your-callback-token
WECOM_CALLBACK_ENCODING_AES_KEY=your-43-char-aes-key
```

Optional:

```env
WECOM_CALLBACK_HOST=0.0.0.0
WECOM_CALLBACK_PORT=8645
WECOM_CALLBACK_ALLOWED_USERS=user1,user2
```

## Callback Endpoint

Official default callback path:

```text
/wecom/callback
```

Typical callback URL:

```text
http://YOUR_PUBLIC_IP:8645/wecom/callback
```

If the current machine is not directly reachable from WeCom, use a tunnel during testing.

## Recommended v1 Constraints

For v1, keep the integration narrow:

- one WeCom app
- one subject entry
- one course-focused Hermes instance
- an explicit user allowlist during bring-up

Recommended setting during early testing:

```env
WECOM_CALLBACK_ALLOWED_USERS=your_wecom_userid
```

## Runtime Expectations

The callback model has some platform constraints:

- no streaming replies
- no typing indicators
- text input only in the current adapter
- long-running tasks may take minutes before reply delivery

Because of that, the course app must keep these message stages explicit:

- accepted
- running
- waiting for confirmation
- completed
- blocked

## Verification Checklist

- WeCom callback URL verification succeeds
- `hermes gateway start` binds the configured callback port
- a test text message reaches the Hermes instance
- the correct dedicated course instance handles the message
- replies return to the same WeCom user

## Security Notes

- Keep all WeCom secrets in `$HERMES_HOME/.env`
- Do not commit secrets into this repo
- Start with `WECOM_CALLBACK_ALLOWED_USERS`
- Expand to broader access only after e2e validation
