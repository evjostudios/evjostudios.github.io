# Feed de Discord — sin hosting

Un workflow de GitHub Actions (`.github/workflows/discord-feed.yml`) copia cada
~5 min las últimas publicaciones de tus canales a `discord/feed.json`, y la web
las muestra como tarjetas flotantes. No hay servidor que mantener.

## Ponerlo en marcha (solo se hace una vez)

1. **Crea el bot**: https://discord.com/developers → New Application → pestaña
   **Bot** → Reset Token y cópialo. Activa los 3 **Privileged Intents**.
2. **Invítalo a tu servidor** (OAuth2 → URL Generator → scopes `bot` +
   `applications.commands`, permiso mínimo: Ver canal + Leer historial...
   o Administrador para no pelearte) y abre la URL generada.
3. **Guarda el token en el repo**: GitHub → tu repo → Settings → Secrets and
   variables → **Actions** → New repository secret → nombre
   `DISCORD_BOT_TOKEN`, valor el token. Nadie lo ve, ni va en el código.
4. En el **panel de la web** (💬 Discord en vivo) pon tu Server ID y añade los
   canales (nombre de pestaña + ID) → **Publicar**.
5. Ve a la pestaña **Actions** del repo → *Discord feed* → **Run workflow**
   para la primera sincronización (si no, corre solo en ~10 min).

## Notas

- `feed.json` se genera solo; no lo edites a mano.
- Los canales se leen de `config.json` → `discordFeed.channels` (lo que pongas
  en el panel). El título de cada pestaña es su `label`.
- Sin secreto, el workflow avisa y no falla.
- Si un canal sale vacío: revisa que el bot pueda **verlo y leer su historial**.
