# Orientação Executiva e Operacional: Projeto Dashboard Gralha

**Preparado por:** Manus AI (Product Owner Sênior & Analista de Dados)  
**Data:** Agosto 2026  
**Objetivo:** Guiar decisões de MVP, mitigar riscos de dados e orientar implementação em Antigravity (backend), Lovable (frontend) e Atlas (sincronização/dados)

---

## 1. Resumo Executivo: 10 Decisões Recomendadas

| # | Decisão | Racional | Risco Mitigado |
|---|---------|---------|----------------|
| **1** | **MVP focado em funil de 3 estágios:** Leads → Oportunidades → Vendas (sem Visitas/Propostas isoladas) | Reduz complexidade de dados; alinha com métrica de conversão lead-to-close | Escopo descontrolado; dados incompletos |
| **2** | **Venda Concluída = Status "Contrato Assinado" na API Vista + Data de Assinatura** | Padrão imobiliário; elimina ambiguidade com proposta/negociação | Campo ausente; múltiplas interpretações |
| **3** | **Data de Venda = Data de Assinatura do Contrato (campo oficial Vista a confirmar)** | Ponto de formalização canônico; auditável | Confusão com data de registro/cartório |
| **4** | **Origem de Captação: Rastreamento de Primeiro Toque + Último Toque (sem atribuição multi-toque no MVP)** | Simples de implementar; cobre 80% dos casos de uso | Não captura jornada completa; revisão pós-MVP necessária |
| **5** | **Comissões: Regra comercial separada de dado operacional; cálculo automatizado, auditável via histórico** | Transparência; conformidade; facilita ajustes | Mistura lógica de negócio com dados; auditoria fraca |
| **6** | **Janela histórica inicial: Últimos 24 meses (jan/2025–ago/2026) + incrementais diários** | Cobre ciclo de venda típico (16 meses); reduz volume inicial | Dados antigos podem estar incompletos; sincronização lenta |
| **7** | **Frequência de sincronização: Diária (noturna) + webhook em tempo real para eventos críticos** | Equilíbrio entre performance e frescor; não sobrecarrega API | Falhas de webhook; atrasos aceitáveis até 24h |
| **8** | **Tolerância de reconciliação: 0% para vendas/VGV; ±2% para leads/oportunidades; ±5% para comissões** | Rigor em métricas financeiras; flexibilidade em volume | Reprocessamento frequente; custo operacional |
| **9** | **Segurança MVP: RBAC por corretor/gerente; soft delete; logs de auditoria; criptografia em trânsito (HTTPS)** | Conformidade LGPD básica; controle de acesso simples | Dados expostos; rastreabilidade fraca |
| **10** | **Go/No-Go: Reconciliação com Power BI ≥98% em 3 métricas-chave (Leads, Vendas, VGV); 0 erros críticos em testes** | Validação objetiva; confiança para lançamento | Lançamento prematuro; reputação prejudicada |

---

## 2. Matriz de Decisões: Decidir Agora / Validar / Bloqueia o MVP

| Tema | Status | Decisão/Hipótese | Evidência | Responsável | Ação |
|------|--------|------------------|-----------|-------------|------|
| **Repositório MarcelManduca/crm-vista-BI** | ❌ Bloqueador | Repositório não é público ou não existe | Falha ao clonar/visualizar no GitHub | Manduca | Confirmar acesso; fornecer credenciais ou documentação alternativa |
| **API Vista CRM - Endpoints** | ✅ Validado | Endpoints `/imoveis`, `/clientes`, `/negocios`, `/historico` existem | Documentação oficial: https://novovista-rest.vistahost.com.br/doc/ | Atlas | Testar endpoints; mapear schema via `/listarcampos` |
| **API Vista CRM - Autenticação** | ⚠️ Validar | Chave de API (tenant autenticado); OAuth não mencionado | Documentação menciona "chave pública" mas sem detalhes | Atlas | Solicitar credenciais de teste; testar fluxo de autenticação |
| **API Vista CRM - Rate Limits** | ⚠️ Validar | Não documentado | Ausência de informação | Atlas | Contatar suporte Loft; testar empiricamente |
| **Campo "Venda Concluída"** | ⚠️ Validar | Status "Contrato Assinado" ou equivalente em `/negocios` | Padrão imobiliário; não confirmado em Vista | Atlas | Consultar dicionário de dados Vista; testar endpoint `/negocios/listarcampos` |
| **Campo "Data de Venda"** | ⚠️ Validar | Data de Assinatura do Contrato | Padrão imobiliário; não confirmado em Vista | Atlas | Mapear campos de data em `/negocios`; validar com Gralha |
| **Origem/Mídia de Captação** | ⚠️ Validar | Campo em `/clientes` ou `/negocios`; rastreamento UTM | Conhecimento da Gralha; não confirmado em Vista | Atlas + Lovable | Verificar campos disponíveis; definir estratégia de rastreamento |
| **Cálculo de Comissões** | ⚠️ Validar | Regra comercial da Gralha (tabelas, splits, descontos) | Não documentado em Vista; é regra de negócio | Manduca + Antigravity | Documentar regras; implementar motor de cálculo separado |
| **Modelo Cliente–Imóvel–Histórico** | ✅ Validado | Estrutura padrão em CRM imobiliário; Vista suporta | Documentação API + padrões de indústria | Atlas | Mapear relacionamentos em Vista; testar queries |
| **Funil de Vendas** | ✅ Decidido | Leads → Oportunidades → Vendas (MVP); Visitas/Propostas pós-MVP | Reduz escopo; alinha com conversão | Lovable | Desenhar UI do funil; definir transições |
| **Arquitetura React + FastAPI + PostgreSQL + Redis** | ✅ Validado | Padrão robusto; suporta cache, validação, segurança | Documentação e tutoriais disponíveis | Antigravity + Lovable | Iniciar scaffold; definir convenções |
| **Idempotência e Deduplicação** | ✅ Recomendado | Chaves únicas por entidade (cliente_id, imovel_id, negocio_id) | Padrão ETL; essencial para sincronização | Atlas | Implementar no pipeline; testar reprocessamento |
| **Soft Delete vs Hard Delete** | ✅ Decidido | Soft delete (MVP); hard delete pós-MVP com auditoria | Auditoria; conformidade LGPD | Atlas | Adicionar flag `deleted_at` em tabelas |
| **RBAC e Controle de Acesso** | ✅ Recomendado | Por corretor/gerente; princípio do menor privilégio | Conformidade LGPD; segurança | Antigravity | Implementar middleware de autenticação; testar permissões |
| **Criptografia de Dados** | ✅ Recomendado | Em trânsito (HTTPS); em repouso (opcional MVP) | Segurança básica; conformidade | Antigravity | Configurar TLS; avaliar criptografia em repouso pós-MVP |

