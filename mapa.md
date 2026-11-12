# Mapa de reconocimiento — Proyecto 1: Know Your Target

## 1. Resumen

Airbnb, Inc. es la organización analizada mediante técnicas de reconocimiento pasivo sobre el dominio `airbnb.com`.
WHOIS identifica a MarkMonitor Inc. como registrador y muestra que el dominio fue creado el 5 de agosto de 2008.
Las consultas DNS, DNSDumpster y Subfinder han permitido identificar registros públicos, subdominios y proveedores de infraestructura.
Los resultados muestran referencias a Akamai, Amazon Web Services (AWS), Google Cloud y servicios de correo de Google y SendGrid.
No se ha confirmado ninguna vulnerabilidad; antes de realizar pruebas activas, es necesario verificar el alcance oficial del programa de HackerOne.

## 2. Dominios y subdominios

La tabla recoge una selección de los resultados documentados en las consultas DNS y en las herramientas de reconocimiento. Las funciones indicadas son interpretaciones basadas en los nombres y los datos recopilados, no confirmaciones de la función interna de cada sistema.

| Dominio o subdominio | IP observada | ¿En alcance? | Función aparente |
|---|---|---|---|
| `airbnb.com` | `166.117.189.176` (Netcraft); `166.117.27.62` (DNSDumpster/otra captura) | Dominio base; no lo cubre el patrón `*.airbnb.com` por sí solo | Dominio principal |
| `www.airbnb.com` | `96.16.88.137` | Sí por comodín (sujeto a la política) | Sitio web; reverse DNS indica Akamai CDN |
| `api.airbnb.com` | `23.216.132.63` | Sí por comodín (sujeto a la política) | El nombre sugiere API; función no verificada |
| `callbacks.airbnb.com` | `23.44.111.31` | Sí por comodín (sujeto a la política) | El nombre sugiere callbacks; función no verificada |
| `admin-staging.airbnb.com` | `34.120.23.133` | Sí por comodín (sujeto a la política) | El nombre sugiere entorno staging; no se probó acceso |
| `admin-lite-staging.airbnb.com` | `34.120.23.133` | Sí por comodín (sujeto a la política) | El nombre sugiere entorno staging; no se probó acceso |
| `community-staging.airbnb.com` | `13.248.132.14` | Sí por comodín (sujeto a la política) | El nombre sugiere entorno de comunidad staging |
| `api.akamai-ci.airbnb.com` | En la captura de Subfinder no se indica | Sí por comodín (sujeto a la política) | Nombre observado por Subfinder; IP no documentada aquí |
| `api.akamai-dev.airbnb.com` | En la captura de Subfinder no se indica | Sí por comodín (sujeto a la política) | Nombre observado por Subfinder; IP no documentada aquí |
| `email.airbnb.com` | `3.20.87.51` | Sí por comodín (sujeto a la política) | Nombre relacionado con correo; función no verificada |
| `o10.email.airbnb.com` | `167.89.35.182` | Sí por comodín (sujeto a la política) | DNSDumpster lo asocia con SendGrid |
| `o11.email.airbnb.com` | `50.31.32.157` | Sí por comodín (sujeto a la política) | DNSDumpster lo asocia con SendGrid |
| `de.airbnb.com` | En la captura de Subfinder no se indica | Sí por comodín (sujeto a la política) | Nombre regional aparente; función no verificada |

**Criterio de alcance:** el scope del proyecto contiene `*.airbnb.com`, que cubre subdominios, no el dominio raíz `airbnb.com`. La tabla expresa coincidencia sintáctica con ese patrón; no confirma por sí sola elegibilidad vigente en HackerOne. Las IP pertenecientes a CDN o proveedores externos no se consideran activos autorizados por el mero hecho de aparecer en una resolución DNS.

Es necesario contrastar cada dominio con los activos incluidos y las exclusiones de la política vigente de HackerOne. La presencia de un nombre en DNSDumpster o Subfinder no equivale a autorización.

