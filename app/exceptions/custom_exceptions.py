class InvalidStyleError(Exception):
    """Lançada quando o image_style não está no mapeamento."""

class EmptyUrlError(Exception):
    """Lançada quando a API não retorna imagem."""