from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler,filters, CallbackContext
import json
from secrets import token_hex
from enviar_email import *

async def start(update: Update, context) -> None:
    await update.message.reply_text(f"Olá {update.message.chat.first_name}.\nSeja bem vindo ao BUG DO SABOR, sou um chat-bot e estou aqui para te ajudar com o seu pedido!\nQualquer dúvida, digite ou clique /ajuda")
    
async def ajuda(update: Update, context) -> None:
    await update.message.reply_text(f"""
Sou um chat-bot que auxilia os clientes com seus pedidos, basta interagir comigo que eu ajudo no possível.
Posso cadastrar clientes, mostrar nossos produtos, realizar pedidos entre outras coisas. Digite ou clique em /comandos para ver minhas possíveis interações.                                 
""")

async def echo(update: Update, context) -> None:
    user_id = update.message.from_user.id
    mensagem = update.message.text

    if user_id in cadastro_estado:
        estado = cadastro_estado[user_id]["estado"]

        if estado == "email":
            cadastro_estado[user_id]["email"] = mensagem
            cadastro_estado[user_id]["estado"] = "email_cod"
            await update.message.reply_text("Enviamos um código para o seu email, digite aqui para confirmar seu email: ")

            codigo = token_hex(4)

            titulo = "Confirmação de Email"
            corpo = f"""
            <thml>
            <body>
            <p>Olá!
            Este é o seu código de confirmação.</p>
            <h2><b>[{codigo}]</b></h2>

            <p>Atenciosamente,
            Equipe Bug do Sabor.</p>
            </body>
            </html>
            """

            enviar_email(mensagem, titulo, corpo)

        elif estado == "email_cod":
            
            await update.message.reply_text("Agora digite sua nome: ")

        elif estado == "nome":
            cadastro_estado[user_id]["nome"] = mensagem
            cadastro_estado[user_id]["estado"] = "idade"
            await update.message.reply_text("Agora digite sua idade: ")

        elif estado == "idade":
            cadastro_estado[user_id]["idade"] = mensagem
            cadastro_estado[user_id]["estado"] = "cpf"
            await update.message.reply_text("Digite o seu cpf: ")

        elif estado == "cpf":
            cadastro_estado[user_id]["cpf"] = mensagem
            cadastro_estado[user_id]["estado"] = "endereco_cep"
            await update.message.reply_text("Vamos precisar do seu endeço, digite seu cep: ")

        elif estado == "endereco_cep":
            cadastro_estado[user_id]["endereco"] = {"cep":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_bairro"
            await update.message.reply_text("Agora digite seu bairro: ")

        elif estado == "endereco_bairro":
            cadastro_estado[user_id]["endereco"] = {"bairro":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_rua"
            await update.message.reply_text("Agora digite o nome de sua rua: ")

        elif estado == "endereco_rua":
            cadastro_estado[user_id]["endereco"] = {"rua":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_num"
            await update.message.reply_text("Agora digite o numero da sua rua: ")

        elif estado == "endereco_num":
            cadastro_estado[user_id]["endereco"] = {"numero":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_complemento"
            await update.message.reply_text("Agora digite complemento. Exemplo (res oliveira, apt 107, bloco b): ")

        elif estado == "endereco_complemento":
            cadastro_estado[user_id]["endereco"] = {"complemento":mensagem}

            #####SALVAR

            # Remove do estado do cadastro (finalizou)
            del cadastro_estado[user_id]
            await update.message.reply_text("Cadastro concluído com sucesso! ✅")


    await update.message.reply_text(f"Olá, não entendi oque você disse. Use /ajuda ou /comandos para eu poder melhor te auxiliar",reply_to_message_id=update.message.message_id)

async def comandos(update: Update, context) -> None:
    await update.message.reply_text(f"""
Estes são os comandos (digite ou clique):

/realizar_pedido
/consultar_produtos
/cadastro
/avaliar
/comandos
/ajuda
""")

async def cadastro(update: Update, context) -> None:
    user_id = update.message.from_user.id
    try:
        with open(file, "r") as arquivo:
            clientes = json.load(arquivo)
        if user_id in clientes['id']:
            await update.message.reply_text(f"Você ja é um usuário cadastrado!")
            return None
    except FileNotFoundError:
        #enviar um email para o proprietário falando sobre tal problema
        await update.message.reply_text(f"Desculpe-me {update.message.chat.first_name}. Houve um erro inesperado, tente novamente! caso o problema prossiga envie um email para nossa equipe.")
        return None
    
    if user_id in cadastro_estado:
        await update.message.reply_text("Você está no processo de cadastro. Conclua ou cancele com /cancelar_cadastro para continuar.")
        return
    
    cadastro_estado[user_id] = {"estado": "email"}
    await update.message.reply_text("Digite seu e-mail:")
    


    
file = 'clientes.json'
cadastro_estado = {} #guarda a informação sobre qual etapa de cadastro o  usuário se encontra

# Configuração e execução do bot
def main():
 # Insira o token do seu bot aqui
    token = "7679897120:AAHO9LD6pfchrKJ8RhVVVHmgpT7dlVLbbLA"
 # Cria a aplicação
    application = Application.builder().token(token).build()
 # Registra os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(CommandHandler("comandos", comandos))
    application.add_handler(CommandHandler("cadastro", cadastro))
    application.add_handler(MessageHandler(filters.TEXT, echo)) 

 # Inicia o bot
    print("Bot está rodando...")
    application.run_polling()
main()