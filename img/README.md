# Carpeta de imágenes — EVJO Store

Sube aquí tus imágenes (fondos, logos, partners, fondos de hero, etc.) para usarlas
en el panel SIN perder calidad y sin inflar `config.json`.

## Cómo subir (desde el navegador)
1. Entra a esta carpeta `img/` en GitHub.
2. **Add file → Upload files**.
3. Arrastra tus PNG/JPG (a resolución original).
4. **Commit changes**. En 1-2 min estarán publicadas.

## Cómo usarlas en el panel
En cualquier campo de imagen escribe la ruta relativa, por ejemplo:

```
img/fondo.png
img/logo.png
img/partners/topv.png
```

O la URL completa:

```
https://evjo.store/img/fondo.png
```

## Consejos de calidad / peso
- **Fondos**: JPG de ancho 1920–2560px (calidad ~80%). Pesan poco y se ven nítidos.
- **Logos / PNG con transparencia**: PNG. Para logos de partners, 200–400px de alto basta.
- **Miniaturas de scripts**: PNG cuadrado (ej. 800×800) ya con su borde.
- Evita subir imágenes de varios MB sin necesidad; comprime con squoosh.app o tinypng.com.
- **No** uses el botón "Subir" del panel para imágenes grandes (eso las mete en config.json y ralentiza la web). Usa esta carpeta y pega la ruta.
