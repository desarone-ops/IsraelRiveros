from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------------
# Helpers de validación
# ---------------------------
def validar_nota(valor):
    """Devuelve (ok, numero|mensaje_error). Rango 10..70."""
    try:
        n = float(valor)
    except (TypeError, ValueError):
        return False, "Debe ser numérico"
    if n < 10 or n > 70:
        return False, "Fuera de rango (10 a 70)"
    return True, n

def validar_asistencia(valor):
    """Devuelve (ok, numero|mensaje_error). Rango 0..100."""
    try:
        a = float(valor)
    except (TypeError, ValueError):
        return False, "Debe ser numérico"
    if a < 0 or a > 100:
        return False, "Fuera de rango (0 a 100)"
    return True, a

def mas_largos(nombres):
    """Devuelve (lista_de_nombres_mas_largos, largo)."""
    if not nombres:
        return [], 0
    max_len = max(len(n) for n in nombres)
    tops = [n for n in nombres if len(n) == max_len]
    return tops, max_len


# ---------------------------
# Rutas
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = None
    errores = {}
    datos = {"n1": "", "n2": "", "n3": "", "asistencia": ""}

    if request.method == "POST":
        # Traer valores crudos para re-llenar el formulario
        datos["n1"] = request.form.get("nota1", "").strip()
        datos["n2"] = request.form.get("nota2", "").strip()
        datos["n3"] = request.form.get("nota3", "").strip()
        datos["asistencia"] = request.form.get("asistencia", "").strip()

        ok1, n1 = validar_nota(datos["n1"])
        ok2, n2 = validar_nota(datos["n2"])
        ok3, n3 = validar_nota(datos["n3"])
        oka, a = validar_asistencia(datos["asistencia"])

        if not ok1: errores["nota1"] = n1
        if not ok2: errores["nota2"] = n2
        if not ok3: errores["nota3"] = n3
        if not oka:  errores["asistencia"] = a

        if not errores:
            promedio = round((n1 + n2 + n3) / 3, 1)
            estado = "APROBADO" if (promedio >= 40 and a >= 75) else "REPROBADO"
            resultado = {
                "promedio": promedio,
                "estado": estado
            }

    return render_template("ejercicio1.html", datos=datos, errores=errores, resultado=resultado)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    resultado = None
    datos = {"nom1": "", "nom2": "", "nom3": ""}

    if request.method == "POST":
        datos["nom1"] = request.form.get("nombre1", "").strip()
        datos["nom2"] = request.form.get("nombre2", "").strip()
        datos["nom3"] = request.form.get("nombre3", "").strip()

        nombres = [n for n in [datos["nom1"], datos["nom2"], datos["nom3"]] if n]
        if nombres:
            top, largo = mas_largos(nombres)  # puede devolver 1 o varios (empate)
            resultado = {
                "lista": top,
                "largo": largo
            }

    return render_template("ejercicio2.html", datos=datos, resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
