# Guía rápida de AWS

## Conexión SSH a EC2

```console
ssh -i "archivo_claves" usuario@IP
```

## Subida de archivos a EC2 por SSH

```console
scp -i "archivo_claves" "archivo" usuario@IP:directorio
```
