import shutil
import datetime
import os
from ftplib import FTP
from getpass import getpass

def copiar_arquivos():
    while True:
        try:
            caminho_atual = os.getcwd() #Aqui deixa o caminho onde esta o executavel
            data_hoje = datetime.datetime.now().strftime("%d-%m-%Y")  #variavel data hoje
    
            nome_arquivo = input('Digite o nome do arquivo a ser copiado: ').strip() #qual o nome do arquivo a ser copiado com strip para tirar os espaco
            novo_nome = input('Digite o novo nome da copia: ').strip() #qual novo nome da copia do arquivo strip para tirar espaco

            _,extensao = os.path.splitext(nome_arquivo) #ele pega a extencao do arquivo e ignora o nome dele.
            nome_final = f"{novo_nome}_{data_hoje}{extensao}" # variavel para o nome final da copia com a data

            nome_caminho = os.path.join(caminho_atual, nome_arquivo) #junta o caminho atual com o nome do arquivo para termos o caminho completo do arquivo a ser copiado
            nome_caminho_novo = os.path.join(caminho_atual, nome_final) # junta caminho atual com o nome final para onde quer colar
            shutil.copy2(nome_caminho, nome_caminho_novo)#funcao para copia 

            print(f" Arquivo copiado para: {nome_caminho_novo}") #print para mostrar onde foi copiado

            pasta_temp = os.path.join(caminho_atual, f"temp_{nome_final}") #caminho da poasta temporaria para zipar
            os.makedirs(pasta_temp) #criando pasta temporaria
            shutil.move(nome_caminho_novo, os.path.join(pasta_temp, nome_final)) #move o arquivo novo para pasta
            zip_nome = os.path.join(caminho_atual, f"{novo_nome}_{data_hoje}.zip") #caminho para zip com o .zip para retornar com .zip
            shutil.make_archive(zip_nome.replace(".zip", ""), 'zip', pasta_temp) #zipar a pasta temp
            shutil.rmtree(pasta_temp) #excluir pasta temp

        except FileNotFoundError as fnf_erro:
            print(f"Erro: {fnf_erro}")

        except Exception as erro:
            print(f"Erro inesperado: {erro}")

        repetir = input("\nDeseja copiar outro arquivo? (sim/nao): ").strip().lower()
        if repetir != 'sim':
            print("tchau")
            break
    
    return zip_nome



def enviar_arquivo(zip_nome):
    try:
        host = "mercohost.com.br" #caminho do ftp
        usuario = "merco"
        senha = getpass("Digite a senha: ")

        ftp = FTP(host) 
        ftp.login(usuario, senha) #logar no ftp
        print("Entrou no Servidor FTP")
        codigo_empresa = input("digite o codigo da empresa: ")

        ftp.cwd(f"/ENTRADAS/{codigo_empresa}") 

        with open(zip_nome, 'rb') as f:
            ftp.storbinary(f"STOR {os.path.basename(zip_nome)}", f) #envia o arquivo para o serivodr
        
        ftp.quit()
        print("Arquivo enviado")

    except Exception as e:
        print(f"erro ao enviar arquivo: {e}")


arquivo_compactado = copiar_arquivos()

pergunta = input("\nGostaria de enviar este arquivo para o FTP (sim/nao): ")
if pergunta == "sim":
    enviar_arquivo(arquivo_compactado)
else:
    print("Acabamos por aqui.")
