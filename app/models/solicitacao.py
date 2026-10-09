from datetime import date, time

from app.data.solicitacao_mock import SOLICITACOES


class Solicitacao:
    STATUS_VALIDOS = ("solicitada", "confirmada", "concluida", "cancelada")

    def __init__(self, id, prestador, servico, data, horario, status="solicitada", valor=None):
        self._id = id
        self._prestador = None
        self._servico = None
        self.alterar_prestador(prestador)
        self.alterar_servico(servico)
        self.alterar_data(data)
        self.alterar_horario(horario)
        self.alterar_status(status)
        valor_inicial = servico.mostrar_preco_base() if valor is None else valor
        self.alterar_valor(valor_inicial)

    def mostrar_id(self):
        return self._id

    def mostrar_prestador(self):
        return self._prestador

    def alterar_prestador(self, prestador):
        if not prestador.mostrar_ativo():
            raise ValueError("Não é possível solicitar atendimento de um prestador inativo.")
        if self._servico is not None and not prestador.aceita_servico(self._servico.mostrar_id()):
            raise ValueError("O prestador selecionado não oferece esse serviço.")
        self._prestador = prestador

    def mostrar_servico(self):
        return self._servico

    def alterar_servico(self, servico):
        if not servico.mostrar_ativo():
            raise ValueError("Não é possível solicitar um serviço inativo.")
        if not self._prestador.aceita_servico(servico.mostrar_id()):
            raise ValueError("O prestador selecionado não oferece esse serviço.")
        self._servico = servico

    def mostrar_data(self):
        return self._data

    def alterar_data(self, data_atendimento):
        try:
            data_validada = date.fromisoformat(data_atendimento)
        except (TypeError, ValueError):
            raise ValueError("A data precisa estar no formato AAAA-MM-DD.")
        self._data = data_validada.isoformat()

    def mostrar_horario(self):
        return self._horario

    def alterar_horario(self, horario):
        try:
            horario_validado = time.fromisoformat(horario)
        except (TypeError, ValueError):
            raise ValueError("O horário precisa estar no formato HH:MM.")
        self._horario = horario_validado.strftime("%H:%M")

    def mostrar_status(self):
        return self._status

    def alterar_status(self, status):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("O status precisa ser solicitada, confirmada, concluida ou cancelada.")
        self._status = status

    def mostrar_valor(self):
        return self._valor

    def alterar_valor(self, valor):
        try:
            valor_validado = float(valor)
        except (TypeError, ValueError):
            raise ValueError("O valor da solicitação precisa ser numérico.")
        if valor_validado <= 0:
            raise ValueError("O valor da solicitação precisa ser maior que zero.")
        self._valor = round(valor_validado, 2)

    def __repr__(self):
        return (
            f"Solicitacao(id={self._id}, prestador_id={self._prestador.mostrar_id()}, "
            f"servico_id={self._servico.mostrar_id()}, data={self._data!r}, horario={self._horario!r})"
        )


def carregar_solicitacoes(servicos, prestadores):
    servicos_por_id = {servico.mostrar_id(): servico for servico in servicos}
    prestadores_por_id = {prestador.mostrar_id(): prestador for prestador in prestadores}
    solicitacoes = []
    for registro in SOLICITACOES:
        solicitacoes.append(
            Solicitacao(
                id=registro["id"],
                prestador=prestadores_por_id[registro["prestador_id"]],
                servico=servicos_por_id[registro["servico_id"]],
                data=registro["data"],
                horario=registro["horario"],
                status=registro["status"],
                valor=registro["valor"],
            )
        )
    return solicitacoes
