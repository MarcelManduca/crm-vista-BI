# Dashboard Gralha - CRM Imobiliário Moderno

**Status:** 🚀 Fase 1 em Desenvolvimento (Manus + ChatGPT)  
**Objetivo:** Reprodução moderna do Dashboard Gralha em aplicação web com React + FastAPI + PostgreSQL + Redis

---

## 📋 Visão Geral

O **Dashboard Gralha** é um sistema de gestão de vendas imobiliárias que reproduz e moderniza o dashboard comercial da Gralha Imóveis, originalmente em Power BI. O projeto utiliza a **API Vista CRM (Loft)** como fonte de dados e oferece visualizações em tempo real do funil de vendas, VGV (Valor Geral de Vendas) e taxa de conversão.

### Arquitetura
- **Frontend:** React + TypeScript + TailwindCSS (Lovable - Fase 3)
- **Backend:** FastAPI + PostgreSQL + Redis (Manus/Antigravity - Fase 1/2)
- **Sincronização:** Pipeline ETL com API Vista CRM (Atlas - Fase 1)
- **Deployment:** Docker Compose (dev) → Produção (Fase 4)

---

## 📁 Estrutura do Repositório

```
dashboard-gralha/
├── docs/                              # Documentação
│   ├── dashboard_gralha_orientacao_executiva.md    # Guia completo (50+ páginas)
│   ├── dashboard_gralha_resumo_executivo.md        # Resumo executivo
│   ├── dashboard_gralha_arquitetura.png            # Diagrama técnico
│   ├── dashboard_gralha_roadmap_gantt.png          # Timeline visual
│   ├── dashboard_gralha_decisoes_matriz.png        # Matriz de decisões
│   └── dashboard_gralha_wide_research.json         # Pesquisa paralela
├── backend/                           # Backend FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Aplicação principal
│   │   ├── config.py                  # Configurações
│   │   ├── database.py                # Conexão PostgreSQL
│   │   ├── models/                    # Modelos SQLAlchemy
│   │   ├── schemas/                   # Schemas Pydantic
│   │   ├── api/                       # Endpoints REST
│   │   ├── services/                  # Lógica de negócio
│   │   ├── etl/                       # Pipeline ETL
│   │   └── auth/                      # Autenticação JWT
│   ├── requirements.txt               # Dependências Python
│   ├── Dockerfile                     # Container FastAPI
│   └── .env.example                   # Variáveis de ambiente
├── tests/                             # Testes
│   ├── unit/                          # Testes unitários
│   ├── integration/                   # Testes de integração
│   └── conftest.py                    # Configuração pytest
├── scripts/                           # Scripts auxiliares
│   ├── init_db.py                     # Inicializar banco de dados
│   └── seed_data.py                   # Dados de teste
├── .github/
│   └── workflows/
│       ├── ci.yml                     # CI/CD (testes)
│       └── deploy.yml                 # Deploy automático
├── docker-compose.yml                 # Orquestração de containers
├── .env.example                       # Variáveis de ambiente
└── README.md                          # Este arquivo
```

---

## 🚀 Quick Start

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Setup Local (Desenvolvimento)

**1. Clone o repositório**
```bash
git clone https://github.com/MarcelManduca/crm-vista-BI.git
cd crm-vista-BI
```

**2. Configure variáveis de ambiente**
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

**3. Inicie os containers**
```bash
docker-compose up -d
```

**4. Inicialize o banco de dados**
```bash
docker-compose exec backend python scripts/init_db.py
```

**5. Acesse a API**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

---

## 📊 Roadmap (16 Semanas)

| Fase | Semanas | Objetivo | Status |
|------|---------|----------|--------|
| **Fase 0** | 1–2 | Descoberta e Validação | ✅ Concluída |
| **Fase 1** | 3–6 | Backend + Sincronização | 🚀 Em Andamento (Manus) |
| **Fase 2** | 7–10 | Frontend React | ⏳ Planejado (Lovable) |
| **Fase 3** | 11–13 | Validação + Reconciliação | ⏳ Planejado |
| **Fase 4** | 14–16 | Lançamento + Monitoramento | ⏳ Planejado |

---

## 🎯 Fase 1: Backend + Sincronização (ATUAL)

**Responsável:** Manus AI + ChatGPT  
**Duração:** 4 semanas (Sem 3–6)  
**Objetivo:** Implementar backend FastAPI completo com sincronização de dados

