# Sistema de Auxílio à Tomada de Decisões para Investimento em Criptoativos

Este repositório contém uma aplicação que utiliza Inteligência Artificial para auxiliar investidores em criptoativos, oferecendo previsões do valor de fechamento do Bitcoin para os próximos 7 dias. A ferramenta tem como objetivo facilitar a tomada de decisão, ao analisar tendências históricas e projetar cenários futuros.

## Etapas do Projeto

O desenvolvimento do sistema envolveu as seguintes etapas principais:

### 1. Exploração e Tratamento de Dados
Antes de treinar o modelo de previsão, foi necessário explorar e tratar os dados históricos do Bitcoin. Esse processo é detalhado no arquivo **"exploracao_modelo.ipynb"**, onde foi realizada uma análise completa das características dos dados, como tendências, sazonalidade, e padrões relevantes.
Além disso, durante esse processo foi reaizado a Transformações de dados, baseado principalmente na normalização e criação de features derivadas para melhorar a capacidade preditiva do modelo.

### 2. Escolha do Modelo
Após a exploração dos dados, foram testados diversos modelos para a previsão de séries temporais. A partir dos experimentos, o modelo **LSTM (Long Short-Term Memory)** foi selecionado como o mais adequado, principalmente porque:

- **Redes Neurais Recorrentes (RNN)**, como o LSTM, são especialmente eficazes na modelagem de **séries temporais**, que envolvem dados sequenciais. Isso porque a RNN possui uma memória interna que consegue capturar dependências temporais de curto e longo prazo entre os dados históricos.
  
- **LSTM vs. GRU**: Entre os modelos LSTM e GRU (Gated Recurrent Unit), ambos são variantes das RNN. No entanto, o LSTM mostrou melhor desempenho para este conjunto de dados. O LSTM é particularmente eficaz porque:
  - **LSTM**: Possui uma estrutura interna que inclui portas de entrada, esquecimento e saída, permitindo que ele retenha informações importantes ao longo do tempo e aprenda padrões complexos.
  - **GRU**: É uma variante mais simples e rápida do LSTM, mas pode não capturar tão bem dependências de longo prazo.

### 3. Geração do Modelo de Previsão
Com base nos experimentos, o modelo **LSTM** foi salvo no arquivo **"modelo_btc.h5"**. Este arquivo contém a arquitetura do modelo e os pesos otimizados, prontos para realizar previsões futuras.

## Estrutura do Projeto

A aplicação está organizada da seguinte forma:

```
--app
  |-- templates
    |-- index.html      # Responsável pela interface frontend da aplicação
  |-- app.py            # Arquivo principal da aplicação (backend)
  |-- data_ingestion.py # Script para a ingestão de dados e preparação para as previsões
  |-- database.py       # Configuração inicial do banco de dados
  |-- db_connector.py   # Responsável pela conexão ao banco de dados PostgreSQL
  |-- plot.py           # Função para gerar o gráfico de previsões
  |-- prediction.py     # Realiza as previsões com base no modelo salvo
  |-- Dockerfile        # Arquivo de configuração para dockerizar a aplicação
  |-- requirements.txt  # Dependências necessárias para rodar a aplicação
--database
  |-- create_tables.sql  # Script SQL para criar as tabelas no banco de dados
--models
  |-- modelo_btc.h5     # Arquivo com o modelo LSTM treinado para previsões
--notebook
  |-- exploracao_modelo.ipynb # Notebook que detalha a exploração dos dados e o processo de escolha do modelo
```

### Descrição dos Arquivos

