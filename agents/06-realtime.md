# Agent: Real-Time & Live Experience

## Mission
Build the real-time infrastructure that makes CrowdForge feel alive. Every page should have something moving. The Live Pulse, Forge Stream, spectator mode, and real-time collaboration are what differentiate this from a static project management tool. This is the "Twitch Plays Pokemon" energy layer.

## What to Build

### Live Pulse
Persistent, minimizable activity stream on every page (bottom-right corner):
- Real-time events via WebSocket: pitches, merges, deploys, revenue events, karma awards
- Filterable: projects I follow / all / trending
- Events batched at 100ms intervals to prevent UI thrashing

### Forge Stream
Cinema-mode full-screen spectator view of a project being built:
- Center: live code editor view showing latest changes (30-second batch delay)
- Left sidebar: scrolling activity log
- Right sidebar: contributor chat
- Bottom: project health bar (tasks remaining, contributors active, time since last commit)
- Ambient sound design that intensifies with activity

### Spectator Mode
Per-project read-only real-time view:
- Live code diffs, task board updates, staging preview updates
- Contributor presence indicators (who's currently active)
- Emoji reactions on activity items
- Convert to contributor at any time

### Real-Time Collaboration
- Collaborative editing in the Forge (CRDT-based via Yjs)
- Live presence (see who's editing what file)
- Real-time task board (claim/release/complete visible instantly)
- Vote counts animating in real-time on Idea Ring

## Architecture
- Redis pub/sub for event distribution
- WebSocket server (Socket.io) for client connections
- Event producers: every action publishes to Redis channels
- Event router: fans out events to relevant WebSocket connections
- Client subscriptions: per-project, per-user, global channels

## Reference Docs
- `../docs/architecture/design.md` — real-time architecture section, Forge architecture, magic moments
- `../docs/vision.md` — "alive by default" principle

## Constraints
- Latency: events must reach spectators within 500ms of occurrence
- Scale: must handle 1,000+ concurrent spectators per project
- Graceful degradation: if WebSocket drops, the page still works (just not live)
- Mobile: pulse and spectator mode must work on mobile browsers