### Tarefas
- [ ] Scaffold FastAPI + PostgreSQL + Redis
- [ ] Autenticação JWT + RBAC
- [ ] Modelos de dados (Clients, Properties, Deals, History)
- [ ] Endpoints REST (Funil, VGV, Conversão)
- [ ] Pipeline ETL (Connector Vista)
- [ ] Idempotência e Deduplicação
- [ ] Logs de Auditoria
- [ ] Testes Unitários (≥80% cobertura)
- [ ] CI/CD (GitHub Actions)
- [ ] Documentação de API (Swagger)

---

## 📚 Documentação

### Documentos Principais
1. **[Orientação Executiva Completa](docs/dashboard_gralha_orientacao_executiva.md)** (50+ páginas)
   - 14 seções com decisões críticas, roadmap, métricas, riscos
   
2. **[Resumo Executivo](docs/dashboard_gralha_resumo_executivo.md)** (10 páginas)
   - Versão condensada para leitura rápida

3. **[Pesquisa Paralela](docs/dashboard_gralha_wide_research.json)**
   - 12 frentes de pesquisa com achados verificados

### Diagramas
- **[Arquitetura Técnica](docs/dashboard_gralha_arquitetura.png)** - Componentes e fluxos
- **[Roadmap Gantt](docs/dashboard_gralha_roadmap_gantt.png)** - Timeline visual
- **[Matriz de Decisões](docs/dashboard_gralha_decisoes_matriz.png)** - Status de decisões

---

## 🔐 Segurança & Conformidade

- **Autenticação:** JWT (JSON Web Tokens)
- **Autorização:** RBAC (Role-Based Access Control)
- **Dados:** Soft delete, criptografia em trânsito (HTTPS)
- **LGPD:** Conformidade com Lei Geral de Proteção de Dados
- **Auditoria:** Logs de todas as operações

---

## 📊 Contrato de Métricas

| Métrica | Tolerância | Fonte | Reprocessamento |
|---------|-----------|-------|-----------------|
| **Leads** | ±2% | API Vista `/clientes` | Se duplicado: manter ID antigo |
| **Oportunidades** | ±2% | API Vista `/negocios` | Se duplicado: manter ID antigo |
| **Vendas** | **0%** | API Vista `/negocios` | Se status mudou: incluir/remover |
| **VGV** | **0%** | Cálculo | Se valor alterado: recalcular |
| **Taxa de Conversão** | ±0.5pp | Cálculo derivado | Se Leads/Vendas mudarem |
| **Ciclo de Venda** | ±1 dia | Cálculo | Se datas mudarem |
| **Comissão** | ±5% | Tabela Gralha | Se tabela/valor mudar |
| **Origem** | ±10% | API Vista + Histórico | Se origem vazia: "Direto" |

---

## 🔄 Workflow de Desenvolvimento

### Etapa 1: Manus + ChatGPT (ATUAL)
- Implementar backend FastAPI completo
- Criar pipeline ETL
- Testes e CI/CD
- Documentação técnica

### Etapa 2: Antigravity (Quando você disser)
- Assumir backend via GitHub (issues, PRs)
- ChatGPT como PO guiando via documentação
- Refinamentos e otimizações

### Etapa 3: Lovable (Quando você disser)
- Frontend React integrado com backend
- UI/UX conforme wireframes

---

## 🐛 Troubleshooting

### Erro: "Connection refused" ao conectar PostgreSQL
```bash
# Verifique se o container está rodando
docker-compose ps

# Reinicie os containers
docker-compose restart
```

### Erro: "API Vista indisponível"
```bash
# Verifique credenciais em .env
# Teste manualmente: curl https://novovista-rest.vistahost.com.br/doc/
```

### Erro: "Testes falhando"
```bash
# Rode testes localmente
pytest tests/ -v --cov=app
```

---

## 📞 Contato & Suporte

- **Product Owner:** ChatGPT (via GitHub issues)
- **Backend:** Manus AI (Fase 1) → Antigravity (Fase 2)
- **Frontend:** Lovable (Fase 3)
- **Dados:** Atlas (Sincronização)

---

## 📄 Licença

Proprietary - Gralha Imóveis

---

## 🔗 Links Úteis

- **API Vista CRM:** https://novovista-rest.vistahost.com.br/doc/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **PostgreSQL:** https://www.postgresql.org/
- **Redis:** https://redis.io/

---

**Última atualização:** Agosto 2026  
**Versão:** 1.0.0  
**Status:** 🚀 Em Desenvolvimento
