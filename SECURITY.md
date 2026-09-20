# Security Policy

ChomView is primarily a prompt/Agent-Skill protocol. It should be treated as advisory logic, not as a security boundary.

## Important limitations

- The Second-Thought Peer is not a trusted verifier.
- `OK`, `LOOK_AGAIN`, and `WARNING` outputs may be wrong.
- Do not use ChomView as the sole authorization mechanism for destructive, privileged, financial, security-sensitive, or irreversible actions.
- Keep the peer read-only where practical.
- Never transmit secrets or credentials in BROTLI packets unless the surrounding runtime already authorizes that disclosure.

## Reporting a vulnerability

Please report security-sensitive issues privately through GitHub's security advisory mechanism when available rather than opening a public issue with exploit details.
