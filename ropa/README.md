# Probador 3D — Ropa EUP (YDD/YTD → GLB)

El navegador **no lee `.ydd` / `.ytd` directamente**.
El flujo es: conviertes cada prenda a `.glb` **una sola vez**, lo subes a esta carpeta
y la sección "Probador 3D" de la web lo muestra con visor 3D (`model-viewer`).

## 1. Convertir tu prenda a .glb (elige una vía)

Tienes por ejemplo:
```
D:\FiveM\...\camiseta1brazo_hombre\stream\mp_m_freemode_01_mp_m_camiseta1brazo_hombre\mp_m_...^jbib_000_u.ydd
D:\FiveM\...\camiseta1brazo_hombre\stream\mp_m_freemode_01_mp_m_camiseta1brazo_hombre\mp_m_...^jbib_diff_000_a_uni.ytd
```

**Vía A — CodeWalker + Blender (gratis, recomendada):**
1. Abre el `.ydd` en CodeWalker (model viewer) con su `.ytd` al lado para ver texturas.
2. Exporta a XML / importa en Blender con el addon Sollumz.
3. Exporta desde Blender como `camiseta1brazo_hombre.glb` (embed textures, +Y up).

**Vía B — gtax.dev (rápida):**
1. Entra a https://gtax.dev/preview/ydd, suelta tu `.ydd` + su `.ytd` y comprueba que se ve.
2. Convierte con su CLI/API `v-drawable-to-glb` (ver https://github.com/gtax-dev/v-drawable-to-glb):
   `v-drawable-to-glb -i tu.ydd -ytd tu.ytd -o camiseta1brazo_hombre.glb`
3. Revisa el `.glb` resultante antes de subirlo.

## 2. Subir a esta carpeta

Sube aquí (misma carpeta `ropa/`):
- `camiseta1brazo_hombre.glb` (modelo, ideal < 8 MB; comprime texturas a 1024px)
- Miniatura opcional: `camiseta1brazo_hombre.png` (800×800) o reutiliza una de `img/`

> No subas los `.ydd`/`.ytd` originales al repo salvo que quieras ofrecer descarga:
> pesan mucho e inflan el git. Si los quieres para descargar, pon enlaces externos
> o usa Git LFS.

## 3. Dar de alta en el catálogo

Edita `ropa/catalogo.json` y añade un objeto por prenda:

```json
{
  "id": "camiseta1brazo_hombre",
  "nombre": "Camiseta 1 Brazo (Hombre)",
  "categoria": "Camisetas",
  "descripcion": "EUP jbib masculino.",
  "glb": "ropa/camiseta1brazo_hombre.glb",
  "thumb": "ropa/camiseta1brazo_hombre.png",
  "ydd": "",
  "ytd": "",
  "precio": ""
}
```

- `glb`: ruta relativa al `.glb` (obligatorio para el 3D).
- `thumb`: imagen de la tarjeta (opcional; si falla se muestra icono 👕).
- `ydd` / `ytd`: enlaces de descarga opcionales (URL o vacíos).
- La web **no puede listar la carpeta sola** (GitHub Pages es estático):
  el `catalogo.json` es el manifiesto que la sección lee con `fetch`.

## 4. Probar en local

```powershell
cd evjostudios.github.io
python -m http.server 8000
# abre http://localhost:8000/ (sección "Probador 3D")
# abre http://localhost:8000/ropa/catalogo.json para verificar el JSON
```

Si el `.glb` aún no existe, la tarjeta muestra "GLB pendiente de convertir" y el
visor avisa en vez de romperse.
