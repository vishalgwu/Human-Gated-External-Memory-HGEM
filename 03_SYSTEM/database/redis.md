# Redis Setup

Redis stores the T3 ephemeral rolling context buffer.

Expected local settings:

```text
host: localhost
port: 6379
db: 0
```

T3 should hold only the last five turns for a session. Keys should use a session-scoped prefix, for example:

```text
hgem:t3:<session_id>
```

