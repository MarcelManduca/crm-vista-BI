# Guia de Contribuição - Dashboard Gralha

**Repositório:** Privado - Acesso Restrito  
**Status:** Fase 1 em Desenvolvimento

---

## 📋 Antes de Começar

Este repositório é **privado** e contém código proprietário da Gralha Imóveis. Apenas membros autorizados podem contribuir.

**Leia primeiro:**
- [SECURITY.md](SECURITY.md) - Políticas de segurança
- [README.md](README.md) - Visão geral do projeto
- [docs/dashboard_gralha_orientacao_executiva.md](docs/dashboard_gralha_orientacao_executiva.md) - Orientação técnica

---

## 🚀 Workflow de Desenvolvimento

### 1. Clone o Repositório
```bash
git clone https://github.com/MarcelManduca/crm-vista-BI.git
cd crm-vista-BI
```

### 2. Crie uma Branch de Feature
```bash
git checkout -b feature/sua-feature
# ou para hotfix
git checkout -b hotfix/seu-hotfix
```

### 3. Faça Suas Alterações
- Escreva código limpo e bem documentado
- Siga as convenções de código (PEP 8 para Python)
- Adicione testes para novas funcionalidades
- Atualize documentação se necessário

### 4. Commit com Mensagens Claras
```bash
git commit -m "feat: adicionar endpoint de funil de vendas"
# ou
git commit -m "fix: corrigir cálculo de VGV"
# ou
git commit -m "docs: atualizar guia de API"
```

**Formato de Commit:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação de código
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Tarefas de manutenção

### 5. Faça Push e Crie Pull Request
```bash
git push origin feature/sua-feature
```

Acesse GitHub e crie um Pull Request para `develop`.

### 6. Code Review
- Aguarde revisão de pelo menos 1 membro
- Responda aos comentários
- Faça ajustes se solicitado
- Merge após aprovação

---

## 🧪 Testes

### Rodar Testes Localmente
```bash
# Testes unitários
pytest tests/unit/ -v

# Testes de integração
pytest tests/integration/ -v

# Cobertura
pytest tests/ --cov=app --cov-report=html
```

### Requisitos de Cobertura
- Mínimo 80% de cobertura
- Todas as funcionalidades críticas devem ter testes
- Testes devem passar antes de merge

---

## 📝 Convenções de Código

### Python (Backend)
- Seguir PEP 8
- Usar type hints
- Docstrings em todas as funções públicas
- Máximo 100 caracteres por linha

Exemplo:
```python
def get_funnel_data(
    start_date: date,
    end_date: date,
    broker_id: Optional[int] = None
) -> Dict[str, int]:
    """
    Retorna dados do funil de vendas para o período especificado.
    
    Args:
        start_date: Data inicial do período
        end_date: Data final do período
        broker_id: ID do corretor (opcional)
    
    Returns:
        Dicionário com contagens por estágio do funil
    """
    pass
```

### Commits
- Mensagens em inglês
- Primeira linha com máximo 50 caracteres
- Corpo com máximo 72 caracteres por linha
- Referenciar issues quando aplicável: `Fixes #123`

---

## 🔒 Segurança

### Antes de Fazer Commit
- [ ] Nenhum arquivo `.env` com valores reais
- [ ] Nenhuma chave de API ou token
- [ ] Nenhum dado de cliente real
- [ ] `.gitignore` está atualizado

### Se Você Descobrir uma Vulnerabilidade
- **NÃO** publique em issues
- **CONTATE** imediatamente
- **DOCUMENTE** o incidente
- **REVOGUE** credenciais comprometidas

---

## 📚 Documentação

### Ao Adicionar Nova Funcionalidade
1. Adicione docstring em Python
2. Atualize [docs/](docs/) se necessário
3. Adicione exemplos de uso
4. Documente endpoints em Swagger

### Ao Corrigir um Bug
1. Adicione teste que reproduz o bug
2. Corrija o bug
3. Verifique que o teste passa
4. Documente a correção em commit

---

## 🔄 Processo de Review

### O que Revisor Verifica
- Código segue convenções
- Testes estão presentes e passam
- Documentação está atualizada
- Nenhum secret foi commitado
- Performance é aceitável
- Sem código duplicado

### Como Responder a Feedback
- Agradeça o feedback
- Faça os ajustes solicitados
- Commit com mensagem clara
- Marque como "ready for review" novamente

---

## 🐛 Reportar Bugs

Se encontrar um bug:

1. **Verifique** se já existe issue aberta
2. **Crie** uma nova issue com:
   - Título descritivo
   - Descrição do problema
   - Passos para reproduzir
   - Resultado esperado vs. obtido
   - Ambiente (SO, versão Python, etc.)

---

## 💡 Sugestões de Melhoria

Para sugerir melhorias:

1. **Abra** uma discussion (não issue)
2. **Descreva** a melhoria proposta
3. **Explique** o benefício
4. **Aguarde** feedback da equipe

---

## 📞 Contato

- **Backend:** Manus AI (Fase 1) → Antigravity (Fase 2)
- **Frontend:** Lovable (Fase 3)
- **Dados:** Atlas (Sincronização)
- **PO:** ChatGPT (via issues e discussions)

---

## 📄 Licença

Proprietary - Gralha Imóveis

---

**Obrigado por contribuir ao Dashboard Gralha!** 🚀
