from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler,filters, CallbackContext,CallbackQueryHandler
import json
from secrets import token_hex
from enviar_email import *
import validar


async def start(update: Update, context) -> None:
    await update.message.reply_text(f"Olá {update.message.chat.first_name}.\nSeja bem vindo ao BUG DO SABOR, sou um chat-bot e estou aqui para te ajudar com o seu pedido!\nQualquer dúvida, digite ou clique /ajuda")
    
async def ajuda(update: Update, context) -> None:
    await update.message.reply_text(f"""
Sou um chat-bot que auxilia os clientes com seus pedidos, basta interagir comigo que eu ajudo no possível.
Posso cadastrar clientes, mostrar nossos produtos, realizar pedidos entre outras coisas. Digite ou clique em /comandos para ver minhas possíveis interações.                                 
""")

async def echo(update: Update, context) -> None:
    user_id = update.message.from_user.id
    user_name =update.message.chat.first_name.upper()
    mensagem = update.message.text.upper()
    

    if user_id in cadastro_estado:
        estado = cadastro_estado[user_id]["estado"]

        if estado == "email":
            #Validar email
            cadastro_estado[user_id]["email"] = mensagem
            cadastro_estado[user_id]["estado"] = "email_cod"
            await update.message.reply_text("Enviamos um código para o seu email, digite aqui para confirmar seu email: ")

            codigo = token_hex(4)
            print(codigo)
            cadastro_estado[user_id]["codigo"] = codigo

            titulo = "Confirmação de Email"
            corpo = f"""
            <thml>
            <body>
            <p>Olá {user_name}!
            Este é o seu código de confirmação.</p>
            <h2><b>[{codigo}]</b></h2>

            <p>Atenciosamente,
            Equipe Bug do Sabor.</p>
            </body>
            </html>
            """

            enviar_email(mensagem, titulo, corpo)
            return None

        elif estado == "email_cod":
            print(cadastro_estado[user_id["codigo"]])
            print(mensagem)
            if mensagem == cadastro_estado[user_id]["codigo"]:
                cadastro_estado[user_id]["estado"] = "nome"
                await update.message.reply_text("Código confirmado!\nAgora digite sua nome: ")
            else:
                await update.message.reply_text("O código informado está incorreto!\nDigite ou clique em /cadastro para recomeçar.")
                del cadastro_estado[user_id] #cancela cadastro

            return None

        elif estado == "nome":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! não pode deixar em branco! digite novamente ou utilize /cancelar para cancelar o cadastro.")
                return None                

            cadastro_estado[user_id]["nome"] = mensagem
            cadastro_estado[user_id]["estado"] = "idade"
            await update.message.reply_text("Agora digite sua idade: ")
            return None

        elif estado == "idade":
            #validar idade
            cadastro_estado[user_id]["idade"] = mensagem
            cadastro_estado[user_id]["estado"] = "cpf"
            await update.message.reply_text("Digite o seu cpf: ")
            return None

        elif estado == "cpf":
            #validar cpf
            cadastro_estado[user_id]["cpf"] = mensagem
            cadastro_estado[user_id]["estado"] = "endereco_cep"
            await update.message.reply_text("Vamos precisar do seu endeço, digite seu cep: ")
            return None

        elif estado == "endereco_cep":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! não pode deixar em branco! digite novamente ou utilize /cancelar para cancelar o cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"] = {"cep":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_bairro"
            await update.message.reply_text("Agora digite seu bairro: ")
            return None

        elif estado == "endereco_bairro":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! não pode deixar em branco! digite novamente ou utilize /cancelar para cancelar o cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"] = {"bairro":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_rua"
            await update.message.reply_text("Agora digite o nome de sua rua: ")
            return None

        elif estado == "endereco_rua":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! não pode deixar em branco! digite novamente ou utilize /cancelar para cancelar o cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"] = {"rua":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_num"
            await update.message.reply_text("Agora digite o numero da sua rua: ")
            return None

        elif estado == "endereco_num":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! não pode deixar em branco! digite novamente ou utilize /cancelar para cancelar o cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"] = {"numero":mensagem}
            cadastro_estado[user_id]["estado"] = "endereco_complemento"
            await update.message.reply_text("Agora digite complemento. Exemplo (res oliveira, apt 107, bloco b): ")
            return None

        elif estado == "endereco_complemento":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! não pode deixar em branco! digite novamente ou utilize /cancelar para cancelar o cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"] = {"complemento":mensagem}
            cadastro_estado[user_id]["estado"] = "confirmar"

            keyboard = [
                [
                    InlineKeyboardButton("✅ CONFIRMAR", callback_data=f"confirmar_{user_id}"),
                    InlineKeyboardButton("❌ CANCELAR", callback_data=f"cancelar_{user_id}")
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(f"""
            Estamos finalizando seu cadastro, para finalizar, confirme o seu cadastro:
            Email: {cadastro_estado[user_id]["email"]}
            Nome: {cadastro_estado[user_id]["nome"]}
            Idade: {cadastro_estado[user_id]["Idade"]}
            CPF: {cadastro_estado[user_id]["cpf"]}
            Bairro: {cadastro_estado[user_id]["bairro"]}
            Rua: {cadastro_estado[user_id]["Rua"]}
            Numero: {cadastro_estado[user_id]["numero"]}
            Complemento: {cadastro_estado[user_id]["complemento"]}

            Clique em uma opção abaixo:""",reply_markup)

            #####SALVAR

            # Remove do estado do cadastro (finalizou)

            del cadastro_estado[user_id]
            await update.message.reply_text("Cadastro concluído com sucesso! ✅")
            return None


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

async def button_callback(update: Update, context: CallbackContext) -> None:

    query = update.callback_query  
    await query.answer()  # Confirma o recebimento para evitar carregamento infinito

    new_text = ""
    if query.data == "cadastro_yes":
        new_text = "Você escolheu: Sim ✅ para o cadastro"
    elif query.data == "cadastro_no":
        new_text = "Você escolheu: Não ❌ para o cadastro"

    # ⚡️ Edita a mensagem original para remover os botões e mostrar a escolha
    await query.message.edit_text(new_text)

async def cadastro(update: Update, context) -> None:
    user_id = update.message.from_user.id
    try:
        with open(file, "r") as arquivo:
            conteudo = arquivo.read().strip()  # Remove espaços e quebras de linha extras
            if not conteudo:  # Se o arquivo estiver vazio, inicializa um JSON válido
                clientes = {"id": []}
            else:
                clientes = json.loads(conteudo)  # Carrega o JSON

        if user_id in clientes.get('id', []):
            await update.message.reply_text("Você já é um usuário cadastrado!")
            return None

    except (FileNotFoundError, json.JSONDecodeError):
        await update.message.reply_text(
            f"Desculpe-me {update.message.chat.first_name}. Houve um erro inesperado. "
            "Tente novamente! Caso o problema persista, envie um e-mail para nossa equipe."
        )
        return None
    
    if  user_id in cadastro_estado:
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
    application.add_handler(CallbackQueryHandler(button_callback))

 # Inicia o bot
    print("Bot está rodando...")
    application.run_polling()
main()