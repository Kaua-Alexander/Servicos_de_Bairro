from app.data.prestador_mock import PRESTADORES


class Prestador:
    TAXA_COMISSAO = 0.10

    def __init__(self, id, nome, bairro, telefone, servicos_ids, ativo=True, avaliacao=0.0):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_bairro(bairro)
        self.alterar_telefone(telefone)
        self.alterar_servicos_ids(servicos_ids)
        self.alterar_ativo(ativo)
        self.alterar_avaliacao(avaliacao)

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def alterar_nome(self, nome):
        if not nome or not nome.strip():
            raise ValueError("O nome do prestador é obrigatório.")
        self._nome = nome.strip()

    def mostrar_bairro(self):
        return self._bairro

    def alterar_bairro(self, bairro):
        if not bairro or not bairro.strip():
            raise ValueError("O bairro de atendimento é obrigatório.")
        self._bairro = bairro.strip()

    def mostrar_telefone(self):
        return self._telefone

    def alterar_telefone(self, telefone):
        telefone_limpo = "".join(caractere for caractere in str(telefone) if caractere.isdigit())
        if len(telefone_limpo) not in (10, 11):
            raise ValueError("O telefone precisa ter 10 ou 11 dígitos.")
        self._telefone = telefone_limpo

    def mostrar_servicos_ids(self):
        return list(self._servicos_ids)

    def alterar_servicos_ids(self, servicos_ids):
        try:
            ids = [int(servico_id) for servico_id in servicos_ids]
        except (TypeError, ValueError):
            raise ValueError("Os serviços do prestador precisam ser informados por IDs numéricos.")
        if not ids:
            raise ValueError("O prestador precisa oferecer pelo menos um serviço.")
        if len(ids) != len(set(ids)):
            raise ValueError("A lista de serviços do prestador não pode conter IDs repetidos.")
        self._servicos_ids = ids

    def mostrar_ativo(self):
        return self._ativo

    def alterar_ativo(self, ativo):
        if ativo not in (True, False):
            raise ValueError("O estado ativo do prestador precisa ser verdadeiro ou falso.")
        self._ativo = ativo

    def mostrar_avaliacao(self):
        return self._avaliacao

    def alterar_avaliacao(self, avaliacao):
        try:
            nota = float(avaliacao)
        except (TypeError, ValueError):
            raise ValueError("A avaliação precisa ser numérica.")
        if nota < 0 or nota > 5:
            raise ValueError("A avaliação deve ficar entre 0 e 5.")
        self._avaliacao = round(nota, 1)

    def aceita_servico(self, servico_id):
        return servico_id in self._servicos_ids

    def descricao_perfil(self):
        return "Prestador"

    def mostrar_taxa_comissao(self):
        return self.TAXA_COMISSAO

    def calcular_comissao(self, valor_servico):
        try:
            valor = float(valor_servico)
        except (TypeError, ValueError):
            raise ValueError("O valor do serviço precisa ser numérico.")
        if valor <= 0:
            raise ValueError("O valor do serviço precisa ser maior que zero.")
        return round(valor * self.TAXA_COMISSAO, 2)

    def __repr__(self):
        return f"Prestador(id={self._id}, nome={self._nome!r}, bairro={self._bairro!r})"


class PrestadorAutonomo(Prestador):
    TAXA_COMISSAO = 0.08

    def descricao_perfil(self):
        return f"{super().descricao_perfil()} autônomo"

    def __repr__(self):
        return f"PrestadorAutonomo(id={self._id}, nome={self._nome!r})"


class PrestadorVerificado(PrestadorAutonomo):
    TAXA_COMISSAO = 0.05

    def descricao_perfil(self):
        return f"{super().descricao_perfil()} com selo verificado"

    def __repr__(self):
        return f"PrestadorVerificado(id={self._id}, nome={self._nome!r})"


PERFIS = {
    "prestador": Prestador,
    "autonomo": PrestadorAutonomo,
    "verificado": PrestadorVerificado,
}


def carregar_prestadores():
    prestadores = []
    for registro_original in PRESTADORES:
        registro = dict(registro_original)
        classe_prestador = PERFIS[registro.pop("perfil")]
        prestadores.append(classe_prestador(**registro))
    return prestadores
