ChileUP.py es una herramienta escrita en Python que, a partir de una lista de URLs, determina si cada sitio web se encuentra operativo (UP) o inactivo (DOWN). Para ello, utiliza el comando `curl` con un tiempo de espera (timeout) de 10 segundos y un User-Agent configurado como si se tratara del navegador Google Chrome.

El script aprovecha el módulo `concurrent.futures` para lanzar varias peticiones en paralelo, acelerando el proceso de verificación cuando la lista de URLs es grande. Cada petición obtiene y almacena el tiempo total de respuesta proporcionado por `curl`.

Durante la ejecución, se muestran en la consola los resultados de cada URL de forma inmediata (conforme se van completando las solicitudes), pero al final se genera un archivo de salida en el que las URL se ordenan de forma que primero aparezcan las que están DOWN, seguidas de las que están UP.

**Principales características**  
- Verificación concurrente (multi-hilo) con `ThreadPoolExecutor` para mayor eficiencia.  
- Inclusión de un User-Agent de Chrome y un timeout de 10 segundos.  
- Muestra el tiempo de respuesta (`%{time_total}`) que indica el tiempo que tardó `curl` en completar la solicitud.  
- Resultados impresos en tiempo real y ordenados (DOWN primero) en el archivo de salida.

**Modo de uso**  
```bash
python ChileUP.py -l lista.txt -o output.txt
```
- `-l, --lista`: archivo con la lista de URLs (una por línea).  
- `-o, --out`: archivo de salida donde se guardarán los resultados.

**Ejemplo de output** (con las URLs DOWN primero y luego las UP):
```
www.subtel.gob.cl DOWN 0.000
www.esval.cl DOWN 0.000
www.demre.cl UP 0.047599
www.contraloria.cl UP 0.054257
www.defensa.cl UP 0.057681
www.cne.cl UP 0.073941
www.bancoestado.cl UP 0.077870
www.aguasantofagasta.cl UP 0.119422
www.cmfchile.cl UP 0.102030
www.dpp.cl UP 0.047557
www.efe.cl UP 0.050830
www.enap.cl UP 0.047126
www.carabineros.cl UP 0.214402
```
