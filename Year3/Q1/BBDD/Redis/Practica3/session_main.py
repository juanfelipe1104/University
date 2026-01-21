import session as session

# Crear usuario
session.create_user("Juan Luis", "juan", "1234")

print("Login con usuario/contraseña:")
priv, token = session.login_user_password("juan", "1234")
print("privilegios:", priv, "token:", token)

print("Login con token:")
priv2 = session.login_token(token)
print("privilegios:", priv2)

print("Cambio de nombre")
session.update_user("juan", full_name="Juan Rodriguez")
print(session.get_user("juan"))

# Borrar usuario
session.delete_user("juan")