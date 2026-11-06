"""Herramientas iniciales de reconocimiento. AQUÍ PUEDES AÑADIR LAS TUYAS.

WHOIS (whois.py), DNS y crt.sh ya están implementadas y activas en lanzar.py.
DNS y crt.sh proceden de la solución del profesor (herramientas/recon.py).

Para ampliar: una tarea por función, @protegida, sin shell, con timeout,
salida recortada, errores como texto y resultados filtrados por el alcance.
Importa tu nueva función en lanzar.py y añádela a HERRAMIENTAS.

Ideas: subdominios_subfinder, wayback_urls, correos (theHarvester / hunter.io),
infraestructura_ip, correo_postura (SPF/DMARC/MTA-STS/CAA), urlscan, shodan_host.
"""

import json
import subprocess
import urllib.parse
import urllib.request
import os
import re
import ipaddress

from guard import protegida, filtrar
from whois import recortar

UA = "aap-recon/1.0 (educativo; IES Rafael Alberti)"
TIPOS_DNS = {"A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"}


def _http(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


@protegida(objetivo="dominio")
def dns_registros(dominio: str, tipo: str = "A") -> str:
    """Consulta registros DNS de un dominio. tipo: A, AAAA, MX, NS, TXT, CNAME o SOA.
    Devuelve los valores, uno por línea."""
    tipo = tipo.upper()
    if tipo not in TIPOS_DNS:
        return f"ERROR: tipo DNS no válido ({tipo}). Usa uno de: {', '.join(sorted(TIPOS_DNS))}."
    try:
        r = subprocess.run(["dig", "+short", tipo, dominio],
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar dig: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: dig falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"Sin registros {tipo} para {dominio}."


@protegida(objetivo="dominio")
def subdominios_crtsh(dominio: str) -> str:
    """Enumera subdominios de un dominio por transparencia de certificados (crt.sh).
    Pasivo: no toca el objetivo. Devuelve solo los subdominios dentro del alcance."""
    url = f"https://crt.sh/?q=%25.{urllib.parse.quote(dominio)}&output=json"
    try:
        datos = json.loads(_http(url, timeout=90))
    except Exception as e:
        return (f"ERROR: crt.sh no respondió ({e}). crt.sh suele ir lento; "
                "puedes reintentar más tarde o añadir otra fuente de subdominios.")
    if not isinstance(datos, list) or any(
        not isinstance(fila, dict) or not isinstance(fila.get("name_value"), str)
        for fila in datos
    ):
        return "ERROR: crt.sh devolvió un formato de certificados inesperado."
    nombres = set()
    for fila in datos:
        for n in str(fila.get("name_value", "")).splitlines():
            n = n.strip().lstrip("*.").lower()
            if n:
                nombres.add(n)
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))


@protegida(objetivo="dominio")
def subdominios_subfinder(dominio: str) -> str:
    """Enumera subdominios mediante Subfinder utilizando
    fuentes OSINT pasivas. Devuelve únicamente los resultados
    que pertenecen al alcance definido."""

    try:
        r = subprocess.run(
            ["subfinder", "-d", dominio, "-silent"],
            capture_output=True,
            text=True,
            timeout=120
        )
    except subprocess.TimeoutExpired:
        return "ERROR: Subfinder superó el tiempo máximo de 120 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar Subfinder: {e}")

    if r.returncode != 0:
        return recortar(
            f"ERROR: Subfinder falló ({r.returncode}): "
            f"{r.stderr.strip() or 'sin detalles'}"
        )

    nombres = {
        linea.strip().lower().rstrip(".")
        for linea in r.stdout.splitlines()
        if linea.strip()
    }

    dentro, fuera = filtrar(sorted(nombres))

    cabecera = (
        f"{len(dentro)} subdominios encontrados en alcance "
        f"({fuera} filtrados por estar fuera):\n"
    )

    return recortar(cabecera + "\n".join(dentro))

@protegida(objetivo="dominio")
def robots_txt(dominio: str) -> str:
    """Consulta el fichero robots.txt y extrae sus directivas."""

    url = f"https://{dominio}/robots.txt"

    try:
        contenido = _http(url, timeout=20)
    except Exception as e:
        return recortar(f"ERROR: no se pudo consultar robots.txt: {e}")

    lineas = [
        linea.strip()
        for linea in contenido.splitlines()
        if linea.strip() and not linea.strip().startswith("#")
    ]

    return recortar(
        f"Robots.txt de {dominio}:\n" + "\n".join(lineas)
    )

@protegida(objetivo="dominio")
def security_txt(dominio: str) -> str:
    """Consulta security.txt en sus ubicaciones estándar."""

    rutas = [
        "/.well-known/security.txt",
        "/security.txt"
    ]

    for ruta in rutas:
        try:
            contenido = _http(
                f"https://{dominio}{ruta}",
                timeout=20
            )

            return recortar(
                f"security.txt encontrado en {ruta}:\n{contenido}"
            )

        except Exception:
            continue

    return f"No se encontró security.txt para {dominio}."