---

## 3. Escopo do MVP: O Que Entra, O Que Fica Fora

### ✅ Incluso no MVP

**Funcionalidades Principais:**
- Sincronização diária de Clientes, Imóveis e Negócios da API Vista
- Dashboard com 3 visualizações: Funil (Leads → Oportunidades → Vendas), VGV por Corretor, Taxa de Conversão
- Filtros por período (mês/trimestre/ano), corretor, tipo de imóvel
- Exportação em CSV/JSON
- Autenticação básica (login/logout)
- Logs de auditoria (quem acessou o quê e quando)

**Dados Inclusos:**
- Últimos 24 meses (jan/2025–ago/2026)
- Clientes únicos, imóveis, negócios com status
- Origem de captação (primeiro/último toque)
- Comissões calculadas (regra simples, sem splits complexos)
- Histórico de atividades (registrar, não detalhar)

**Segurança MVP:**
- RBAC: Corretor vê apenas seus dados; Gerente vê equipe; Admin vê tudo
- Soft delete (registros marcados como deletados, não removidos)
- HTTPS obrigatório
- Logs de auditoria (user_id, ação, timestamp, recurso)
- Conformidade LGPD básica (consentimento, direito de acesso/exclusão)

### ❌ Fora do MVP (Pós-MVP)

- Atribuição multi-toque (W-Shaped, algorítmica)
- Alertas inteligentes e notificações em tempo real
- Integração com Power BI (apenas reconciliação manual)
- Cálculo de comissões com splits complexos, descontos, bônus
- Análise preditiva (churn, próxima venda)
- Integração com plataformas de marketing (Ads, email)
- Visitas e Propostas como entidades separadas (apenas em histórico)
- Criptografia de dados em repouso
- Webhooks bidireccionais (apenas sincronização unidirecional)

---

## 4. Roadmap por Fases com Dependências e Critérios de Aceite

### **Fase 0: Descoberta e Validação (Semana 1–2)**

**Objetivo:** Confirmar hipóteses críticas; desbloquear Fase 1.

**Atividades:**
1. **Atlas:** Testar acesso à API Vista; mapear schema via `/listarcampos` para Clientes, Imóveis, Negócios
2. **Atlas:** Confirmar campos de "Venda Concluída", "Data de Venda", "Origem de Captação"
3. **Manduca:** Fornecer documentação de regras comerciais (comissões, splits, descontos)
4. **Manduca:** Confirmar acesso ao repositório MarcelManduca/crm-vista-BI ou fornecer alternativa
5. **Lovable:** Desenhar wireframes do dashboard (funil, VGV, conversão)
6. **Antigravity:** Definir convenções de código, estrutura de pastas, CI/CD

**Critérios de Aceite:**
- ✅ Acesso confirmado à API Vista (credenciais de teste funcionando)
- ✅ Schema de dados mapeado e documentado
- ✅ Regras comerciais documentadas
- ✅ Wireframes aprovados por stakeholders
- ✅ Ambiente de desenvolvimento (Docker Compose) rodando

**Responsável:** Atlas (lead); Manduca (validação)

---

### **Fase 1: Backend & Sincronização Inicial (Semana 3–6)**

**Objetivo:** Implementar pipeline de sincronização; banco de dados; API básica.

**Atividades:**
1. **Antigravity:** Scaffold FastAPI + PostgreSQL + Redis; configurar Docker Compose
2. **Atlas:** Implementar connector para API Vista (autenticação, paginação, tratamento de erros)
3. **Atlas:** Implementar pipeline de sincronização (Clientes, Imóveis, Negócios); idempotência e deduplicação
4. **Antigravity:** Criar tabelas: `clients`, `properties`, `deals`, `deal_history`, `users`, `audit_logs`
5. **Antigravity:** Implementar endpoints: `GET /api/deals/funnel`, `GET /api/deals/vgv`, `GET /api/deals/conversion`
6. **Antigravity:** Implementar autenticação (JWT) e RBAC
7. **Antigravity:** Adicionar logs de auditoria em todas as operações

**Critérios de Aceite:**
- ✅ Sincronização de 100 clientes/imóveis/negócios sem erros
- ✅ Idempotência testada (reprocessamento não duplica dados)
- ✅ Endpoints retornam dados corretos (validados contra API Vista)
- ✅ Autenticação funciona; RBAC testado
- ✅ Logs de auditoria registram todas as ações
- ✅ Testes unitários ≥80% de cobertura

**Responsável:** Antigravity (lead); Atlas (sincronização)

**Dependências:** Fase 0 concluída

---

### **Fase 2: Frontend & Visualizações (Semana 7–10)**

**Objetivo:** Implementar UI do dashboard; integrar com backend.

**Atividades:**
1. **Lovable:** Implementar componentes React: Funil, VGV por Corretor, Taxa de Conversão
2. **Lovable:** Implementar filtros (período, corretor, tipo de imóvel)
3. **Lovable:** Implementar exportação (CSV/JSON)
4. **Lovable:** Implementar login/logout
5. **Lovable:** Integrar com endpoints do backend
6. **Lovable:** Testar responsividade (desktop, tablet)
7. **Lovable:** Testes E2E (Cypress/Playwright)

