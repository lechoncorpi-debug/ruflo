/* ============================================================
   CARGADOR DE PROPIEDADES
   Fuentes soportadas:
     1) Archivo local  : properties.json  (junto a index.html)
     2) GitHub raw     : https://raw.githubusercontent.com/USUARIO/REPO/main/properties.json
     3) Dropbox archivo: https://www.dropbox.com/scl/fi/xxxx/archivo.json?rlkey=...
                         -> host dl.dropboxusercontent.com (con CORS)
   Las CARPETAS de Dropbox NO se leen desde el navegador (CORS + tamaño):
   se sincronizan server-side con .github/workflows/sync-dropbox.yml.
   ============================================================ */
(function (global) {
  'use strict';

  /* ---------- Utilidades de Dropbox ---------- */

  // Convierte cualquier enlace compartido de Dropbox en enlace de descarga
  // directa compatible con CORS.
  // IMPORTANTE: www.dropbox.com NO envía cabeceras CORS (fetch desde el
  // navegador falla); el host de contenido dl.dropboxusercontent.com SÍ envía
  // Access-Control-Allow-Origin: *. Por eso sustituimos el host.
  function aEnlaceDirecto(url) {
    try {
      var u = new URL(url);
      if (u.hostname !== 'www.dropbox.com' && u.hostname !== 'dropbox.com') return url;
      u.hostname = 'dl.dropboxusercontent.com';
      u.searchParams.set('dl', '1');
      return u.toString();
    } catch (e) {
      return url;
    }
  }

  // ¿Es un enlace de CARPETA compartida de Dropbox?
  function esCarpetaDropbox(url) {
    try {
      var u = new URL(url);
      if (!u.hostname.endsWith('dropbox.com')) return false;
      return /^\/(scl\/fo|sh)\//.test(u.pathname);
    } catch (e) {
      return false;
    }
  }

  function esJson(url) {
    try {
      var p = new URL(url).pathname.toLowerCase();
      return p.endsWith('.json');
    } catch (e) {
      return /\.json(\?|$)/i.test(url);
    }
  }

  /* ---------- Normalización de una propiedad ---------- */

  function normalizar(crudo, nombreArchivo) {
    var p = Object.assign({}, crudo);
    if (!p.id) {
      p.id = (p.nombre || nombreArchivo || 'propiedad')
        .toString().toLowerCase()
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'propiedad';
    }
    p.nombre = p.nombre || 'Propiedad sin nombre';
    p.destino = p.destino || 'riviera-nayarit';
    p.fotos = Array.isArray(p.fotos) ? p.fotos.filter(Boolean) : [];
    if (p.foto && !p.fotos.length) p.fotos = [p.foto];
    p.amenidades = Array.isArray(p.amenidades) ? p.amenidades : [];
    p.etiquetas = Array.isArray(p.etiquetas) ? p.etiquetas : [];
    p.specs = Object.assign({ recamaras: null, banos: null, m2: null, terreno: null }, p.specs || {});
    // Enlaces de Dropbox -> descarga directa (para las fotos)
    p.fotos = p.fotos.map(function (f) {
      return /dropbox\.com/.test(f) ? aEnlaceDirecto(f) : f;
    });
    return p;
  }

  function extraerLista(obj) {
    if (Array.isArray(obj)) return obj;
    if (obj && Array.isArray(obj.propiedades)) return obj.propiedades;
    if (obj && typeof obj === 'object') return [obj];
    return [];
  }

  /* ---------- Carga principal ---------- */

  // fuente: { tipo:'auto'|'url'|'carpeta', url:'...' }
  // 'auto' prueba en cascada: properties.json local y luego fuente.url.
  // Devuelve el primer resultado CON propiedades; si ninguno tiene,
  // devuelve el último resultado (para mostrar su diagnóstico).
  async function cargar(fuente) {
    fuente = fuente || {};
    var candidatas = [];

    if (fuente.tipo === 'url' || fuente.tipo === 'carpeta') {
      candidatas.push(fuente.url);
    } else {
      if (location.protocol === 'http:' || location.protocol === 'https:') {
        candidatas.push('properties.json');
      }
      if (fuente.url) candidatas.push(fuente.url);
    }

    var ultimo = null;
    for (var i = 0; i < candidatas.length; i++) {
      var url = candidatas[i];
      if (!url) continue;
      try {
        var resultado = await cargarUno(url);
        resultado.fuente = url;
        if (resultado.propiedades && resultado.propiedades.length) return resultado;
        ultimo = resultado;
      } catch (e) {
        ultimo = {
          propiedades: [],
          fuente: url,
          origen: null,
          error: e && e.message ? e.message : String(e)
        };
      }
    }

    if (ultimo) return ultimo;
    return {
      propiedades: [],
      fuente: null,
      origen: 'ninguna',
      error: null,
      nota: 'Configura FUENTE_PROPIEDADES en index.html o crea properties.json.'
    };
  }

  async function cargarUno(url) {
    // --- Carpeta de Dropbox: imposible desde el navegador ---
    // Verificado contra Dropbox real: www.dropbox.com no envía cabeceras CORS,
    // el host de contenido da 404 a carpetas y una carpeta de material puede
    // pesar varios GB. Las carpetas las sincroniza el workflow de GitHub
    // (scripts/sync-dropbox.mjs); el navegador solo lee el manifest .json.
    if (esCarpetaDropbox(url)) {
      throw new Error(
        'El enlace es de una CARPETA de Dropbox: el navegador no puede leerla ' +
        'directamente (Dropbox lo bloquea por CORS) y puede pesar varios GB. ' +
        'Dos soluciones: 1) genera properties.json con admin.html, guárdalo en esa ' +
        'carpeta, comparte SOLO ese archivo ("Cualquier persona con el enlace") y pega ' +
        'ese enlace en fuente.url; 2) sincroniza la carpeta completa a GitHub con el ' +
        'workflow incluido (README, sección 3).'
      );
    }

    // --- JSON suelto (local, GitHub raw o Dropbox) ---
    var final = /dropbox\.com/.test(url) ? aEnlaceDirecto(url) : url;
    if (location.protocol === 'http:' || location.protocol === 'https:') {
      final += (final.indexOf('?') >= 0 ? '&' : '?') + 't=' + Date.now();
    }
    var res = await fetch(final, { cache: 'no-store' });
    if (!res.ok) throw new Error('No se pudo leer ' + url + ' (HTTP ' + res.status + ').');
    var texto = await res.text();
    var dato;
    try {
      dato = JSON.parse(texto);
    } catch (e) {
      throw new Error('El JSON de ' + url + ' tiene un error de formato.');
    }
    var lista = extraerLista(dato).map(function (p, i) { return normalizar(p, 'propiedad-' + (i + 1)); });
    var origen = /raw\.githubusercontent/.test(url) ? 'GitHub'
      : /dropbox\.com/.test(url) ? 'Dropbox'
      : 'Archivo local';
    return { propiedades: ordenar(lista), origen: origen };
  }

  function ordenar(lista) {
    return lista.slice().sort(function (a, b) {
      var oa = Number(a.orden || 999), ob = Number(b.orden || 999);
      if (oa !== ob) return oa - ob;
      return (a.nombre || '').localeCompare(b.nombre || '');
    });
  }

  global.Cargador = {
    cargar: cargar,
    aEnlaceDirecto: aEnlaceDirecto,
    esCarpetaDropbox: esCarpetaDropbox,
    normalizar: normalizar
  };
})(window);
