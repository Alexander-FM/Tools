# General

| **Campo** | **Valor** | **Descripción** |
| --- | --- | --- |
| Propósito | Eliminar un campo de integración existente de la base de datos | Describir el objetivo por el cual se necesita esta nueva operación de la API. |
| Recurso | campos | Un recurso está asociado al objeto o entidad que se requiere consultar, modificar, actualizar o eliminar. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). | 
| Identificador | id | Identificador del recurso. |
| Sub-recurso |  | Un sub-recurso tiene relación con respecto a un recurso, se puede interpretar como un parte-todo de un objeto. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). |

# Petición

### Query Parameter
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| accountId | string | 60131dc4c8c36c0069797992 | ID del usuario que realiza la acción | Obligatorio |

# Respuesta

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** |
| --- | --- | --- | --- |
| success | boolean | true | Indica si la operación fue exitosa |

# Errores
| **Código error TdP** | **Código Backend** | **Descripción Backend** |
| --- | --- | --- |
| SVC0001 | NA | Generic Client Error. |
| SVC1000 | NA | Missing mandatory parameter. |
| SVC1006 | NA | Not existing Resource Id. |
| SVR1000 | NA | Generic Server Fault. |
| SEC1001 | NA | Unauthenticated request. |
