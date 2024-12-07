# General

| **Campo** | **Valor** | **Descripción** |
| --- | --- | --- |
| Propósito | Permite Consultar las Metas. |
| Recurso | [GET]/salesAdvance | Un recurso está asociado al objeto o entidad que se requiere consultar, modificar, actualizar o eliminar. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). | 
| Sub-recurso | NA | Un sub-recurso tiene relación con respecto a un recurso, se puede interpretar como un parte-todo de un objeto. Enlace de referencia [URIs](https://ad-tdp.azurewebsites.net/lineamientos/gobierno-api/lineamiento#4-5-uris). |

# Petición
### Query Parameter
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| sellerIdentification.nationalIdType | string | NA | Tipo de documento del vendedor | Obligatorio |
| sellerIdentification.nationalId | string | NA | Documento del vendedor | Obligatorio |
| additionalData | string | value1, value2... | Informacion adicional | Opcional |

# Respuesta
| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| sellerIdentification | [LegalId](#legalid) | NA | Objeto legalId del Vendedor | Obligatorio |
| salesAdvance | [SalesAdvance[]](#salesadvance) | NA | NA | Opcional |

# Definiciones

## salesAdvance

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| category | string |  | La Categoría | Obligatorio |
| type | number |  |  | Opcional |
| dateSeller | string($date-time) |  |  |  |
| general | [GeneralInfo](#generalinfo) | NA |  | Opcional |
| goals | [Goals](#goals) | N/A |  | Opcional |
| throttle | [Throttle](#throttle) | NA |  | Opcional |
| additionalData | [AdditionalData[]](#additionaldata) | NA |  | Opcional |

## GeneralInfo

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| code | number |  |  | Opcional |
| product | string |  |  | Opcional |
| operation | string |  |  | Opcional |
| mode | string |  |  | Opcional |
| plan | string |  |  | Opcional |
| message | string |  |  | Opcional |

## Goals

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| value | number |  |  | Opcional |
| hoardSale | number |  |  | Opcional |
| conRecharge | number |  |  | Opcional |
| cuantityRecharge | number |  |  | Opcional |
| updateDate | string($date-time) |  |  | Opcional |

## throttle

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| goal | number |  |  | Opcional |
| validityStart | String |  |  | Opcional |
| validityEnd | String |  |  | Opcional |
| hoardSale | number |  |  | Opcional |
| conRecharge | number |  |  | Opcional |
| cuantityRecharge | number |  |  | Opcional |
| updateDate | string($date) |  |  | Opcional |

## legalId

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| nationalIdType | string | DNI | tipo de documento | Obligatorio |
| nationalId | string | 76230172 | Numero de documento de identidad. | Obligatorio |

## AdditionalData

| **Campo** | **Tipo** | **Ejemplo** | **Descripción** | **Obligatoriedad** |
| --- | --- | --- | --- | --- |
| key | string |  | N/A | Opcional |
| value | string |  | N/A | Opcional |