# 🔌 Fluxo de Potência com Newton-Raphson

Este projeto implementa um solucionador de **fluxo de potência em sistemas elétricos** utilizando o método iterativo de **Newton-Raphson**. Ele foi desenvolvido em Python com foco em modularidade, extensibilidade e compatibilidade com arquivos `.pwf` no formato ANAREDE.

## 📦 Estrutura do Projeto

```text
power_flow/
├── power_flow/            # Pacote principal (código-fonte)
│   ├── models/            # Modelos de dados (Bus, Load, Generator, etc.)
│   ├── solver/            # Implementações do método de Newton-Raphson
│   ├── components/        # Linhas, Transformadores e elementos do sistema
│   ├── ybus.py            # Construção da matriz de admitância nodal
│   ├── config.py          # Parâmetros e caminhos globais
├── data/                  # Arquivos de entrada .pwf
├── output/                # Arquivos de saída (.xlsx, .csv)
├── main.py                # Script principal
├── README.md
├── pyproject.toml         # Gerenciamento de dependências (Poetry)
└── LICENSE
```

## ⚙️ Funcionalidades

- Leitura de arquivos `.pwf` no formato ANAREDE
- Implementação do método Newton-Raphson com barra SWING tratada via Big Number
- Exportação da matriz Ybus separando parte real e imaginária
- Projeto modular com suporte a extensão futura (controle de reativo, geração, etc.)

## 📄 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).

## 👤 Autor

Desenvolvido por **Giovani Santiago Junqueira** no contexto do curso de Pós-graduação em Análise de Redes Elétricas.

## ⚡️ Analisador de Fluxo de Potência com Newton-Raphson

Este projeto implementa um solucionador de **fluxo de potência** para sistemas elétricos usando o método iterativo de **Newton-Raphson**, com suporte a entrada nos formatos `.pwf` (ANAREDE) e `.json`. O código foi desenvolvido em Python com foco em modularidade, clareza e facilidade de extensão.

---

## 📁 Estrutura do Projeto

```text
power_flow/
├── power_flow/
│   ├── models/             # Estruturas de dados (Bus, Load, Line, Transformer, etc.)
│   ├── readers/            # Leitores para arquivos .pwf e .json
│   ├── solver/             # Algoritmo de Newton-Raphson e verificação de convergência
│   ├── ybus.py             # Construção da matriz de admitância nodal Ybus
│   ├── config.py           # Parâmetros e caminhos globais
│   └── labels.py           # Traduções e mensagens multilíngues
├── data/                   # Casos de teste (.pwf, .json)
├── output/                 # Resultados gerados (.xlsx, .csv)
├── main.py                 # Script principal de execução
├── pyproject.toml          # Gerenciamento de dependências (Poetry)
└── README.md
```

---

## 🚀 Instalação

Este projeto utiliza o [Poetry](https://python-poetry.org/) para gerenciamento de dependências. Para instalar:

```bash
git clone https://github.com/seuusuario/power-flow.git
cd power-flow
poetry install
poetry shell
```

---

## ▶️ Como Executar

O programa pode ser executado com qualquer um dos formatos de entrada disponíveis:

```bash
python main.py IEEE14 --formato pwf
# ou
python main.py IEEE14 --formato json
```

Caso o argumento `--formato` não seja informado, o programa tentará detectar automaticamente com base nos arquivos em `data/`.

---

## 🔧 Funcionalidades

- ✅ Leitura de arquivos `.pwf` (ANAREDE) e `.json` (estruturado)
- ✅ Geração automática da matriz de admitância nodal (Ybus)
- ✅ Método de Newton-Raphson modular, com cálculo das submatrizes H, M, N, L
- ✅ Tratamento da barra swing via técnica do Big Number
- ✅ Suporte a transformadores com tap e defasagem, shunts e múltiplos geradores
- ✅ Exportação da matriz Ybus e resultados em Excel (.xlsx)
- ✅ Mensagens multilíngues (Português/Inglês)
- ✅ Estrutura extensível e compatível com novos componentes

---

## 📈 Saídas Geradas

Após a execução, os seguintes arquivos são salvos na pasta `output/`:

- `IEEE14_Ybus_exportada.xlsx` — Matriz Ybus separada em partes real e imaginária
- `IEEE14_resultado_fluxo.xlsx` — Tensão e ângulo por barra após convergência
- `IEEE14_sumario.xlsx` — Sumário detalhado com potências especificadas, geradas, cargas, etc.

---

## 📚 Requisitos

- Python 3.10+ (ou 3.12, testado)
- Poetry para gerenciamento de ambiente
- Bibliotecas: `numpy`, `pandas`, `openpyxl`, `scipy`

---

## 👨‍💻 Autor

Desenvolvido por **Giovani Santiago Junqueira** no contexto do curso de Pós-graduação em Análise de Redes Elétricas.

---

## 📝 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
