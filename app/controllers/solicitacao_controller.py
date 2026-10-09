from app.models.solicitacao import Solicitacao, carregar_solicitacoes
from app.models.servico import carregar_servicos
from app.models.prestador import carregar_prestadores


class SolicitacaoController:
    def __init__(self, servicos=None, prestadores=None, solicitacoes=None):
        self._servicos = carregar_servicos() if servicos is None else servicos
        self._prestadores = carregar_prestadores() if prestadores is None else prestadores
        self._solicitacoes = (
            carregar_solicitacoes(self._servicos, self._prestadores)
            if solicitacoes is None
            else solicitacoes
        )

    def _para_dicionario(self, solicitacao):
        prestador = solicitacao.mostrar_prestador()
        servico = solicitacao.mostrar_servico()
        return {
            "id": solicitacao.mostrar_id(),
            "prestador": {
                "id": prestador.mostrar_id(),
                "nome": prestador.mostrar_nome(),
                "bairro": prestador.mostrar_bairro(),
                "perfil": prestador.descricao_perfil(),
            },
            "servico": {
                "id": servico.mostrar_id(),
                "nome": servico.mostrar_nome(),
                "categoria": servico.mostrar_categoria(),
            },
            "data": solicitacao.mostrar_data(),
            "horario": solicitacao.mostrar_horario(),
            "status": solicitacao.mostrar_status(),
            "valor": solicitacao.mostrar_valor(),
            "comissao_estimada": prestador.calcular_comissao(solicitacao.mostrar_valor()),
        }

    def criar_solicitacao(self, dados):
        prestador = next(
            (item for item in self._prestadores if item.mostrar_id() == dados.get("prestador_id")),
            None,
        )
        servico = next(
            (item for item in self._servicos if item.mostrar_id() == dados.get("servico_id")),
            None,
        )
        if prestador is None or servico is None:
            return None

        novo_id = max((item.mostrar_id() for item in self._solicitacoes), default=0) + 1
        nova = Solicitacao(
            id=novo_id,
            prestador=prestador,
            servico=servico,
            data=dados.get("data"),
            horario=dados.get("horario"),
            status=dados.get("status", "solicitada"),
            valor=dados.get("valor", servico.mostrar_preco_base()),
        )
        for existente in self._solicitacoes:
            mesmo_horario = (
                existente.mostrar_prestador().mostrar_id() == prestador.mostrar_id()
                and existente.mostrar_data() == nova.mostrar_data()
                and existente.mostrar_horario() == nova.mostrar_horario()
                and existente.mostrar_status() != "cancelada"
            )
            if mesmo_horario:
                raise ValueError("Conflito: o prestador já possui uma solicitação nesse dia e horário.")

        self._solicitacoes.append(nova)
        return self._para_dicionario(nova)

    def historico_por_prestador(self, prestador_id):
        correspondentes = [
            solicitacao
            for solicitacao in self._solicitacoes
            if solicitacao.mostrar_prestador().mostrar_id() == prestador_id
        ]
        return [self._para_dicionario(solicitacao) for solicitacao in correspondentes]

    def relatorio_comissoes(self):
        por_prestador = []
        for prestador in self._prestadores:
            solicitacoes_validas = [
                solicitacao
                for solicitacao in self._solicitacoes
                if solicitacao.mostrar_prestador().mostrar_id() == prestador.mostrar_id()
                and solicitacao.mostrar_status() != "cancelada"
            ]
            total_servicos = round(sum(item.mostrar_valor() for item in solicitacoes_validas), 2)
            total_comissao = round(
                sum(prestador.calcular_comissao(item.mostrar_valor()) for item in solicitacoes_validas),
                2,
            )
            por_prestador.append(
                {
                    "prestador_id": prestador.mostrar_id(),
                    "prestador": prestador.mostrar_nome(),
                    "perfil": prestador.descricao_perfil(),
                    "quantidade_solicitacoes": len(solicitacoes_validas),
                    "total_servicos": total_servicos,
                    "comissao_estimada": total_comissao,
                }
            )
        return {
            "quantidade_prestadores": len(por_prestador),
            "total_comissoes_estimadas": round(
                sum(item["comissao_estimada"] for item in por_prestador), 2
            ),
            "por_prestador": por_prestador,
        }
