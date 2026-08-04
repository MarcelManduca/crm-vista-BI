"""
Endpoints de Negócios (Deals) - Funil de Vendas
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List
from datetime import date
from app.database import get_db
from app.models.deal import Deal, DealStatus
from app.models.user import User
from app.auth.security import get_current_active_user
from app.schemas.deal import DealRead, DealCreate, DealUpdate

router = APIRouter()


@router.get("/funnel", response_model=Dict[str, int])
async def get_funnel(
    start_date: date = Query(..., description="Data inicial"),
    end_date: date = Query(..., description="Data final"),
    broker_id: int = Query(None, description="ID do corretor (opcional)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, int]:
    """
    Retorna dados do funil de vendas
    
    Args:
        start_date: Data inicial do período
        end_date: Data final do período
        broker_id: ID do corretor (opcional)
        db: Sessão do banco de dados
        current_user: Usuário autenticado
    
    Returns:
        Dicionário com contagens por estágio do funil
    """
    query = db.query(Deal).filter(
        Deal.created_at >= start_date,
        Deal.created_at <= end_date,
        Deal.deleted_at.is_(None),
    )
    
    if broker_id:
        query = query.filter(Deal.user_id == broker_id)
    
    # Contar por status
    funnel = {}
    for status in DealStatus:
        count = query.filter(Deal.status == status).count()
        funnel[status.value] = count
    
    return funnel


@router.get("/vgv", response_model=Dict[str, float])
async def get_vgv(
    start_date: date = Query(..., description="Data inicial"),
    end_date: date = Query(..., description="Data final"),
    broker_id: int = Query(None, description="ID do corretor (opcional)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, float]:
    """
    Retorna VGV (Valor Geral de Vendas)
    
    Args:
        start_date: Data inicial do período
        end_date: Data final do período
        broker_id: ID do corretor (opcional)
        db: Sessão do banco de dados
        current_user: Usuário autenticado
    
    Returns:
        Dicionário com VGV por corretor e total
    """
    query = db.query(Deal).filter(
        Deal.date_signed >= start_date,
        Deal.date_signed <= end_date,
        Deal.status == DealStatus.CONTRACT_SIGNED,
        Deal.deleted_at.is_(None),
    )
    
    if broker_id:
        query = query.filter(Deal.user_id == broker_id)
    
    # Calcular VGV total
    total_vgv = db.session.query(func.sum(Deal.value)).filter(
        Deal.date_signed >= start_date,
        Deal.date_signed <= end_date,
        Deal.status == DealStatus.CONTRACT_SIGNED,
        Deal.deleted_at.is_(None),
    ).scalar() or 0.0
    
    # VGV por corretor
    vgv_by_broker = db.query(
        Deal.user_id,
        func.sum(Deal.value).label("vgv")
    ).filter(
        Deal.date_signed >= start_date,
        Deal.date_signed <= end_date,
        Deal.status == DealStatus.CONTRACT_SIGNED,
        Deal.deleted_at.is_(None),
    ).group_by(Deal.user_id).all()
    
    result = {"total": total_vgv}
    for user_id, vgv in vgv_by_broker:
        result[f"broker_{user_id}"] = vgv or 0.0
    
    return result


@router.get("/conversion-rate", response_model=Dict[str, float])
async def get_conversion_rate(
    start_date: date = Query(..., description="Data inicial"),
    end_date: date = Query(..., description="Data final"),
    broker_id: int = Query(None, description="ID do corretor (opcional)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, float]:
    """
    Retorna taxa de conversão (Leads → Vendas)
    
    Args:
        start_date: Data inicial do período
        end_date: Data final do período
        broker_id: ID do corretor (opcional)
        db: Sessão do banco de dados
        current_user: Usuário autenticado
    
    Returns:
        Dicionário com taxa de conversão
    """
    query = db.query(Deal).filter(
        Deal.created_at >= start_date,
        Deal.created_at <= end_date,
        Deal.deleted_at.is_(None),
    )
    
    if broker_id:
        query = query.filter(Deal.user_id == broker_id)
    
    # Contar leads
    total_leads = query.count()
    
    # Contar vendas
    total_sales = query.filter(
        Deal.status == DealStatus.CONTRACT_SIGNED
    ).count()
    
    # Calcular taxa
    conversion_rate = (total_sales / total_leads * 100) if total_leads > 0 else 0.0
    
    return {
        "total_leads": total_leads,
        "total_sales": total_sales,
        "conversion_rate": round(conversion_rate, 2),
    }


@router.get("/{deal_id}", response_model=DealRead)
async def get_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DealRead:
    """Obtém um negócio por ID"""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("", response_model=DealRead)
async def create_deal(
    deal: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DealRead:
    """Cria um novo negócio"""
    db_deal = Deal(**deal.dict())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.put("/{deal_id}", response_model=DealRead)
async def update_deal(
    deal_id: int,
    deal_update: DealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DealRead:
    """Atualiza um negócio"""
    db_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    for key, value in deal_update.dict(exclude_unset=True).items():
        setattr(db_deal, key, value)
    
    db.commit()
    db.refresh(db_deal)
    return db_deal
