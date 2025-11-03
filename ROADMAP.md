# ArgDigest — Argument Auditing and Normalization Library

## 🧩 Definición del proyecto

**ArgDigest** es una librería ligera y extensible para **auditar, validar y normalizar argumentos de entrada** en funciones y métodos científicos.

Su propósito es proporcionar una infraestructura genérica que:
- Verifique la **coherencia y tipo** de los argumentos.
- **Coercione** objetos heterogéneos hacia las formas internas esperadas.
- Aplique **reglas semánticas** definidas por el dominio (p. ej. topografía, sistemas moleculares).
- Genere **mensajes claros y consistentes** de error y advertencia.
- Permita **reutilizar y compartir** pipelines de validación entre diferentes librerías (MolSysMT, TopoMT, etc.).

ArgDigest surge a partir del decorador `@digest` desarrollado originalmente para **MolSysMT** y posteriormente utilizado en **TopoMT**, con la idea de aislar su funcionalidad en un proyecto independiente, bien documentado y con interfaz estable.

---

## ⚙️ Objetivos principales

1. **Core agnóstico del dominio**
   - No asumir conocimiento de moléculas, features, ni estructuras específicas.
   - Orquestar pipelines de *coerción* y *validación* configurables por nombre o tipo.

2. **Extensibilidad modular**
   - Permitir que cada librería registre sus propias reglas mediante *plugins* o *registries*.
   - Soportar validadores contextuales (`link.child→parent`, `selection.atom→group`).

3. **Integración fluida con tipado moderno**
   - Compatibilidad con `TypeAlias`, `Literal`, `Protocol`.
   - Uso opcional de `beartype` o `pydantic` para enforcement en runtime.

4. **Mensajería y trazabilidad**
   - Sistema de errores estandarizado con contexto: función, argumento, valor, sugerencia.
   - Logging opcional y modo “profiling” para auditoría masiva.

5. **Desacoplamiento y rendimiento**
   - Zero-dependency core (solo `typing`, `inspect`, `dataclasses`).
   - Capas opcionales (`contrib`) para ecosistemas específicos (beartype, pydantic, attrs).

---

## 🏗️ Estructura inicial del paquete

```
argdigest/
  __init__.py
  core/
    decorator.py        # implementación de @digest y @digest.map
    registry.py         # registro global de pipelines y validadores
    context.py          # encapsula información de llamada (función, arg, valor)
    errors.py           # jerarquía de excepciones uniformes
    utils.py            # binding de argumentos, helpers comunes
  pipelines/
    base_coercers.py    # coerciones genéricas (dict→obj, normalización de strings)
    base_validators.py  # validadores simples (tipos, dominios, unicidad)
  contrib/
    beartype_support.py # integración opcional con beartype
    pydantic_support.py # integración opcional con pydantic v2
    attrs_support.py    # integración opcional con attrs/cattrs
tests/
  ...
docs/
  index.md
  api_reference.md
  examples/
```

---

## 🔧 API principal (boceto)

### Decorador básico

```python
from argdigest import digest

@digest(kind="feature")
def register_feature(feature):
    ...
```

### Decorador con mapeo por argumento

```python
@digest.map(
    feature={"kind": "feature", "rules": ["feature.base", "shape.consistency"]},
    parent={"kind": "feature", "rules": ["topology.is_2d"]}
)
def link(feature, parent, topo):
    ...
```

### Registro de pipelines

```python
from argdigest import registry, pipeline

@pipeline(kind="feature")
def coerce_feature(obj, ctx):
    """Convierte un dict o dataclass en un objeto Feature válido."""
    ...

@pipeline(kind="feature", name="topology.shape_consistency")
def validate_shape(obj, ctx):
    """Valida compatibilidad entre shape_type y dimensionalidad."""
    ...
```

---

## 🧱 Jerarquía de errores

| Clase | Descripción |
|:--|:--|
| `DigestError` | Base de todas las excepciones de ArgDigest. |
| `DigestTypeError` | Tipo de dato inesperado o incoherente. |
| `DigestValueError` | Valor fuera de dominio o inválido. |
| `DigestInvariantError` | Violación de regla semántica (p. ej. relación padre-hijo). |
| `DigestCoercionWarning` | Advertencia de coerción automática o silenciosa. |

Cada error incluirá:
- `context.function`: nombre de la función donde ocurrió.
- `context.argname`: nombre del argumento.
- `context.value_repr`: representación resumida del valor.
- `hint`: sugerencia de corrección o causa probable.

---

## 🔌 Integración con ecosistemas

| Integración | Propósito |
|:-------------|:-----------|
| **beartype** | Validar tipos en runtime según anotaciones (`@beartype` opcional). |
| **pydantic v2** | Validar y parsear DTOs (inputs externos). |
| **attrs/cattrs** | Conversiones rápidas dict↔objeto en pipelines. |
| **numpy/pandas** (futuro) | Coerción de arrays y tablas a secuencias o DataFrames validados. |

---

## ⚙️ Uso típico en librerías científicas

### En MolSysMT
```python
@digest.map(
    molecular_system={"kind": "molecular_system"},
    selection={"kind": "selection"}
)
def get_n_atoms(molecular_system, selection='all'):
    ...
```

### En TopoMT
```python
@digest.map(
    child={"kind": "feature", "rules": ["parent_child.mouth_concavity"]},
    parent={"kind": "feature", "rules": ["is_2d"]}
)
def link(child, parent, topo):
    ...
```

---

## 🧭 Roadmap de desarrollo

| Fase | Objetivos | Entregables |
|:------|:-----------|:-------------|
| **v0.1 (Prototype)** | Decorador `@digest` funcional + registry básico | Pipeline mínimo, ejemplos, tests unitarios |
| **v0.2** | Sistema de errores con contexto + logging | Excepciones enriquecidas, reporting |
| **v0.3** | Integración opcional con `beartype` y `pydantic` | Módulos `contrib/` con tests de compatibilidad |
| **v0.4** | Documentación y ejemplos en MolSysMT / TopoMT | Carpeta `docs/`, notebooks ilustrativos |
| **v1.0** | API estable + cobertura >90% + publicación PyPI/conda-forge | Release 1.0.0, semver, CI completo |

---

## 📦 Publicación y licencia

- **Nombre del paquete**: `argdigest`
- **Licencia**: BSD-3 o Apache-2.0 (coherente con UIBCDF).
- **Repositorio GitHub**: `uibcdf/argdigest`
- **Distribución**:
  - `PyPI` (wheels y sdist)
  - `conda-forge` (meta.yaml con tests)
- **CI/CD**:
  - GitHub Actions: lint (ruff), type-check (mypy/pyright), test (pytest), build/publish.
  - Codecov: cobertura mínima 85%.

---

## 💡 Ideas futuras

- Modo **profiling**: recolectar estadísticas de coerción y errores en tiempo de ejecución.
- Validaciones declarativas (`YAML`/`JSONSchema` → pipelines).
- Integración con **Sphinx** para generar documentación de validación automáticamente.
- Hooks para **deshacer coerciones** o revertir transformaciones.
- CLI minimal para auditar scripts (`argdigest audit script.py`).

---

## ✨ Tagline final

> **ArgDigest** — the lightweight, extensible toolkit to audit, coerce and validate function arguments across scientific libraries.
