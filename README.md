# ABAPify

<p align="center">
  <img src="docs/images/main.png" alt="ABAPify Logo" width="300"/>
</p>

ABAPify é um gerador de código ABAP baseado em IA. Ele permite criar rapidamente diversos tipos de código ABAP, incluindo relatórios ALV, classes, módulos de função e estruturas, utilizando modelos de linguagem avançados como Groq e OpenAI.

## Características

- Geração de vários tipos de código ABAP
- Interface de linha de comando amigável
- Suporte a múltiplos provedores de IA (Groq, OpenAI)
- Templates específicos para diferentes componentes ABAP
- Persistência automática dos códigos gerados

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/esc4n0rx/abapify.git
   cd abapify
   ```

2. Crie e ative um ambiente virtual:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure suas chaves de API:

   Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API:
   ```
   GROQ_API_KEY=sua_chave_aqui
   # ou
   # OPENAI_API_KEY=sua_chave_aqui
   ```

## Uso

### Interface Visual

A maneira mais simples de usar o ABAPify é através de sua interface visual interativa:

```
python main.py
```

Isso iniciará um menu interativo que guiará você pelo processo de geração de código.

### Exemplos de uso via linha de comando

O ABAPify também pode ser usado via linha de comando para integração com scripts:

**Gerar um relatório ALV:**
```
python -m abapify generate-alv --description "Relatório de saldos de estoque" --tables MARA MAKT MCHB --output ./output
```

**Gerar uma classe ABAP:**
```
python -m abapify generate-class --description "Classe para processamento de pedidos" --methods constructor process_order validate --output ./output
```

**Gerar um módulo de função:**
```
python -m abapify generate-function --description "Cálculo de impostos" --params "I_VBELN:CHAR(10):I" "E_RESULT:BAPIRET2:E" --output ./output
```

## Estrutura do Projeto

```
abapify/
├── pyproject.toml
├── requirements.txt
├── README.md
├── main.py                # Ponto de entrada principal
├── abapify/
│   ├── cli/               # Interface de linha de comando
│   ├── core/              # Lógica principal
│   ├── llm/               # Integração com modelos de linguagem
│   ├── prompts/           # Templates de prompts
│   ├── templates/         # Templates de código
│   └── utils/             # Utilitários
└── tests/                 # Testes unitários
```

## Exemplos de códigos gerados

### Exemplo de Relatório ALV

```abap
*----------------------------------------------------------------------*
* Programa gerado pelo ABAPify - Gerador de código ABAP baseado em IA  *
* Data de geração: 25.04.2025                                         *
*----------------------------------------------------------------------*

REPORT zr_estoque_materiais.

TABLES: mara, makt, mchb.

* Tipos e estruturas
TYPES: BEGIN OF ty_saida,
         matnr     TYPE mara-matnr,
         maktx     TYPE makt-maktx,
         werks     TYPE mchb-werks,
         lgort     TYPE mchb-lgort,
         charg     TYPE mchb-charg,
         clabs     TYPE mchb-clabs,
         cinsm     TYPE mchb-cinsm,
         cspem     TYPE mchb-cspem,
         meins     TYPE mara-meins,
       END OF ty_saida.

* Tabelas internas
DATA: gt_saida TYPE TABLE OF ty_saida,
      gs_saida TYPE ty_saida.

* Tela de seleção
SELECTION-SCREEN BEGIN OF BLOCK b1 WITH FRAME TITLE TEXT-001.
  SELECT-OPTIONS: s_matnr FOR mara-matnr,
                  s_werks FOR mchb-werks,
                  s_lgort FOR mchb-lgort.
SELECTION-SCREEN END OF BLOCK b1.
```

### Exemplo de Classe ABAP

```abap
*----------------------------------------------------------------------*
* Programa gerado pelo ABAPify - Gerador de código ABAP baseado em IA  *
* Data de geração: 25.04.2025                                         *
*----------------------------------------------------------------------*

CLASS zcl_proc_pedido DEFINITION
  PUBLIC
  FINAL
  CREATE PUBLIC.

  PUBLIC SECTION.
    METHODS:
      constructor,
      process_order
        IMPORTING
          iv_vbeln      TYPE vbeln_va
        EXPORTING
          et_return     TYPE bapiret2_t
        RETURNING VALUE(rv_success) TYPE abap_bool,
      validate
        IMPORTING
          iv_vbeln     TYPE vbeln_va
        RETURNING VALUE(rv_valid) TYPE abap_bool.

  PRIVATE SECTION.
    DATA:
      mv_last_order TYPE vbeln_va.

    METHODS:
      check_status
        IMPORTING
          iv_vbeln           TYPE vbeln_va
        RETURNING VALUE(rv_processable) TYPE abap_bool.

ENDCLASS.
```

## Recursos Adicionais

- **Diretório de saída**: Por padrão, os códigos são gerados no diretório `./output`, mas você pode especificar qualquer diretório.
- **Personalização**: Os prompts de sistema e usuário podem ser personalizados no diretório `abapify/prompts/`.
- **Extensibilidade**: A estrutura modular facilita a adição de novos tipos de código para geração.

## Solução de Problemas

- **Chave de API não encontrada**: Verifique se o arquivo `.env` está no diretório raiz e contém a chave correta.
- **Erro de módulo não encontrado**: Execute o programa a partir do diretório raiz do projeto.
- **Diretório de saída**: No Windows, use `.\output` em vez de `./output` para evitar problemas com caminhos.

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit de suas alterações (`git commit -am 'Adicionar nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.