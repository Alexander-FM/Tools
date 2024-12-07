# General

| **Campo** | **Valor** | **Descripción** |
| --- | --- | --- |
| Propósito | Agregar un nuevo campo de integración en la base de datos | Describir el objetivo por el cual se necesita esta nueva operación de la API. |
| Recurso | campos | Un recurso está asociado al objeto o entidad que se requiere consultar, modificar, actualizar o eliminar. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). | 
| Sub-recurso | NA | Un sub-recurso tiene relación con respecto a un recurso, se puede interpretar como un parte-todo de un objeto. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). |

# Petición
### Path Parameter
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| userAccount | string | jaimito | ID del usuario que realiza la acción | Obligatorio |
| isRoot | boolean | true | Es super usuario para realizar la acción | Obligatorio |
### Query Parameter
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| accountId | string | 60131dc4c8c36c0069797992 | ID del usuario que realiza la acción | Obligatorio |
### Body Parameters
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| jiraAttribute | string | summary | Nombre del campo en Jira | Obligatorio |
| soapAttribute | string | A_CHANNEL_PLAT | Nombre del atributo del outbound de TOA | Obligatorio |
| typeId | number | 1 | ID tipo de integración entre TOA y Jira | Obligatorio |
| jiraFieldType | number | string | Tipo de campo en Jira [string,singleList] | Obligatorio |


# Respuesta

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** |
| --- | --- | --- | --- |
| id | integer | 1 | ID del tipo creado |

# Errores
| **Código error TdP** | **Código Backend** | **Descripción Backend** |
| --- | --- | --- |
| SVC0001 | NA | Generic Client Error. |

