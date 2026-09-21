/* ============================================================
   PUNTA MITA HOMES · lógica del sitio
   ============================================================ */
(function () {
  'use strict';

  /* ----------------------------------------------------------
     1. CONFIGURACIÓN
     Cambia FUENTE_PROPIEDADES para apuntar a tu Dropbox / GitHub.
     Opciones:
       { tipo:'auto',    url:'' }                                     -> properties.json local
       { tipo:'url',     url:'https://raw.githubusercontent.com/USUARIO/REPO/main/properties.json' }
       { tipo:'carpeta', url:'https://www.dropbox.com/scl/fo/XXXX/YYYY?rlkey=ZZZZ' }
     ---------------------------------------------------------- */
  var CONFIG = (window.SITIO_CONFIG && window.SITIO_CONFIG.fuente) || { tipo: 'auto', url: '' };
  var CONTACTO = (window.SITIO_CONFIG && window.SITIO_CONFIG.contacto) || {};

  var ESTADO = { propiedades: [], filtro: 'todas', fuente: null };

  /* ----------------------------------------------------------
     2. Utilidades
     ---------------------------------------------------------- */
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  function esc(t) {
    return String(t == null ? '' : t)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function moneda(v) {
    if (!v) return '';
    var n = Number(v);
    if (!isFinite(n)) return String(v);
    var s = n >= 1000000
      ? 'USD $' + (n / 1000000).toFixed(n % 1000000 === 0 ? 0 : 2) + 'M'
      : 'USD $' + n.toLocaleString('en-US');
    return s;
  }

  function nombreDestino(id) {
    return {
      'riviera-nayarit': 'Riviera Nayarit',
      'riviera-maya': 'Riviera Maya',
      'puerto-vallarta': 'Puerto Vallarta',
      'tulum': 'Tulum'
    }[id] || String(id || '').replace(/-/g, ' ');
  }

  var DESTINOS_VALIDOS = ['riviera-nayarit', 'riviera-maya', 'puerto-vallarta', 'tulum'];

  /* ----------------------------------------------------------
     3. Iconos SVG (hoja, cama, baño, superficie, wa, ig, flecha)
     ---------------------------------------------------------- */
  var ICONO = {
    hoja: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
    cama: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4v16"/><path d="M2 8h18a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/></svg>',
    bano: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.7 3 4 3.7 4 4.5V13"/><path d="M2 13h20v2a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5z"/><path d="M7 20l-1 2"/><path d="M18 20l1 2"/></svg>',
    m2: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 3H3v18h18z"/><path d="M3 9h18M9 21V3"/></svg>',
    pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    flecha: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg>',
    wa: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.76-1.66-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.68-1.63-.93-2.23-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.01-1.04 2.470 0 1.46 1.06 2.87 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.42-.07-.12-.27-.2-.57-.35Z"/><path d="M12.04 2C6.6 2 2.17 6.43 2.17 11.87c0 1.74.46 3.44 1.32 4.94L2 22l5.34-1.4a9.83 9.83 0 0 0 4.7 1.2h.01c5.43 0 9.86-4.43 9.86-9.87 0-2.63-1.02-5.1-2.88-6.96A9.79 9.79 0 0 0 12.04 2Zm0 18.02h-.01a8.2 8.2 0 0 1-4.17-1.14l-.3-.18-3.1.81.83-3.02-.2-.31a8.15 8.15 0 0 1-1.25-4.35c0-4.52 3.68-8.2 8.2-8.2a8.14 8.14 0 0 1 5.8 2.4 8.14 8.14 0 0 1 2.4 5.8c0 4.53-3.68 8.19-8.2 8.19Z"/></svg>',
    ig: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg>',
    correo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>',
    tel: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
    alerta: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    planta: '<svg viewBox="0 0 200 160" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M100 150V70"/><path d="M100 105c-16 0-28-10-30-28 18-2 30 8 30 28Z"/><path d="M100 88c16 0 28-10 30-28-18-2-30 8-30 28Z"/><path d="M100 70c-12-4-18-14-16-28 12 2 18 12 16 28Z"/><path d="M100 70c12-4 18-14 16-28-12 2-18 12-16 28Z"/><path d="M100 44c-8-8-8-20 0-32 8 12 8 24 0 32Z"/><path d="M70 150h60"/></svg>'
  };

  /* ----------------------------------------------------------
     4. Hojas decorativas del dosel
     ---------------------------------------------------------- */
  function hojaSVG(tipo) {
    if (tipo === 'monstera') {
      return '<svg viewBox="0 0 200 200" fill="currentColor"><path fill-rule="evenodd" d="M100 8c46 0 84 40 84 92 0 46-34 88-84 92C54 188 16 146 16 100 16 48 54 8 100 8Zm0 22c-6 0-12 26-12 62s6 66 12 66 12-30 12-66-6-62-12-62Zm-34 6c-14 12-16 40-8 70 4-18 12-32 22-42-6-12-10-22-14-28Zm68 0c-4 6-8 16-14 28 10 10 18 24 22 42 8-30 6-58-8-70ZM44 96c-10 14-14 32-12 48 10-14 22-26 34-34-8-6-16-10-22-14Zm112 0c-6 4-14 8-22 14 12 8 24 20 34 34 2-16-2-34-12-48Z"/></svg>';
    }
    if (tipo === 'palma') {
      return '<svg viewBox="0 0 220 200" fill="currentColor"><path d="M110 200c0-60 6-100 18-128l-10-4C104 98 98 140 98 200h12Z"/><path d="M118 66C104 40 78 22 44 18c22 20 38 36 48 52 8-6 16-8 26-4Z"/><path d="M122 66c14-26 40-44 74-48-22 20-38 36-48 52-8-6-16-8-26-4Z"/><path d="M116 74C96 60 68 56 38 64c26 10 44 20 58 32 6-10 12-18 20-22Z"/><path d="M124 74c20-14 48-18 78-10-26 10-44 20-58 32-6-10-12-18-20-22Z"/><path d="M118 82c-6 18-4 40 6 60-14-14-24-32-26-52 6-6 12-9 20-8Z"/><path d="M122 82c6 18 4 40-6 60 14-14 24-32 26-52-6-6-12-9-20-8Z"/></svg>';
    }
    return '<svg viewBox="0 0 160 200" fill="currentColor"><path d="M80 4c40 30 60 66 60 104 0 44-26 82-60 88-34-6-60-44-60-88C20 70 40 34 80 4Zm0 34c-18 24-28 52-28 82 0 20 6 38 14 48 2-30 6-76 14-130Zm0 0c8 54 12 100 14 130 8-10 14-28 14-48 0-30-10-58-28-82Z"/></svg>';
  }

  function pintarDosel() {
    var dosel = $('#dosel');
    if (!dosel) return;
    dosel.innerHTML =
      '<div class="h1">' + hojaSVG('palma') + '</div>' +
      '<div class="h2">' + hojaSVG('monstera') + '</div>' +
      '<div class="h3">' + hojaSVG('hoja') + '</div>' +
      '<div class="h4">' + hojaSVG('palma') + '</div>';
  }

  /* ----------------------------------------------------------
     5. Enlaces de contacto
     ---------------------------------------------------------- */
  function soloDigitos(t) { return String(t || '').replace(/\D/g, ''); }

  function waLink(mensaje) {
    var tel = soloDigitos(CONTACTO.whatsapp);
    var txt = encodeURIComponent(mensaje || CONTACTO.mensajeDefault || 'Hola, me interesa la Colección Privada.');
    if (!tel || CONTACTO.whatsappPendiente) {
      return CONTACTO.instagramUrl || 'https://www.instagram.com/puntamita.homes';
    }
    return 'https://wa.me/' + tel + '?text=' + txt;
  }

  function actualizarContacto() {
    // WhatsApp
    $$('[data-wa]').forEach(function (a) {
      var msg = a.getAttribute('data-wa') || '';
      var url = waLink(msg);
      a.href = url;
      a.target = '_blank';
      a.rel = 'noopener';
    });

    var telEl = $('#contacto-telefono');
    if (telEl) {
      if (CONTACTO.telefono && !CONTACTO.telefonoPendiente) {
        telEl.innerHTML = '<a href="tel:' + esc(soloDigitos(CONTACTO.telefono)) + '">' + esc(CONTACTO.telefono) + '</a>';
      } else {
        telEl.innerHTML = '<span class="v pendiente">Por confirmar — escríbenos por Instagram</span>';
      }
    }
    var correoEl = $('#contacto-correo');
    if (correoEl) {
      if (CONTACTO.email && !CONTACTO.emailPendiente) {
        correoEl.innerHTML = '<a href="mailto:' + esc(CONTACTO.email) + '">' + esc(CONTACTO.email) + '</a>';
      } else {
        correoEl.innerHTML = '<span class="v pendiente">Por confirmar — escríbenos por Instagram</span>';
      }
    }

    // Aviso global de datos pendientes
    var aviso = $('#aviso-contacto');
    if (aviso) {
      var faltan = (CONTACTO.whatsappPendiente ? 'WhatsApp' : '') +
        (CONTACTO.telefonoPendiente ? ', teléfono' : '') +
        (CONTACTO.emailPendiente ? ', correo' : '');
      if (faltan) {
        aviso.hidden = false;
        aviso.innerHTML = ICONO.alerta + '<div><b>Datos por completar:</b> ' + esc(faltan.replace(/^,\s*/, '')) +
          ' no son públicos en el perfil de Instagram. Súbelos a <code>SITIO_CONFIG.contacto</code> en <code>index.html</code>.</div>';
      } else {
        aviso.hidden = true;
      }
    }

    // Formulario
    var form = $('#formulario-contacto');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var d = new FormData(form);
        var msg = 'Hola, soy ' + (d.get('nombre') || '') + '.\n' +
          'Destino de interés: ' + (d.get('destino') || 'sin especificar') + '\n' +
          'Presupuesto: ' + (d.get('presupuesto') || 'sin especificar') + '\n\n' +
          (d.get('mensaje') || '');
        window.open(waLink(msg), '_blank', 'noopener');
      });
    }
  }

  /* ----------------------------------------------------------
     6. Render de la colección
     ---------------------------------------------------------- */
  function tarjetaHTML(p) {
    var foto = p.fotos && p.fotos[0];
    var specs = [];
    if (p.specs.recamaras) specs.push('<span>' + ICONO.cama + esc(p.specs.recamaras) + ' rec.</span>');
    if (p.specs.banos) specs.push('<span>' + ICONO.bano + esc(p.specs.banos) + ' baños</span>');
    if (p.specs.m2) specs.push('<span>' + ICONO.m2 + esc(Number(p.specs.m2).toLocaleString('es-MX')) + ' m²</span>');

    var etiqueta = '';
    if (p.status === 'preventa') etiqueta = '<span class="etiqueta oro">Preventa</span>';
    else if (p.status === 'nuevo') etiqueta = '<span class="etiqueta verde">Nueva</span>';
    else if (p.status === 'exclusiva') etiqueta = '<span class="etiqueta">Exclusiva</span>';

    return '<article class="tarjeta rev" data-id="' + esc(p.id) + '" tabindex="0" role="button" aria-label="Ver ' + esc(p.nombre) + '">' +
      '<div class="tarjeta-img">' +
      (foto
        ? '<img src="' + esc(foto) + '" alt="' + esc(p.nombre) + '" loading="lazy" onerror="this.remove()">'
        : '<div class="sin-img">' + ICONO.planta + '</div>') +
      etiqueta +
      '</div>' +
      '<div class="tarjeta-cuerpo">' +
      '<span class="tarjeta-lugar">' + esc(nombreDestino(p.destino)) + (p.zona ? ' · ' + esc(p.zona) : '') + '</span>' +
      '<h3>' + esc(p.nombre) + '</h3>' +
      (p.descripcionCorta ? '<p>' + esc(p.descripcionCorta) + '</p>' : '') +
      (specs.length ? '<div class="tarjeta-specs">' + specs.join('') + '</div>' : '') +
      '<div class="tarjeta-pie">' +
      '<div class="precio">' + esc(p.precio === 'a-consulta' ? 'A consulta' : moneda(p.precio)) +
      '<small>' + esc(p.tipo || 'Residencia') + '</small></div>' +
      '<span class="ver">Ver detalles</span>' +
      '</div></div></article>';
  }

  function vacioHTML(mensaje, error) {
    return '<div class="vacio rev visible">' +
      ICONO.planta.replace('<svg ', '<svg class="planta" ') +
      '<h3 class="display">La colección está creciendo</h3>' +
      '<p>' + esc(mensaje) + '</p>' +
      '<div class="estado-fuente' + (error ? ' error' : '') + '">' +
      '<i class="punto' + (error ? ' error' : '') + '"></i>' + esc(error ? 'Fuente con error' : 'Fuente conectada') +
      '</div>' +
      (error ? '<p style="margin-top:1rem;font-size:.85rem;color:#8A3B25">' + esc(error) + '</p>' : '') +
      '<p style="margin-top:1.4rem"><a class="btn contorno" href="#contacto">Solicitar la Colección Privada</a></p>' +
      '</div>';
  }

  function pintarFiltros() {
    var cont = $('#filtros');
    if (!cont) return;
    var destinos = [];
    ESTADO.propiedades.forEach(function (p) {
      if (p.destino && destinos.indexOf(p.destino) < 0) destinos.push(p.destino);
    });
    var html = '<button class="filtro" data-destino="todas" aria-pressed="' + (ESTADO.filtro === 'todas') + '">Todas</button>';
    destinos.forEach(function (d) {
      html += '<button class="filtro" data-destino="' + esc(d) + '" aria-pressed="' + (ESTADO.filtro === d) + '">' +
        esc(nombreDestino(d)) + '</button>';
    });
    cont.innerHTML = html;
    $$('.filtro', cont).forEach(function (b) {
      b.addEventListener('click', function () {
        ESTADO.filtro = b.getAttribute('data-destino');
        pintarFiltros();
        pintarRejilla();
      });
    });
  }

  function pintarRejilla() {
    var rejilla = $('#rejilla');
    if (!rejilla) return;
    var lista = ESTADO.propiedades.filter(function (p) {
      return ESTADO.filtro === 'todas' || p.destino === ESTADO.filtro;
    });

    var contador = $('#contador');
    if (contador) {
      contador.textContent = ESTADO.propiedades.length
        ? ESTADO.propiedades.length + (ESTADO.propiedades.length === 1 ? ' propiedad' : ' propiedades') + ' en la colección'
        : 'Colección en construcción';
    }

    if (!lista.length) {
      var fuente = ESTADO.fuente;
      var msg, err = null;
      if (fuente && fuente.error) {
        msg = 'No pudimos leer el archivo de propiedades. Revisa el enlace de Dropbox o GitHub configurado.';
        err = fuente.error;
      } else if (ESTADO.propiedades.length) {
        msg = 'No hay propiedades en este destino todavía.';
      } else {
        msg = 'Estamos curando cada residencia una por una. Muy pronto aparecerán aquí las primeras piezas de la Colección Privada en Riviera Nayarit y Riviera Maya.';
      }
      rejilla.innerHTML = vacioHTML(msg, err);
      return;
    }

    rejilla.innerHTML = '<div class="rejilla">' + lista.map(tarjetaHTML).join('') + '</div>';
    $$('.tarjeta', rejilla).forEach(function (t) {
      var abrir = function () { abrirModal(t.getAttribute('data-id')); };
      t.addEventListener('click', abrir);
      t.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrir(); }
      });
    });
    observarRevelado();
  }

  /* ----------------------------------------------------------
     7. Modal de detalle
     ---------------------------------------------------------- */
  function abrirModal(id) {
    var p = ESTADO.propiedades.filter(function (x) { return x.id === id; })[0];
    if (!p) return;
    var modal = $('#modal');
    var foto = p.fotos && p.fotos[0];

    var specs = '';
    if (p.specs.recamaras) specs += '<div><b>' + esc(p.specs.recamaras) + '</b><span>Recámaras</span></div>';
    if (p.specs.banos) specs += '<div><b>' + esc(p.specs.banos) + '</b><span>Baños</span></div>';
    if (p.specs.m2) specs += '<div><b>' + esc(Number(p.specs.m2).toLocaleString('es-MX')) + '</b><span>m² construcción</span></div>';
    if (p.specs.terreno) specs += '<div><b>' + esc(Number(p.specs.terreno).toLocaleString('es-MX')) + '</b><span>m² terreno</span></div>';
    if (p.torre) specs += '<div><b>' + esc(p.torre) + '</b><span>Torre</span></div>';
    if (p.entrega) specs += '<div><b>' + esc(p.entrega) + '</b><span>Entrega</span></div>';

    var galeria = (p.fotos || []).slice(1);

    $('#modal-contenido').innerHTML =
      '<div class="modal-img">' +
      (foto ? '<img src="' + esc(foto) + '" alt="' + esc(p.nombre) + '">' : '<div class="sin-img" style="display:grid;place-items:center;height:100%;color:#2A5439;opacity:.5">' + ICONO.planta + '</div>') +
      '<button class="modal-cerrar" aria-label="Cerrar">' +
      '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg></button>' +
      '</div>' +
      '<div class="modal-cuerpo">' +
      '<nav class="migas" aria-label="Migas de pan">' +
      '<a href="index.html">Inicio</a><span>›</span><a href="#coleccion" data-cierra-modal>Colección</a><span>›</span>' +
      '<span>' + esc(nombreDestino(p.destino)) + '</span>' +
      (p.torre ? '<span>›</span><span>' + esc(p.torre) + '</span>' : '') +
      '</nav>' +
      '<span class="tarjeta-lugar">' + esc(nombreDestino(p.destino)) + (p.zona ? ' · ' + esc(p.zona) : '') + '</span>' +
      '<h2 class="display" style="margin:.5rem 0 .8rem">' + esc(p.nombre) + '</h2>' +
      '<div style="font-family:var(--serif);font-size:2rem;color:var(--bosque)">' +
      esc(p.precio === 'a-consulta' ? 'Precio a consulta' : moneda(p.precio)) + '</div>' +
      (specs ? '<div class="modal-specs">' + specs + '</div>' : '') +
      (p.descripcion ? '<p class="parrafo">' + esc(p.descripcion).replace(/\n/g, '<br>') + '</p>' : '') +
      (p.amenidades && p.amenidades.length
        ? '<h3 style="font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;color:var(--helecho);margin:1.6rem 0 .7rem">Amenidades</h3>' +
        '<ul class="amenidades">' + p.amenidades.map(function (a) { return '<li>' + esc(a) + '</li>'; }).join('') + '</ul>'
        : '') +
      (galeria.length
        ? '<div class="galeria">' + galeria.map(function (g) { return '<img src="' + esc(g) + '" alt="' + esc(p.nombre) + '" loading="lazy">'; }).join('') + '</div>'
        : '') +
      (p.material && p.material.length
        ? '<h3 style="font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;color:var(--helecho);margin:1.6rem 0 .7rem">Material de ventas</h3>' +
          '<ul class="amenidades material">' + p.material.map(function (m) {
            return '<li><a href="' + esc(m.url) + '" target="_blank" rel="noopener">' + esc(m.nombre) + ' ↗</a></li>';
          }).join('') + '</ul>'
        : '') +
      '<div class="modal-acciones">' +
      '<a class="btn" data-wa="Hola, me interesa ' + esc(p.nombre) + ' (' + esc(nombreDestino(p.destino)) + '). ¿Me compartes más información?" href="#">' + ICONO.wa + 'Consultar por WhatsApp</a>' +
      '<a class="btn contorno" href="' + esc(CONTACTO.instagramUrl || '#') + '" target="_blank" rel="noopener">' + ICONO.ig + 'Ver en Instagram</a>' +
      '</div></div>';

    modal.classList.add('abierto');
    document.body.style.overflow = 'hidden';
    $('.modal-cerrar', modal).addEventListener('click', cerrarModal);
    var miga = $('[data-cierra-modal]', modal);
    if (miga) miga.addEventListener('click', cerrarModal);
    actualizarContacto();
  }

  function cerrarModal() {
    var modal = $('#modal');
    modal.classList.remove('abierto');
    document.body.style.overflow = '';
  }

  /* ----------------------------------------------------------
     8. Animaciones y navegación
     ---------------------------------------------------------- */
  var observador = null;
  function observarRevelado() {
    if (!('IntersectionObserver' in window)) {
      $$('.rev').forEach(function (el) { el.classList.add('visible'); });
      return;
    }
    if (!observador) {
      observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('visible'); observador.unobserve(e.target); }
        });
      }, { threshold: .12, rootMargin: '0px 0px -8% 0px' });
    }
    $$('.rev:not(.visible)').forEach(function (el) { observador.observe(el); });
  }

  function iniciarNav() {
    var nav = $('#nav');
    var hero = $('#inicio');
    var burger = $('#nav-burger');
    var links = $('#nav-links');

    if (burger && links) {
      burger.addEventListener('click', function () { links.classList.toggle('abierto'); });
      $$('a', links).forEach(function (a) {
        a.addEventListener('click', function () { links.classList.remove('abierto'); });
      });
    }
    function alScroll() {
      if (!nav || !hero) return;
      nav.classList.toggle('oscura', window.scrollY > hero.offsetHeight - 90);
    }
    window.addEventListener('scroll', alScroll, { passive: true });
    alScroll();
  }

  /* ----------------------------------------------------------
     9. Arranque
     ---------------------------------------------------------- */
  async function iniciar() {
    pintarDosel();
    iniciarNav();
    actualizarContacto();
    observarRevelado();

    var rejilla = $('#rejilla');
    if (rejilla) {
      rejilla.innerHTML = vacioHTML('Cargando la colección…', null);
    }

    var resultado = await window.Cargador.cargar(CONFIG);
    ESTADO.propiedades = resultado.propiedades || [];
    ESTADO.fuente = resultado;

    console.info('[Colección] fuente:', resultado.origen || 'ninguna',
      '| archivo:', resultado.fuente || '—',
      '| propiedades:', ESTADO.propiedades.length,
      resultado.error ? '| error: ' + resultado.error : '');

    pintarFiltros();
    pintarRejilla();

    var nota = $('#nota-fuente');
    if (nota) {
      nota.textContent = resultado.origen
        ? 'Colección sincronizada desde ' + resultado.origen +
        (resultado.fuente && !/^properties\.json$/.test(resultado.fuente) ? '' : '') +
        ' · ' + ESTADO.propiedades.length + ' propiedad(es)'
        : 'Sin fuente configurada';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
