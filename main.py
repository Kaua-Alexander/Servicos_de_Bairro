from fastapi import FastAPI

from app.controllers.prestador_controller import PrestadorController
from app.controllers.servico_controller import ServicoController
from app.controllers.solicitacao_controller import SolicitacaoController
from app.models.prestador import carregar_prestadores
from app.models.servico import carregar_servicos
from app.models.solicitacao import carregar_solicitacoes
from app.routes.prestador_routes import criar_router_prestadores
from app.routes.servico_routes import criar_router_servicos
from app.routes.solicitacao_routes import criar_router_solicitacoes


servicos = carregar_servicos()
prestadores = carregar_prestadores()
solicitacoes = carregar_solicitacoes(servicos, prestadores)

servico_controller = ServicoController(servicos)
prestador_controller = PrestadorController(prestadores)
solicitacao_controller = SolicitacaoController(servicos, prestadores, solicitacoes)

app = FastAPI(
    title="Serviços do Bairro API",
    description=(
        "API demonstrativa para catálogo de serviços locais, prestadores e solicitações "
        "de atendimento. Dados mantidos em memória a partir de mocks."
    ),
    version="1.0.0",
)

app.include_router(criar_router_servicos(servico_controller))
app.include_router(criar_router_prestadores(prestador_controller, solicitacao_controller))
app.include_router(criar_router_solicitacoes(solicitacao_controller))

