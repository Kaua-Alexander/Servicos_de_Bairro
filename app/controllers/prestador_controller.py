from app.models.prestador import carregar_prestadores


class PrestadorController:
    def __init__(self, prestadores=None):
        self._prestadores = carregar_prestadores() if prestadores is None else prestadores

    def _para_dicionario(self, prestador):
        return {
            "id": prestador.mostrar_id(),
            "nome": prestador.mostrar_nome(),
            "bairro": prestador.mostrar_bairro(),
            "telefone": prestador.mostrar_telefone(),
            "servicos_ids": prestador.mostrar_servicos_ids(),
            "ativo": prestador.mostrar_ativo(),
            "avaliacao": prestador.mostrar_avaliacao(),
            "perfil": prestador.descricao_perfil(),
            "taxa_comissao_percentual": round(prestador.mostrar_taxa_comissao() * 100, 2),
        }

    def listar_prestadores(self, bairro=None):
        prestadores = self._prestadores
        if bairro:
            prestadores = [
                prestador
                for prestador in prestadores
                if prestador.mostrar_bairro().casefold() == bairro.strip().casefold()
            ]
        return [self._para_dicionario(prestador) for prestador in prestadores]

    def buscar_por_id(self, prestador_id):
        for prestador in self._prestadores:
            if prestador.mostrar_id() == prestador_id:
                return self._para_dicionario(prestador)
        return None
