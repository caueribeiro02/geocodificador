import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def obter_coordenadas_google(endereco, api_key):
    """
    Obtém coordenadas usando Google Maps API
    """
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {'address': endereco, 'key': api_key}
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"   ❌ Google API: {data.get('status', 'Unknown error')}")
            return None, None
            
    except Exception as e:
        print(f"   ❌ Erro Google API: {e}")
        return None, None

def obter_coordenadas_nominatim(endereco):
    """
    Obtém coordenadas usando Nominatim (OpenStreetMap) - gratuito
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': endereco,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'br'  # Foca no Brasil
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            return None, None
            
    except Exception as e:
        print(f"   ❌ Erro Nominatim: {e}")
        return None, None

def obter_coordenadas(endereco, api_key=None, tentar_nominatim=True):
    """
    Tenta Google Maps primeiro, depois Nominatim se falhar
    """
    # Primeira tentativa: Google Maps (se a chave existir)
    if api_key:
        lat, lng = obter_coordenadas_google(endereco, api_key)
        if lat and lng:
            return lat, lng
        else:
            print("   🔄 Google Maps falhou, tentando serviço alternativo...")
    
    # Segunda tentativa: Nominatim (se permitido)
    if tentar_nominatim:
        lat, lng = obter_coordenadas_nominatim(endereco)
        if lat and lng:
            return lat, lng
    
    return None, None

def processar_planilha(arquivo_excel, coluna_endereco='ENDEREÇO', api_key=None):
    """
    Processa a planilha e adiciona coordenadas
    """
    try:
        # Ler arquivo Excel
        df = pd.read_excel(arquivo_excel)
        
        # Verificar se a coluna existe
        if coluna_endereco not in df.columns:
            print(f"❌ Coluna '{coluna_endereco}' não encontrada!")
            print(f"📋 Colunas disponíveis: {list(df.columns)}")
            return None
        
        # Adicionar colunas de coordenadas
        df['LATITUDE'] = None
        df['LONGITUDE'] = None
        
        total = len(df)
        print(f"📍 Processando {total} endereços...")
        print(f"🔑 Google Maps API: {'SIM' if api_key else 'NÃO'}")
        print(f"🔄 Serviço alternativo: SIM")
        
        # Processar cada endereço
        for index, row in df.iterrows():
            endereco = str(row[coluna_endereco]).strip()
            
            if endereco and endereco != 'nan':
                print(f"\n[{index+1}/{total}] 📍 {endereco}")
                
                # Tentar obter coordenadas
                lat, lng = obter_coordenadas(endereco, api_key, tentar_nominatim=True)
                
                df.at[index, 'LATITUDE'] = lat
                df.at[index, 'LONGITUDE'] = lng
                
                if lat and lng:
                    print(f"   ✅ Lat: {lat:.6f}, Lng: {lng:.6f}")
                else:
                    print(f"   ❌ Endereço não encontrado")
            else:
                print(f"   ⚠️  Endereço vazio na linha {index+2}")
            
            # Pausa para respeitar limites da API
            time.sleep(1)  # 1 segundo entre requisições
        
        # Salvar resultado
        nome_saida = arquivo_excel.replace('.xlsx', '_com_coordenadas.xlsx')
        df.to_excel(nome_saida, index=False)
        
        # Estatísticas
        sucessos = df['LATITUDE'].notna().sum()
        print(f"\n🎯 Resultado: {sucessos}/{total} endereços geocodificados!")
        print(f"💾 Arquivo salvo: {nome_saida}")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        return None

def main():
    """
    Função principal que carrega configurações do ambiente
    """
    # 🔧 CONFIGURAÇÕES (podem ser alteradas no .env)
    arquivo_excel = os.getenv('ARQUIVO_EXCEL', 'enderecos.xlsx')
    coluna_endereco = os.getenv('COLUNA_ENDERECO', 'ENDEREÇO')
    
    # 🔑 CHAVE API (carregada do .env)
    google_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # Verificar se arquivo existe
    if not os.path.exists(arquivo_excel):
        print(f"❌ Arquivo '{arquivo_excel}' não encontrado!")
        print("📁 Arquivos disponíveis no diretório:")
        for file in os.listdir('.'):
            if file.endswith('.xlsx'):
                print(f"   - {file}")
        return
    
    # Executar
    print("🚀 INICIANDO GEOCODIFICAÇÃO")
    print("=" * 50)
    print(f"📊 Arquivo: {arquivo_excel}")
    print(f"📍 Coluna: {coluna_endereco}")
    print(f"🔑 Google Maps: {'Configurado' if google_api_key else 'Não configurado'}")
    print("=" * 50)
    
    resultado = processar_planilha(arquivo_excel, coluna_endereco, google_api_key)
    
    if resultado is not None:
        print("\n📊 VISUALIZAÇÃO DOS PRIMEIROS RESULTADOS:")
        print("=" * 80)
        colunas_mostrar = [coluna_endereco, 'LATITUDE', 'LONGITUDE']
        colunas_disponiveis = [col for col in colunas_mostrar if col in resultado.columns]
        print(resultado[colunas_disponiveis].head(10))
        
        # Estatísticas finais
        total = len(resultado)
        sucessos = resultado['LATITUDE'].notna().sum()
        falhas = total - sucessos
        
        print(f"\n📈 ESTATÍSTICAS FINAIS:")
        print(f"✅ Sucessos: {sucessos}/{total} ({sucessos/total*100:.1f}%)")
        print(f"❌ Falhas: {falhas}/{total} ({falhas/total*100:.1f}%)")
        
        if falhas > 0:
            print(f"\n💡 Dica: Endereços com falhas podem ser formatados como:")
            print("   'Rua, Número, Cidade, Estado, País'")
    else:
        print("❌ Falha no processamento do arquivo.")

if __name__ == "__main__":
    main()