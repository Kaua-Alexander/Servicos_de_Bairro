from app.models.servico import carregar_servicos


class ServicoController:
    def __init__(self, servicos=None):
        self._servicos = carregar_servicos() if servicos is None else servicos

    def _para_dicionario(self, servico):
        return {
            "id": servico.mostrar_id(),
            "nome": servico.mostrar_nome(),
            "categoria": servico.mostrar_categoria(),
            "descricao": servico.mostrar_descricao(),
            "preco_base": servico.mostrar_preco_base(),
            "ativo": servico.mostrar_ativo(),
        }

    def listar_servicos(self):
        return [self._para_dicionario(servico) for servico in self._servicos]

    def buscar_por_id(self, servico_id):
        for servico in self._servicos:
            if servico.mostrar_id() == servico_id:
                return self._para_dicionario(servico)
        return None

    def listar_por_categoria(self, categoria):
        servicos = [
            servico
            for servico in self._servicos
            if servico.mostrar_categoria().casefold() == categoria.strip().casefold()
        ]
        return [self._para_dicionario(servico) for servico in servicos]
