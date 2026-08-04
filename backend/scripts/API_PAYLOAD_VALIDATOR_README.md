# API Payload Validator v1

**Simulador de Testes de API para Dashboard Gralha**

---

## 📋 Descrição

O **API Payload Validator** é uma ferramenta web interativa (HTML standalone) que permite testar, validar e homogenizar dados vindos da API Vista CRM antes de serem armazenados no banco de dados do Dashboard Gralha.

**Objetivo:** Garantir qualidade, consistência e conformidade dos dados na Fase 1 de desenvolvimento.

---

## 🚀 Como Usar

### 1. Abrir o Validador

```bash
# Opção A: Abrir diretamente no navegador
open backend/scripts/api_payload_validator.html

# Opção B: Servir via Python
cd backend/scripts
python3 -m http.server 8080
# Acessar: http://localhost:8080/api_payload_validator.html
```

### 2. Fluxo de Uso

#### Passo 1: Selecionar Tipo de Recurso
- Clientes
- Imóveis
- Negócios
- Usuários

#### Passo 2: Definir Período (Opcional)
- Data Inicial
- Data Final
- Filtra dados no período especificado

#### Passo 3: Carregar Dados
- **Opção A:** Clique em "Carregar Template" para dados de exemplo
- **Opção B:** Cole payload JSON da API Vista no campo de entrada

#### Passo 4: Validar
- Clique em "✅ Validar" para verificar:
  - Campos obrigatórios
  - Tipos de dados
  - Formatos (email, telefone, etc.)

#### Passo 5: Analisar
- Clique em "🔍 Analisar" para:
  - Gerar estatísticas
  - Homogenizar dados
  - Exportar dados limpos

#### Passo 6: Exportar
- Aba "Exportar" contém dados homogenizados
- Download JSON ou copiar para clipboard

---

## ✅ Funcionalidades

### 1. Validação de Dados

**Regras por Tipo de Recurso:**

#### Clientes
```
Campos Obrigatórios: id, name, email, phone
Tipos Esperados: string, string, string, string
Padrões:
  - email: válido (contém @)
  - phone: 10-11 dígitos
```

#### Imóveis
```
Campos Obrigatórios: id, address, city, state, type, area, price
Tipos Esperados: string, string, string, string, string, number, number
```

#### Negócios
```
Campos Obrigatórios: id, client_id, property_id, user_id, status, value
Tipos Esperados: string, string, string, string, string, number
```

#### Usuários
```
Campos Obrigatórios: id, username, email, full_name, role
Tipos Esperados: string, string, string, string, string
```

### 2. Homogenização de Dados

**Normalização Automática:**

#### Clientes
- **Telefone:** Remove caracteres especiais (apenas dígitos)
- **Email:** Converte para minúsculas e remove espaços
- **Origem:** Mapeia valores inconsistentes
  - "google" → "Google Ads"
  - "meta" → "Meta Ads"
  - "zap" → "Zap Imóveis"
  - "indicacao" → "Indicação"
  - "direto" → "Direto"

#### Imóveis
- **Tipo:** Normaliza variações
  - "apt" → "Apartamento"
  - "casa" → "Casa"
  - "lote" → "Lote"
  - "comercial" → "Comercial"
- **Estado:** Converte para maiúsculas (SP, RJ, etc.)

#### Negócios
- **Status:** Mapeia status inconsistentes
  - "lead" → "Lead"
  - "negociacao" → "Em Negociação"
  - "proposta" → "Proposta Enviada"
  - "contrato" → "Contrato Assinado"
  - "fechado" → "Fechado"

### 3. Análise de Dados

**Estatísticas Geradas:**

#### Clientes
- Quantidade por origem
- Período analisado
- Registros válidos/inválidos

#### Imóveis
- Quantidade por tipo
- Área total
- Preço médio

#### Negócios
- Quantidade por status
- VGV (Valor Geral de Vendas)
- Taxa de conversão

---

## 📊 Abas de Resultados

### Aba: Estatísticas
- Cards com métricas principais
- Total de registros
- Registros válidos/inválidos
- Avisos

### Aba: Validação
- Detalhes de cada registro
- Erros encontrados
- Padrões violados
- Resumo geral

### Aba: Homogenização
- Regras aplicadas
- Registros processados
- Transformações realizadas

### Aba: Exportar
- Dados homogenizados em JSON
- Download para arquivo
- Copiar para clipboard

---

## 🔍 Exemplos de Uso

