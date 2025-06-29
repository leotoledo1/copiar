import shutil
import datetime
import os

def copiar_arquivos():
    while True:
        try:
            caminho_atual = os.getcwd()
            data_hoje = datetime.datetime.now().strftime("%d-%m-%Y")
    
            nome_arquivo = input('Digite o nome do arquivo a ser copiado: ').strip()
            novo_nome = input('Digite o novo nome da copia: ').strip()

            nome_final = f"{novo_nome}_{data_hoje}.txt"
            
            nome_caminho = os.path.join(caminho_atual, nome_arquivo)
            nome_caminho_novo = os.path.join(caminho_atual, nome_final)
            shutil.copy2(nome_caminho, nome_caminho_novo)

            print(f" Arquivo copiado para: {nome_caminho_novo}")

            pasta_temp = os.path.join(caminho_atual, f"temp_{nome_final}")
            os.makedirs(pasta_temp)

            shutil.move(nome_caminho_novo, os.path.join(pasta_temp, nome_final))

            zip_nome = os.path.join(caminho_atual, f"{novo_nome}_{data_hoje}")
            shutil.make_archive(zip_nome, 'zip', root_dir=pasta_temp)

            shutil.rmtree( os.path.join(caminho_atual, f"temp_{nome_final}"))




    
        except FileNotFoundError as fnf_erro:
            print(f"Erro: {fnf_erro}")

        except Exception as erro:
            print(f"Erro inesperado: {erro}")

        repetir = input("\nDeseja copiar outro arquivo? (sim/nao): ").strip().lower()
        if repetir != 'sim':
            print("tchau")
            break

copiar_arquivos()