**Critérios de Aceite:**
- ✅ Dashboard carrega em <2s
- ✅ Filtros funcionam corretamente
- ✅ Exportação gera arquivos válidos
- ✅ Autenticação integrada
- ✅ Testes E2E ≥70% de cobertura
- ✅ Sem erros de console

**Responsável:** Lovable (lead); Antigravity (suporte)

**Dependências:** Fase 1 concluída

---

### **Fase 3: Validação & Reconciliação (Semana 11–13)**

**Objetivo:** Reconciliar com Power BI; validar acurácia; preparar lançamento.

**Atividades:**
1. **Atlas:** Extrair dados do Power BI (Leads, Vendas, VGV)
2. **Atlas:** Comparar com Dashboard Gralha em 3 períodos (jan–mar, abr–jun, jul–ago 2026)
3. **Atlas:** Identificar discrepâncias; documentar causas
4. **Antigravity:** Corrigir bugs identificados
5. **Lovable:** Ajustar UI conforme feedback de usuários
6. **Manduca:** Validar métricas de negócio
7. **Todos:** Testes de carga (1000 usuários simultâneos)

**Critérios de Aceite:**
- ✅ Reconciliação ≥98% em Leads, Vendas, VGV
- ✅ Discrepâncias documentadas e aceitas
- ✅ 0 erros críticos em testes
- ✅ Performance: Funil carrega em <1s; Exportação em <5s
- ✅ Disponibilidade ≥99.5% em testes de carga
- ✅ Documentação de usuário completa

**Responsável:** Atlas (lead); Manduca (validação)

**Dependências:** Fase 2 concluída

---

### **Fase 4: Lançamento & Monitoramento (Semana 14–16)**

**Objetivo:** Deploy em produção; monitoramento; suporte.

**Atividades:**
1. **Antigravity:** Deploy em produção (staging → prod)
2. **Antigravity:** Configurar monitoramento (Prometheus, Grafana, alertas)
3. **Antigravity:** Configurar backups (PostgreSQL, diário)
4. **Lovable:** Treinar usuários (corretores, gerentes, admin)
5. **Todos:** Suporte em tempo real (primeiras 2 semanas)
6. **Manduca:** Coletar feedback; priorizar pós-MVP

**Critérios de Aceite:**
- ✅ Deploy bem-sucedido; 0 downtime
- ✅ Monitoramento ativo; alertas funcionando
- ✅ Backups testados
- ✅ ≥90% de adoção de usuários (logins ativos)
- ✅ Tempo médio de resposta <500ms
- ✅ 0 incidentes críticos em 1 semana

**Responsável:** Antigravity (lead); Todos (suporte)

**Dependências:** Fase 3 concluída

---

## 5. Registro de Decisões Críticas

| Decisão | Contexto | Opções Consideradas | Escolha | Racional | Data de Revisão |
|---------|---------|-------------------|--------|---------|-----------------|
| **Funil MVP: 3 estágios** | Escopo | 3 estágios (Leads/Opp/Vendas) vs. 6 estágios (+ Visitas/Propostas/Fechamento) | 3 estágios | Reduz complexidade; cobre 80% dos casos; pós-MVP expande | Semana 8 |
| **Venda Concluída = Contrato Assinado** | Definição | Status "Contrato Assinado" vs. "Negócio Fechado" vs. "Documentação Completa" | Contrato Assinado | Ponto de formalização canônico; auditável; alinha com CRECI | Semana 2 |
| **Data de Venda = Data de Assinatura** | Definição | Data de Assinatura vs. Data de Registro vs. Data de Documentação | Data de Assinatura | Ponto de formalização; não depende de cartório | Semana 2 |
| **Origem: Primeiro + Último Toque** | Atribuição | Primeiro toque vs. Último toque vs. Multi-toque | Primeiro + Último | Simples; cobre 80%; multi-toque em pós-MVP | Semana 8 |
| **Comissões: Separar Regra de Dado** | Arquitetura | Calcular inline vs. Motor separado vs. Tabela de lookup | Motor separado | Auditoria; flexibilidade; conformidade | Semana 4 |
| **Janela Histórica: 24 meses** | Dados | 12 meses vs. 24 meses vs. 36 meses | 24 meses | Cobre ciclo de venda (16 meses); reduz volume; incrementais diários | Semana 2 |
| **Sincronização: Diária + Webhook** | Frequência | Horária vs. Diária vs. Semanal; com/sem webhook | Diária + Webhook | Equilíbrio performance/frescor; webhook para críticos | Semana 4 |
| **Tolerância: 0% Vendas, ±2% Leads, ±5% Comissões** | Validação | Sem tolerância vs. ±1% vs. ±5% | Diferenciada | Rigor em financeiro; flexibilidade em volume | Semana 11 |
| **RBAC: Corretor/Gerente/Admin** | Segurança | Sem RBAC vs. 3 níveis vs. Granular por campo | 3 níveis | Simples; cobre 90% dos casos; granular em pós-MVP | Semana 3 |
| **Go/No-Go: Reconciliação ≥98%** | Lançamento | 95% vs. 98% vs. 100% | 98% | Rigor; permite pequenas discrepâncias documentadas | Semana 11 |

---

## 6. Contrato de Métricas do Funil

### **Definições Canônicas**

