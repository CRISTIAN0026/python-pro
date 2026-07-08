# 🎯 Adivina el Número — Juego web con Flask

## Descripción

Este proyecto es un juego web sencillo llamado **"Adivina el Número"**, creado con **Flask**.
El servidor genera un número secreto dentro de un rango que depende de la dificultad
elegida, y el jugador debe adivinarlo. En cada intento recibe una pista indicando si
el número secreto es **mayor** o **menor** que su intento, hasta acertar o quedarse
sin intentos disponibles.

El proyecto usa funciones y herramientas propias de Flask (no se usan clases, ya que
es opcional según la consigna):

- `render_template()` para mostrar las páginas HTML con Jinja2.
- `request.form` para leer el número enviado por el jugador.
- `session` para guardar el estado de la partida (número secreto, intentos usados,
  historial, etc.) de forma individual para cada usuario, sin necesidad de base de datos.
- `redirect()` y `url_for()` para navegar entre rutas.
- `flash()` para mostrar mensajes de error o aviso.
- Rutas dinámicas (`/jugar/<dificultad>`) para manejar las distintas dificultades.

## Funcionalidades

- **3 niveles de dificultad**: Fácil (1-50, 10 intentos), Normal (1-100, 8 intentos)
  y Difícil (1-200, 6 intentos).
- **Pistas en cada intento**: el juego indica si hay que subir o bajar el número.
- **Historial de intentos**: se muestra la lista completa de números probados y
  el resultado de cada uno.
- **Ranking de mejores partidas**: guarda (en memoria, mientras el servidor esté
  activo) las partidas ganadas, ordenadas por menor cantidad de intentos.
- **Reinicio de partida**: se puede jugar de nuevo o volver al inicio en cualquier momento.
- **Validación de datos**: si el usuario ingresa algo que no es un número, el juego
  se lo advierte sin romperse.

## Estructura del proyecto

```
adivina_numero/
├── app.py                 # Lógica principal y rutas de Flask
├── requirements.txt        # Dependencias necesarias
├── vercel.json               # Configuración del entrypoint para Vercel
├── LEEME.md                    # Este archivo
├── templates/
│   ├── base.html            # Plantilla base compartida
│   ├── inicio.html           # Página de inicio / selección de dificultad
│   └── juego.html            # Página donde se juega
└── public/
    └── style.css             # Estilos del juego (carpeta que espera Vercel)
```

## Cómo ejecutarlo

1. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

4. Abrir el navegador en:
   ```
   http://127.0.0.1:5000
   ```

## Despliegue en Vercel

Este proyecto ya está listo para subirse a [Vercel](https://vercel.com):

1. Sube la carpeta a un repositorio de GitHub.
2. En Vercel, elige **Add New → Project** e importa el repositorio.
3. Vercel detecta Flask automáticamente (encuentra `app.py` y `Flask` en `requirements.txt`), así que no hace falta configurar nada más.
4. (Opcional) En **Settings → Environment Variables**, agrega `SECRET_KEY` con un valor propio para producción.

**Nota importante:** el ranking de mejores partidas se guarda en una lista en memoria
(`ranking = []` en `app.py`). En Vercel cada función corre de forma *serverless*
y efímera, así que el ranking **puede reiniciarse** en cualquier momento
(no hay un proceso de servidor persistente). El juego en sí funciona igual de bien;
solo el ranking no es 100% persistente en este entorno. Para que sea persistente
habría que guardar los datos en una base de datos externa (por ejemplo Vercel KV o Postgres).

## Posibles mejoras futuras

- Guardar el ranking en una base de datos (SQLite) en lugar de memoria.
- Agregar un sistema de usuarios con nombre para el ranking.
- Añadir un modo "contrarreloj".
