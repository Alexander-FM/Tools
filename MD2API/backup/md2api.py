import os
import yaml
import re


# Función que permite extraer los objetos definidos en la sección de #Definiciones
def parse_definitions_section(md_content):
    # Primero, extraemos la sección completa de definiciones.
    lines = md_content.splitlines()
    in_definitions_section = False
    definitions_lines = []

    for line in lines:
        if line.strip().startswith("# Definiciones"):
            in_definitions_section = True
            continue
        if in_definitions_section:
            # Si encontramos una sección principal nueva (# algo), dejamos de leer
            if re.match(r"^# ", line) and not line.strip().startswith("# Definiciones"):
                break
            definitions_lines.append(line)

    definitions_content = "\n".join(definitions_lines)

    # Cada definición se identifica con '## NombreDefinicion'
    # Usamos una expresión regular que capture cada sección.
    definition_pattern = r"(##\s+([A-Za-z0-9_]+)([\s\S]*?)(?=##\s+[A-Za-z0-9_]+|$))"
    matches = re.findall(definition_pattern, definitions_content)

    schemas = {}

    # Función auxiliar para mapear tipos de la tabla a tipos OpenAPI
    def map_type(tipo_str):
        tipo_str = tipo_str.lower()
        # Detectar tipo date-time
        # Formato esperado: string($date-time)
        date_time_match = re.match(r"string\(\$date-time\)", tipo_str)
        if date_time_match:
            return {"type": "string", "format": "date-time"}

        # Detectar tipo date
        # Formato esperado: string($date)
        date_match = re.match(r"string\(\$date\)", tipo_str)
        if date_match:
            return {"type": "string", "format": "date"}

        # Otros tipos directos
        # Podrías ampliarlos según tus necesidades
        if tipo_str in ["string", "number", "integer", "boolean"]:
            return {"type": tipo_str}

        # Si no es uno de los reconocidos, se asume string
        return {"type": "string"}

    # Primera fase: construir los schemas con referencias sin convertir aún
    for full_match, definition_name, definition_body in matches:
        definition_name = definition_name.strip()
        schema = {
            "type": "object",
            "properties": {},
        }
        required_fields = []

        # Procesar las tablas dentro de cada definición
        # Formato esperado:
        # | Campo | Tipo | Ejemplo | Descripción | Obligatoriedad |
        body_lines = definition_body.strip().splitlines()

        for line_def in body_lines:
            line_def = line_def.strip()
            # Ignorar separadores y encabezados
            if line_def.startswith("| ---"):
                continue
            if re.match(
                r"\| \*\*Campo\*\* \| \*\*Tipo\*\* \| \*\*Ejemplo\*\* \| \*\*Descripción\*\* \| \*\*Obligatoriedad\*\*",
                line_def,
            ):
                continue

            # Extraer filas
            match_props = re.match(
                r"\| (.+?) \| (.+?) \| (.*?) \| (.*?) \| (.*?) \|", line_def
            )
            if match_props:
                campo, tipo, ejemplo, descripcion, obligatoriedad = match_props.groups()
                campo = campo.strip()
                tipo = tipo.strip()
                ejemplo = ejemplo.strip()
                descripcion = descripcion.strip()
                obligatoriedad = obligatoriedad.strip()

                # Detectar Referencias
                array_ref_match = re.match(
                    r"\[([A-Za-z0-9_]+)\[\]\]\(#([A-Za-z0-9_\-]+)\)",
                    tipo,
                    re.IGNORECASE,
                )
                object_ref_match = re.match(
                    r"\[([A-Za-z0-9_]+)\]\(#([A-Za-z0-9_\-]+)\)", tipo, re.IGNORECASE
                )

                if array_ref_match:
                    # Es un array de un tipo definido
                    ref_name = array_ref_match.group(2)
                    prop_schema = {
                        "type": "array",
                        "items": {"$ref": f"#/components/schemas/{ref_name}"},
                    }
                elif object_ref_match:
                    # Es un objeto definido
                    ref_name = object_ref_match.group(2)
                    prop_schema = {"$ref": f"#/components/schemas/{ref_name}"}
                else:
                    # Si no es referencia, usar map_type
                    prop_schema = map_type(tipo)

                # Añadir ejemplo si existe y no es "NA"
                if ejemplo and ejemplo.upper() != "NA":
                    prop_schema["example"] = ejemplo
                
                # Añadir descripción si existe y no está vacía
                if descripcion and descripcion.upper() != "NA" and descripcion.upper() != "N/A":
                    prop_schema["description"] = descripcion

                # Marcar campos obligatorios si es necesario
                if obligatoriedad.lower() == "obligatorio":
                    required_fields.append(campo)

                schema["properties"][campo] = prop_schema

        if required_fields:
            schema["required"] = required_fields

        # Guardamos el esquema con el nombre tal cual aparece en la definición.
        schemas[definition_name] = schema

    # Segunda fase: ahora que schemas está completo, construimos el mapping
    definitions_map = {d.lower(): d for d in schemas.keys()}
    # Recorrer todos los schemas y sus propiedades para ajustar las referencias
    for sch_name, sch_value in schemas.items():
        for prop_name, prop_schema in sch_value.get("properties", {}).items():
            # Si es una referencia simple
            if "$ref" in prop_schema:
                ref_path = prop_schema["$ref"]
                # ref_path será algo como "#/components/schemas/generalinfo"
                ref_split = ref_path.split("/")
                ref_schema_name = ref_split[-1]  # ej: 'generalinfo'
                ref_schema_lower = ref_schema_name.lower()

                if ref_schema_lower in definitions_map:
                    # Cambiamos el nombre a su PascalCase
                    correct_name = definitions_map[ref_schema_lower]
                    prop_schema["$ref"] = f"#/components/schemas/{correct_name}"

            # Si es un array con $ref
            if prop_schema.get("type") == "array" and "items" in prop_schema:
                items_ref = prop_schema["items"].get("$ref")
                if items_ref:
                    ref_split = items_ref.split("/")
                    ref_schema_name = ref_split[-1]
                    ref_schema_lower = ref_schema_name.lower()
                    if ref_schema_lower in definitions_map:
                        correct_name = definitions_map[ref_schema_lower]
                        prop_schema["items"][
                            "$ref"
                        ] = f"#/components/schemas/{correct_name}"
    return schemas


