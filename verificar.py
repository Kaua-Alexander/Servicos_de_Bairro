"""Verificações simples dos requisitos centrais do projeto."""

from app.controllers.servico_controller import ServicoController
from app.controllers.solicitacao_controller import SolicitacaoController
from app.models.prestador import (
    Prestador,
    PrestadorAutonomo,
    PrestadorVerificado,
    carregar_prestadores,
)
from app.models.servico import Servico, carregar_servicos
from app.models.solicitacao import Solicitacao, carregar_solicitacoes


def deve_gerar_value_error(acao):
    try:
        acao()
    except ValueError:
        return True
    return False


def executar_verificacoes():
    resultados = []

    def checar(nome, condicao):
        passou = bool(condicao)
        resultados.append((nome, passou))
        print(f"{'OK' if passou else 'FALHOU'} - {nome}")

    servicos = carregar_servicos()
    prestadores = carregar_prestadores()
    solicitacoes = carregar_solicitacoes(servicos, prestadores)

    checar("Existem pelo menos 5 serviços mockados", len(servicos) >= 5)
    checar("Existem pelo menos 5 prestadores mockados", len(prestadores) >= 5)
    checar("Existem pelo menos 5 solicitações mockadas", len(solicitacoes) >= 5)
    checar("Todos os preços dos serviços são positivos", all(s.mostrar_preco_base() > 0 for s in servicos))
    checar("Todos os prestadores possuem ao menos um serviço", all(p.mostrar_servicos_ids() for p in prestadores))
    checar("A hierarquia de herança tem dois níveis", issubclass(PrestadorVerificado, PrestadorAutonomo) and issubclass(PrestadorAutonomo, Prestador))
    checar("As subclasses definem taxas de comissão diferentes", len({Prestador.TAXA_COMISSAO, PrestadorAutonomo.TAXA_COMISSAO, PrestadorVerificado.TAXA_COMISSAO}) == 3)

    perfil_verificado = next(p for p in prestadores if p.descricao_perfil().endswith("com selo verificado"))
    checar("O método sobrescrito estende a descrição usando super()", "Prestador autônomo" in perfil_verificado.descricao_perfil())
    comissoes = [Prestador.TAXA_COMISSAO * 100, PrestadorAutonomo.TAXA_COMISSAO * 100, PrestadorVerificado.TAXA_COMISSAO * 100]
    checar("O cálculo polimórfico produz comissões diferentes", len(set(comissoes)) == 3)
    checar(
        "A model recusa preço de serviço igual a zero",
        deve_gerar_value_error(lambda: Servico(99, "Teste", "Teste", "Descrição", 0)),
    )
    checar(
        "A model recusa avaliação fora da faixa de 0 a 5",
        deve_gerar_value_error(lambda: Prestador(99, "Teste", "Centro", "11987654321", [1], True, 6)),
    )
    checar(
        "A model recusa lista vazia de serviços do prestador",
        deve_gerar_value_error(lambda: Prestador(99, "Teste", "Centro", "11987654321", [], True, 4)),
    )

    prestador_base = prestadores[0]
    servico_do_prestador = next(
        servico for servico in servicos if prestador_base.aceita_servico(servico.mostrar_id())
    )
    checar(
        "A model recusa data em formato inválido",
        deve_gerar_value_error(
            lambda: Solicitacao(99, prestador_base, servico_do_prestador, "32-12-2026", "10:00")
        ),
    )
    checar(
        "A model recusa horário inválido",
        deve_gerar_value_error(
            lambda: Solicitacao(99, prestador_base, servico_do_prestador, "2099-05-20", "hora")
        ),
    )
    checar(
        "A model recusa status que não pertence à lista permitida",
        deve_gerar_value_error(
            lambda: Solicitacao(99, prestador_base, servico_do_prestador, "2099-05-20", "10:00", "inventado")
        ),
    )

    servico_controller = ServicoController(servicos)
    categoria = servicos[0].mostrar_categoria()
    filtrados = servico_controller.listar_por_categoria(categoria)
    checar(
        "O filtro por categoria retorna apenas serviços da categoria pedida",
        bool(filtrados) and all(item["categoria"].casefold() == categoria.casefold() for item in filtrados),
    )
    checar("A busca de serviço inexistente retorna None", servico_controller.buscar_por_id(99999) is None)

    controller = SolicitacaoController(servicos, prestadores, list(solicitacoes))
    dados_nova = {
        "prestador_id": prestador_base.mostrar_id(),
        "servico_id": servico_do_prestador.mostrar_id(),
        "data": "2099-05-20",
        "horario": "21:45",
        "status": "solicitada",
    }
    criada = controller.criar_solicitacao(dados_nova)
    checar("O controller cria uma solicitação válida", criada is not None and criada["id"] > 0)
    checar(
        "O controller recusa duas solicitações no mesmo horário do prestador",
        deve_gerar_value_error(lambda: controller.criar_solicitacao(dados_nova)),
    )
    checar(
        "O relatório de comissões inclui todos os prestadores",
        controller.relatorio_comissoes()["quantidade_prestadores"] == len(prestadores),
    )

    total = len(resultados)
    aprovadas = sum(1 for _, passou in resultados if passou)
    print(f"\nResultado: {aprovadas}/{total} verificações aprovadas.")
    return aprovadas == total


if __name__ == "__main__":
    raise SystemExit(0 if executar_verificacoes() else 1)