**Trazabilidad:** para cada fila, la IP y el nombre provienen de la entrada 2.1 (DNSDumpster) salvo `www.airbnb.com` y su IP, documentados en la entrada 7 (dig + Shodan); los nombres sin IP se ven en la entrada 3 (Subfinder). La función indicada es una inferencia a partir del nombre, no un hallazgo confirmado.

## 3. Infraestructura y servicios

### 3.1. Registro del dominio

La consulta WHOIS proporcionó los siguientes datos:

- Organización registrante: Airbnb, Inc.
- Registrador: MarkMonitor Inc.
- Fecha de creación: 5 de agosto de 2008.
- Fecha de caducidad indicada: 5 de agosto de 2028.
- Servidores de nombres asociados a NS1 y Amazon Web Services.
- Estados de bloqueo para proteger el registro del dominio.

**Fuente:** entrada 1 del cuaderno, «Registro del dominio — WHOIS».

### 3.2. DNS y correo electrónico

Se consultaron los registros MX, DMARC, NS y TXT mediante `dig`. Los MX visibles son cinco servidores de Google Workspace (`aspmx.l.google.com`, prioridades 1/5/10). El DMARC usa `p=reject`, `sp=reject` y `pct=100`; el SPF comienza con `include:spf1.airbnb.com` y termina con `-all`. Los NS visibles incluyen cuatro servidores AWS DNS y cuatro NS1. DNSDumpster amplió la información y reportó 178 registros, con 50 mostrados en la vista gratuita.

Entre los resultados observados:

- **Akamai:** la tabla de DNSDumpster asocia varios hosts/IP a Akamai; las capturas incluyen `api.airbnb.com` (`23.216.132.63`) y `callbacks.airbnb.com` (`23.44.111.31`).
- **AWS:** Netcraft asocia `166.117.189.176` con Amazon/AS16509 y reverse DNS `a333dda39e3b496ea.awsglobalaccelerator.com`.
- **Google Cloud:** DNSDumpster etiqueta `admin-staging.airbnb.com` y `admin-lite-staging.airbnb.com` con `34.120.23.133`; se conserva como etiqueta de la fuente, no como validación independiente.
- **Correo:** los MX de `airbnb.com` son de Google Workspace; DNSDumpster lista `email.airbnb.com`, `o10.email.airbnb.com` y `o11.email.airbnb.com`.
- **SendGrid:** DNSDumpster asocia `o10.email.airbnb.com` (`167.89.35.182`) y `o11.email.airbnb.com` (`50.31.32.157`) con SendGrid.
- **Registros TXT:** SPF contiene `include:spf1.airbnb.com` y `-all`; también hay verificaciones de EcoStruxure, Google, Anthropic, Segment, Microsoft, Stripe, Apple y Okta (captura `dig-txt.png`).

Los proveedores y las direcciones observados no demuestran por sí solos que exista una configuración incorrecta o una vulnerabilidad.

**Fuentes:** entradas 2 y 2.1 del cuaderno, «Consulta de registros DNS — dig» y «Reconocimiento DNS con DNSDumpster».

### 3.3. Huella tecnológica

Netcraft reporta hosting de Amazon en EE. UU., netblock owner Amazon.com, IPv4 `166.117.189.176`/AS16509 y reverse DNS de AWS Global Accelerator. También muestra `dns1.p02.nsone.net`, DNSSEC habilitado, y un certificado cuyo CN es `airbnb.com`, emitido por DigiCert Inc., con negociación `h2` y Perfect Forward Secrecy habilitado. Son valores reportados por Netcraft en la fecha de captura.

**Fuente:** entrada 4 del cuaderno, «Huella tecnológica — Netcraft» (capturas `netcraft.png`–`netcraft4.png`).

### 3.4. Shodan InternetDB

Se consultó InternetDB para la IP `96.16.88.137`, obtenida mediante una consulta DNS de `www.airbnb.com`.

El resultado mostró:

- Nombre de host: `a96-16-88-137.deploy.static.akamaitechnologies.com`.
- Puertos registrados: `80` y `443`.
- Etiqueta: `cdn`.
- Vulnerabilidades conocidas: el resultado consultado no mostraba referencias a vulnerabilidades.