# Función para extraer el propósito de la sección "General"
def extract_purpose(md_content):
    match = re.search(r"\|\s*Propósito\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|", md_content)
    if match:
        # match.group(1) es el valor y match.group(2) es la descripción
        summary = match.group(1).strip()
        return summary
    else:
        return None


def parse_markdown_tables(md_content):
    sections = {}
    current_section = None
    current_subsection = None

    for line in md_content.splitlines():
        # Detecta las secciones principales (Ej. "Petición", "Respuesta", etc.)
        section_match = re.match(r"^# (.+)", line)
        if section_match:
            current_section = section_match.group(1)
            sections[current_section] = {}
            continue

        # Detecta subsecciones (Ej. "Query Parameter", "Body Parameters")
        subsection_match = re.match(r"^### (.+)", line)
        if subsection_match and current_section:
            current_subsection = subsection_match.group(1)
            sections[current_section][current_subsection] = []
            continue

        # Detecta tablas con las filas
        if line.startswith("|") and current_subsection:
            row = [cell.strip() for cell in line.split("|")[1:-1]]
            if len(row) > 1 and any(
                cell != "---" for cell in row
            ):  # Asegura que la fila no esté vacía o llena de "---"
                if current_section and current_subsection in sections[current_section]:
                    sections[current_section][current_subsection].append(row)

    return sections