| Métrica | Definição | Unidade | Chave de Deduplicação | Data de Referência | Fonte Canônica | Regra de Reprocessamento |
|---------|-----------|--------|----------------------|-------------------|-----------------|------------------------|
| **Lead** | Cliente criado no CRM com contato (nome, telefone/email) | Contagem | `client_id` | Data de criação do cliente | API Vista `/clientes/listar` | Se cliente duplicado: manter ID mais antigo; marcar novo como soft delete |
| **Oportunidade** | Negócio (deal) criado com status "Em Negociação" ou "Proposta Enviada" | Contagem | `deal_id` | Data de criação do negócio | API Vista `/negocios/listar` | Se negócio duplicado: manter ID mais antigo; marcar novo como soft delete |
| **Venda** | Negócio com status "Contrato Assinado" + Data de Assinatura preenchida | Contagem | `deal_id` | Data de Assinatura do Contrato | API Vista `/negocios/detalhes` (status + data_assinatura) | Se status mudou para "Contrato Assinado": incluir em Vendas; se reverteu: remover |
| **VGV (Valor Geral de Vendas)** | Soma do valor de negócios com status "Contrato Assinado" | R$ (reais) | `deal_id` | Data de Assinatura do Contrato | API Vista `/negocios/detalhes` (valor_negocio) | Se valor alterado: recalcular VGV; se status revertido: remover do VGV |
| **Taxa de Conversão (Lead→Venda)** | (Vendas / Leads) × 100 | % | N/A (agregada) | Período (mês/trimestre/ano) | Cálculo: Vendas ÷ Leads | Recalcular se Leads ou Vendas mudarem |
| **Ciclo de Venda** | Dias entre criação do Lead e Assinatura do Contrato | Dias | `client_id` + `deal_id` | Data de Assinatura do Contrato | Cálculo: data_assinatura - data_criacao_cliente | Recalcular se datas mudarem |
| **Comissão por Venda** | Percentual sobre valor do negócio, conforme tabela comercial da Gralha | R$ (reais) | `deal_id` + `user_id` (corretor) | Data de Assinatura do Contrato | Tabela de Comissões (Gralha) + API Vista (valor_negocio, user_id) | Se tabela de comissão mudou: recalcular; se valor_negocio mudou: recalcular |
| **Origem de Captação (Primeiro Toque)** | Primeiro canal de contato do cliente (ex: Google Ads, Zap, Indicação) | Categoria | `client_id` | Data de criação do cliente | API Vista `/clientes/detalhes` (campo de origem) ou UTM parameters | Se origem não preenchida: classificar como "Direto"; se preenchida: manter |
| **Origem de Captação (Último Toque)** | Último canal de contato antes da venda (ex: Contato Direto, Email) | Categoria | `client_id` + `deal_id` | Data de Assinatura do Contrato | Histórico de atividades (API Vista `/historico` ou `/registrar/historico`) | Se histórico incompleto: usar origem do lead como fallback |

### **Tolerâncias de Reconciliação**

| Métrica | Tolerância | Justificativa | Ação se Excedida |
|---------|-----------|--------------|-----------------|
| **Leads** | ±2% | Volume; pequenas variações em sincronização | Investigar; reprocessar se >2% |
| **Oportunidades** | ±2% | Volume; status pode variar entre sistemas | Investigar; reprocessar se >2% |
| **Vendas** | 0% | Crítico; deve ser exato | Bloquear lançamento; investigar imediatamente |
| **VGV** | 0% | Crítico; financeiro; deve ser exato | Bloquear lançamento; investigar imediatamente |
| **Taxa de Conversão** | ±0.5pp (pontos percentuais) | Derivada de Leads/Vendas; tolerância propagada | Investigar se >0.5pp |
| **Ciclo de Venda** | ±1 dia | Pequenas variações em sincronização de datas | Investigar se >1 dia |
| **Comissão por Venda** | ±5% | Regra comercial complexa; pequenos ajustes aceitáveis | Investigar se >5%; auditar tabela |
| **Origem de Captação** | ±10% (por categoria) | Rastreamento imperfeito; fallback para "Direto" | Investigar; melhorar rastreamento em pós-MVP |

### **Frequência de Validação**

- **Diária:** Leads, Oportunidades, Vendas, VGV (automática via script)
- **Semanal:** Ciclo de Venda, Comissão por Venda (manual + automática)
- **Mensal:** Taxa de Conversão, Origem de Captação (manual + relatório)

---

## 7. Plano de Descoberta da API Vista e dos Dados

### **Testes Reproduzíveis (Fase 0)**

#### **Teste 1: Autenticação e Acesso Básico**

```bash
# Objetivo: Confirmar credenciais e acesso à API
# Responsável: Atlas

curl -X GET "https://novovista-rest.vistahost.com.br/api/clientes/listar" \
  -H "Authorization: Bearer <CHAVE_API>" \
  -H "Content-Type: application/json"

# Esperado: Status 200; lista de clientes
# Se falhar: Verificar chave; contatar suporte Loft
```

#### **Teste 2: Mapear Schema de Clientes**

```bash
# Objetivo: Listar todos os campos disponíveis em Clientes
# Responsável: Atlas

curl -X GET "https://novovista-rest.vistahost.com.br/api/clientes/listarcampos" \
  -H "Authorization: Bearer <CHAVE_API>" \
  -H "Content-Type: application/json"

# Esperado: JSON com lista de campos (nome, email, telefone, etc.)
# Documentar: Nomes de campos; tipos de dados; obrigatoriedade
```

#### **Teste 3: Mapear Schema de Negócios**

```bash
# Objetivo: Listar todos os campos disponíveis em Negócios
# Responsável: Atlas

curl -X GET "https://novovista-rest.vistahost.com.br/api/negocios/listarcampos" \
  -H "Authorization: Bearer <CHAVE_API>" \
  -H "Content-Type: application/json"

# Esperado: JSON com lista de campos (status, valor, data_assinatura, etc.)
# Documentar: Nomes de campos; valores possíveis de status; tipos de dados
# Crítico: Confirmar existência de "status=Contrato Assinado" e "data_assinatura"
```

#### **Teste 4: Buscar Negócios com Status "Contrato Assinado"**

```bash
# Objetivo: Confirmar que negócios fechados podem ser filtrados
# Responsável: Atlas

curl -X GET "https://novovista-rest.vistahost.com.br/api/negocios/listar?status=Contrato%20Assinado" \
  -H "Authorization: Bearer <CHAVE_API>" \
  -H "Content-Type: application/json"

# Esperado: Lista de negócios com status "Contrato Assinado"
# Documentar: Quantidade; valores; datas de assinatura
```

