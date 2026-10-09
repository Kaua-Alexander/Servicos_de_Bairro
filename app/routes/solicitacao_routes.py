from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


class SolicitacaoEntrada(BaseModel):
    prestador_id: int = Field(gt=0)
    servico_id: int = Field(gt=0)
    data: str
    horario: str
    status: str = "solicitada"
    valor: float | None = Field(default=None, gt=0)


def criar_router_solicitacoes(controller):
    router = APIRouter(tags=["Solicitações"])

    @router.post("/api/solicitacoes", status_code=201)
    def criar_solicitacao(entrada: SolicitacaoEntrada):
        try:
            criada = controller.criar_solicitacao(entrada.dict())
            if criada is None:
                raise HTTPException(
                    status_code=404,
                    detail="Prestador ou serviço não encontrado.",
                )
            return criada
        except HTTPException:
            raise
        except ValueError as erro:
            status = 409 if "conflito" in str(erro).casefold() else 422
            raise HTTPException(status_code=status, detail=str(erro)) from erro

    @router.get("/api/relatorio/comissoes")
    def relatorio_comissoes():
        return controller.relatorio_comissoes()

    return router
