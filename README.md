# AREF — Análise de Risco em Estádios de Futebol

Aplicação web do **Ministério Público do Estado da Bahia (MPBA)** que implementa a metodologia **AREF (Avaliação de Risco em Estádios de Futebol) da ABIN** para classificar o risco de partidas de futebol e dimensionar efetivos de segurança em **Salvador/BA**.

Baseada na planilha original AREF da Federação de Futebol do Estado do Rio de Janeiro (FERJ), adaptada para a realidade institucional de Salvador (PMBA, CBMBA, GCM-SSA, Transalvador, Limpurb, SUSP, SUVISA, SEMOP, SAS, Metrô SSA).

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`.

## Executar os testes

```bash
python -m pytest tests/ -v
```

17 testes validando a paridade entre o port Python e as fórmulas da planilha ABIN.

## Deploy público — Streamlit Community Cloud (recomendado para teste)

1. Crie um repositório no GitHub (público) com o conteúdo deste diretório.
2. Acesse [https://share.streamlit.io](https://share.streamlit.io) e conecte sua conta GitHub.
3. Clique em **New app**, selecione o repositório, aponte para `app.py`.
4. Deploy automático — a aplicação fica em `https://<seu-app>.streamlit.app`.
5. Compartilhe o link com os promotores.

### Alternativa rápida — ngrok (sem deploy, para teste em segundos)

```bash
streamlit run app.py &
ngrok http 8501
```

O ngrok devolve um link público temporário. Útil para validar com 2–3 colegas antes do deploy oficial.

## Estrutura

```
aref-mpba/
├── app.py                     # Entry point Streamlit
├── .streamlit/config.toml     # Cores institucionais MPBA
├── aref/
│   ├── model.py               # 7 funções puras AREF (testável sem Streamlit)
│   ├── tables.py              # Loader das matrizes ABIN + override
│   └── basedados.py           # Loader de efetivos Salvador
├── ui/
│   ├── header.py              # Cabeçalho MPBA
│   ├── input_form.py          # Formulário 14 parâmetros × 2 torcidas
│   ├── output_view.py         # Resultado + tabela de efetivos
│   ├── tables_editor.py       # Edição das matrizes ABIN
│   ├── analysis_io.py         # Export/Import JSON
│   └── footer.py              # Rodapé institucional
├── data/
│   ├── default_tables.json    # Matrizes 4, 7, 11 extraídas da planilha
│   ├── basedados_ssa.json     # Efetivos Salvador por órgão/papel/risco
│   └── catalogos_ba.json      # Clubes, estádios, torneios da Bahia
├── assets/
│   └── mpba_logo.png          # Logo MPBA (placeholder se ausente)
├── tests/
│   └── test_model.py          # 17 testes de paridade + cobertura
├── requirements.txt
└── README.md
```

## Persistência

A aplicação **não armazena dados no servidor**. Cada análise pode ser:

- **Exportada** como arquivo `.json` (botão no sidebar)
- **Reimportada** depois para continuar/revisar (uploader no sidebar)

Isto resolve dois problemas: (a) servidor compartilhado entre promotores e (b) conformidade com a LGPD para dados de inteligência sobre torcidas.

## Adaptando para outra cidade

1. Edite `data/basedados_ssa.json` substituindo os órgãos/papéis pelos da sua realidade local.
2. Edite `data/catalogos_ba.json` ajustando clubes, estádios e torneios.
3. Ajuste `ui/header.py` para o branding da sua instituição (cores em `.streamlit/config.toml`).

A lógica AREF em `aref/model.py` é genérica — não depende de Salvador.

## Cascata de cálculo AREF (visão geral)

A análise é feita **por torcida**, em 7 etapas que reproduzem as Tabelas 2/3/4/5/6/7/8/9/10/11 da metodologia ABIN:

1. **Perfil da Ameaça** (Tabela 2): média aritmética dos 5 atributos → MUITO BAIXO/BAIXO/MÉDIO/ALTO/MUITO ALTO.
2. **Sistema de Segurança** (Tabela 3): média dos 4 atributos → DESPREZÍVEL/INSUFICIENTE/RAZOÁVEL/SUFICIENTE/ADEQUADO.
3. **Efetividade da Ameaça** (Tabelas 4+5): lookup na Matriz 4 (Perfil × Segurança) → 1–25 pts → MUITO BAIXA..MUITO ALTA.
4. **Histórico da Torcida** (Tabela 6): contagem de respostas SIM (0–3) → NÍVEL 1..4.
5. **Probabilidade** (Tabelas 7+8): lookup na Matriz 7 (Efetividade × Histórico) → 1–25 pts → REMOTA..ALTAMENTE PROVÁVEL.
6. **Impacto** (Tabelas 9+10): soma dos 3 fatores → MUITO BAIXO/BAIXO/MODERADO/SEVERO/CRÍTICO.
7. **Risco Final** (Tabela 11): lookup na Matriz 11 (Probabilidade × Impacto) → 1–100 pts → MUITO BAIXO/BAIXO/MÉDIO/ALTO/MUITO ALTO.

A **classificação do jogo** é o **máximo** entre as duas torcidas. Em seguida, BASEDADOS define os efetivos recomendados por órgão para o nível final.

## Observações sobre fidelidade à planilha original

- A célula MUITO BAIXO × RAZOÁVEL da Matriz 4 da planilha original retornava 0 por um **erro de digitação** (`RAZOAVÉL` sem acento agudo correto nas fórmulas). Aqui está corrigida para o valor consistente com a metodologia (3).
- A aba "Plano de Ação" da planilha original (texto livre com #REF! quebrados) não foi replicada — apenas o modelo AREF.

## Licença / Uso

Aplicação interna do Ministério Público do Estado da Bahia. Baseada na metodologia pública AREF da ABIN — Agência Brasileira de Inteligência.