- **index.html**: Responsável pela interface gráfica da aplicação, exibindo ao usuário os gráficos e previsões do valor do Bitcoin.
- **app.py**: Arquivo principal que integra todas as funcionalidades da aplicação, gerencia as requisições do frontend e conecta com o modelo para realizar previsões.
- **data_ingestion.py**: Automatiza o processo de obtenção e preparação dos dados do Bitcoin, preparando-os para serem inseridos no banco de dados e utilizados pelo modelo de previsão.
- **database.py**: Inicializa a conexão com o banco de dados MySql, responsável por armazenar os dados históricos e as previsões geradas.
- **db_connector.py**: Implementa funções específicas para gerenciar a conexão com o banco de dados.
- **plot.py**: Gera gráficos que exibem tanto os dados históricos quanto as previsões futuras do preço do Bitcoin.
- **prediction.py**: Executa o processo de previsão utilizando o modelo LSTM salvo no arquivo **modelo_btc.h5**.
- **create_tables.sql**: Script SQL para criar as tabelas necessárias no banco de dados para armazenar os dados e previsões do Bitcoin.
- **Dockerfile**: Arquivo de configuração utilizado para criar a imagem Docker da aplicação, garantindo que ela rode em qualquer ambiente de forma consistente.
- **requirements.txt**: Lista todas as dependências Python necessárias para executar o projeto, como `Flask`, `Keras`, `yfinance`, entre outras.

## Como Executar o Projeto

### 1. Clonar o Repositório
Clone o repositório para sua máquina local:
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Instalar as Dependências
Instale todas as dependências listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Configurar o Banco de Dados
Crie as tabelas necessárias no banco de dados executando o script **create_tables.sql**:
```bash
psql -U seu_usuario -d seu_banco_de_dados -f database/create_tables.sql
```

### 4. Executar a Aplicação
Após configurar o ambiente e o banco de dados, vá até a pasta app e rode o código:
```bash
cd app
flask run
```
A aplicação estará disponível localmente no endereço `http://localhost:5000`.

### 5. Utilizar o Docker (Opcional)
Para facilitar a implantação da aplicação, utilize o **Docker** para rodar o projeto:
```bash
docker-compose up --build
```
ou 

```bash
bash run.sh
```

Aqui está uma versão mais detalhada e compreensível da documentação para a seção de funcionamento da aplicação:

---

## Funcionamento da Aplicação

A aplicação foi projetada para ser simples e intuitiva, oferecendo uma interface onde o usuário pode facilmente gerar previsões e visualizar gráficos históricos e futuros do preço do Bitcoin.

### Passo a Passo do Funcionamento:

1. **Acesso à Aplicação**: 
   Quando o usuário acessa a página principal, ele encontra um botão que permite gerar uma previsão para os próximos 7 dias do valor do Bitcoin.

2. **Geração da Previsão**:
   Ao clicar no botão, a aplicação:
   - Recupera os dados históricos mais de 2022 até a data atual utilizando o yfinance.
   - Passa esses dados pelo modelo **LSTM** previamente treinado (**modelo_btc.h5**) para calcular as previsões do valor de fechamento para os próximos 7 dias.

3. **Visualização do Gráfico**:
   Após a previsão ser gerada, a aplicação exibe um gráfico interativo que mostra:
   - **Dados históricos**: O preço de fechamento do Bitcoin dos últimos 30 dias.
   - **Previsões futuras**: Os valores previstos para os próximos 7 dias.
   O gráfico permite que o usuário visualize claramente a tendência dos preços e compare as previsões com o histórico recente.

4. **Armazenamento dos Dados**:
   Além de exibir as previsões e os dados históricos, a aplicação também realiza o **armazenamento automático**:
   - Os dados históricos utilizados para a previsão são salvos no banco de dados.
   - As previsões geradas também são armazenadas no banco, permitindo que o usuário possa acessá-las posteriormente ou realizar novas análises.

### Resumo Visual:
- **Entrada**: O usuário fornece o comando (clicando no botão) para gerar a previsão.
- **Processamento**: O sistema coleta os dados históricos, processa as previsões com o modelo LSTM e gera um gráfico.
- **Saída**: O usuário visualiza o gráfico contendo os últimos 30 dias de histórico e os próximos 7 dias previstos.
- **Persistência**: Todos os dados utilizados e gerados (históricos e previsões) são armazenados no banco de dados.

Para visualizar o funcionamento da aplicação em ação, [clique aqui](https://drive.google.com/file/d/1uQ5RcRoiP1QMv2Lf_q-6R8ArywHCUv3Q/view?usp=sharing).
