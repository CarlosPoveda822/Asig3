from pymongo import MongoClient
from bson.objectid import ObjectId
import re

client = MongoClient('mongodb://localhost:27017/')
db = client['RecetaDB']
recetas_collection = db['recetas']

def agregar_receta(nombre, ingredientes, pasos):
    if not nombre or not ingredientes or not pasos:
        print("Todos los campos son obligatorios.")
        return

    nueva_receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }
    try:
        recetas_collection.insert_one(nueva_receta)
        print("Receta agregada exitosamente.")
    except Exception as e:
        print(f"Error al agregar la receta: {e}")

def actualizar_receta(id_receta, nombre, ingredientes, pasos):
    if not nombre or not ingredientes or not pasos:
        print("Todos los campos son obligatorios.")
        return

    try:
        result = recetas_collection.update_one(
            {"_id": ObjectId(id_receta)},
            {"$set": {"nombre": nombre, "ingredientes": ingredientes, "pasos": pasos}}
        )
        if result.matched_count:
            print("Receta actualizada exitosamente.")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print(f"Error al actualizar la receta: {e}")

def eliminar_receta(id_receta):
    try:
        result = recetas_collection.delete_one({"_id": ObjectId(id_receta)})
        if result.deleted_count:
            print("Receta eliminada exitosamente.")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print(f"Error al eliminar la receta: {e}")

def ver_listado_recetas():
    try:
        recetas = recetas_collection.find()
        if recetas_collection.count_documents({}) > 0:
            for receta in recetas:
                print(f"ID: {receta['_id']}, Nombre: {receta['nombre']}")
        else:
            print("No hay recetas en la base de datos.")
    except Exception as e:
        print(f"Error al obtener el listado de recetas: {e}")

def buscar_receta_por_ingredientes(ingredientes):
    try:
        regex = re.compile(ingredientes, re.IGNORECASE)
        recetas = recetas_collection.find({"ingredientes": regex})
        if recetas_collection.count_documents({"ingredientes": regex}) > 0:
            for receta in recetas:
                print(f"Nombre: {receta['nombre']}")
                print(f"Ingredientes: {receta['ingredientes']}")
                print(f"Pasos: {receta['pasos']}")
                print()
        else:
            print("No se encontraron recetas con esos ingredientes.")
    except Exception as e:
        print(f"Error al buscar recetas por ingredientes: {e}")

def buscar_receta_por_pasos(pasos):
    try:
        regex = re.compile(pasos, re.IGNORECASE)
        recetas = recetas_collection.find({"pasos": regex})
        if recetas_collection.count_documents({"pasos": regex}) > 0:
            for receta in recetas:
                print(f"Nombre: {receta['nombre']}")
                print(f"Ingredientes: {receta['ingredientes']}")
                print(f"Pasos: {receta['pasos']}")
                print()
        else:
            print("No se encontraron recetas con esos pasos.")
    except Exception as e:
        print(f"Error al buscar recetas por pasos: {e}")

def main():
    try:
        while True:
            print("\n--- Menú ---")
            print("a) Agregar nueva receta")
            print("b) Actualizar receta existente")
            print("c) Eliminar receta existente")
            print("d) Ver listado de recetas")
            print("e) Buscar recetas por ingredientes")
            print("f) Buscar recetas por pasos")
            print("g) Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == 'a':
                nombre = input("Nombre de la receta: ")
                ingredientes = input("Ingredientes (separados por comas): ")
                pasos = input("Pasos de la receta: ")
                agregar_receta(nombre, ingredientes, pasos)
            elif opcion == 'b':
                id_receta = input("ID de la receta a actualizar: ")
                nombre = input("Nuevo nombre de la receta: ")
                ingredientes = input("Nuevos ingredientes (separados por comas): ")
                pasos = input("Nuevos pasos de la receta: ")
                actualizar_receta(id_receta, nombre, ingredientes, pasos)
            elif opcion == 'c':
                id_receta = input("ID de la receta a eliminar: ")
                eliminar_receta(id_receta)
            elif opcion == 'd':
                ver_listado_recetas()
            elif opcion == 'e':
                ingredientes = input("Ingrese los ingredientes a buscar: ")
                buscar_receta_por_ingredientes(ingredientes)
            elif opcion == 'f':
                pasos = input("Ingrese los pasos a buscar: ")
                buscar_receta_por_pasos(pasos)
            elif opcion == 'g':
                print("Adios owo/")
                break
            else:
                print("Opción no válida.")
    finally:
        client.close()

if __name__ == "__main__":
    main()