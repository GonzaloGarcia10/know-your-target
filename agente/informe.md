# Reconocimiento Pasivo: airbnb.es

## 1. Registro del Dominio (WHOIS)

- **Estado**: No disponible. El registro .es no ofrece respuesta WHOIS ni RDAP pública. `whois_dominio`

---

## 2. Registros DNS

| Tipo | Valor | Fuente |
|------|-------|--------|
| **A** | `166.117.189.176` | `dns_registros` |
| **A** | `166.117.27.62` | `dns_registros` |
| **AAAA** | Sin registros | `dns_registros` |
| **MX** | Sin registros | `dns_registros` / `correo_postura` |
| **NS** | `dns2.p04.nsone.net.` | `dns_registros` |
| **NS** | `ns-949.awsdns-54.net.` | `dns_registros` |
| **NS** | `ns-1087.awsdns-07.org.` | `dns_registros` |
| **NS** | `dns1.p04.nsone.net.` | `dns_registros` |
| **NS** | `dns3.p04.nsone.net.` | `dns_registros` |
| **NS** | `ns-394.awsdns-49.com.` | `dns_registros` |
| **NS** | `ns-1877.awsdns-42.co.uk.` | `dns_registros` |
| **SOA** | `ns-1877.awsdns-42.co.uk. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400` | `dns_registros` |
| **CNAME** | Sin registros | `dns_registros` |
| **TXT** | `"google-site-verification=CPmQwoRuNGQMgYJnXhrlez7yrsTvWPcfeV-2AD6s03g"` | `dns_registros` |
| **TXT** | `"v=spf1 -all"` | `dns_registros` |
| **TXT** | `"facebook-domain-verification=z5t4llckztaonkyfp0vdp40ffvs2l7"` | `dns_registros` |

---

## 3. Subdominios

- **crt.sh**: Error 502 (Bad Gateway). Sin resultados obtenidos. `subdominios_crtsh`
- **Subfinder**: 0 subdominios en alcance (7 filtrados por estar fuera de scope). `subdominios_subfinder`

---

## 4. Infraestructura (Shodan InternetDB)

| IP | Hostnames relevantes | Puertos | Etiquetas | Vulnerabilidades |
|----|---------------------|---------|-----------|-----------------|
| `166.117.189.176` | `airbnb.es`, `airbnb.com`, `a333dda39e3b496ea.awsglobalaccelerator.com` + ~50 dominios airbnb.xx | 80, 443 | cloud | Ninguna |
| `166.117.27.62` | `a333dda39e3b496ea.awsglobalaccelerator.com`, `ingress.airbnb.net` | 80, 443 | cloud | Ninguna |

- `shodan_internetdb`

Ambas IPs comparten infraestructura cloud con AWS Global Accelerator.

---

## 5. Postura de Correo Electrónico

| Registro | Valor | Fuente |
|----------|-------|--------|
| **SPF** | `"v=spf1 -all"` (rechaza todo correo) | `correo_postura` / `dns_registros` |
| **DMARC** | `"v=DMARC1;p=reject;sp=reject;pct=100;rua=mailto:a4v1jq9a@ag.dmarcian.com;ruf=mailto:a4v1jq9a@fr.dmarcian.com;aspf=r;adkim=r;fo=1;ri=3600"` | `correo_postura` |
| **MTA-STS** | Sin registros | `correo_postura` |
| **CAA** | `0 issue "digicert.com"`; `0 iodef "mailto:caa-alerts@airbnb.com"` | `correo_postura` |
| **MX** | Sin registros | `correo_postura` |

**Resumen**: airbnb.es tiene una postura de correo muy restrictiva: SPF con `-all` (rechazo total), DMARC con `p=reject` y `pct=100`. No recibe correo directamente (sin MX) y no implementa MTA-STS. Los certificados deben ser emitidos por Digicert.

---

## 6. Robots.txt

Archivo presente con directivas extensas para `Googlebot` y `Bingbot`. Principales observaciones:
- **Permite**: `/calendar/ical/`, `/.well-known/amphtml/apikey.pub`
- **Bloquea**: `/account`, `/book/`, `/calendar/`, `/inbox`, `/login_with_redirect`, `/my_listings`, `/trips/upcoming`, `/users/*`, rutas API y de gestión de alojamientos.
- `robots_txt`

---

## 7. Security.txt

Archivo presente en `/.well-known/security.txt`:

| Campo | Valor |
|-------|-------|
| Contact | `https://hackerone.com/airbnb/` |
| Policy | `https://hackerone.com/airbnb#overview` |
| Hiring | `https://careers.airbnb.com/positions/?_search_input=security` |
| Preferred-Languages | `en` |
| Canonical | `https://www.airbnb.com/.well-known/security.txt` |
| Expires | `2027-06-01T04:59:00.000Z` |

- `security_txt`

---

## 8. Historial Web (Wayback Machine)

- 0 URLs en alcance. 1 host filtrado. `wayback_urls`

---

## 9. Búsqueda de Correos

| Herramienta | Resultado |
|-------------|-----------|
| **theHarvester** | 0 correos, 0 hosts en alcance | `theharvester_correos` |
| **Hunter.io** | Error: API key no configurada | `hunter_correos` |

---

## 10. Análisis en urlscan.io

- 0 resultados. 1 host filtrado. `urlscan_busqueda`

---

## 11. Google Dorks (consultas generadas)

Las siguientes consultas pueden usarse para reconocimiento adicional:

```
site:airbnb.es
site:airbnb.es filetype:pdf
site:airbnb.es filetype:docx
site:airbnb.es filetype:xlsx
site:airbnb.es inurl:login
site:airbnb.es inurl:api
site:airbnb.es security
site:airbnb.es intitle:documentation
site:airbnb.es filetype:txt
site:airbnb.es inurl:robots.txt
```

- `google_dorks`

---

## Resumen Ejecutivo

| Aspecto | Hallazgo |
|---------|----------|
| **Dominio** | `airbnb.es` — sin datos WHOIS públicos |
| **Resolución** | 2 IPs (166.117.189.176, 166.117.27.62) vía AWS Global Accelerator |
| **DNS** | NS mixtos (NS1 + AWS Route53); sin MX, sin AAAA, sin CNAME |
| **Correo** | SPF `-all`, DMARC `reject`, sin MX propio, CAA restrictivo (Digicert) |
| **Seguridad** | security.txt presente → HackerOne; políticas en inglés |
| **Subdominios** | Ninguno adicional en alcance de `airbnb.es` |
| **Infraestructura** | Cloud (AWS), puertos 80/443, sin vulnerabilidades públicas en Shodan |
| **Correos encontrados** | 0 (theHarvester); Hunter no disponible |
| **Historial** | Sin URLs Wayback ni análisis urlscan en alcance |

**Conclusiones clave**:
1. `airbnb.es` actúa como proxy/passthrough hacia la infraestructura global de Airbnb (AWS), sin servicios propios de backend (sin MX, sin subdominios propios).
2. La postura de correo es **muy restrictiva** (SPF `-all`, DMARC `reject`), lo que indica que el dominio no envía correo directamente o usa infraestructura centralizada en `airbnb.com`.
3. La superficie de ataque directa de `airbnb.es` es reducida: principalmente HTTP/S en dos IPs compartidas con decenas de otros dominios `.xx` de Airbnb.