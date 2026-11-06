
# Know Your Target — Reconocimiento pasivo

## Autor

- **Nombre:** Gonzalo García Vega
- **Formación:** Curso de Especialización en Ciberseguridad
- **Centro:** IES Rafael Alberti

## Objetivo seleccionado: Airbnb

El objetivo elegido para este proyecto es Airbnb, utilizando como referencia su programa público de divulgación de vulnerabilidades en HackerOne.

- **Programa HackerOne:** [Airbnb](https://hackerone.com/airbnb)
- **Dominio del reconocimiento manual:** `airbnb.com`
- **Dominio utilizado por el agente:** `airbnb.es`

El objetivo del proyecto es realizar un reconocimiento pasivo de la superficie de exposición pública de Airbnb, utilizando técnicas OSINT y comparando los resultados manuales con los obtenidos mediante un agente de inteligencia artificial.

## Documentación del proyecto

### Parte 1 — Reconocimiento manual

- [Alcance del reconocimiento](./alcance.md)
- [Scope en formato TXT](./scope.txt)
- [Cuaderno de trabajo](./cuaderno.md)
- [Mapa de superficie](./mapa.md)

### Parte 2 — Agente de inteligencia artificial

- [Instrucciones del agente](./agente/instrucciones.md)
- [Herramientas implementadas](./agente/src/tus_herramientas.py)
- [Informe generado por el agente](./agente/informe.md)
- [Pruebas del agente](./agente/pruebas.md)
- [Traza de ejecución](./agente/traza.jsonl)

### Parte 3 — Análisis comparativo

- [Comparativa entre reconocimiento manual y agente IA](./comparativa.md)