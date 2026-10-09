from fastapi import APIRouter, HTTPException, Query


def criar_router_prestadores(prestador_controller, solicitacao_controller):
    router = APIRouter(tags=["Prestadores"])

    @router.get("/api/prestadores")
    def listar_prestadores(bairro: str | None = Query(default=None, description="Filtra pelo bairro de atendimento")):
        return prestador_controller.listar_prestadores(bairro)

    @router.get("/api/prestadores/{prestador_id}/solicitacoes")
    def historico_prestador(prestador_id: int):
        prestador = prestador_controller.buscar_por_id(prestador_id)
        if prestador is None:
            raise HTTPException(status_code=404, detail="Prestador não encontrado.")
        return solicitacao_controller.historico_por_prestador(prestador_id)

    return router