#### **Teste 5: Mapear Histórico de Atividades**

```bash
# Objetivo: Confirmar que histórico de atividades está disponível
# Responsável: Atlas

curl -X GET "https://novovista-rest.vistahost.com.br/api/historico/listar?client_id=<ID>" \
  -H "Authorization: Bearer <CHAVE_API>" \
  -H "Content-Type: application/json"

# Esperado: JSON com histórico de atividades (tipo, data, usuário, descrição)
# Documentar: Campos disponíveis; frequência de sincronização possível
```

#### **Teste 6: Rate Limits e Paginação**

```bash
# Objetivo: Testar rate limits e paginação
# Responsável: Atlas

# Fazer 100 requisições em 1 minuto; documentar respostas
for i in {1..100}; do
  curl -X GET "https://novovista-rest.vistahost.com.br/api/clientes/listar?page=$i" \
    -H "Authorization: Bearer <CHAVE_API>" \
    -H "Content-Type: application/json"
done

# Esperado: Sem erros 429 (rate limit); paginação funciona
# Documentar: Limite de requisições; tamanho de página padrão
```

#### **Teste 7: Campos de Origem/Mídia de Captação**

```bash
# Objetivo: Confirmar que origem de captação está disponível
# Responsável: Atlas

curl -X GET "https://novovista-rest.vistahost.com.br/api/clientes/detalhes?client_id=<ID>" \
  -H "Authorization: Bearer <CHAVE_API>" \
  -H "Content-Type: application/json"

# Esperado: JSON com campo de origem (ex: "origem_captacao", "source", "utm_source")
# Documentar: Nome do campo; valores possíveis
```

### **Matriz de Descoberta de Dados**

| Campo | Endpoint | Tipo | Obrigatório | Valores Possíveis | Status | Ação |
|-------|----------|------|------------|------------------|--------|------|
| `client_id` | `/clientes/listar` | String/Int | Sim | Único por cliente | ✅ Confirmado | Usar como chave primária |
| `client_name` | `/clientes/listar` | String | Sim | Qualquer | ✅ Confirmado | Exibir em UI |
| `client_email` | `/clientes/listar` | String | Não | Email válido | ⚠️ Validar | Usar para contato |
| `client_phone` | `/clientes/listar` | String | Não | Telefone | ⚠️ Validar | Usar para contato |
| `deal_id` | `/negocios/listar` | String/Int | Sim | Único por negócio | ✅ Confirmado | Usar como chave primária |
| `deal_status` | `/negocios/listar` | String | Sim | "Em Negociação", "Proposta Enviada", "Contrato Assinado", etc. | ⚠️ Validar | Usar para funil |
| `deal_value` | `/negocios/listar` | Float | Sim | Valor em R$ | ✅ Confirmado | Usar para VGV |
| `deal_date_signed` | `/negocios/listar` | Date | Sim (se status="Contrato Assinado") | YYYY-MM-DD | ⚠️ Validar | Usar para Data de Venda |
| `deal_origin` | `/negocios/listar` ou `/clientes/detalhes` | String | Não | "Google Ads", "Zap", "Indicação", etc. | ⚠️ Validar | Usar para Origem de Captação |
| `user_id` (corretor) | `/negocios/listar` | String/Int | Sim | ID do corretor | ✅ Confirmado | Usar para Comissão e RBAC |
| `property_id` | `/imoveis/listar` | String/Int | Sim | Único por imóvel | ✅ Confirmado | Usar como chave estrangeira |

---

## 8. Arquitetura de Dados Recomendada (Conceitual)

### **Modelo Conceitual (ER Diagram)**

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│   CLIENTS   │         │  PROPERTIES  │         │    DEALS     │
├─────────────┤         ├──────────────┤         ├──────────────┤
│ client_id   │◄────────│ property_id  │────────►│ deal_id      │
│ name        │         │ address      │         │ client_id    │
│ email       │         │ type         │         │ property_id  │
│ phone       │         │ area         │         │ user_id      │
│ origin      │         │ bedrooms     │         │ status       │
│ created_at  │         │ created_at   │         │ value        │
│ deleted_at  │         │ deleted_at   │         │ date_signed  │
└─────────────┘         └──────────────┘         │ created_at   │
       │                                         │ updated_at   │
       │                                         │ deleted_at   │
       │                                         └──────────────┘
       │                                                 │
       └─────────────────────┬───────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  DEAL_HISTORY    │
                    ├──────────────────┤
                    │ history_id       │
                    │ deal_id          │
                    │ status_from      │
                    │ status_to        │
                    │ changed_by       │
                    │ changed_at       │
                    └──────────────────┘

┌──────────────────┐
│  AUDIT_LOGS      │
├──────────────────┤
│ log_id           │
│ user_id          │
│ action           │
│ resource_type    │
│ resource_id      │
│ timestamp        │
│ details          │
└──────────────────┘
```

### **Tabelas Principais (PostgreSQL)**

```sql
-- Clientes
CREATE TABLE clients (
  client_id SERIAL PRIMARY KEY,
  vista_client_id VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(20),
  origin VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  CONSTRAINT no_duplicate_vista_id UNIQUE (vista_client_id)
);

-- Imóveis
CREATE TABLE properties (
  property_id SERIAL PRIMARY KEY,
  vista_property_id VARCHAR(255) UNIQUE NOT NULL,
  address VARCHAR(500) NOT NULL,
  type VARCHAR(50),
  area FLOAT,
  bedrooms INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL
);

