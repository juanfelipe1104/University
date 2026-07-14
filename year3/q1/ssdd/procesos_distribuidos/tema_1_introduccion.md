# Tema 1. Introducción a los sistemas distribuidos

## Evolución de la computación distribuida

Las ideas que sustentan la computación distribuida aparecieron antes de que existieran las tecnologías necesarias para implantarlas:

- En los años cincuenta se planteó separar los grandes computadores centrales de los terminales y compartir su tiempo de cómputo entre varios usuarios.
- En los sesenta se formuló la computación como un servicio público. Douglas Parkhill describió propiedades como el acceso en línea, la elasticidad y la apariencia de un suministro ilimitado.
- En los noventa, Internet proporcionó una infraestructura de comunicaciones global y el abaratamiento del hardware impulsó los clústeres.
- En los años 2000, el *grid computing* permitió coordinar recursos heterogéneos y geográficamente dispersos.
- Desde 2006, plataformas como Amazon Web Services consolidaron el *cloud computing* y la provisión elástica de recursos como servicio.

## Modelos de computación distribuida

| Modelo | Idea principal | Control y localización de los recursos | Uso habitual |
|---|---|---|---|
| Clúster | Varios equipos trabajan como un sistema coordinado | Cercanos y normalmente bajo una misma organización | Cálculo paralelo, bases de datos, alta disponibilidad |
| *Cycle scavenging* | Aprovecha ciclos ociosos de equipos existentes | Equipos de propósito general que no siempre están disponibles | Tareas divisibles y de baja prioridad |
| Grid | Federa recursos heterogéneos de distintas ubicaciones | Distribuidos y sin un control central único | Investigación y cálculo intensivo |
| Cloud | Ofrece recursos virtualizados bajo demanda como servicio | Gestionados por un proveedor y accesibles por red | Infraestructura, plataformas y aplicaciones escalables |

### Clústeres

Un clúster agrupa computadores conectados mediante una red de altas prestaciones. Su principal ventaja es aumentar la capacidad incorporando nodos, pero presenta limitaciones:

- La instalación es dedicada y puede permanecer infrautilizada fuera de los picos de carga.
- El mantenimiento y la ampliación se vuelven costosos a gran escala.
- La escalabilidad no es ilimitada: la red, la sincronización y las partes secuenciales de los programas introducen cuellos de botella.
- Un aumento de capacidad permite abordar problemas mayores, pero siempre pueden aparecer cargas que superen los recursos disponibles.

### Grid computing

El *grid computing* permite acceder a potencia de cálculo, almacenamiento y equipos especializados geográficamente dispersos. Combina protocolos de Internet con técnicas de computación paralela y distribuida para ejecutar aplicaciones que procesan grandes cantidades de datos.

Frente a un clúster, un grid suele integrar recursos más heterogéneos, separados geográficamente y pertenecientes a distintas organizaciones.

### Cloud computing

El cloud surgió, entre otros motivos, para aprovechar mejor servidores dimensionados para picos de tráfico que permanecían ociosos gran parte del tiempo. La virtualización y la automatización permiten asignar y liberar capacidad según la demanda.

Sus ideas fundamentales son:

- recursos ofrecidos como servicio a través de la red;
- aprovisionamiento bajo demanda;
- elasticidad para adaptar la capacidad a la carga;
- uso compartido de la infraestructura;
- pago o medición en función del consumo.

El cloud no sustituye conceptualmente al clúster o al grid: puede apoyarse en grandes clústeres y emplear mecanismos desarrollados para grids, pero añade un modelo de servicio, automatización y explotación comercial.