Los puertos 80 y 443 suelen corresponder a HTTP y HTTPS. La etiqueta CDN y el nombre del host son compatibles con el uso de infraestructura de Akamai. Al tratarse de infraestructura de distribución de contenido, no se puede asumir que todos los servicios asociados a esa IP pertenezcan exclusivamente a Airbnb. La ausencia de vulnerabilidades listadas tampoco demuestra que el sistema sea completamente seguro.

**Fuente:** entrada 7 del cuaderno, «Servicios expuestos — InternetDB de Shodan».

### 3.5. Ficheros públicos

La captura de `robots.txt` muestra, entre otras, reglas `Disallow` para `/account`, `/login_with_redirect`, `/home/dashboard`, `/manage-listing`, `/my_listings`, `/payments/book`, `/reservation`, `/api/v1/trebuchet` y `/messaging/ajax_already_messaged/`, además de `Allow` para `/.well-known/apple-app-site-association`. Son directivas para rastreadores, no controles de acceso.

El `security.txt` obtenido vía `airbnb.es` da Contact `https://hackerone.com/airbnb/`, Policy `https://hackerone.com/airbnb#overview`, Preferred-Languages `en`, Canonical bajo `www.airbnb.com` y expiración `2027-06-01T04:59:00.000Z`. `airbnb.es` no está en el scope actual (`*.airbnb.com`), por lo que esta consulta se conserva como referencia documental, no como activo autorizado.

**Fuentes:** entradas 5 y 6 del cuaderno, «Ficheros públicos — robots.txt» y «Fichero de seguridad — security.txt».

## 4. Correos y personas

### 4.1. Correos electrónicos

TheHarvester no devolvió direcciones de correo ni IP en las consultas anotadas. Hunter.io mostró 4.814 resultados asociados al dominio, con 4.533 perfiles de personas y 421 perfiles de responsables de decisiones según la interfaz capturada; son métricas de la plataforma, no una lista de correos validados. La búsqueda de Google usada fue `site:airbnb.com "@airbnb.com"`; no se contactó a nadie.

Como alternativa, se consultó Hunter.io y se realizó una búsqueda en Google con el operador:

`site:airbnb.com "@airbnb.com"`

Hunter.io mostró referencias a direcciones asociadas al dominio, algunas parcialmente ocultas. No se ha confirmado su validez ni un patrón corporativo fiable.

DNSDumpster también mostró `email.airbnb.com` (`3.20.87.51`), `o10.email.airbnb.com` (`167.89.35.182`) y `o11.email.airbnb.com` (`50.31.32.157`); la entrada 2 documenta los MX de Google Workspace y la política SPF/DMARC.

### 4.2. Información sobre la organización

WHOIS identifica a Airbnb, Inc. como organización registrante. La investigación también localizó información pública relacionada con el programa de seguridad de Airbnb en HackerOne.

No se han documentado nombres de empleados verificados ni se ha contactado con ninguna persona. Por tanto, no se puede establecer un patrón de correo corporativo confirmado a partir de los resultados disponibles.

**Fuentes:** entrada 9 del cuaderno para los resultados de correo y Hunter.io; entradas 2 y 2.1 para DNS de correo; entrada 1 para la organización registrante.

## 5. Puntos de interés para una futura fase activa

Los siguientes tres elementos se proponen como prioridades para evaluar **solo si las reglas del programa permiten expresamente las pruebas correspondientes**. No representan vulnerabilidades confirmadas.

### 1. Sitio web público: `www.airbnb.com`

**Motivo:** es el punto de entrada web principal identificado en la investigación. Se dispone de información DNS y de una consulta de InternetDB sobre una IP asociada al sitio.

**Antes de continuar:** verificar el alcance del dominio y las reglas aplicables a la infraestructura CDN. No atribuir automáticamente todos los servicios de la IP a Airbnb.

**Trazabilidad:** entradas 2, 2.1 y 7 del cuaderno.

