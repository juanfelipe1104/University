import ODM as ODM

if __name__ == '__main__':
    # Inicializar base de datos y modelos con initApp
    ODM.initApp(db_name="practica1")
    
    # Borrar datos anteriores
    for persona in ODM.Persona.find({}):
        persona.delete()
    
    #Ejemplo
    p1 = ODM.Persona(nombre="Pablo", direccion="Calle de Alcalá, Madrid", dni="12345678A", edad = 30)
    p2 = ODM.Persona(nombre="Ana", dni="87654321B", edad = 25)
    p3 = ODM.Persona(nombre="Luis", dni="11223344C", edad = 40)

    # Inserta en base de datos
    p1.save()           
    p2.save()
    p3.save()
    # Update
    p1.nombre = "Pedro"
    p1.save()
    p2.edad = 20
    p2.save()
    p3.dni = "44332211D"
    p3.save()

    # Busqueda
    for persona in ODM.Persona.find({"nombre": "Pedro"}):
        print(persona.nombre, persona.direccion, persona.dni, persona.edad, persona.direccion_loc)
    
    print(p2._id, p2.nombre, p2.dni, p2.edad)
    print(p3._id, p3.nombre, p3.dni, p3.edad)
    # Intento de acceso a atributo no existente
    try:
        print(p1.casa) # AttributeError
    except AttributeError:
        pass

    # Quitar atributo a documento (unset)
    p3.dni = ""
    p3.save()
    print(p3._data)

    # Volver a añadir atributo
    p3.dni = "11223344C"
    p3.save()
    print(p3._data)
        