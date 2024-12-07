# General

| **Campo** | **Valor** | **Descripción** |
| --- | --- | --- |
| Propósito | Permite Consultar Roles. |
| Recurso | [GET]/roles| Un recurso está asociado al objeto o entidad que se requiere consultar, modificar, actualizar o eliminar. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). | 
| Sub-recurso | NA | Un sub-recurso tiene relación con respecto a un recurso, se puede interpretar como un parte-todo de un objeto. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). |

# Petición
### Query Parameter
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| id | String | NA | Identificador del usuario | Opcional |
| name | String | NA | Nombre | Opcional |

# Respuesta
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| status | Boolean | true | Estado | Obligatorio |
| msg | String | Operación Exitosa | Mensaje | Obligatorio |
| code | Integer | 200 | Codigo | Obligatorio |
| rolList | [Role[]](#role) | NA | Lista de roles | Obligatorio |
| general | [GeneralInfo](#generalinfo) |  NA | Objeto general | Opcional |

# Definiciones

## role

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| id | String | NA | Identificador | Obligatorio |
| name | String | NA | Nombre | Obligatorio |

## GeneralInfo

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| code | number | 100 | Código | Opcional |
| product | string | iPhone 15  | Producto | Opcional |
| operation | string |  |  | Obligatorio |
| mode | string |  |  | Opcional |
| plan | string |  |  | Opcional |
| message | string |  |  | Obligatorio |
| date | string($date-time) |  |  | Obligatorio |