@protegida(objetivo="dominio")
def shodan_internetdb(dominio: str) -> str:
    """Consulta información pública de Shodan InternetDB
    para las direcciones IPv4 del dominio."""

    try:
        r = subprocess.run(
            ["dig", "+short", "A", dominio],
            capture_output=True,
            text=True,
            timeout=15
        )
    except subprocess.TimeoutExpired:
        return "ERROR: timeout consultando DNS."
    except OSError as e:
        return recortar(f"ERROR: {e}")

    ips = set()

    for linea in r.stdout.splitlines():
        try:
            ip = ipaddress.ip_address(linea.strip())
            if isinstance(ip, ipaddress.IPv4Address):
                ips.add(str(ip))
        except ValueError:
            continue

    if not ips:
        return f"No se encontraron IPs IPv4 para {dominio}."

    resultados = []

    for ip in sorted(ips)[:5]:
        try:
            datos = json.loads(
                _http(
                    f"https://internetdb.shodan.io/{ip}",
                    timeout=20
                )
            )

            resultados.append(
                f"IP: {ip}\n"
                f"Hostnames: {datos.get('hostnames', [])}\n"
                f"Puertos: {datos.get('ports', [])}\n"
                f"Etiquetas: {datos.get('tags', [])}\n"
                f"Vulnerabilidades: {datos.get('vulns', [])}"
            )

        except Exception as e:
            resultados.append(f"IP {ip}: ERROR: {e}")

    return recortar("\n\n".join(resultados))


@protegida(objetivo="dominio")
def wayback_urls(dominio: str) -> str:
    """Obtiene URLs históricas mediante Wayback Machine.
    Devuelve únicamente URLs cuyos hosts están en alcance."""

    parametros = urllib.parse.urlencode({
        "url": f"*.{dominio}/*",
        "output": "json",
        "fl": "original",
        "filter": "statuscode:200",
        "collapse": "urlkey",
        "limit": "500"
    })

    url = f"https://web.archive.org/cdx/search/cdx?{parametros}"

    try:
        datos = json.loads(_http(url, timeout=60))
    except Exception as e:
        return recortar(f"ERROR consultando Wayback Machine: {e}")

    if not isinstance(datos, list):
        return "ERROR: respuesta inesperada de Wayback Machine."

    urls = set()

    for fila in datos[1:]:
        if isinstance(fila, list) and fila:
            valor = fila[0]

            try:
                host = urllib.parse.urlparse(valor).hostname
                if host:
                    urls.add((host.lower(), valor))
            except ValueError:
                continue

    hosts = sorted({host for host, _ in urls})
    dentro, fuera = filtrar(hosts)
    permitidos = set(dentro)

    resultados = sorted(
        url for host, url in urls if host in permitidos
    )

    return recortar(
        f"Wayback Machine: {len(resultados)} URLs en alcance "
        f"({fuera} hosts filtrados).\n"
        + "\n".join(resultados)
    )

@protegida(objetivo="dominio")
def correo_postura(dominio: str) -> str:
    """Comprueba registros públicos de seguridad del dominio:
    SPF, DMARC, MTA-STS y CAA."""

    consultas = {
        "SPF": ("TXT", dominio),
        "DMARC": ("TXT", f"_dmarc.{dominio}"),
        "MTA-STS": ("TXT", f"_mta-sts.{dominio}"),
        "CAA": ("CAA", dominio),
        "MX": ("MX", dominio)
    }

    resultados = []

    for nombre, (tipo, host) in consultas.items():
        try:
            r = subprocess.run(
                ["dig", "+short", tipo, host],
                capture_output=True,
                text=True,
                timeout=15
            )

            if r.returncode != 0:
                resultados.append(
                    f"{nombre}: ERROR {r.stderr.strip()}"
                )
                continue

            valores = r.stdout.strip()

            if nombre == "SPF":
                valores = "\n".join(
                    linea for linea in valores.splitlines()
                    if "v=spf1" in linea.lower()
                )

            resultados.append(
                f"{nombre} ({host}):\n"
                + (valores or "Sin registros encontrados.")
            )

        except subprocess.TimeoutExpired:
            resultados.append(f"{nombre}: ERROR de timeout.")
        except OSError as e:
            resultados.append(f"{nombre}: ERROR: {e}")

    return recortar(
        f"Postura de correo de {dominio}:\n\n"
        + "\n\n".join(resultados)
    )

