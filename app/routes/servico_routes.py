from fastapi import APIRouter, HTTPException


def criar_router_servicos(controller):
    router = APIRouter(tags=["Serviços"])

    @router.get("/api/servicos")
    def listar_servicos():
        return controller.listar_servicos()

    @router.get("/api/servicos/categoria/{categoria}")
    def listar_por_categoria(categoria: str):
        return controller.listar_por_categoria(categoria)

    @router.get("/api/servicos/{servico_id}")
    def buscar_servico(servico_id: int):
        servico = controller.buscar_por_id(servico_id)
        if servico is None:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        return servico

    return router
