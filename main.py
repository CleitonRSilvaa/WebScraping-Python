import subprocess
import time
import os
import re
# instalando as dependencias essenciais para funcionamento do script
print("instalando dependencias aguarde...")
subprocess.run("pip install pytest-playwright", shell=True)
subprocess.run("playwright install", shell=True)
subprocess.run("pip install pyodb", shell=True)
subprocess.run("pip install requests", shell=True)
subprocess.run("cls", shell=True)
time.sleep(30)
#inportando as dependencias instaladas
from playwright.sync_api import sync_playwright
from datetime import datetime
import db_query
import bot_telegran
print("Processo de Dowload iniciado")

def messagem_inicial():
    hora_inicial = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = 'Processo de download dos boletos iniciado em : \n' + hora_inicial
    bot_telegran.send_message(msg=msg)

def messagem_final():
    hora_final = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = 'Processo de download dos boletos finalizado em : \n' + hora_final + '\n' \
        'NÚMERO TOTAL DE BOLETOS : ' + str(len(lista_cpf)) + '\n' \
        'NÚMERO DE BOLETOS BAIXADOS : ' + cont_boletos_baixados() + '\n' \
        'NÚMERO DE SOCIO SEM BOLETO :' + cont_sem_boletos() + '\n'                                                                                                                                    'NÚMERO DE BOLETO PARA BAIXAR NOVAMENTE :' + cont_boletos_para_baixar() + '\n'
    bot_telegran.send_message(msg=msg)


def cont_boletos_baixados():
    cont = 0
    lista_cpf_com_boleto = open("cpfs.txt", "r")
    for iten in lista_cpf_com_boleto:
        cont = cont + 1
    lista_cpf_com_boleto.close()
    return cont

def cont_sem_boletos():
    cont = 0
    lista_cpf_sem_boleto = open("sem_boleto.txt", "r")
    for iten in lista_cpf_sem_boleto:
        cont = cont + 1
    lista_cpf_sem_boleto.close()
    return cont

def cont_boletos_para_baixar():
    cont = 0
    lista_boletos_para_baixar = open("baixar_novamente.txt", "r")
    for iten in lista_boletos_para_baixar:
        cont = cont + 1
    lista_boletos_para_baixar.close()
    return cont

# função que tira todos os caracteres não numéricos retornar o mesmo
def re_cpf(cpf_obj):
    cpf = re.sub('[^0-9]', '', cpf_obj)
    return cpf


def download_boletos(cpf):
    try:
        cpf = re_cpf(cpf_obj=cpf)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_context(accept_downloads=True).new_page()
            page.goto("link_site")
            page.fill('input[name="txtCPF"]', cpf)
            time.sleep(2)
            # Ação click btn Verificar Boleto
            page.locator('button >> text=Verificar Boleto').click()
            time.sleep(2)
            with page.expect_popup() as popup_info:
                # Ação click btn segunda via boleto
                page.locator('input[type="submit"]').click()
                time.sleep(3)
                popup = popup_info.value
                popup.wait_for_load_state()
            popup.wait_for_load_state()
            valida_acao_boleto = popup.locator('xpath=//*[@id="Table8"]/tbody/tr[3]/td[4]/font/b/a').element_handles()
            if valida_acao_boleto:
                with popup.expect_popup() as new_aba:
                    popup.locator('xpath=//*[@id="Table8"]/tbody/tr[3]/td[4]/font/b/a').click()
                    time.sleep(2)
                    new_aba = new_aba.value
                    new_aba.wait_for_load_state()
                new_aba.wait_for_load_state()
                with new_aba.expect_download() as download_info:
                    new_aba.locator('xpath=//*[@id="Table4"]/tbody/tr[2]/td/a/img').click()
                    time.sleep(4)
                    download = download_info.value
                    path = download.path()
                    file_name = cpf + '.pdf'
                download.save_as(os.path.join(boleto_destino, file_name))
                # cria um arquivo txt caso não exita e grava o cpf com beleto baixado com sucesso
                arquivo = open("cpfs.txt", 'a')
                arquivo.write(cpf + '\n')
                arquivo.close()
                return True
            else:
                # cria um arquivo txt e grava o cpf sem boleto
                arquivo = open("sem_boleto.txt", 'a')
                arquivo.write(cpf + '\n')
                browser.close()
                return False
    except Exception as e:
        # cria um arquivo txt e grava o cpf dos boletos que deram erro de download
        arquivo = open("baixar_novamente.txt", 'a')
        arquivo.write(cpf + '\n')
        time.sleep(1)
        arquivo.close()
        # cria um arquivo txt e grava as exceções geradas
        arquivo_log = open("arquivo_log.txt", 'a')
        arquivo_log.write(e + '\n')
        arquivo_log.close()
        browser.close()

def main(lista_cpf_obj):
    messagem_inicial()
    arquivo = open("cpfs.txt", 'a')
    arquivo.write(datetime.now().strftime("%Y-%m-%d %H:%M") + '\n')
    arquivo = open("sem_boleto.txt", 'a')
    arquivo.write(datetime.now().strftime("%Y-%m-%d %H:%M") + '\n')
    for cpf in lista_cpf_obj:
        download_boletos(cpf)
    messagem_final()
# cria nova lista com cpfs de boletos com erro de donload
def lista_cpf_2via(arquivo_lista):
    array_cpf = []
    cont = 0
    for cont in arquivo_lista:
        array_cpf.append(cont)
    arquivo_lista.close()
    return array_cpf

def cpf_obj (lista_cpf):
    for row in lista_cpf:
        return row


def etapa_2():
    msg = 'Processo de download 2ª etapa iniciado em : \n' + datetime.now().strftime("%Y-%m-%d %H:%M")
    bot_telegran.send_message(msg=msg)
    # cria um arquivo txt caso não exista
    lista_cpf_nao_baixados = open("baixar_novamente.txt", 'a')
    lista_cpf_nao_baixados.close()
    # abrindo arquivo com cpfs com erro de download do boleto
    lista_cpf_nao_baixados = open("baixar_novamente.txt", 'r')
    # criando a lista com cpfs com erro de download do boleto
    new_lista_cpf = lista_cpf_2via(lista_cpf_nao_baixados)
    lista_cpf_nao_baixados.close()
    while len(new_lista_cpf) > 0:
        cpf = cpf_obj(new_lista_cpf)
        if download_boletos(cpf):
            new_lista_cpf.remove(cpf)
    msg = 'Processo de download 2ª etapa finalizado em : \n' + datetime.now().strftime("%Y-%m-%d %H:%M")
    bot_telegran.send_message(msg=msg)



""""
Primeira etapa iniciara o processo padrão do download dos boletos percorrendo uma lista vinda do bando de dados 
"""

# diretorio onde sera salvo os arquivos baixados.
boleto_destino = r'./boletos'
#Criar diretorio boleto_destino caso não exita
if not os.path.exists(boleto_destino):
        os.mkdir(boleto_destino)
# lista cpfs direto do banco de dados
lista_cpf = db_query.list_cpf()

print("instalando dependencias aguarde...")
print(subprocess.run("pip install pytest-playwright & playwright install & pip install pyodbc", shell=True))
time.sleep(60)

main(lista_cpf_obj=lista_cpf)

""""
Segunda etapa iniciara o processo de downloads dos boletos que tiveram erro na primeira etapa  
"""

etapa_2()

