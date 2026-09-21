/* ============================================================
   ADMIN · Punta Mita Homes
   Captura propiedades una por una y genera properties.json
   ============================================================ */
(function () {
  'use strict';

  var CLAVE = 'pmh_borrador_v1';
  var $ = function (s) { return document.querySelector(s); };

  var CAMPOS = {
    nombre: '#p-nombre', orden: '#p-orden', destino: '#p-destino', zona: '#p-zona',
    tipo: '#p-tipo', status: '#p-status', precio: '#p-precio', entrega: '#p-entrega',
    recamaras: '#p-recamaras', banos: '#p-banos', m2: '#p-m2', terreno: '#p-terreno',
    corta: '#p-corta', larga: '#p-larga', amenidades: '#p-amenidades', fotos: '#p-fotos', material: '#p-material'
  };

  var lista = [];
  var editando = null;

  /* ---------- Persistencia ---------- */
  function guardar() {
    try { localStorage.setItem(CLAVE, JSON.stringify(lista)); } catch (e) { /* modo privado */ }
  }
  function leer() {
    try {
      var raw = localStorage.getItem(CLAVE);
      lista = raw ? JSON.parse(raw) : [];
    } catch (e) { lista = []; }
  }

  /* ---------- Lectura del formulario ---------- */
  function num(v) { var n = parseFloat(v); return isFinite(n) ? n : null; }
  function lineas(v) {
    return String(v || '').split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
  }

  function leerFormulario() {
    var precioRaw = $(CAMPOS.precio).value.trim();
    var precio = precioRaw.toLowerCase().indexOf('consulta') >= 0 ? 'a-consulta' : num(precioRaw);

    var fotos = lineas($(CAMPOS.fotos).value).map(function (u) {
      return /dropbox\.com/.test(u) ? window.Cargador.aEnlaceDirecto(u) : u;
    });

    var material = lineas($(CAMPOS.material).value).map(function (l) {
      var partes = l.split('::');
      var url = (partes[1] || partes[0]).trim();
      return {
        nombre: (partes[1] ? partes[0] : 'Material').trim(),
        url: /dropbox\.com/.test(url) ? window.Cargador.aEnlaceDirecto(url) : url
      };
    }).filter(function (m) { return m.url; });

    var p = {
      id: '',
      orden: num($(CAMPOS.orden).value) || (lista.length + 1),
      nombre: $(CAMPOS.nombre).value.trim(),
      destino: $(CAMPOS.destino).value,
      zona: $(CAMPOS.zona).value.trim(),
      tipo: $(CAMPOS.tipo).value.trim(),
      status: $(CAMPOS.status).value,
      precio: precio,
      entrega: $(CAMPOS.entrega).value.trim(),
      descripcionCorta: $(CAMPOS.corta).value.trim(),
      descripcion: $(CAMPOS.larga).value.trim(),
      specs: {
        recamaras: num($(CAMPOS.recamaras).value),
        banos: num($(CAMPOS.banos).value),
        m2: num($(CAMPOS.m2).value),
        terreno: num($(CAMPOS.terreno).value)
      },
      amenidades: lineas($(CAMPOS.amenidades).value),
      fotos: fotos,
      material: material
    };
    if (!p.material.length) delete p.material;
    p.id = slug(p.nombre || ('propiedad-' + p.orden));
    return p;
  }

  function slug(t) {
    return String(t).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  }

  function limpiarCampos() {
    Object.keys(CAMPOS).forEach(function (k) {
      var el = $(CAMPOS[k]);
      if (!el) return;
      if (el.tagName === 'SELECT') el.selectedIndex = 0;
      else el.value = '';
    });
    $(CAMPOS.orden).value = lista.length + 1;
  }

  function llenarFormulario(p) {
    limpiarCampos();
    $(CAMPOS.nombre).value = p.nombre || '';
    $(CAMPOS.orden).value = p.orden || '';
    $(CAMPOS.destino).value = p.destino || 'riviera-nayarit';
    $(CAMPOS.zona).value = p.zona || '';
    $(CAMPOS.tipo).value = p.tipo || '';
    $(CAMPOS.status).value = p.status || '';
    $(CAMPOS.precio).value = p.precio == null ? '' : p.precio;
    $(CAMPOS.entrega).value = p.entrega || '';
    $(CAMPOS.recamaras).value = p.specs.recamaras == null ? '' : p.specs.recamaras;
    $(CAMPOS.banos).value = p.specs.banos == null ? '' : p.specs.banos;
    $(CAMPOS.m2).value = p.specs.m2 == null ? '' : p.specs.m2;
    $(CAMPOS.terreno).value = p.specs.terreno == null ? '' : p.specs.terreno;
    $(CAMPOS.corta).value = p.descripcionCorta || '';
    $(CAMPOS.larga).value = p.descripcion || '';
    $(CAMPOS.amenidades).value = (p.amenidades || []).join('\n');
    $(CAMPOS.fotos).value = (p.fotos || []).join('\n');
    $(CAMPOS.material).value = (p.material || []).map(function (m) { return m.nombre + ' :: ' + m.url; }).join('\n');
  }

  function aviso(msg, ok) {
    var el = $('#aviso-form');
    el.hidden = false;
    el.textContent = msg;
    el.style.background = ok ? 'rgba(76,154,106,.14)' : 'rgba(220,124,87,.14)';
    el.style.borderLeftColor = ok ? '#4C9A6A' : '#DC7C57';
    clearTimeout(aviso._t);
    aviso._t = setTimeout(function () { el.hidden = true; }, 4200);
  }

  /* ---------- Render ---------- */
  var DESTINOS = {
    'riviera-nayarit': 'Riviera Nayarit', 'riviera-maya': 'Riviera Maya',
    'puerto-vallarta': 'Puerto Vallarta', 'tulum': 'Tulum'
  };

  function pintar() {
    var ul = $('#lista');
    $('#conteo').textContent = lista.length ? '(' + lista.length + ')' : '(vacía)';

    if (!lista.length) {
      ul.innerHTML = '<li style="justify-content:flex-start;color:#6A7C71">Aún no hay propiedades. Agrega la primera con el formulario.</li>';
    } else {
      ul.innerHTML = lista.map(function (p, i) {
        return '<li>' +
          '<div><b>' + i + 1 + '. ' + esc(p.nombre) + '</b>' +
          '<small>' + esc(DESTINOS[p.destino] || p.destino) + (p.zona ? ' · ' + esc(p.zona) : '') +
          (p.precio ? ' · ' + esc(typeof p.precio === 'number' ? 'USD ' + p.precio.toLocaleString('en-US') : 'A consulta') : '') + '</small></div>' +
          '<div style="display:flex;gap:.4rem">' +
          '<button class="boton-mini" data-editar="' + esc(p.id) + '" style="color:#245336;border-color:rgba(36,83,54,.4)">Editar</button>' +
          '<button class="boton-mini" data-prompt="' + esc(p.id) + '" style="color:#245336;border-color:rgba(36,83,54,.4)">Prompt</button>' +
          '<button class="boton-mini peligro" data-borrar="' + esc(p.id) + '">Borrar</button>' +
          '</div></li>';
      }).join('');

      ul.querySelectorAll('[data-editar]').forEach(function (b) {
        b.addEventListener('click', function () {
          var p = porId(b.getAttribute('data-editar'));
          if (p) { editando = p.id; llenarFormulario(p); aviso('Editando «' + p.nombre + '». Pulsa Guardar cambios.', true); }
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
      });
      ul.querySelectorAll('[data-borrar]').forEach(function (b) {
        b.addEventListener('click', function () {
          var id = b.getAttribute('data-borrar');
          var p = porId(id);
          if (p && confirm('¿Borrar «' + p.nombre + '» del borrador?')) {
            lista = lista.filter(function (x) { return x.id !== id; });
            guardar(); pintar();
          }
        });
      });
      ul.querySelectorAll('[data-prompt]').forEach(function (b) {
        b.addEventListener('click', function () {
          var p = porId(b.getAttribute('data-prompt'));
          if (p) copiar(promptDe(p), 'Prompt de «' + p.nombre + '» copiado.');
        });
      });
    }

    $('#preview').textContent = JSON.stringify({ propiedades: lista }, null, 2);
    $('#btn-agregar').textContent = editando ? 'Guardar cambios' : 'Agregar a la colección';
  }

  function porId(id) { return lista.filter(function (p) { return p.id === id; })[0]; }

  function esc(t) {
    return String(t == null ? '' : t).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* ---------- Prompt listo para la IA ---------- */
  function promptDe(p) {
    var destino = DESTINOS[p.destino] || p.destino;
    return [
      'Agrega esta propiedad a la Colección Privada del sitio de Punta Mita Homes.',
      'Guárdala en properties.json dentro de mi carpeta de Dropbox sincronizada con GitHub,',
      'manteniendo el diseño biofílico y el tono cálido del sitio. No inventes datos que no estén aquí.',
      '',
      'DATOS:',
      JSON.stringify(p, null, 2),
      '',
      'INSTRUCCIONES:',
      '1. Añade el objeto al arreglo "propiedades" de properties.json (respeta el campo "orden").',
      '2. Si faltan fotos, deja el arreglo vacío: el sitio muestra una ilustración botánica como respaldo.',
      '3. Verifica que el JSON sea válido antes de subirlo.',
      '4. Confírmame que quedó publicada en ' + destino + '.'
    ].join('\n');
  }

  /* ---------- Portapapeles y descarga ---------- */
  function copiar(texto, msg) {
    var listo = function () { if (msg) aviso(msg, true); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(texto).then(listo, function () { fallback(texto, listo); });
    } else {
      fallback(texto, listo);
    }
  }
  function fallback(texto, cb) {
    var ta = document.createElement('textarea');
    ta.value = texto; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); cb(); } catch (e) { alert(texto); }
    document.body.removeChild(ta);
  }

  function descargar(nombre, contenido) {
    var blob = new Blob([contenido], { type: 'application/json;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = nombre;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  /* ---------- Arranque ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    leer();
    limpiarCampos();
    pintar();

    $('#btn-agregar').addEventListener('click', function () {
      var p = leerFormulario();
      if (!p.nombre) { aviso('Ponle un nombre a la propiedad.', false); $(CAMPOS.nombre).focus(); return; }

      if (editando) {
        var i = lista.findIndex(function (x) { return x.id === editando; });
        if (i >= 0) lista[i] = p;
        editando = null;
        aviso('Cambios guardados en el borrador.', true);
      } else {
        if (porId(p.id)) { p.id = p.id + '-' + (lista.length + 1); }
        lista.push(p);
        aviso('«' + p.nombre + '» agregada. Descarga properties.json para publicarla.', true);
      }
      guardar(); limpiarCampos(); pintar();
    });

    $('#btn-limpiar').addEventListener('click', function () {
      editando = null; limpiarCampos(); pintar();
    });

    $('#btn-vaciar').addEventListener('click', function () {
      if (!lista.length) return;
      if (confirm('¿Vaciar todo el borrador local? (no borra el properties.json ya subido)')) {
        lista = []; guardar(); pintar();
      }
    });

    $('#btn-descargar').addEventListener('click', function () {
      if (!lista.length) { aviso('No hay propiedades para descargar.', false); return; }
      descargar('properties.json', JSON.stringify({ propiedades: lista }, null, 2) + '\n');
      aviso('properties.json descargado. Súbelo a tu carpeta de Dropbox / repo de GitHub.', true);
    });

    $('#btn-copiar-json').addEventListener('click', function () {
      copiar(JSON.stringify({ propiedades: lista }, null, 2), 'JSON copiado.');
    });

    // Convertidor de Dropbox
    $('#btn-convertir').addEventListener('click', function () {
      var url = $('#db-entrada').value.trim();
      if (!url) { $('#db-salida').textContent = 'Pega primero un enlace.'; $('#db-tipo').textContent = ''; return; }
      var directo = window.Cargador.aEnlaceDirecto(url);
      var carpeta = window.Cargador.esCarpetaDropbox(url);
      $('#db-salida').textContent = directo;
      $('#db-tipo').innerHTML = carpeta
        ? 'Es una <b>carpeta</b>: el navegador no puede leerla directamente (Dropbox lo ' +
          'bloquea por CORS y puede pesar varios GB). Úsala en el workflow de GitHub ' +
          '(secret <code>DROPBOX_FOLDER_URL</code>), o guarda dentro el ' +
          '<code>properties.json</code> que generas aquí y comparte solo ese archivo.'
        : 'Es un <b>archivo</b>. Pégalo en <code>fuente.url</code> de <code>index.html</code>: el sitio lo leerá al instante.';
      // sincroniza también el configurador de fuente de abajo
      // (carpeta: se guarda el enlace original www; el host dl da 404 en carpetas)
      $('#db-config-url').value = carpeta ? url : directo;
      $('#db-config-url').dispatchEvent(new Event('input'));
      copiar(carpeta ? url : directo, carpeta ? 'Enlace de carpeta copiado.' : 'Enlace directo copiado.');
    });

    $('#btn-copiar-snippet').addEventListener('click', function () {
      copiar($('#snippet-fuente').textContent, 'Configuración copiada.');
    });

    // Snippet de configuración reactivo
    var inputFuente = $('#db-config-url');
    function actualizarSnippet() {
      var url = inputFuente.value.trim();
      var pre = $('#snippet-fuente');
      if (!url) {
        pre.textContent = "fuente: { tipo: 'auto', url: '' }   // lee properties.json local";
        return;
      }
      if (window.Cargador.esCarpetaDropbox(url)) {
        pre.textContent =
          '// CARPETA de Dropbox (el navegador no la lee directa):\n' +
          '// 1) workflow de GitHub → Settings → Secrets:\n' +
          'DROPBOX_FOLDER_URL = ' + url + '\n' +
          '// 2) o guarda properties.json en la carpeta, compártelo como archivo y usa:\n' +
          "fuente: { tipo: 'url', url: 'PEGA_AQUI_EL_ENLACE_DEL_ARCHIVO' }";
        return;
      }
      pre.textContent = "fuente: { tipo: 'url', url: '" + url + "' }";
    }
    inputFuente.addEventListener('input', actualizarSnippet);

    // Precargar con la fuente configurada en el sitio, si existe
    try {
      var cfg = window.SITIO_CONFIG;
      if (cfg && cfg.fuente && cfg.fuente.url) {
        inputFuente.value = cfg.fuente.url;
      }
    } catch (e) { /* sin configuración */ }
    actualizarSnippet();
  });
})();
