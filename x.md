# ABAPify

**Gerador de Código ABAP com Inteligência Artificial para Desenvolvedores SAP**

## 🚀 Visão Geral
O **ABAPify** é uma ferramenta CLI (Command Line Interface) que utiliza IA para gerar, validar e documentar código ABAP de forma automatizada. Criado para acelerar o dia a dia de desenvolvedores SAP, o ABAPify foca em programas ALV, módulos de função, classes orientadas a objetos, estruturas de dados e testes unitários.

---

## ⚙️ Funcionalidades

- ✏️ **Geração de Templates**
  - Programas ALV
  - Módulos de Função
  - Classes OO

- 📊 **Estruturas de Dados**
  - Tabelas
  - Estruturas (Types)
  - Inclusão de domínios, data elements (futuramente)

- ✍️ **Documentação Automática**
  - Comentários descritivos para métodos, parâmetros e tabelas

- 🔧 **Validação Sintática**
  - Verifica se o código gerado segue os padrões do ABAP

- 🎓 **Testes Unitários**
  - Gera estrutura base com ABAP Unit

- 🔮 **Prompt Customizado**
  - Gera código com base em instruções textuais, como:
    > "Criar BAPI de consulta de pedidos com parâmetros de data e status"

---

## 📂 Instalação
```bash
pip install abapify
```

Ou via GitHub:
```bash
git clone https://github.com/seuusuario/abapify.git
cd abapify
pip install -e .
```

---

## 📲 Uso Básico

```bash
abapify generate-alv --name ZREPORT_SALDOS --fields MATNR,WERKS
```

Outros comandos:
```bash
abapify generate-func-module --name ZFM_OBTER_CLIENTES
abapify generate-class --name ZCL_PEDIDO_SERVICE
abapify generate-structure --name ZSTR_CLIENTE --fields NAME,EMAIL,CPF
abapify generate-unit-test --for ZCL_PEDIDO_SERVICE
```

---

## 🤖 Roadmap Futuro

- [ ] Refatorador de código legado ABAP
- [ ] Suporte a CDS Views, AMDP e RAP
- [ ] Integração com Eclipse ADT ou SAP GUI
- [ ] Interface Web para edição e visualização
- [ ] Deploy direto via Git/Transport

---

## 🚀 Contribuindo
Pull requests são bem-vindos! Sugestões, correções e novas ideias também.

---

## 🌐 Licença
Este projeto está sob a licença MIT.

---

**ABAPify** - Automatize seu desenvolvimento no SAP com IA.