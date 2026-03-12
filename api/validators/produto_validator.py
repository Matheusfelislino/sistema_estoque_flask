"""Validação de dados para produtos."""

NOME_MAX_LEN = 100
MARCA_MAX_LEN = 50


def validate_create(dados: dict) -> list[str]:
    """Valida os dados para a criação de um novo produto.

    Retorna uma lista de mensagens de erro. Uma lista vazia significa que os dados são válidos.
    """
    errors: list[str] = []

    if "nome" not in dados:
        errors.append("Campo 'nome' é obrigatório")
    else:
        nome = dados["nome"]
        if not isinstance(nome, str) or not nome.strip():
            errors.append("Campo 'nome' não pode ser vazio ou apenas espaços")
        elif len(nome) > NOME_MAX_LEN:
            errors.append(
                f"Campo 'nome' deve ter no máximo {NOME_MAX_LEN} caracteres"
            )

    if "marca" in dados and dados["marca"] is not None:
        marca = dados["marca"]
        if not isinstance(marca, str):
            errors.append("Campo 'marca' deve ser uma string")
        elif len(marca) > MARCA_MAX_LEN:
            errors.append(
                f"Campo 'marca' deve ter no máximo {MARCA_MAX_LEN} caracteres"
            )

    if "preco" not in dados:
        errors.append("Campo 'preco' é obrigatório")
    else:
        errors.extend(_validate_preco(dados["preco"]))

    if "quantidade" in dados:
        errors.extend(_validate_quantidade(dados["quantidade"]))

    return errors


def validate_update(dados: dict) -> list[str]:
    """Valida os dados para uma atualização completa (PUT) de um produto.

    Retorna uma lista de mensagens de erro.
    """
    errors: list[str] = []

    if "quantidade" not in dados:
        errors.append("Campo 'quantidade' é obrigatório")
    else:
        errors.extend(_validate_quantidade(dados["quantidade"]))

    if "preco" not in dados:
        errors.append("Campo 'preco' é obrigatório")
    else:
        errors.extend(_validate_preco(dados["preco"]))

    return errors


def validate_patch(dados: dict) -> list[str]:
    """Valida os dados para uma atualização parcial (PATCH) de um produto.

    Pelo menos um campo atualizável deve ser fornecido.
    Retorna uma lista de mensagens de erro.
    """
    errors: list[str] = []
    allowed_fields = {"nome", "marca", "preco", "quantidade"}

    if not any(field in dados for field in allowed_fields):
        errors.append(
            "Informe ao menos um campo para atualizar: "
            + ", ".join(sorted(allowed_fields))
        )
        return errors

    if "nome" in dados:
        nome = dados["nome"]
        if not isinstance(nome, str) or not nome.strip():
            errors.append("Campo 'nome' não pode ser vazio ou apenas espaços")
        elif len(nome) > NOME_MAX_LEN:
            errors.append(
                f"Campo 'nome' deve ter no máximo {NOME_MAX_LEN} caracteres"
            )

    if "marca" in dados and dados["marca"] is not None:
        marca = dados["marca"]
        if not isinstance(marca, str):
            errors.append("Campo 'marca' deve ser uma string")
        elif len(marca) > MARCA_MAX_LEN:
            errors.append(
                f"Campo 'marca' deve ter no máximo {MARCA_MAX_LEN} caracteres"
            )

    if "preco" in dados:
        errors.extend(_validate_preco(dados["preco"]))

    if "quantidade" in dados:
        errors.extend(_validate_quantidade(dados["quantidade"]))

    return errors


def _validate_preco(value) -> list[str]:
    errors: list[str] = []
    try:
        preco = float(value)
        if preco < 0:
            errors.append("Campo 'preco' deve ser um número não-negativo")
    except (ValueError, TypeError):
        errors.append("Campo 'preco' deve ser um número válido")
    return errors


def _validate_quantidade(value) -> list[str]:
    errors: list[str] = []
    try:
        quantidade = int(value)
        if quantidade < 0:
            errors.append("Campo 'quantidade' deve ser um inteiro não-negativo")
    except (ValueError, TypeError):
        errors.append("Campo 'quantidade' deve ser um número inteiro válido")
    return errors
