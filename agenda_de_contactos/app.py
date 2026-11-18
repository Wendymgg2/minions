
from flask import Flask, render_template, request, redirect, url_for, flash
from database import conectar, crear_tabla

app = Flask(__name__)

app.secret_key = "agenda_minions_secreta"

# Personajes permitidos
PERSONAJES = ["kevin", "stuart", "bob", "otto", "gru", "agnes"]

CATEGORIAS = ["Familia", "Escuela", "Trabajo", "Otro"]

# Crear la base de datos
crear_tabla()


# PAGINA PRINCIPAL
@app.route("/")
def inicio():

    conexion = conectar()

    contactos = conexion.execute("""
        SELECT * FROM contactos
        ORDER BY nombre ASC
    """).fetchall()

    conexion.close()

    return render_template(
        "index.html",
        contactos=contactos
    )


# AGREGAR CONTACTO
@app.route("/agregar", methods=["POST"])
def agregar():

    nombre = request.form["nombre"].strip()
    telefono = request.form["telefono"].strip()
    correo = request.form["correo"].strip()
    categoria = request.form["categoria"]
    avatar = request.form["avatar"]

    if not nombre or not telefono:
        flash("¡Ups! Debes escribir nombre y teléfono 🍌")
        return redirect(url_for("inicio"))

    if categoria not in CATEGORIAS:
        flash("Categoría no válida.")
        return redirect(url_for("inicio"))

    if avatar not in PERSONAJES:
        avatar = "kevin"

    conexion = conectar()

    conexion.execute("""
        INSERT INTO contactos
        (nombre, telefono, correo, categoria, avatar)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, telefono, correo, categoria, avatar))

    conexion.commit()
    conexion.close()

    flash("¡Banana! Contacto agregado correctamente 💛")

    return redirect(url_for("inicio"))


# EDITAR CONTACTO
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    conexion = conectar()

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        telefono = request.form["telefono"].strip()
        correo = request.form["correo"].strip()
        categoria = request.form["categoria"]
        avatar = request.form["avatar"]

        if not nombre or not telefono:
            conexion.close()
            flash("El nombre y teléfono son obligatorios.")
            return redirect(url_for("editar", id=id))

        if categoria not in CATEGORIAS:
            conexion.close()
            flash("Categoría no válida.")
            return redirect(url_for("editar", id=id))

        if avatar not in PERSONAJES:
            avatar = "kevin"

        conexion.execute("""
            UPDATE contactos
            SET nombre = ?,
                telefono = ?,
                correo = ?,
                categoria = ?,
                avatar = ?
            WHERE id = ?
        """, (nombre, telefono, correo, categoria, avatar, id))

        conexion.commit()
        conexion.close()

        flash("¡Contacto actualizado correctamente! 💙")

        return redirect(url_for("inicio"))

    contacto = conexion.execute("""
        SELECT * FROM contactos WHERE id = ?
    """, (id,)).fetchone()

    conexion.close()

    if contacto is None:
        flash("No encontramos ese contacto.")
        return redirect(url_for("inicio"))

    return render_template(
        "editar.html",
        contacto=contacto
    )


# ELIMINAR CONTACTO
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    conexion = conectar()

    conexion.execute("""
        DELETE FROM contactos WHERE id = ?
    """, (id,))

    conexion.commit()
    conexion.close()

    flash("¡Contacto eliminado! Hasta la próxima 🍌")

    return redirect(url_for("inicio"))


# EJECUTAR APLICACION
if __name__ == "__main__":
    app.run(debug=True)
