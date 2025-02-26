from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler,filters, CallbackContext,CallbackQueryHandler
import json
from secrets import token_hex
from enviar_email import *
import validar

def arquivo_get():
    try:
        with open(file,"r") as arquivo:
            clientes = json.load(arquivo)
        return clientes
    except (FileNotFoundError, json.JSONDecodeError):
        print("Erro na abertura de arquivo")
        return None

def  arquivo_post(usuario):
    try:
        clientes = arquivo_get()
        clientes.append(usuario)
        with open(file, "w") as arquivo:
            json.dump(clientes, arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        print("Erro na abertura de arquivo")
        return None

def  arquivo_delete(usuario):
    try:
        flag = False
        clientes = arquivo_get()
        for i, cliente in enumerate(clientes):
            if cliente["id"] == usuario:
                clientes.pop(i)
                flag = True
                break
        if flag:
            with open(file, "w") as arquivo:
                json.dump(clientes, arquivo)
        return flag

    except (FileNotFoundError, json.JSONDecodeError):
        print("Erro na abertura de arquivo")
        return None

def cliente_existe(id):
    clientes = arquivo_get()
    return any(cliente.get("id") == id for cliente in clientes)

async def start(update: Update, context) -> None:
    await update.message.reply_text(f"Olá {update.message.chat.first_name}.\nSeja bem vindo ao BUG DO SABOR, sou um chat-bot e estou aqui para te ajudar com o seu pedido!\nCaso tenha dúvidas, digite ou clique em /ajuda")
    
async def ajuda(update: Update, context) -> None:
    await update.message.reply_text(f"""
Sou um chat-bot que auxilia os clientes com seus pedidos, basta interagir comigo que eu lhe auxilio.
Posso cadastrar clientes, mostrar nossos produtos, realizar pedidos, entre outras coisas. Digite ou clique em /comandos para ver minhas possíveis interações.                                 
""")

async def echo(update: Update, context) -> None:
    user_id = str(update.message.from_user.id)
    user_name =update.message.chat.first_name.upper()
    mensagem = update.message.text
    

    if user_id in cadastro_estado:
        estado = cadastro_estado[user_id]["estado"]

        if estado == "email":
            #Validar email
            cadastro_estado[user_id]["email"] = mensagem
            cadastro_estado[user_id]["estado"] = "email_cod"
            await update.message.reply_text("Enviamos um código para o seu email, digite aqui para confirmar seu email: ")

            codigo = token_hex(4)
            cadastro_estado[user_id]["codigo"] = codigo

            titulo = "Confirmação de Email"
            corpo = f"""
            <html>
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
            if mensagem == cadastro_estado[user_id]["codigo"]:
                del cadastro_estado[user_id]["codigo"]
                cadastro_estado[user_id]["estado"] = "nome"
                await update.message.reply_text("Código confirmado!\nAgora digite sua nome: ")
            else:
                await update.message.reply_text("O código informado está incorreto!\nDigite/clique em /cadastro para recomeçar.")
                del cadastro_estado[user_id] #cancela cadastro

            return None

        elif estado == "nome":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! Não deixe em branco! Digite novamente o nome ou  digite/clique em /cancelar_cadastro.")
                return None                

            cadastro_estado[user_id]["nome"] = mensagem.upper()
            cadastro_estado[user_id]["estado"] = "idade"
            await update.message.reply_text("Agora digite sua idade: ")
            return None

        elif estado == "idade":
            if not validar.idade(mensagem):
                await update.message.reply_text("A idade digitada está ínválida! digite novamente a idade ou digite/clique /cancelar_cadastro.")
                return None
            cadastro_estado[user_id]["idade"] = mensagem
            cadastro_estado[user_id]["estado"] = "cpf"
            await update.message.reply_text("Digite o seu cpf: ")
            return None

        elif estado == "cpf":
            if not validar.cpf(mensagem):
                await update.message.reply_text("O CPF digitado está ínválido! digite novamente o CPF ou digite/clique /cancelar_cadastro.")
                return None

            cadastro_estado[user_id]["cpf"] = mensagem
            cadastro_estado[user_id]["estado"] = "endereco_cep"
            await update.message.reply_text("Vamos precisar do seu endereço, digite seu CEP(apenas números): ")
            return None

        elif estado == "endereco_cep":
            if not validar.cep(mensagem):
                await update.message.reply_text("Informação necessária! Não deixe em branco e digite apenas números! Digite novamente ou  digite/clique em /cancelar_cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"]=({"cep":mensagem})
            cadastro_estado[user_id]["estado"] = "endereco_bairro"
            await update.message.reply_text("Agora digite seu bairro: ")
            return None

        elif estado == "endereco_bairro":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! Não deixe em branco! Digite novamente ou  digite/clique em /cancelar_cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"].update({"bairro":mensagem.upper()})
            cadastro_estado[user_id]["estado"] = "endereco_rua"
            await update.message.reply_text("Agora digite o nome de sua rua: ")
            return None

        elif estado == "endereco_rua":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! Não deixe em branco! Digite novamente ou  digite/clique em /cancelar_cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"].update({"rua":mensagem.upper()})
            cadastro_estado[user_id]["estado"] = "endereco_num"
            await update.message.reply_text("Agora digite o numero da sua casa: ")
            return None

        elif estado == "endereco_num":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! Não deixe em branco! Digite novamente ou  digite/clique em /cancelar_cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"].update({"numero":mensagem})
            cadastro_estado[user_id]["estado"] = "endereco_complemento"
            await update.message.reply_text("Digite o complemento. Exemplo(res oliveira, apt 107, bloco b): ")
            return None

        elif estado == "endereco_complemento":
            if validar.string_vazia(mensagem):
                await update.message.reply_text("Informação necessária! Não deixe em branco! Digite novamente ou  digite/clique em /cancelar_cadastro.")
                return None 
            cadastro_estado[user_id]["endereco"].update({"complemento":mensagem.upper()})
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
            Idade: {cadastro_estado[user_id]["idade"]}
            CPF: {cadastro_estado[user_id]["cpf"]}
            Bairro: {cadastro_estado[user_id]["endereco"]["bairro"]}
            Rua: {cadastro_estado[user_id]["endereco"]["rua"]}
            Numero: {cadastro_estado[user_id]["endereco"]["numero"]}
            Complemento: {cadastro_estado[user_id]["endereco"]["complemento"]}""")

            await update.message.reply_text("Clique em uma opção abaixo:", reply_markup=reply_markup)
            return None
    await update.message.reply_text(f"Olá, não entendi o que você disse. Use /ajuda ou /comandos para eu poder lhe auxiliar",reply_to_message_id=update.message.message_id)

