# Hunt Club

Juego de misterio y deducción para el móvil. Ocho ambientes, casos generados
al vuelo y verificados uno a uno, y un modo para jugar toda la familia
alrededor de una mesa.

> Nadie dice toda la verdad. Solo uno mató.

---

## Qué es

Una noche, nueve salas, seis sospechosos y un muerto. Registras salas,
interrogas gente y careas a quien miente, gastando acciones de un presupuesto
que no llega para todo. Cuando creas saber quién, dónde y con qué, acusas. Una
sola vez.

Lo que lo separa de un Cluedo es que **casi todos mienten sobre dónde
estuvieron** — pero solo uno mató. Los demás tapaban un robo, una aventura o
una deserción. Y **el culpable no deja ni una sola prueba física**: es al único
al que no puedes pillar de frente. Se llega a él descartando a los otros cinco.

### Los ocho ambientes

| Ambiente | Cuándo | El encierro |
|---|---|---|
| Villa romana | Roma, 61 d.C. | Puertas cerradas desde el ocaso |
| Mansión Quintanar | Santander, 1928 | Portón con llave, lluvia fuera |
| Monasterio | Castilla, 1327 | Nieve sin pisar en el claustro |
| Cuartel en guerra | Normandía, 1944 | Perímetro cerrado, centinela en la puerta |
| Cortijo andaluz | Jaén, 1931 | Los perros no ladraron |
| Tren nocturno | Los Alpes, 1931 | Cuatro minutos de túnel a ochenta por hora |
| Base antártica | Invernada de 1958 | Nadie en mil kilómetros |
| Estación orbital | Órbita baja, 2091 | Fuera es el vacío |

Cada uno cambia el plano, el elenco, las armas y la clase de secretos que
esconde la gente. El motor de casos es el mismo.

---

## Cómo se juega

**En solitario.** Tú contra el caso. Tres dificultades, que cambian cuánta
gente miente y cuántas acciones tienes.

**En mesa.** Todos con el mismo código, cada uno con su móvil y su número.
El reparto de pistas hace que **en cada sala veas solo una parte** de lo que
hay; el resto lo encuentran los demás. Nadie puede cerrar el caso solo — eso
está verificado caso por caso — así que hay que hablar, enseñar, pedir. Y
mentir, porque lo que te cuentan se apunta en tu cuaderno y **la app no
comprueba nada**: si te la han jugado, tu deducción miente contigo.

Acusar mal en mesa te elimina pero **no destapa el caso**: sigues sentado, con
tu cuaderno, sin nada que perder.

No hace falta conexión entre los móviles. Todo sale del código de la noche.

---

## Cómo se ejecuta

Es una página estática sin dependencias de ejecución. Cualquier servidor vale:

```bash
npm run serve          # http://localhost:8080
```

En el móvil, con la página abierta: **Compartir → Añadir a pantalla de
inicio**. Queda como una app, a pantalla completa, y con el service worker se
juega sin cobertura.

### Publicarlo en GitHub Pages

Ajustes del repositorio → Pages → rama principal, carpeta raíz. La URL que sale
es la que se pasa a la familia.

### La versión de un solo archivo

```bash
python3 build.py
```

Genera `dist/hunt-club.html` con las imágenes dentro (unos 900 KB). Es la
versión para mandar por WhatsApp o abrir desde Archivos sin servidor. El mismo
script sella la versión del service worker a partir del contenido, así que
conviene ejecutarlo antes de cada publicación aunque no vayas a usar el `dist`.

`dist/` está en el `.gitignore`: si quieres repartirlo, súbelo como adjunto de
una release en lugar de versionarlo.

---

## Cómo está montado

```
index.html                 la app entera: motor, contenido e interfaz
assets/                    16 imágenes + icono, lo único que pesa
sw.js                      caché para jugar sin conexión
build.py                   sella el sw y genera el archivo único
tests/                     auditorías sin navegador  (npm test)
tests/browser/             partidas reales en Chromium (npm run test:browser)
```

Un solo HTML a propósito: se abre en cualquier sitio, no hay que compilar nada
y el estado vive en `localStorage`. Las imágenes van fuera para que git pueda
versionar el código de verdad.

### El generador

Cada código de caso es una semilla. A partir de ella se construye la noche
entera —quién estaba dónde a cada hora, quién mató, con qué, si arrastró el
cuerpo— y después se decide qué parte de esa verdad se deja descubrir. Un
solver comprueba que lo descubrible deje **una sola** lectura posible; si no,
el caso se descarta y se genera otro.

De ahí salen dos propiedades que el juego necesita:

- **El mismo código da el mismo caso en cualquier móvil.** Es lo que permite el
  modo mesa sin servidor.
- **Todo caso que se sirve es resoluble**, y con holgura de acciones suficiente.

El reparto del modo mesa funciona igual: se prueban repartos hasta dar con uno
donde nadie pueda cerrar solo y nadie se quede sin nada que aportar, con un
pase de reparación si hace falta. Determinista, así que los ocho móviles eligen
el mismo sin hablar entre ellos.

### Añadir un ambiente

Un ambiente es un objeto dentro de `PACKS`. El motor no sabe nada de épocas.
Necesita:

- 9 salas, con **4 materiales de suelo repetidos dos veces y uno único** — es lo
  que hace deducible la sala a partir de las suelas del muerto
- 6 personajes, uno de ellos quien examina la herida (`forenseIdx`)
- 6 armas, **exactamente dos de cada tipo** (hoja, golpe, veneno)
- 5 frases de descarte, 7 secretos, 3 confesiones, 3 negaciones
- la escena de apertura y el artículo de cada sala

`npm test` valida todo eso y avisa de lo que falte o no concuerde. Además hacen
falta dos imágenes en `assets/`: la lámina panorámica y el tablero cenital de
3×3. Los prompts con los que se generaron las actuales están en el historial
del proyecto.

---

## Pruebas

```bash
npm test               # esquema, generador, textos y reparto de mesa
npm run test:browser   # partidas completas en Chromium (necesita Playwright)
```

Lo que comprueban, por si sirve de referencia: que ningún caso sea
irresoluble, que la ruta mínima quepa en el presupuesto de acciones, que el
culpable nunca deje pruebas, que ninguna coartada falsa apunte a una sala
ocupada, que los textos concuerden en género y número, y que en modo mesa la
mesa entera pueda cerrar el caso pero ningún jugador pueda hacerlo solo.

---

## Licencia

El código, bajo licencia MIT (ver `LICENSE`).

Las imágenes de `assets/` se generaron con herramientas de IA generativa a
partir de prompts propios. Si vas a hacer público el repositorio, conviene
revisar las condiciones de uso del servicio con el que se generaron antes de
darlas por libres, porque varían entre proveedores y con el tiempo.

Las tipografías (Cinzel y Cormorant Garamond) se cargan desde Google Fonts y
tienen licencia SIL Open Font. Si quieres que la app funcione sin conexión con
su tipografía propia, habría que servirlas desde `assets/`.