-- Negócios (Deals)
CREATE TABLE deals (
  deal_id SERIAL PRIMARY KEY,
  vista_deal_id VARCHAR(255) UNIQUE NOT NULL,
  client_id INT NOT NULL,
  property_id INT,
  user_id INT NOT NULL,
  status VARCHAR(50) NOT NULL,
  value DECIMAL(15, 2),
  date_signed DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (client_id) REFERENCES clients(client_id),
  FOREIGN KEY (property_id) REFERENCES properties(property_id),
  CONSTRAINT check_status IN ('Em Negociação', 'Proposta Enviada', 'Contrato Assinado', 'Cancelado')
);

-- Histórico de Negócios
CREATE TABLE deal_history (
  history_id SERIAL PRIMARY KEY,
  deal_id INT NOT NULL,
  status_from VARCHAR(50),
  status_to VARCHAR(50) NOT NULL,
  changed_by INT,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (deal_id) REFERENCES deals(deal_id)
);

-- Logs de Auditoria
CREATE TABLE audit_logs (
  log_id SERIAL PRIMARY KEY,
  user_id INT,
  action VARCHAR(50),
  resource_type VARCHAR(50),
  resource_id INT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  details JSONB
);

-- Índices para Performance
CREATE INDEX idx_clients_vista_id ON clients(vista_client_id);
CREATE INDEX idx_deals_status ON deals(status);
CREATE INDEX idx_deals_date_signed ON deals(date_signed);
CREATE INDEX idx_deals_user_id ON deals(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
```

### **Estratégia de Cache (Redis)**

```
# Cache de Funil (atualizado diariamente)
cache_key: "funnel:2026-08:leads" → 150 (count)
cache_key: "funnel:2026-08:opportunities" → 45 (count)
cache_key: "funnel:2026-08:sales" → 12 (count)
TTL: 24 horas

# Cache de VGV por Corretor (atualizado diariamente)
cache_key: "vgv:2026-08:user_123" → 450000.00 (R$)
TTL: 24 horas

# Cache de Taxa de Conversão (atualizado mensalmente)
cache_key: "conversion_rate:2026-08" → 8.0 (%)
TTL: 30 dias

# Cache de Origem de Captação (atualizado mensalmente)
cache_key: "origin:2026-08:google_ads" → 50 (count)
cache_key: "origin:2026-08:zap" → 60 (count)
TTL: 30 dias
```

---

## 9. Plano de Validação e Reconciliação

### **Processo de Reconciliação (Fase 3)**

**Passo 1: Extração de Dados do Power BI**
- Exportar relatório de Leads, Oportunidades, Vendas, VGV para período jan–ago 2026
- Formato: CSV com colunas (período, métrica, valor, corretor)
- Responsável: Manduca

**Passo 2: Extração de Dados do Dashboard Gralha**
- Executar queries no PostgreSQL para mesmas métricas e período
- Formato: CSV com mesmas colunas
- Responsável: Atlas

**Passo 3: Comparação Automatizada**
```python
# Script Python para reconciliação
import pandas as pd

# Carregar dados
power_bi = pd.read_csv('power_bi_export.csv')
dashboard = pd.read_csv('dashboard_export.csv')

# Comparar
comparison = power_bi.merge(dashboard, on=['periodo', 'metrica', 'corretor'], how='outer')
comparison['diferenca_pct'] = ((comparison['valor_y'] - comparison['valor_x']) / comparison['valor_x'] * 100).abs()

# Filtrar discrepâncias
discrepancias = comparison[comparison['diferenca_pct'] > 2]  # >2% de diferença

# Gerar relatório
print(f"Total de linhas: {len(comparison)}")
print(f"Discrepâncias: {len(discrepancias)}")
print(discrepancias.to_string())
```

**Passo 4: Investigação de Discrepâncias**
- Para cada discrepância >2%, investigar causa
- Possíveis causas: Dados incompletos, status diferente, período diferente, soft delete
- Documentar causa e ação corretiva
- Responsável: Atlas + Manduca

**Passo 5: Correção e Revalidação**
- Implementar correções no backend/banco de dados
- Reexecutar reconciliação
- Validar que discrepância agora está <2%
- Responsável: Antigravity + Atlas

### **Testes de Acurácia (Fase 3)**

| Teste | Método | Critério de Aceite | Responsável |
|-------|--------|-------------------|-------------|
| **Teste 1: Leads Únicos** | Contar `DISTINCT client_id` em Dashboard; comparar com Power BI | ±2% | Atlas |
| **Teste 2: Vendas Exatas** | Contar negócios com status="Contrato Assinado"; comparar com Power BI | 0% | Atlas |
| **Teste 3: VGV Exato** | Somar `value` de negócios com status="Contrato Assinado"; comparar com Power BI | 0% | Atlas |
| **Teste 4: Taxa de Conversão** | Calcular (Vendas / Leads) × 100; comparar com Power BI | ±0.5pp | Atlas |
| **Teste 5: Ciclo de Venda** | Calcular dias médios entre Lead e Venda; comparar com Power BI | ±1 dia | Atlas |
| **Teste 6: Comissão por Corretor** | Somar comissões por `user_id`; comparar com Power BI | ±5% | Atlas |
| **Teste 7: Origem de Captação** | Contar leads por `origin`; comparar com Power BI | ±10% | Atlas |

### **Plano de Amostragem**

- **Amostra 1:** 10 clientes aleatórios; verificar todos os campos (nome, email, telefone, origem)
- **Amostra 2:** 10 negócios aleatórios; verificar status, valor, data de assinatura
- **Amostra 3:** 5 corretores top; verificar VGV, comissão, taxa de conversão
- **Amostra 4:** Período jan–mar 2026 (completo); reconciliação total

---

## 10. Riscos, Contingências e Critérios de Go/No-Go

### **Matriz de Riscos**

| # | Risco | Probabilidade | Impacto | Mitigação | Plano B |
|---|-------|--------------|--------|-----------|---------|
| **R1** | API Vista indisponível (>4h/dia) | Média | Alto | Monitoramento 24/7; contrato SLA com Loft | Cache local; sincronização offline |
| **R2** | Falha de sincronização (dados incompletos) | Média | Alto | Idempotência; checkpoints; alertas | Reprocessamento manual; rollback |
| **R3** | Campo "Venda Concluída" não existe em Vista | Baixa | Alto | Teste em Fase 0; contato com Loft | Usar status alternativo; lógica customizada |
| **R4** | Data de Venda não mapeada em Vista | Baixa | Alto | Teste em Fase 0; contato com Loft | Usar data de criação do negócio; lógica customizada |
| **R5** | Origem de Captação não rastreada | Média | Médio | Implementar UTM; integração com marketing | Usar "Direto" como fallback; pós-MVP melhora |
| **R6** | Comissões não calculadas corretamente | Média | Alto | Documentar regras; testes unitários; auditoria | Cálculo manual; revisão por Manduca |
| **R7** | Performance ruim (funil carrega >5s) | Baixa | Médio | Cache Redis; índices PostgreSQL; testes de carga | Otimização de queries; escalabilidade |
| **R8** | Segurança: Dados expostos (LGPD) | Baixa | Crítico | RBAC; criptografia; logs de auditoria | Notificação de incidente; auditoria forense |
| **R9** | Repositório MarcelManduca/crm-vista-BI privado | Alta | Médio | Contato com Manduca em Fase 0 | Usar documentação alternativa; criar novo repo |
| **R10** | Reconciliação com Power BI falha (>5% discrepância) | Média | Alto | Testes em Fase 3; investigação de causas | Atrasar lançamento; revisar lógica |

### **Critérios de Go/No-Go para Lançamento**

| Critério | Go | No-Go | Responsável |
|----------|-----|-------|-------------|
| **Reconciliação de Leads** | ±2% | >2% | Atlas |
| **Reconciliação de Vendas** | 0% | >0% | Atlas |
| **Reconciliação de VGV** | 0% | >0% | Atlas |
| **Erros Críticos em Testes** | 0 | >0 | Antigravity |
| **Performance: Funil** | <1s | >1s | Lovable |
| **Performance: Exportação** | <5s | >5s | Lovable |
| **Disponibilidade em Carga** | ≥99.5% | <99.5% | Antigravity |
| **Cobertura de Testes** | ≥80% | <80% | Todos |
| **Adoção de Usuários** | ≥70% logins | <70% | Manduca |
| **Incidentes Críticos em 1 Semana** | 0 | >0 | Todos |

**Decisão Final:** Go se todos os critérios atendidos; No-Go se qualquer critério falhar. Atrasar lançamento até correção.

---

## 11. Backlog Priorizado por Frente (P0/P1/P2)

### **Antigravity (Backend)**

#### **P0 (MVP - Crítico)**
- [ ] Scaffold FastAPI + PostgreSQL + Redis + Docker Compose
- [ ] Autenticação JWT; RBAC (Corretor/Gerente/Admin)
- [ ] Tabelas: clients, properties, deals, deal_history, audit_logs
- [ ] Endpoints: `GET /api/deals/funnel`, `GET /api/deals/vgv`, `GET /api/deals/conversion`
- [ ] Logs de auditoria (user_id, ação, timestamp, recurso)
- [ ] Testes unitários (≥80% cobertura)
- [ ] Tratamento de erros (validação, 400/401/403/500)

#### **P1 (MVP - Importante)**
- [ ] Criptografia em trânsito (HTTPS/TLS)
- [ ] Rate limiting (100 req/min por usuário)
- [ ] Paginação em endpoints (limit, offset)
- [ ] Filtros avançados (período, corretor, tipo de imóvel)
- [ ] Soft delete (flag `deleted_at`)
- [ ] Testes de integração (API + PostgreSQL)
- [ ] Documentação de API (Swagger/OpenAPI)

#### **P2 (Pós-MVP)**
- [ ] Criptografia em repouso (PostgreSQL)
- [ ] Webhooks bidireccionais (Vista → Dashboard)
- [ ] Alertas inteligentes (anomalias, thresholds)
- [ ] Integração com Power BI (API)
- [ ] Escalabilidade (sharding, replicação)
- [ ] Monitoramento avançado (Prometheus, Grafana)

---

### **Lovable (Frontend)**

#### **P0 (MVP - Crítico)**
- [ ] Componente Funil (Leads → Oportunidades → Vendas)
- [ ] Componente VGV por Corretor (tabela/gráfico)
- [ ] Componente Taxa de Conversão (gráfico)
- [ ] Filtros (período, corretor, tipo de imóvel)
- [ ] Exportação (CSV/JSON)
- [ ] Login/Logout
- [ ] Responsividade (desktop, tablet)

#### **P1 (MVP - Importante)**
- [ ] Testes E2E (Cypress/Playwright; ≥70% cobertura)
- [ ] Tratamento de erros (mensagens amigáveis)
- [ ] Loading states (spinners, skeletons)
- [ ] Paginação em tabelas
- [ ] Busca/filtro em tempo real
- [ ] Temas (light/dark mode)
- [ ] Acessibilidade (WCAG 2.1 AA)

#### **P2 (Pós-MVP)**
- [ ] Dashboards customizáveis (drag-and-drop)
- [ ] Alertas em tempo real (notificações)
- [ ] Integração com Power BI (embed)
- [ ] Análise preditiva (gráficos de tendência)
- [ ] Exportação em PDF/Excel
- [ ] Integração com Slack/Teams

---

### **Atlas (Sincronização/Dados)**

#### **P0 (MVP - Crítico)**
- [ ] Connector para API Vista (autenticação, paginação)
- [ ] Pipeline de sincronização (Clientes, Imóveis, Negócios)
- [ ] Idempotência (chaves únicas)
- [ ] Deduplicação (soft delete)
- [ ] Tratamento de falhas (retry, logging)
- [ ] Checkpoints (recuperação de falhas)
- [ ] Testes de sincronização (100 registros sem erros)

#### **P1 (MVP - Importante)**
- [ ] Mapeamento de schema (via `/listarcampos`)
- [ ] Validação de dados (tipos, obrigatoriedade)
- [ ] Transformação de dados (normalização, limpeza)
- [ ] Reconciliação com Power BI (script automatizado)
- [ ] Documentação de dados (dicionário, linhagem)
- [ ] Testes de carga (1000 registros/min)

#### **P2 (Pós-MVP)**
- [ ] Sincronização em tempo real (webhooks)
- [ ] Atribuição multi-toque (W-Shaped, algorítmica)
- [ ] Integração com plataformas de marketing (Ads, email)
- [ ] CDC (Change Data Capture) para incrementais
- [ ] Data quality monitoring (anomalias, outliers)
- [ ] Backup e disaster recovery

---

## 12. Perguntas Críticas para Manduca/Gralha

**Antes de iniciar Fase 1, as seguintes perguntas devem ser respondidas:**

1. **Repositório GitHub:** O repositório `MarcelManduca/crm-vista-BI` é privado ou público? Se privado, como fornecer acesso (credenciais, invite)?

2. **Regras de Comissão:** Qual é a tabela de comissões da Gralha? (ex: 6% para imóvel urbano, 50/50 split com corretor). Existem descontos, bônus ou splits complexos?

3. **Período de Análise:** Qual período deve ser considerado para reconciliação inicial? (ex: jan–ago 2026, ou últimos 12 meses?)

4. **Dados de Referência:** Qual é o número esperado de Leads, Oportunidades e Vendas para ago/2026? (para validação rápida)

5. **Acesso à API Vista:** Quais são as credenciais de teste para a API Vista? (chave de API, tenant, rate limits)

6. **Campos Críticos:** Confirmar nomes exatos dos campos em Vista para: "Venda Concluída", "Data de Venda", "Origem de Captação".

7. **Integrações Futuras:** Quais são as prioridades pós-MVP? (ex: Alertas, Power BI, Análise Preditiva)

8. **Usuários:** Quantos corretores, gerentes e admins usarão o dashboard? (para planejamento de capacidade)

9. **SLA:** Qual é o SLA esperado? (ex: 99.5% disponibilidade, <1s de latência)

10. **Conformidade:** Existem requisitos específicos de LGPD ou segurança além dos padrões?

---

## 13. Fontes e Limitações

### **Fontes Consultadas**

| Fonte | URL | Tipo | Confiabilidade |
|-------|-----|------|----------------|
| API Vista CRM (Loft) | https://novovista-rest.vistahost.com.br/doc/ | Documentação Oficial | ✅ Alta |
| Red-Gate: Real Estate Data Model | https://www.red-gate.com/blog/managing-houses-and-properties-a-real-estate-agency-data-model/ | Artigo Técnico | ✅ Alta |
| Salesforce: Real Estate CRM | https://www.salesforce.com/crm/real-estate-crm/ | Documentação de Produto | ✅ Alta |
| Nimble: CRM for Real Estate | https://www.nimble.com/blog/crm-for-real-estate/ | Artigo de Indústria | ✅ Média |
| Use Mix: Métricas de Vendas Imobiliária 2026 | https://www.usemix.app/blog/metricas-vendas-imobiliaria-2026 | Artigo de Indústria | ✅ Média |
| RD Station: Rastreamento de Origem | https://ajuda.rdstation.com/s/article/Rastrear-origem-de-oportunidades-via-Fontes-e-Campanhas | Documentação de Produto | ✅ Alta |
| Salesforce: Multi-Touch Attribution | https://www.salesforce.com/eu/marketing/multi-touch-attribution/ | Documentação de Produto | ✅ Alta |
| FastAPI: Documentação Oficial | https://fastapi.tiangolo.com/ | Documentação Oficial | ✅ Alta |
| ETL Best Practices | https://dev.to/chaets/why-idempotency-is-so-important-in-data-engineering-24mj | Artigo Técnico | ✅ Média |
| LGPD Compliance | https://bigid.com/blog/brazil-lgpd-compliance-guide/ | Artigo de Conformidade | ✅ Alta |

### **Limitações da Análise**

1. **Repositório Privado:** Não foi possível acessar `MarcelManduca/crm-vista-BI` para validar estrutura, documentação e código existente. Recomendações baseadas em padrões de indústria.

2. **API Vista Não Testada:** Recomendações baseadas em documentação oficial; testes práticos necessários em Fase 0 para confirmar endpoints, schema, autenticação, rate limits.

3. **Regras Comerciais Não Documentadas:** Cálculo de comissões, splits, descontos e bônus não foram confirmados. Recomendações baseadas em padrões imobiliários; validação com Manduca necessária.

4. **Dados Históricos Não Acessados:** Não foi possível validar qualidade, completude e consistência dos dados históricos em Vista. Testes em Fase 0 necessários.

5. **Capacidade da Equipe Desconhecida:** Roadmap assume capacidade média (2–3 sprints por fase). Ajustes necessários conforme confirmação de capacidade real.

6. **Requisitos de Negócio Parciais:** Algumas decisões (ex: tolerância de reconciliação, período histórico) baseadas em padrões; validação com stakeholders necessária.

7. **Integração com Power BI Não Testada:** Reconciliação recomendada em Fase 3; possíveis discrepâncias não previstas.

---

## 14. Próximos Passos Imediatos

1. **Semana 1:** Manduca confirma acesso ao repositório e fornece credenciais de API Vista
2. **Semana 1:** Atlas executa testes de descoberta (Seção 7) para validar hipóteses críticas
3. **Semana 2:** Manduca documenta regras de comissão e confirma período de análise
4. **Semana 2:** Lovable apresenta wireframes do dashboard para aprovação
5. **Semana 2:** Antigravity define convenções de código e inicia scaffold
6. **Semana 3:** Fase 1 inicia (backend + sincronização)

---

**Preparado por:** Manus AI  
**Data:** Agosto 2026  
**Versão:** 1.0  
**Status:** Pronto para Aprovação Executiva
