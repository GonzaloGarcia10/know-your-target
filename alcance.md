## Activos dentro y fuera del alcance

**Programa:** Airbnb Security Bug Bounty  
**Plataforma:** HackerOne  
**Política:** https://hackerone.com/airbnb/policy_scopes  
**Fecha de consulta:** 28/10/2026

### Dentro del alcance (In scope)

El activo seleccionado para este proyecto es `*.airbnb.com`, que aparece como elegible en el programa de Airbnb en HackerOne y está clasificado como *Higher Impact Scope*.

Este activo permite estudiar los subdominios cubiertos por el comodín, respetando las exclusiones y las condiciones específicas de la política.

El reconocimiento se limitará a recopilar información pública mediante técnicas pasivas, como consultar registros DNS, Certificate Transparency, información registral y fuentes públicas sobre infraestructura.

### Fuera del alcance (Out of scope)

La política identifica expresamente los siguientes dominios como no elegibles:

- `provider.demo.urbandoor.com`
- `demo.urbandoor.com`
- `admin.demo.urbandoor.com`
- `luckeyhomes.com`
- `luckey.partners`
- `luckey.in`
- `luckey.fr`
- `luckey.app`

Estos dominios no se incluirán en el reconocimiento del proyecto.

Además, no se considerarán autorizados automáticamente los dominios que simplemente estén relacionados con Airbnb. 

# Reglas del programa Airbnb Bug Bounty
 
## 1. Uso de herramientas automáticas

En la política consultada no se especifica una prohibición general del uso de herramientas automáticas. Sin embargo, se exige cumplir las reglas del programa, respetar la privacidad de los usuarios y evitar interrupciones o degradaciones del servicio.

## 2. Límites de peticiones

El programa prohíbe realizar pruebas de fuerza bruta para comprobar si determinadas API o funcionalidades tienen limitación de peticiones (*rate limiting*).

No se especifica un límite numérico general de peticiones en el texto consultado.

## 3. Contacto con empleados

El programa prohíbe la ingeniería social, incluyendo técnicas como phishing, vishing y smishing.

Además, en los requisitos específicos de HotelTonight se indica que no se deben enviar preguntas ni solicitudes de ayuda al equipo de atención al cliente durante las pruebas, ya que se considera una interrupción del servicio. Esta última regla se refiere específicamente a HotelTonight.

## 4. Identificación del investigador

La política consultada no especifica que sea obligatorio verificar la identidad del investigador para participar en el programa.

Sí indica que, al realizar pruebas, se debe proteger la privacidad y la confidencialidad de los usuarios. También recomienda incluir un encabezado personalizado en las solicitudes de prueba para identificar al investigador.
