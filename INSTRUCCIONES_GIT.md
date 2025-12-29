# Instrucciones para Subir el Proyecto a Git

El proyecto ya está inicializado con Git y tiene todos los commits necesarios. Para subirlo a un repositorio remoto (GitHub, GitLab, Bitbucket, etc.), sigue estos pasos:

## 1. Crear un Repositorio Remoto

### GitHub
1. Ve a https://github.com y crea una cuenta (si no tienes una)
2. Haz clic en "New repository"
3. Dale un nombre al repositorio (ej: `sistema-gestion-empresas`)
4. **NO** inicialices con README, .gitignore o licencia (ya los tenemos)
5. Haz clic en "Create repository"

### GitLab
1. Ve a https://gitlab.com y crea una cuenta
2. Haz clic en "New project"
3. Selecciona "Create blank project"
4. Dale un nombre al proyecto
5. Haz clic en "Create project"

## 2. Conectar el Repositorio Local con el Remoto

Una vez creado el repositorio remoto, copia la URL del repositorio (HTTPS o SSH) y ejecuta:

```bash
# Para GitHub/GitLab con HTTPS
git remote add origin https://github.com/tu-usuario/tu-repositorio.git

# O para SSH (si tienes configuradas las claves SSH)
git remote add origin git@github.com:tu-usuario/tu-repositorio.git
```

## 3. Verificar el Remoto

```bash
git remote -v
```

Deberías ver algo como:
```
origin  https://github.com/tu-usuario/tu-repositorio.git (fetch)
origin  https://github.com/tu-usuario/tu-repositorio.git (push)
```

## 4. Subir el Código

```bash
# Subir la rama main al repositorio remoto
git push -u origin main
```

Si tu rama se llama `master` en lugar de `main`:
```bash
git branch -M main  # Renombrar la rama a main
git push -u origin main
```

## 5. Verificar

Ve a tu repositorio en GitHub/GitLab y verifica que todos los archivos estén ahí.

## Comandos Útiles

### Ver el estado del repositorio
```bash
git status
```

### Ver los commits
```bash
git log --oneline
```

### Agregar cambios y hacer commit
```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

### Ver los remotos configurados
```bash
git remote -v
```

### Cambiar la URL del remoto (si es necesario)
```bash
git remote set-url origin https://github.com/nuevo-usuario/nuevo-repo.git
```

## Notas Importantes

- **Nunca subas archivos `.env`** con información sensible (ya están en .gitignore)
- El archivo `.env.example` es solo una plantilla y es seguro subirlo
- Los `node_modules` y `venv` no se suben (están en .gitignore)
- Todos los archivos de configuración Docker están incluidos

## Estructura del Repositorio

El repositorio incluye:
- ✅ Backend completo (Django)
- ✅ Frontend completo (React)
- ✅ Configuración Docker (docker-compose.yml, Dockerfiles)
- ✅ Domain layer
- ✅ Documentación
- ✅ .gitignore configurado
- ✅ README con instrucciones

