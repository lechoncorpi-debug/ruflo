# 🌿 Punta Mita Homes · Colección Privada

Sitio inmobiliario **biofílico** para propiedades de **Riviera Nayarit** y
**Riviera Maya**, con el perfil de Instagram
[@puntamita.homes](https://www.instagram.com/puntamita.homes) (by @soyjaimevaldes)
como contacto principal.

La colección **nace vacía** (cero propiedades precargadas) y tú las vas
agregando **una por una** desde un panel de administración, sin tocar código.
Los datos viven en un archivo `properties.json` que puedes guardar en una
**carpeta de Dropbox sincronizada con tu repositorio de GitHub**: el sitio la
lee en tiempo real.

```
puntamita-homes/
├── index.html              ← sitio público
├── admin.html              ← panel para capturar propiedades
├── properties.json         ← TU colección (hoy: 10 unidades reales de MAENA)
├── img/                    ← portadas optimizadas (~200 KB; originales en Dropbox)
├── css/estilo.css
├── js/cargador.js          ← lee local / GitHub / Dropbox (incluye .zip)
├── js/app.js               ← render del sitio
├── js/admin.js             ← lógica del panel
├── PROMPT-PROPIEDADES.md   ← prompt maestro para agregar propiedades con IA
├── README.md               ← este archivo
├── scripts/
│   ├── sync-dropbox.mjs    ← puente Dropbox → GitHub (workflow)
│   └── generar-maena.py    ← regenera properties.json desde el material MAENA
└── tests/                  ← pruebas unitarias + E2E (opcional)
```

## 1 · Ver el sitio

Súbelo a GitHub y actívalo con GitHub Pages (abajo, paso 4), o ábrelo con
cualquier servidor local:

```bash
cd puntamita-homes && node scripts/serve.mjs
# → http://localhost:3000
```

> Usa `serve.mjs`: es el único servidor local con soporte de **rangos HTTP**,
> que el navegador necesita para reproducir y adelantar el video de la obra.
> (`python3 -m http.server` también sirve el sitio, pero el video no se
> reproduce ahí.)
>
> Abrir `index.html` con doble clic funciona para ver el diseño, pero el
> navegador bloquea leer `properties.json` desde `file://`; por eso configura
> la fuente de Dropbox (paso 3) o usa un servidor.

## 2 · Agregar propiedades una por una

1. Abre **`admin.html`** (enlace «Admin» en el pie del sitio).
2. Llena el formulario y pulsa **«Agregar a la colección»**.
   Las fotos de Dropbox se convierten solas a enlace directo.
3. Pulsa **«Descargar properties.json»** y deja el archivo en tu carpeta de
   Dropbox. En unos segundos Dropbox lo sincroniza con GitHub y el sitio lo
   muestra.
4. Botón **«Prompt»** → copia un texto listo para pedirle a una IA (p. ej. a mí,
   en Arena.ai) que agregue la propiedad con fotos y descripción biofílica.

El borrador se guarda en el navegador; lo permanente siempre es
`properties.json`.

## 3 · Cómo viajan tus datos: Dropbox → GitHub → sitio

Tu carpeta real («Material de Ventas para Brokers») pesa ~3 GB de videos y PDFs.
Contra el Dropbox real verificamos tres cosas que definen el diseño:

1. `www.dropbox.com` **no envía cabeceras CORS** → el navegador no puede listar
   ni descargar carpetas.
2. El ZIP de carpeta **no acepta rangos** y pesa gigas → tampoco lectura parcial.
3. Los **archivos individuales** (`scl/fi`) sí se leen desde el navegador con
   `Access-Control-Allow-Origin: *` vía `dl.dropboxusercontent.com`.

Por eso el flujo es:

- **El dato** vive en un `properties.json` ligero (lo genera `admin.html`).
- **El material pesado** (fotos/videos) se queda en Dropbox y se enlaza
  archivo por archivo dentro del manifest. Nada de gigas en GitHub.
- **La carpeta completa** se sincroniza a GitHub *server-side* con el workflow
  incluido (ahí no hay CORS).
- **El video de avance de obra** vive optimizado en el repo
  (`video/maena-avance.webm` + `.mp4`, ~20 MB en total, con faststart para
  empezar a reproducir al instante); el original de 57 MB sigue en Dropbox.

### Opción A · Manifest en Dropbox (inmediata)
1. `admin.html` → captura la propiedad → **Descargar properties.json**.
2. Guárdalo dentro de tu carpeta de Dropbox.
3. Compártelo («Cualquier persona con el enlace») y pega ese enlace de archivo
   en `window.SITIO_CONFIG.fuente` → `{ tipo:'url', url:'…scl/fi…' }`.
   (El convertidor de `admin.html` te genera la línea lista.)

### Opción B · Sync automático carpeta → GitHub (recomendada para el repo)
1. Sube esta carpeta a un repo de GitHub y activa **Settings → Pages**.
2. **Settings → Secrets → Actions** → crea `DROPBOX_FOLDER_URL` con el enlace
   de tu carpeta (o `DROPBOX_FILE_URL` con el enlace del manifest).
3. **Actions → sync-dropbox → Run workflow** (también corre cada hora).
   El workflow descarga la carpeta en los servidores de GitHub, extrae los
   `.json`, y commitea `properties.json` + `properties/` al repo.
   Si la carpeta pesa >25 MB (la tuya ~3 GB), el script no la descarga: te pide
   el manifest con un mensaje claro.
4. El sitio en Pages lee su propio `properties.json` del repo: siempre actualizado.

> Si configuras solo el enlace de la carpeta en el sitio, verás un diagnóstico
> honesto explicando por qué el navegador no puede leerla y qué hacer.

## 4 · Contacto

En `index.html`, bloque `SITIO_CONFIG.contacto`, ya vienen del Instagram:
`@puntamita.homes`, `@soyjaimevaldes` y el nombre del agente.

**El perfil de Instagram no publica WhatsApp, teléfono ni correo**, por lo que
quedan marcados como pendientes (`whatsappPendiente:true`, etc.) y los botones
dirigen al DM de Instagram con el mensaje «PUNTA MITA». Cuando tengas el número
real:

```js
whatsapp: '+52 322 123 4567',   // con lada internacional
whatsappPendiente: false,
telefono: '+52 322 123 4567',
telefonoPendiente: false,
email: 'hola@puntamitahomes.com',
emailPendiente: false,
```

…y todos los botones de WhatsApp, el formulario y el botón flotante se activan
solos con mensaje prellenado.

## 5 · Esquema de una propiedad

```json
{
  "id": "casa-selva",
  "orden": 1,
  "nombre": "Casa Selva",
  "destino": "riviera-maya",
  "zona": "Aldea Zamá",
  "tipo": "Villa biofílica",
  "status": "preventa",
  "precio": 1850000,
  "entrega": "Dic 2027",
  "descripcionCorta": "Una frase para la tarjeta.",
  "descripcion": "Texto largo, tono biofílico.",
  "specs": { "recamaras": 4, "banos": 4.5, "m2": 420, "terreno": 600 },
  "amenidades": ["Alberca", "Jardín nativo"],
  "fotos": ["https://www.dropbox.com/scl/fi/XXXX/foto.jpg?rlkey=ZZZ&dl=1"]
}
```

Valores de `destino`: `riviera-nayarit`, `riviera-maya`, `puerto-vallarta`,
`tulum`. `status`: `nuevo`, `preventa`, `exclusiva`. `precio`: número o
`"a-consulta"`.

## 6 · Verificación

Corrido más reciente (Chromium real con Playwright + Node 20):
- 21 pruebas unitarias del cargador (host CORS de Dropbox, carpetas, errores 404/JSON roto, cascada de fuentes) ✔
- 26 pruebas E2E en Chromium, incluida lectura CORS real de Dropbox desde el navegador ✔

Para repetir:

```bash
cd tests
npm i && npx playwright install chromium   # primera vez
node unidad.cjs && node e2e.mjs
```

## 7 · Estado actual de la colección (2026-09-21)

Generada automáticamente desde TU carpeta de Dropbox (y corregida: la primera
lectura manual contó 10; el parser vivo cuenta 17 disponibles reales):

- `Lista de Precios/MAE_MPLJN26MSRII.pdf` → **17 unidades DISPONIBLES** con precio,
  m² y torre (las 38 SOLD se omitieron). `scripts/generar-maena.py` descarga y
  parsea el PDF en vivo: cuando Metric publique una lista nueva, el workflow
  actualiza el sitio solo.
- `Renders/{Exterior,Interior,Amenidades}` → fotos de cada tarjeta y galería.
- `Para compartir con clientes/*.pdf` → sección "Material de ventas" del modal.

Las portadas viven en `img/` (JPG ~200 KB generados con `scripts/generar-maena.py`);
los originales de 10-14 MB quedan en Dropbox como galería. Para Riviera Maya la
colección sigue vacía hasta que compartas material de ese destino.

## 8 · Dominio personalizado (puntamita.homes)

El repo ya incluye el archivo `CNAME` con `puntamita.homes` (convención de
GitHub Pages) y todas las URLs canónicas/OG apuntan a ese dominio. Para
conectarlo:

1. En tu registrador de dominio crea estos registros DNS:
   - `A  @  → 185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153`
   - `CNAME  www  →  <tu-usuario>.github.io`
2. En GitHub: *Settings → Pages → Custom domain* → escribe `puntamita.homes`
   y guarda; al validar DNS se activa HTTPS automático (puede tardar minutos).
3. Si tu dominio fuera otro, cambia el contenido de `CNAME` y busca-reemplaza
   `https://puntamita.homes` en `index.html`, `admin.html`, `robots.txt`,
   `sitemap.xml` y `llms.txt`.

## 9 · SEO y calidad técnica (checklist aplicado)

- **Meta descriptions, canonical y Open Graph/Twitter** en `index.html` y
  `admin.html` (admin con `noindex`); imagen de compartir `img/og-portada.jpg`
  (1200×630).
- **`404.html`** personalizada (GitHub Pages la sirve para rutas inexistentes).
- **`robots.txt`**, **`sitemap.xml`** y **`llms.txt`** en la raíz.
- **Datos estructurados JSON-LD**: `RealEstateAgent` (LocalBusiness),
  `WebSite`, `BreadcrumbList` y `VideoObject`.
- **Migas de pan** visibles dentro del modal de cada propiedad
  (Inicio › Colección › Destino › Torre).
- **Alt text** en todas las imágenes (estáticas y generadas por JS).
- **Un h1 por página** y encabezados únicos; **títulos de pestaña únicos**.
- **Favicon** SVG de hoja (data-URI, sin archivos binarios) y marca tipográfica
  «Punta Mita Homes» como logo principal.
- **Sin Vite/React/bundlers**: el JS es vanilla (~44 KB en total, sin
  sourcemaps en producción) → no hay bundles que reducir ni mapas que quitar.
- **Sin texto placeholder** visible: los avisos de «datos por completar»
  desaparecen solos cuando llenas `SITIO_CONFIG.contacto`.
- **Enlaces internos** verificados por las pruebas e2e (sin 404 ni errores de
  consola).
