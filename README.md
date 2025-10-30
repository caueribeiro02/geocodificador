# 🗺️ Geocodificação Automática de Endereços (Google Maps + Nominatim)

Este projeto realiza **geocodificação automática** (obtenção de latitude e longitude) a partir de uma planilha Excel com endereços.  
Ele utiliza a **API do Google Maps** (opcional, se disponível) e o serviço **Nominatim (OpenStreetMap)** como alternativa gratuita e aberta.

---

## 🚀 Funcionalidades

✅ Lê automaticamente uma planilha `.xlsx` contendo endereços  
✅ Busca coordenadas geográficas (latitude e longitude)  
✅ Prioriza a API do **Google Maps** e usa o **Nominatim** se houver falha  
✅ Exibe progresso, estatísticas e salva um novo arquivo com os resultados  
✅ Compatível com variáveis de ambiente (`.env`) para fácil configuração  

---

## 🧠 Estrutura do Código

O script é composto pelas seguintes funções principais:

| Função | Descrição |
|--------|------------|
| `obter_coordenadas_google()` | Consulta a API do Google Maps para obter coordenadas |
| `obter_coordenadas_nominatim()` | Usa o serviço gratuito Nominatim (OpenStreetMap) |
| `obter_coordenadas()` | Gerencia a tentativa entre os dois serviços |
| `processar_planilha()` | Lê, processa e salva a planilha com coordenadas |
| `main()` | Função principal que carrega configurações e inicia o processamento |

---

## ⚙️ Instalação

### 1. Clone este repositório
```bash
git clone https://github.com/seu-usuario/geocodificacao-enderecos.git
cd geocodificacao-enderecos


```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
venv\Scripts\activate   # No Windows
source venv/bin/activate  # No Linux/Mac

```
### 3. Instale as dependências
```bash
pip install -r requirements.txt

```

### 4. Crie um arquivo .env na raiz do projeto

Exemplo:
```bash
GOOGLE_MAPS_API_KEY=SuaChaveDaAPIaqui
ARQUIVO_EXCEL=enderecos.xlsx
COLUNA_ENDERECO=ENDEREÇO

```

💡 A chave do Google Maps é opcional — se não for informada, o código usará o Nominatim (OpenStreetMap).

---

## 📄 Exemplo de Planilha

ENDEREÇO

Rua das Flores, 123, São Paulo, SP

Avenida Paulista, 1000, São Paulo, SP

Praça da Sé, São Paulo, SP

---

## ▶️ Como Executar

Após configurar o .env e colocar a planilha no mesmo diretório:
```bash
python main.py

```

Ou, se o arquivo tiver outro nome:
```bash
python main.py --arquivo nome_da_planilha.xlsx

```

O script exibirá mensagens de progresso como:
```yaml

🚀 INICIANDO GEOCODIFICAÇÃO
📊 Arquivo: enderecos.xlsx
📍 Coluna: ENDEREÇO
🔑 Google Maps: Configurado
📍 Processando 25 endereços...

```

E salvará um novo arquivo chamado:
```bash
enderecos_com_coordenadas.xlsx

```
---

## 📊 Resultado Gerado

O arquivo de saída conterá novas colunas:
```bash
             ENDEREÇO	          LATITUDE  	LONGITUDE
Rua das Flores, 123, São Paulo	  -23.561684	-46.655981
Avenida Paulista, 1000, São Paulo	-23.561924	-46.656278

```

---

## 📈 Estatísticas Exibidas no Final

Ao final da execução, o script mostra um resumo:
```yaml
📈 ESTATÍSTICAS FINAIS:
✅ Sucessos: 23/25 (92.0%)
❌ Falhas: 2/25 (8.0%)

💡 Dica: Endereços com falhas podem ser formatados como:
   'Rua, Número, Cidade, Estado, País'

```
---

## 🧩 Requisitos

- Python 3.8 ou superior

- Bibliotecas:

pandas;

requests;

python-dotenv;

openpyxl;

---

## 📦 Arquivo requirements.txt sugerido
```txt
pandas
requests
python-dotenv
openpyxl

```
---

## 🌍 Limites e Boas Práticas

🔹 Google Maps API: possui limite diário gratuito e requer chave de API válida.

🔹 Nominatim (OpenStreetMap): gratuito, mas limitado a ~1 requisição por segundo (o script já respeita esse tempo).

🔹 Sempre use um User-Agent válido ao consultar o Nominatim — já implementado no código.

🔹 Evite rodar grandes volumes de endereços sem pausas, para não ser bloqueado pelos serviços.


---

## 🧑‍💻 Autor

Caue Ribeiro

📍 Projeto desenvolvido para automação de geocodificação de endereços com suporte a múltiplas APIs.

📧 Contato: https://www.linkedin.com/in/caue-ribeiro-499126260/

---

## 🪪 Licença
```yaml
Este projeto é distribuído sob a licença MIT — sinta-se livre para usar, modificar e compartilhar.

MIT License © 2025 Caue Ribeiro
