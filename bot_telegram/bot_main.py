from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler,filters, CallbackContext
import json

async def start(update: Update, context) -> None:
    await update.message.reply_text(f"Olá {update.message.chat.first_name}.\nSeja bem vindo ao BUG DO SABOR, sou um chat-bot e estou aqui para te ajudar com o seu pedido!\nQualquer dúvida, digite ou clique /ajuda")
    
async def ajuda(update: Update, context) -> None:
    await update.message.reply_text(f"""
Sou um chat-bot que auxilia os clientes com seus pedidos, basta interagir comigo que eu ajudo no possível.
Posso cadastrar clientes, mostrar nossos produtos, realizar pedidos entre outras coisas. Digite ou clique em /comandos para ver minhas possíveis interações.                                 
""")

async def echo(update: Update, context) -> None:
    user_id = update.message.from_user.id

    if user_id in cadastro_estado:
        estado = cadastro_estado[user_id]["estado"]



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