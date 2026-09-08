"""Copia los ultimos mensajes de los canales del panel a discord/feed.json.

Lee los canales de config.json -> discordFeed.channels [{id, label}].
Requiere el secreto DISCORD_BOT_TOKEN (token de un bot dentro del servidor
con permiso de Ver canal + Leer historial; activa los intents privilegiados).
Sin secreto: avisa y no falla (para no ensuciar el historial de Actions).
"""
import datetime
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIMIT = 20


def fetch_messages(channel_id, token):
    req = urllib.request.Request(
        f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={LIMIT}",
        headers={
            "Authorization": f"Bot {token}",
            "User-Agent": "EVJO-Feed/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)


def clean_message(m):
    author = m.get("author", {}) or {}
    uid = author.get("id")
    avatar_hash = author.get("avatar")
    avatar = (
        f"https://cdn.discordapp.com/avatars/{uid}/{avatar_hash}.png?size=80"
        if uid and avatar_hash
        else ""
    )
    images = [
        a["url"]
        for a in (m.get("attachments") or [])
        if str(a.get("content_type") or "").startswith("image/") and a.get("url")
    ]
    # Los anuncios suelen venir solo como embeds: rescatar su texto e imagenes.
    embed_texts = []
    for e in (m.get("embeds") or []):
        for key in ("title", "description"):
            if e.get(key):
                embed_texts.append(str(e[key]))
        for media in (e.get("thumbnail") or {}, e.get("image") or {}):
            if media.get("url"):
                images.append(media["url"])
    content = (m.get("content") or "").strip()
    if embed_texts:
        content = (content + "\n\n" + "\n\n".join(embed_texts)).strip()
    return {
        "id": m.get("id"),
        "author": author.get("global_name") or author.get("username") or "?",
        "avatar": avatar,
        "bot": bool(author.get("bot")),
        "content": content,
        "timestamp": m.get("timestamp"),
        "images": images[:4],
    }


def main():
    token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        print("NOTICE: falta el secreto DISCORD_BOT_TOKEN; omito la sincronizacion.")
        return 0

    with open(os.path.join(ROOT, "config.json"), encoding="utf-8") as f:
        config = json.load(f)

    channels = [
        c
        for c in (config.get("discordFeed", {}).get("channels", []) or [])
        if str(c.get("id", "")).strip()
    ]

    out = {
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "channels": [],
    }
    for ch in channels:
        cid = str(ch["id"]).strip()
        try:
            messages = fetch_messages(cid, token)
        except Exception as err:  # noqa: BLE001 - seguimos con los demas canales
            print(f"WARN canal {cid}: {err}")
            continue
        cleaned = [clean_message(m) for m in messages]
        cleaned = [m for m in cleaned if m["content"].strip() or m["images"]]
        out["channels"].append(
            {"id": cid, "label": ch.get("label") or "Canal", "messages": cleaned}
        )

    feed_path = os.path.join(ROOT, "discord", "feed.json")
    os.makedirs(os.path.dirname(feed_path), exist_ok=True)
    previous = None
    if os.path.exists(feed_path):
        with open(feed_path, encoding="utf-8") as f:
            try:
                previous = json.load(f)
            except json.JSONDecodeError:
                previous = None

    prev_channels = (previous or {}).get("channels")
    if prev_channels == out["channels"]:
        print("Sin cambios en el feed.")
        return 0

    with open(feed_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    total = sum(len(c["messages"]) for c in out["channels"])
    print(f"Feed actualizado: {len(out['channels'])} canales, {total} mensajes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