@protegida(objetivo="dominio")
def theharvester_correos(dominio: str) -> str:
    """Busca información pública mediante theHarvester.
    Utiliza una fuente pasiva y filtra los hosts encontrados."""

    try:
        r = subprocess.run(
            [
                "theHarvester",
                "-d", dominio,
                "-b", "duckduckgo",
                "-l", "100"
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

    except subprocess.TimeoutExpired:
        return "ERROR: theHarvester superó los 120 segundos."
    except OSError as e:
        return recortar(f"ERROR ejecutando theHarvester: {e}")

    if r.returncode != 0:
        return recortar(
            f"ERROR theHarvester ({r.returncode}): "
            f"{r.stderr.strip() or 'sin detalles'}"
        )

    salida = r.stdout

    hosts = set(
        re.findall(
            r"[a-zA-Z0-9.-]+\." + re.escape(dominio),
            salida,
            re.IGNORECASE
        )
    )

    dentro, fuera = filtrar(sorted(hosts))

    correos = set(
        re.findall(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            salida
        )
    )

    # Solo correos del dominio consultado o de hosts autorizados.
    correos_validos = [
        correo for correo in correos
        if correo.lower().endswith("@" + dominio.lower())
        or correo.rsplit("@", 1)[-1].lower() in dentro
    ]

    return recortar(
        f"theHarvester para {dominio}:\n"
        f"Correos encontrados: {len(correos_validos)}\n"
        f"Hosts en alcance: {len(dentro)}\n"
        f"Hosts filtrados: {fuera}\n\n"
        "Correos:\n" + "\n".join(sorted(correos_validos))
        + "\n\nHosts:\n" + "\n".join(dentro)
    )

@protegida(objetivo="dominio")
def urlscan_busqueda(dominio: str) -> str:
    """Consulta análisis públicos existentes en urlscan.io."""

    parametros = urllib.parse.urlencode({
        "q": f"domain:{dominio}",
        "size": "100"
    })

    url = f"https://urlscan.io/api/v1/search/?{parametros}"

    try:
        datos = json.loads(_http(url, timeout=30))
    except Exception as e:
        return recortar(f"ERROR consultando urlscan: {e}")

    resultados = datos.get("results", [])

    hosts = set()
    elementos = []

    for fila in resultados:
        pagina = fila.get("page", {})
        host = pagina.get("domain", "").lower()

        if host:
            hosts.add(host)

    dentro, fuera = filtrar(sorted(hosts))
    permitidos = set(dentro)

    for fila in resultados:
        pagina = fila.get("page", {})
        host = pagina.get("domain", "").lower()

        if host in permitidos:
            elementos.append(
                f"URL: {pagina.get('url', '')}\n"
                f"Dominio: {host}\n"
                f"IP: {pagina.get('ip', 'No disponible')}\n"
                f"Fecha: {fila.get('task', {}).get('time', '')}"
            )

    return recortar(
        f"urlscan.io para {dominio}:\n"
        f"Resultados: {len(elementos)}\n"
        f"Hosts filtrados: {fuera}\n\n"
        + "\n\n".join(elementos)
    )

@protegida(objetivo="dominio")
def hunter_correos(dominio: str) -> str:
    """Consulta Hunter.io para obtener correos corporativos públicos."""

    api_key = os.environ.get("HUNTER_API_KEY")

    if not api_key:
        return "ERROR: configura la variable HUNTER_API_KEY."

    parametros = urllib.parse.urlencode({
        "domain": dominio,
        "api_key": api_key
    })

    url = f"https://api.hunter.io/v2/domain-search?{parametros}"

    try:
        datos = json.loads(_http(url, timeout=30))
    except Exception as e:
        return recortar(f"ERROR consultando Hunter.io: {e}")

    if "errors" in datos:
        return recortar(f"ERROR de Hunter.io: {datos['errors']}")

    resultados = datos.get("data", {}).get("emails", [])

    correos = sorted({
        fila.get("value", "")
        for fila in resultados
        if fila.get("value", "").lower().endswith(
            "@" + dominio.lower()
        )
    })

    return recortar(
        f"Hunter.io para {dominio}:\n"
        f"Correos encontrados: {len(correos)}\n"
        + "\n".join(correos)
    )

@protegida(objetivo="dominio")
def google_dorks(dominio: str) -> str:
    """Genera consultas Google Dorks para reconocimiento pasivo."""

    consultas = [
        f"site:{dominio}",
        f"site:{dominio} filetype:pdf",
        f"site:{dominio} filetype:docx",
        f"site:{dominio} filetype:xlsx",
        f"site:{dominio} inurl:login",
        f"site:{dominio} inurl:api",
        f"site:{dominio} security",
        f"site:{dominio} intitle:documentation",
        f"site:{dominio} filetype:txt",
        f"site:{dominio} inurl:robots.txt",
    ]

    return recortar(
        f"Google Dorks para {dominio}:\n"
        + "\n".join(consultas)
    )
