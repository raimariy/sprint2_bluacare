# Sprint 1 - Exploração, Arquitetura e PoC

## BluaCare

| Nome | RM |
|------|-----|
| Ana Clara Alcântara Lopes | 568463 |
| Caroline Ceccon Rodrigues de Almeida | 567964 |
| Izabely dos Santos Silva | 567088 |
| Natalia Heloisa Rocha de Alcantara Bezerra | 568570 |
| Raissa Marinho de Jesus Viana | 568301 |

---

## Persona Escolhida: Beneficiário Final
 
O agente **Blua** atende o beneficiário do plano Care Plus — o paciente que busca orientação de saúde preventiva, triagem de sintomas e acesso a teleconsultas, sem precisar sair de casa.
 
**Justificativa:** É a persona de maior escala e impacto direto no negócio. O beneficiário é o ponto de entrada de toda jornada de saúde: uma triagem bem feita reduz consultas desnecessárias, prioriza emergências e melhora a experiência do plano.
 
---
 
## Stack Técnico
 
| Componente | Tecnologia | Justificativa |
|---|---|---|
| LLM Principal | `gpt-oss:20b-cloud` via Ollama API | Open-weight, sem envio de dados a terceiros, latência média 1.4s |
| LLM Secundário | `gemma3:4b-cloud` via Ollama API | Modelo leve para comparação de custo-benefício |
| Framework | LangChain (`langchain-openai`) | Compatibilidade OpenAI, fácil integração com tools e memória |
| Memória | `conversation_memory.py` (in-process) | Histórico de sessão por turno, sem dependência de banco externo |
| Function Calling | Simulado via JSON Schema | 3 tools obrigatórias com retornos realistas |
| Ambiente | Python 3.13 + `.env` + `python-dotenv` | Configuração segura sem exposição de chaves |
 
---