def parse_response_section(md_content, definitions_map):
    response_schema = {"type": "object", "properties": {}}
    required_fields = []
    lines = md_content.splitlines()
    response_section = False
    found_properties = False

    for line in lines:
        line = line.strip()

        if line.startswith("# Respuesta"):
            response_section = True
            continue

        if response_section:
            # Ignorar líneas en blanco iniciales después de comenzar la sección
            if line == "" and not found_properties:
                continue

            # Salir si encuentra una línea en blanco después de las propiedades
            if line == "":
                break

            # Ignorar la línea de encabezado de la tabla
            if re.match(
                r"\| \*\*Campo\*\* \| \*\*Tipo\*\* \| \*\*Ejemplo\*\* \| \*\*Descripción\*\* \| \*\*Obligatoriedad\*\* \|",
                line,
            ):
                continue

            # Ignorar la línea de separación
            if line.startswith("| ---"):
                continue

            # Intentar parsear la fila de propiedad con obligatoriedad
            match = re.match(r"\| (.+?) \| (.+?) \| (.*?) \| (.*?) \| (.*?) \|", line)
            if match:
                campo, tipo, ejemplo, descripcion, obligatoriedad = match.groups()
                found_properties = True
                campo = campo.strip()
                tipo = tipo.strip()
                ejemplo = ejemplo.strip()
                descripcion = descripcion.strip()
                obligatoriedad = obligatoriedad.strip()
                # Determinar si es un tipo primitivo o si hace referencia a un objeto definido
                # Patrón para detectar referencias:
                # Para arrays: [ObjectName[]](#objectname)
                # Para objetos: [ObjectName](#objectname)
                array_ref_match = re.match(
                    r"\[([A-Za-z0-9_]+)\[\]\]\(#([A-Za-z0-9_]+)\)", tipo, re.IGNORECASE
                )
                object_ref_match = re.match(
                    r"\[([A-Za-z0-9_]+)\]\(#([A-Za-z0-9_]+)\)", tipo, re.IGNORECASE
                )

                if array_ref_match:
                    # Es un array de un tipo definido
                    ref_name = array_ref_match.group(2).lower()
                    if ref_name in definitions_map:
                        ref_name = definitions_map[ref_name]

                    property_schema = {
                        "type": "array",
                        "items": {"$ref": f"#/components/schemas/{ref_name}"},
                    }
                elif object_ref_match:
                    # Es una referencia a un objeto definido
                    ref_name = object_ref_match.group(2).lower()
                    if ref_name in definitions_map:
                        ref_name = definitions_map[ref_name]

                    property_schema = {"$ref": f"#/components/schemas/{ref_name}"}
                else:
                    # Caso contrario, asumimos que es un tipo primitivo estándar
                    tipo_lower = tipo.lower()
                    # Validar tipos primitivos conocidos:
                    if tipo_lower not in ["string", "integer", "boolean", "number"]:
                        tipo_lower = "string"
                    property_schema = {"type": tipo_lower}

                # Añadir ejemplo si existe y no es "NA"
                if ejemplo and ejemplo.upper() != "NA":
                    property_schema["example"] = ejemplo

                # Añadir descripción si existe y no está vacía
                if descripcion and descripcion.upper() != "NA":
                    property_schema["description"] = descripcion

                # Manejar obligatoriedad
                if obligatoriedad.lower() == "obligatorio":
                    required_fields.append(campo)

                # Agregar la propiedad al response_schema
                response_schema["properties"][campo] = property_schema

    # Si no se encontraron propiedades, vaciar el schema para forzar 204
    if not found_properties:
        response_schema = {}
    else:
        # Si hay campos obligatorios, agregarlos a required
        if required_fields:
            response_schema["required"] = required_fields
    return response_schema