### Exemplo 1: Validar Clientes

**Payload de Entrada:**
```json
[
  {
    "id": "cli_001",
    "name": "João Silva",
    "email": "joao@example.com",
    "phone": "11999999999",
    "origin": "google"
  },
  {
    "id": "cli_002",
    "name": "Maria Santos",
    "email": "maria@example.com",
    "phone": "11 98888-8888",
    "origin": "zap"
  }
]
```

**Resultado da Validação:**
- ✅ Registro 1: Válido
- ⚠️ Registro 2: Telefone com caracteres especiais

**Após Homogenização:**
```json
[
  {
    "id": "cli_001",
    "name": "João Silva",
    "email": "joao@example.com",
    "phone": "11999999999",
    "origin": "Google Ads"
  },
  {
    "id": "cli_002",
    "name": "Maria Santos",
    "email": "maria@example.com",
    "phone": "11988888888",
    "origin": "Zap Imóveis"
  }
]
```

### Exemplo 2: Analisar Imóveis por Período

**Período:** 01/08/2026 a 31/08/2026

**Resultado:**
- Total: 10 imóveis
- Apartamentos: 6
- Casas: 3
- Lotes: 1
- Área Total: 2.500 m²
- Preço Médio: R$ 750.000

### Exemplo 3: Validar Negócios

**Payload:**
```json
[
  {
    "id": "deal_001",
    "client_id": "cli_001",
    "property_id": "prop_001",
    "user_id": "user_001",
    "status": "Contrato Assinado",
    "value": 500000
  }
]
```

**Resultado:**
- ✅ Válido
- VGV: R$ 500.000
- Status: Contrato Assinado

---

## 🎯 Casos de Uso

### 1. Teste de Integração com API Vista
- Cole payload real da API Vista
- Valide estrutura e tipos
- Identifique campos faltantes

### 2. Homogenização de Dados
- Normalize dados inconsistentes
- Aplique regras de transformação
- Exporte dados limpos

### 3. Análise de Qualidade
- Verifique cobertura de dados
- Identifique anomalias
- Gere relatórios

### 4. Teste de Período
- Filtre dados por data
- Analise tendências
- Compare períodos

---

## ⚠️ Limitações Conhecidas

1. **Tamanho de Payload:** Máximo ~10MB (limitação do navegador)
2. **Performance:** Recomendado até 10.000 registros por análise
3. **Offline:** Funciona totalmente offline (sem dependências externas)
4. **Navegadores:** Compatível com Chrome, Firefox, Safari, Edge (versões recentes)

---

## 🔄 Roadmap v2

- [ ] Conectar com API real do Dashboard Gralha
- [ ] Salvar histórico de validações
- [ ] Comparar antes/depois de homogenização
- [ ] Gráficos e visualizações
- [ ] Exportar para CSV
- [ ] Integração com banco de dados
- [ ] Alertas em tempo real
- [ ] Validação customizável

---

## 📝 Notas Técnicas

### Arquitetura
- **Frontend:** HTML5 + CSS3 + JavaScript Vanilla
- **Armazenamento:** LocalStorage (opcional)
- **Dependências:** Nenhuma (standalone)
- **Tamanho:** ~15KB

### Compatibilidade
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Segurança
- ✅ Sem envio de dados para servidor
- ✅ Processamento local apenas
- ✅ Sem cookies ou tracking

---

## 🤝 Integração com Backend

### Próximas Etapas

1. **Criar Endpoint de Validação:**
   ```python
   POST /api/validate/payload
   {
       "resource_type": "clients",
       "data": [...]
   }
   ```

2. **Retornar Resultado:**
   ```json
   {
       "valid": true,
       "total": 100,
       "valid_records": 98,
       "invalid_records": 2,
       "warnings": [...]
   }
   ```

3. **Integrar com ETL:**
   - Validar antes de sincronizar
   - Registrar erros em audit log
   - Reprocessar dados inválidos

---

## 📞 Suporte

**Problemas Comuns:**

1. **"JSON inválido"**
   - Verifique se o JSON está bem formatado
   - Use um validador JSON online

2. **"Campos obrigatórios ausentes"**
   - Verifique a estrutura esperada
   - Consulte as regras de validação

3. **"Dados não aparecem"**
   - Limpe o cache do navegador
   - Recarregue a página

---

## 📄 Licença

Proprietary - Gralha Imóveis

---

**Versão:** 1.0  
**Data:** Agosto 2026  
**Status:** ✅ Pronto para Uso
