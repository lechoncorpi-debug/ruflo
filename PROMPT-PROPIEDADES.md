# 🌿 Prompt maestro · Agregar propiedades una por una

Copia y pega este prompt en Arena.ai (o tu IA de confianza) cada vez que quieras
sumar una propiedad nueva a este sitio. Rellena los datos entre corchetes o
déjalos en blanco si no aplican. Si prefieres, usa el panel **admin.html** →
botón **«Prompt»**: genera este mismo texto con los datos ya capturados.

---

```
Actúa como el desarrollador del sitio "Punta Mita Homes · Colección Privada"
(carpeta: puntamita-homes/). Quiero AGREGAR UNA PROPIEDAD nueva a la colección.

Reglas:
1. Mantén intacto el diseño biofílico del sitio: verdes musgo y salvia, tipografía
   serif elegante, tono cálido y natural. NO cambies CSS ni estructura.
2. La propiedad vive en mi carpeta de Dropbox sincronizada con mi repositorio de
   GitHub. Edita SOLO el archivo de datos (properties.json) o crea un .json nuevo
   dentro de la carpeta, respetando el esquema exacto que ya existe.
3. No inventes información: si un dato está vacío, deja el campo vacío o el
   arreglo fotos en [] (el sitio muestra una ilustración botánica de respaldo).
4. Verifica que el JSON sea válido antes de terminar y confírmelo.

DATOS DE LA NUEVA PROPIEDAD:

- Nombre: [ej. Casa Destiladeras 12]
- Destino (riviera-nayarit | riviera-maya | puerto-vallarta | tulum): [destino]
- Zona / comunidad: [ej. Playa Destiladeras, Punta de Mita]
- Tipo: [Villa frente al mar | Departamento | Homesite | Residencia]
- Etiqueta (nuevo | preventa | exclusiva | vacía): [etiqueta]
- Precio USD (número, o "a-consulta"): [precio]
- Entrega: [Inmediata | Dic 2027 | …]
- Recámaras / baños / m² construcción / m² terreno: [n / n / n / n]
- Descripción corta (1 frase para la tarjeta): [frase]
- Descripción larga (2-4 frases, tono biofílico: luz, brisa, vegetación, mar): [texto]
- Amenidades (lista): [Alberca infinita, Acceso a playa, …]
- Fotos (enlaces de Dropbox o URLs, uno por línea):
  [https://www.dropbox.com/scl/fi/XXXX/foto1.jpg?rlkey=ZZZ]

Convierte los enlaces de fotos de Dropbox a descarga directa (añade dl=1).
Al terminar dime: 1) qué archivo quedó modificado, 2) el orden asignado,
3) qué comando ejecuto para subirlo a GitHub.
```

---

## Variante rápida (si ya llenaste admin.html)

Abre `admin.html`, captura la propiedad con el formulario y pulsa **«Prompt»**.
El portapapeles queda con este texto ya relleno: pégalo tal cual en la IA.

## Variante para mí (Arena.ai, esta conversación)

Basta con que me digas, en lenguaje natural, algo como:

> "Agrega a la colección: Casa X en Sayulita, 3 recámaras, 2.5 baños, 260 m²,
> USD 790,000, preventa, entrega inmediata, con alberca y jardín nativo.
> Fotos: [enlace de Dropbox]. Descríbela con tono biofílico."

Yo mismo edito `properties.json` (o el archivo individual dentro de tu carpeta
de Dropbox) y te confirmo el cambio.