def generate_openapi_spec_from_md(
    file_name,
    operation_type,
    operation_name,
    operation_path,
    sections,
    response_schema,
    summary,
    tags,
):
    # Extrae parámetros de Path y Body
    path_params = sections.get("Petición", {}).get("Path Parameter", [])[1:]
    # Extrae parámetros de Query y Body
    query_params = sections.get("Petición", {}).get("Query Parameter", [])[1:]
    # Omite el encabezado
    body_params = sections.get("Petición", {}).get("Body Parameters", [])[1:]

    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": f"API for {operation_name}",
            "version": "1.0.0",
            "description": f"Generated API specification from {file_name}.",
        },
        "servers": [{"url": "http://localhost:8080/"}],
        "paths": {
            operation_path: {
                operation_type.lower(): {
                    "tags": [f"{tags}"],
                    "summary": operation_name,
                    "description": summary or "Detailed description not available.",
                    "operationId": operation_name,
                    "parameters": (
                        (
                            [
                                {
                                    "name": param[0],
                                    "in": "query",
                                    "required": param[4].lower() == "obligatorio",
                                    "description": param[3],
                                    "schema": {
                                        "type": param[1].lower(),
                                        "example": param[2],
                                    },
                                }
                                for param in query_params
                            ]
                            if query_params
                            else []
                        )
                        + (
                            [
                                {
                                    "name": param[0],
                                    "in": "path",
                                    "required": param[4].lower() == "obligatorio",
                                    "description": param[3],
                                    "schema": {
                                        "type": param[1].lower(),
                                        "example": param[2],
                                    },
                                }
                                for param in path_params
                            ]
                            if path_params
                            else []
                        )
                    ),
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Request"}
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Ok",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Response"}
                                }
                            },
                        }
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Request": {
                    "type": "object",
                    "properties": {
                        param[0]: {
                            "type": param[1].lower(),
                            "example": param[2],
                            "description": param[3],
                        }
                        for param in body_params
                    },
                },
                "Response": response_schema,
            }
        },
    }
    # Si no hay body_params, eliminamos el requestBody y su esquema
    if not body_params:
        del openapi_spec["paths"][operation_path][operation_type.lower()]["requestBody"]
        del openapi_spec["components"]["schemas"]["Request"]

    # Si la respuesta es vacía o no hay esquema de respuesta, colocamos un 204 no content
    if not response_schema or response_schema == {}:
        openapi_spec["paths"][operation_path][operation_type.lower()]["responses"] = {
            "204": {"description": "No content"}
        }
        del openapi_spec["components"]["schemas"]["Response"]

    return openapi_spec


def process_md_files_in_directory(directory="."):
    for file_name in os.listdir(directory):
        if file_name.endswith(".md"):
            with open(file_name, "r", encoding="utf-8") as file:
                md_content = file.read()
            sections = parse_markdown_tables(md_content)
            definitions_schemas = parse_definitions_section(md_content)
            # Guardamos los nombres originales de las referencias de las definiciones
            definitions_map = {d.lower(): d for d in definitions_schemas.keys()}
            response_schema = parse_response_section(md_content, definitions_map)

            # Llama a la función extract_purpose para obtener summary
            summary = extract_purpose(md_content)
            print(f"Procesando archivo: {file_name}")
            operation_type = (
                input("Ingresa el tipo de operación (POST, PUT, DELETE, GET): ")
                .strip()
                .upper()
            )
            operation_name = input("Ingresa el nombre de la operación: ").strip()
            operation_path = input("Ingresa el path para la operación: ").strip()
            tags = input("Ingresa un tags para la operación: ").strip()
            openapi_spec = generate_openapi_spec_from_md(
                file_name,
                operation_type,
                operation_name,
                operation_path,
                sections,
                response_schema,
                summary,
                tags,
            )

            # Actualizar los schemas con las definiciones parseadas
            if definitions_schemas:
                openapi_spec["components"]["schemas"].update(definitions_schemas)

            yaml_file_name = file_name.replace(".md", ".yaml")
            with open(yaml_file_name, "w", encoding="utf-8") as yaml_file:
                yaml.dump(openapi_spec, yaml_file, sort_keys=False, allow_unicode=True)

            print(f"Generado {yaml_file_name} desde {file_name}")


process_md_files_in_directory()