async def comandos(update: Update, context) -> None:
    await update.message.reply_text(f"""
Estes são os comandos (digite ou clique):

/realizar_pedido: 
/consultar_produtos : 
/cadastro : Para clientes que desejam ter vínculo e comprar nossos produtos
/cancelar_cadastro : Para clientes que iniciaram o cadastro mas desejam cancelar.
/cancelar_cliente : Para clientes cadastrados que desejam cancelar o vínculo.
/avaliar : Avalia nosso atendimento e produtos por meio de uma mensagem.
/comandos : Mostra todos os comandos possíveis.
/ajuda : Explica como o bot funciona de maneira simples.
""")

async def button_callback(update: Update, context: CallbackContext) -> None:

    query = update.callback_query  
    user_id = str(query.from_user.id)
    await query.answer()  # Confirma o recebimento para evitar carregamento infinito

    if query.data == f"confirmar_{user_id}":
        new_text = "✅ Cadastro confirmado! Seu cadastro foi salvo."
        del cadastro_estado[user_id]["estado"]
        arquivo_post(cadastro_estado[user_id]) #salvo o cadastro caso o usuario queira
        del cadastro_estado[user_id]

    elif query.data == f"cancelar_{user_id}":
        new_text = "❌ Cadastro cancelado. Seus dados foram descartados."
        del cadastro_estado[user_id]

    #Edita a mensagem original para remover os botões e mostrar a escolha
    await query.message.edit_text(new_text)

async def cancelar_cliente(update: Update, context) -> None:
    user_id = str(update.message.from_user.id)
    if arquivo_delete(user_id):
        await update.message.reply_text("Cadastro como cliente cancelado!\n Você já não é mais um cliente cadastrado, sinta-se a vontade para voltar quando quiser! O BUG DO SABOR sempre estará de portas abertas!")


async def cancelar_cadastro(update: Update, context) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in cadastro_estado:
        del cadastro_estado[user_id]
        await update.message.reply_text("Processo de cadastro cancelado! caso queira ser cliente digite/clique em /cadastro.")

async def cadastro(update: Update, context) -> None:
    user_id = str(update.message.from_user.id)
    if cliente_existe(user_id):
        await update.message.reply_text("Você ja é um de nossos clientes cadastrados.\nCaso queira cancelar o seu cadastro como cliente, digite ou clique em /cancelar_cliente.")
        return None
    
    cadastro_estado[user_id] = {"estado": "email"}
    cadastro_estado[user_id]["id"] = user_id
    await update.message.reply_text("Digite seu e-mail:")


    
file = 'clientes.json'
try:
    with open(file, "r") as arquivo:
        conteudo = arquivo.read().strip()

    if not conteudo:  # Se estiver vazio, cria um novo JSON válido
        print(f"O arquivo {file} está vazio. Criando um novo...")
        clientes = [{"id":0}]
        with open(file, "w") as arquivo:
            json.dump(clientes, arquivo)
    else:
        print("Arquivo carregado com sucesso:")

except FileNotFoundError:
    print(f"O arquivo {file} não existe. Criando um novo...")
    clientes = [{"id":0}]
    with open(file, "w") as arquivo:
        json.dump(clientes, arquivo)

except json.JSONDecodeError:
    print(f"O arquivo {file} está corrompido! Criando um novo...")
    clientes = [{"id":0}]
    with open(file, "w") as arquivo:
        json.dump(clientes, arquivo)

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
    application.add_handler(CommandHandler("cancelar_cadastro", cancelar_cadastro))
    application.add_handler(CommandHandler("cancelar_cliente", cancelar_cliente))
    application.add_handler(MessageHandler(filters.TEXT, echo)) 
    application.add_handler(CallbackQueryHandler(button_callback))

 # Inicia o bot
    print("Bot está rodando...")
    application.run_polling()
main()