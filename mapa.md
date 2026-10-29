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
| `airbnb.com` | No documentada en el cuaderno | No | Dominio principal de la organización |
| `www.airbnb.com` | `96.16.88.137` | Si | Sitio web público; IP asociada a infraestructura CDN |
| `api.airbnb.com` | `23.216.132.63` | Si | Posible API del servicio |
| `callbacks.airbnb.com` | `23.44.111.31` | Si | Posible servicio de callbacks |
| `admin-staging.airbnb.com` | `34.120.23.133` | Si | Posible entorno administrativo de pruebas |
| `admin-lite-staging.airbnb.com` | `34.120.23.133` | Si | Posible servicio administrativo de pruebas |
| `community-staging.airbnb.com` | `13.248.132.14` | Si | Posible entorno de pruebas relacionado con la comunidad |
| `api.akamai-ci.airbnb.com` | `23.206.172.7` | Si | Posible servicio relacionado con API e infraestructura de Akamai |
| `api.akamai-dev.airbnb.com` | `23.50.52.251` | Si | Posible servicio de desarrollo |
| `email.airbnb.com` | `3.20.87.51` | Si | Servicio relacionado con correo electrónico |
| `o10.email.airbnb.com` | `167.89.35.182` | Si | Host relacionado con SendGrid |
| `o11.email.airbnb.com` | `50.31.32.157` | Si | Host relacionado con SendGrid |
| `de.airbnb.com` | `23.33.42.142` | Si | Posible servicio regional o en alemán |

**Criterio de alcance:** «Sí» = cubierto por *.airbnb.com o listado explícitamente en policy_scopes; «No» = no listado y fuera del comodín. El hostname está en alcance, pero la infraestructura del proveedor (Akamai, SendGrid, AWS, Google) no lo está: la política excluye activos de terceros.

Es necesario contrastar cada dominio con los activos incluidos y las exclusiones de la política vigente de HackerOne. La presencia de un nombre en DNSDumpster o Subfinder no equivale a autorización.

**Trazabilidad:** las consultas DNS se documentan en las entradas 2 y 2.1 del cuaderno; la enumeración de subdominios, en la entrada 3; y la IP de `www.airbnb.com`, en la entrada 7.

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

Se consultaron los registros MX, DMARC, NS y TXT mediante `dig`. DNSDumpster amplió la información disponible y mostró 178 registros, de los cuales se visualizaron 50 con la versión gratuita.

Entre los resultados observados:

- **Akamai:** numerosos subdominios resuelven a direcciones asociadas a su infraestructura CDN.
- **AWS:** aparecen hosts y direcciones asociados a Amazon, incluidos registros relacionados con AWS Global Accelerator.
- **Google Cloud:** algunos subdominios, como `admin-staging.airbnb.com`, aparecen asociados a una dirección identificada por DNSDumpster como infraestructura de Google Cloud.
- **Correo:** los registros MX mostrados por DNSDumpster apuntan a servidores de Google.
- **SendGrid:** aparecen los hosts `o10.email.airbnb.com` y `o11.email.airbnb.com`, asociados en los resultados a SendGrid.
- **Registros TXT:** se observaron verificaciones de servicios y una política SPF. Estos registros aportan información sobre la configuración del dominio y del correo.

Los proveedores y las direcciones observados no demuestran por sí solos que exista una configuración incorrecta o una vulnerabilidad.

**Fuentes:** entradas 2 y 2.1 del cuaderno, «Consulta de registros DNS — dig» y «Reconocimiento DNS con DNSDumpster».

### 3.3. Huella tecnológica

Se consultó el informe público de Netcraft para `airbnb.com`. La investigación documenta la consulta y las capturas, pero el cuaderno no transcribe tecnologías concretas del informe. Por tanto, no se atribuyen tecnologías adicionales sin revisar esas evidencias.

**Fuente:** entrada 4 del cuaderno, «Huella tecnológica — Netcraft».

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

La consulta de `robots.txt` de `www.airbnb.com` mostró directivas para rastreadores relacionadas con rutas de cuentas, autenticación, gestión de anuncios, pagos y reservas. Estas directivas no son controles de acceso ni pruebas de vulnerabilidad.

También se consultó un recurso de seguridad localizado a través de `airbnb.es`, que enlazaba con información de HackerOne y otros recursos relacionados con seguridad. El cuaderno señala que debe comprobarse si `airbnb.es` está incluido en el alcance autorizado.

**Fuentes:** entradas 5 y 6 del cuaderno, «Ficheros públicos — robots.txt» y «Fichero de seguridad — security.txt».

## 4. Correos y personas

### 4.1. Correos electrónicos

Se utilizó TheHarvester con fuentes de búsqueda como DuckDuckGo y Bing. En esas consultas no se obtuvieron direcciones de correo electrónico ni direcciones IP.

Como alternativa, se consultó Hunter.io y se realizó una búsqueda en Google con el operador:

`site:airbnb.com "@airbnb.com"`

Hunter.io mostró información de la organización y referencias a direcciones de correo asociadas al dominio, algunas parcialmente ocultas. Sin embargo, no se ha confirmado la validez de esas direcciones ni un patrón corporativo fiable.

DNSDumpster también mostró registros relacionados con correo, incluidos `email.airbnb.com`, `o10.email.airbnb.com` y `o11.email.airbnb.com`, y registros MX relacionados con Google.

### 4.2. Información sobre la organización

WHOIS identifica a Airbnb, Inc. como organización registrante. La investigación también localizó información pública relacionada con el programa de seguridad de Airbnb en HackerOne.

No se han documentado nombres de empleados verificados ni se ha contactado con ninguna persona. Por tanto, no se puede establecer un patrón de correo corporativo confirmado a partir de los resultados disponibles.

**Fuentes:** entradas 1, 2, 2.1 y 9 del cuaderno.

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
| Información de huella tecnológica | 4. Huella tecnológica — Netcraft | `netcraft.png`, `netcraft2.png`, `netcraft3.png`, `netcraft4.png` |
| Directivas de rastreo | 5. Ficheros públicos — robots.txt | `robots.png`, `robots2.png`, `robots3.png` |
| Recurso público de seguridad | 6. Fichero de seguridad — security.txt | `security.png` |
| IP, CDN y puertos registrados | 7. Servicios expuestos — InternetDB de Shodan | `internetdb.png`, `shodan.png` |
| Documentos públicos indexados | 8. Búsquedas avanzadas — Google dorks | `googledorks-pdf.png`, `googledork-docx.png`, `googledorks-security.png` |
| Búsqueda de correos y datos de organización | 9. Búsqueda de correos — theHarvester y Hunter.io | `harvester.png`, `correo-alternativa.png` |

