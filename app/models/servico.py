from app.data.servico_mock import SERVICOS


class Servico:
    def __init__(self, id, nome, categoria, descricao, preco_base, ativo=True):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_categoria(categoria)
        self.alterar_descricao(descricao)
        self.alterar_preco_base(preco_base)
        self.alterar_ativo(ativo)

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def alterar_nome(self, nome):
        if not nome or not nome.strip():
            raise ValueError("O nome do serviço é obrigatório.")
        self._nome = nome.strip()

    def mostrar_categoria(self):
        return self._categoria

    def alterar_categoria(self, categoria):
        if not categoria or not categoria.strip():
            raise ValueError("A categoria do serviço é obrigatória.")
        self._categoria = categoria.strip()

    def mostrar_descricao(self):
        return self._descricao

    def alterar_descricao(self, descricao):
        if not descricao or not descricao.strip():
            raise ValueError("A descrição do serviço é obrigatória.")
        self._descricao = descricao.strip()

    def mostrar_preco_base(self):
        return self._preco_base

    def alterar_preco_base(self, preco_base):
        try:
            preco = float(preco_base)
        except (TypeError, ValueError):
            raise ValueError("O preço base precisa ser numérico.")
        if preco <= 0:
            raise ValueError("O preço base precisa ser maior que zero.")
        self._preco_base = round(preco, 2)

    def mostrar_ativo(self):
        return self._ativo

    def alterar_ativo(self, ativo):
        if ativo not in (True, False):
            raise ValueError("O estado ativo do serviço precisa ser verdadeiro ou falso.")
        self._ativo = ativo

    def __repr__(self):
        return f"Servico(id={self._id}, nome={self._nome!r}, preco_base={self._preco_base})"


def carregar_servicos():
    return [Servico(**registro) for registro in SERVICOS]