### 2. Subdominios de API: `api.airbnb.com`

**Motivo:** la enumeración pasiva identificó este subdominio y DNSDumpster le asoció la IP `23.216.132.63`. Los servicios API pueden ser relevantes para comprender la superficie de aplicación expuesta.

**Antes de continuar:** confirmar que el subdominio está incluido en el alcance y revisar las restricciones específicas sobre API. Su identificación no demuestra que sea vulnerable.

**Trazabilidad:** entradas 2.1 y 3 del cuaderno.

### 3. Subdominios con nombres de pruebas o preproducción

**Motivo:** se encontraron nombres como `admin-staging.airbnb.com`, `admin-lite-staging.airbnb.com` y `community-staging.airbnb.com`. Son candidatos para una revisión documental adicional porque sus nombres sugieren entornos distintos del sitio público.

**Antes de continuar:** confirmar expresamente su inclusión en el alcance y no inferir que son accesibles o vulnerables por sus nombres. No realizar pruebas activas sin autorización.

**Trazabilidad:** entradas 2.1 y 3 del cuaderno.

## 6. Limitaciones y consideraciones

- El reconocimiento realizado se basa en fuentes públicas y técnicas pasivas.
- DNSDumpster mostró 50 de los 178 registros indicados por la herramienta; el conjunto consultado no es necesariamente exhaustivo.
- La función de algunos subdominios se ha inferido a partir de sus nombres y debe confirmarse.
- Las direcciones IP pueden corresponder a infraestructura compartida de CDN o de proveedores externos.
- Los resultados de Shodan InternetDB no constituyen una auditoría completa de seguridad.
- No se ha confirmado un patrón válido de correo corporativo ni la identidad de empleados.
- Debe comprobarse el alcance oficial de HackerOne antes de seleccionar activos para una fase activa.
- No se han confirmado vulnerabilidades durante esta fase de reconocimiento.

## 7. Índice de trazabilidad

| Información del mapa | Entrada de `cuaderno.md` | Evidencias |
|---|---|---|
| Organización registrante, registrador y fechas | 1. Registro del dominio — WHOIS | `whois.png`, `whois2.png`, `whois3.png`, `whois4.png`, `whois5.png` |
| Registros MX, DMARC, NS y TXT | 2. Consulta de registros DNS — dig | `dig-mx.png`, `dig-dmarc.png`, `dig-ns.png`, `dig-txt.png` |
| Subdominios, direcciones IP y proveedores observados | 2.1. Reconocimiento DNS con DNSDumpster | `dnsdumpster.png`, `dnsdumpster2.png`, `dnsdumpster3.png`, `dnsdumpster4.png` |
| Subdominios encontrados por fuentes públicas | 3. Enumeración de subdominios — Subfinder | `subfinder1.png`, `subfinder2.png` |
| Hosting Amazon/AS16509, reverse DNS AWS Global Accelerator, DNSSEC y TLS DigiCert/h2/PFS | 4. Huella tecnológica — Netcraft | `netcraft.png`, `netcraft2.png`, `netcraft3.png`, `netcraft4.png` |
| Directivas de rastreo | 5. Ficheros públicos — robots.txt | `robots.png`, `robots2.png`, `robots3.png` |
| Recurso público de seguridad | 6. Fichero de seguridad — security.txt | `security.png` |
| IP, CDN y puertos registrados | 7. Servicios expuestos — InternetDB de Shodan | `internetdb.png`, `shodan.png` |
| Resultados de `site:airbnb.com filetype:pdf`, `filetype:docx` y `site:airbnb.com security` | 8. Búsquedas avanzadas — Google dorks | `googledorks-pdf.png`, `googledork-docx.png`, `googledorks-security.png` |
| TheHarvester: cero correos/IP; Hunter.io: 4.814 resultados, incluidos 4.533 perfiles y 421 decision makers según interfaz | 9. Búsqueda de correos — theHarvester y Hunter.io | `harvester.png`, `hunterio.png`, `hunter.png`, `hunter-datos.png`, `correo-alternativa.png` |

