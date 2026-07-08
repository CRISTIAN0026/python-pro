"""
Adivina el Número - Juego web hecho con Flask
------------------------------------------------
El usuario elige una dificultad, el servidor genera un número
secreto y el jugador debe adivinarlo recibiendo pistas
("muy alto" / "muy bajo") en cada intento.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import random

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-secreta-cambiar-en-produccion")

# Configuración de cada nivel de dificultad: rango de números e intentos permitidos
DIFICULTADES = {
    "facil": {"nombre": "Fácil", "rango": 50, "intentos": 10},
    "normal": {"nombre": "Normal", "rango": 100, "intentos": 8},
    "dificil": {"nombre": "Difícil", "rango": 200, "intentos": 6},
}

# Ranking simple en memoria (se reinicia si se reinicia el servidor)
ranking = []


@app.route("/")
def inicio():
    """Página principal: elegir la dificultad y ver el ranking de mejores partidas."""
    top_ranking = sorted(ranking, key=lambda x: x["intentos"])[:5]
    return render_template("inicio.html", dificultades=DIFICULTADES, ranking=top_ranking)


@app.route("/jugar/<dificultad>")
def jugar(dificultad):
    """Inicia una partida nueva guardando el estado en la sesión del usuario."""
    if dificultad not in DIFICULTADES:
        flash("Esa dificultad no existe.")
        return redirect(url_for("inicio"))

    config = DIFICULTADES[dificultad]
    session["numero_secreto"] = random.randint(1, config["rango"])
    session["intentos_usados"] = 0
    session["intentos_max"] = config["intentos"]
    session["rango_max"] = config["rango"]
    session["dificultad"] = dificultad
    session["terminado"] = False
    session["historial"] = []

    return redirect(url_for("juego"))


@app.route("/juego", methods=["GET", "POST"])
def juego():
    """Pantalla del juego: procesa cada intento enviado por el jugador."""
    if "numero_secreto" not in session:
        flash("Primero elige una dificultad para empezar a jugar.")
        return redirect(url_for("inicio"))

    mensaje = None
    ganado = False

    if request.method == "POST" and not session.get("terminado"):
        valor = request.form.get("numero", "")

        if not valor.isdigit():
            flash("Ingresa solo números enteros positivos.")
            return redirect(url_for("juego"))

        intento = int(valor)
        session["intentos_usados"] += 1
        historial = session.get("historial", [])

        if intento == session["numero_secreto"]:
            ganado = True
            session["terminado"] = True
            mensaje = f"¡Correcto! El número era {intento}."
            ranking.append({
                "dificultad": DIFICULTADES[session["dificultad"]]["nombre"],
                "intentos": session["intentos_usados"],
            })
            historial.append({"valor": intento, "pista": "¡Acertaste!"})

        elif session["intentos_usados"] >= session["intentos_max"]:
            session["terminado"] = True
            mensaje = f"Te quedaste sin intentos. El número era {session['numero_secreto']}."
            historial.append({"valor": intento, "pista": "Sin más intentos"})

        elif intento < session["numero_secreto"]:
            mensaje = "El número secreto es MAYOR que tu intento."
            historial.append({"valor": intento, "pista": "Muy bajo ⬆️"})

        else:
            mensaje = "El número secreto es MENOR que tu intento."
            historial.append({"valor": intento, "pista": "Muy alto ⬇️"})

        session["historial"] = historial
        session.modified = True

    intentos_restantes = session["intentos_max"] - session["intentos_usados"]

    return render_template(
        "juego.html",
        mensaje=mensaje,
        ganado=ganado,
        terminado=session.get("terminado", False),
        intentos_usados=session["intentos_usados"],
        intentos_restantes=intentos_restantes,
        rango_max=session["rango_max"],
        dificultad=DIFICULTADES[session["dificultad"]]["nombre"],
        dificultad_clave=session["dificultad"],
        historial=session.get("historial", []),
    )


@app.route("/reiniciar")
def reiniciar():
    """Borra la partida actual guardada en la sesión y vuelve al inicio."""
    claves = ["numero_secreto", "intentos_usados", "intentos_max",
              "rango_max", "dificultad", "terminado", "historial"]
    for clave in claves:
        session.pop(clave, None)
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
