
# 📘 Projeto: Resolução e Visualização de Fluxo Máximo

Este projeto implementa um sistema completo para **ler instâncias de fluxo máximo**, **resolver o problema usando o OR-Tools**, **exibir resultados didáticos no terminal** e **gerar visualizações gráficas** destacando as arestas utilizadas no fluxo.

Ele foi desenvolvido com fins didáticos, para auxiliar no entendimento de algoritmos de fluxo e na interpretação de soluções.

---

## ✨ Funcionalidades

* 📄 **Leitura de instâncias** no formato:

  ```
  n m s t
  u v cap
  ...
  ```
* ⚙️ **Resolução automática** usando o `SimpleMaxFlow` (Google OR-Tools).
* 📊 **Exibição organizada do fluxo máximo**, incluindo:

  * Arestas utilizadas
  * Arestas saturadas
  * Interpretação e observações
* 🎨 **Visualização do grafo** usando NetworkX e Matplotlib:

  * Nós mais espaçados e legíveis
  * Arestas com fluxo destacadas em vermelho
  * Labels de capacidades
* 🧹 Código documentado seguindo **PEP 257**.

---


## 🔧 Instalação

### 1. Instalar dependências:

```bash
pip install ortools networkx matplotlib
```

### 2. Verificar o arquivo de entrada

O arquivo `fluxo_maximo.txt` deve conter o formato:

```
n m s t
u v cap
u v cap
...
```

Exemplo:

```
6 8 0 5
0 1 16
0 2 13
1 2 10
1 3 12
2 1 4
2 4 14
3 2 9
4 5 4
```

---

## ▶️ Como Executar

```bash
python main.py fluxo_maximo.txt
```

### Opções de Linha de Comando

- `--help` mensagem de ajuda
- `--plot` exibe uma imagem do grafo final
- `--sort` ordena o grafo gerado


## 🧠 Funções Principais

### 🔹 `parse_instance(path)`

Lê o arquivo, ignora comentários e valida o número de arestas.

### 🔹 `solve_max_flow(n, s, t, edge_list)`

Resolve o fluxo máximo usando OR-Tools.

### 🔹 `print_didactic_output(...)`

Mostra uma saída limpa e explicativa no terminal.

### 🔹 `plot_grafo(flows)`

Gera um grafo visual destacando arestas com fluxo > 0.

## 👨‍💻 Desenvolvedores
- **Iago Cordeiro Canguçu** — Desenvolvedor principal
  GitHub: [@iaguian0](https://github.com/iaguian0)

- **Luiz Gustavo Soares**  
  GitHub: [@LuizGustavo-lg](https://github.com/LuizGustavo-lg)
