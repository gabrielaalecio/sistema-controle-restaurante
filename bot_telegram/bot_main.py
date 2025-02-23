from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler,filters

# Função para responder ao comando /start
async def start(update: Update, context) -> None:
    await update.message.reply_text("Olá! Eu sou um bot simples. Envie-me uma mensagem e eu a repetirei.")

# Função para repetir mensagens de texto
async def echo(update: Update, context) -> None:
    user_message = update.message.text
    await update.message.reply_text(f"Você disse: {user_message}")

# Configuração e execução do bot
def main():
 # Insira o token do seu bot aqui
    token = "7679897120:AAHO9LD6pfchrKJ8RhVVVHmgpT7dlVLbbLA"
 # Cria a aplicação
    application = Application.builder().token(token).build()
 # Registra os handlers
    application.add_handler(CommandHandler("start", start)) # Responde ao /start
    application.add_handler(MessageHandler(filters.TEXT, echo)) # Repete mensagens de texto
 # Inicia o bot
    print("Bot está rodando...")
    application.run_polling()
main()