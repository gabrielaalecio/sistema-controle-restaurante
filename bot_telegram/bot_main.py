from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler,filters, CallbackContext,CallbackQueryHandler
import json
from secrets import token_hex
from enviar_email import *
import validar
from terminal.fun_pratos import *
from terminal.database import *

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


async def consultar_produtos(update: Update, context) -> None:
    with open(file_pratos,"r") as arquivo:
        pratos = json.load(arquivo)

    for prato in pratos:
        keyboard = [[
            InlineKeyboardButton("➕ Adicionar à Sacola", callback_data=f"add_{prato['nome']}"),
            InlineKeyboardButton("➖ Remover da Sacola", callback_data=f"rem_{prato['nome']}")
        ]]
        
        await update.message.reply_photo(
            photo=prato["img"],  
            caption=f"*🍽 Nome:* {prato['nome']}\n📖 *Descrição:* {prato['descricao']}\n💰 *Preço:* R${float(prato['preco']):.2f}\n⏳ *Tempo de preparo:* {prato['tempo']} min",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    await update.message.reply_text("🛒 Use /ver_carrinho para conferir ou utilize /limpar_carrinho para deixar o carrinho vazio.")
    
file = 'bot_telegram/clientes.json'
file_pratos = 'terminal/pratos.json'

async def ver_carrinho(update: Update, context) -> None:
    user_id = str(update.message.from_user.id)
    mensagem_responder = update.message

    # Verifica se o carrinho está vazio
    if user_id not in carrinho or not carrinho[user_id]:  
        await mensagem_responder.reply_text("🛒 Seu carrinho está vazio! Use /menu para adicionar itens.")
        return

    # Monta a lista de produtos no carrinho
    carrinho_text = "🛍 *Seu Carrinho:*\n"
    total = 0

    with open(file_pratos, "r") as arquivo:
        pratos = json.load(arquivo)

    precos = {prato["nome"]: float(prato["preco"]) for prato in pratos}

    for item, qtd in carrinho[user_id].items():
        preco = precos.get(item, 0) * qtd
        total += preco
        carrinho_text += f"• {item} x{qtd} - R${preco:.2f}\n"

    carrinho_text += f"\n💰 *Total: R${total:.2f}*"

    keyboard = [[
        InlineKeyboardButton("✅ Confirmar Pedido", callback_data="confirmar_pedido"),
        InlineKeyboardButton("❌ Cancelar Pedido", callback_data="cancelar_pedido")
    ]]

    await mensagem_responder.reply_text(carrinho_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def limpar_carrinho(update: Update, context) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in carrinho:
        del carrinho[user_id]
        await update.message.reply_text("🛒 Carrinho limpo!")
        return None
    await update.message.reply_text("🛒 Você não possui carrinho!")


async def callback_handler(update: Update, context: CallbackContext) -> None:
    """Gerencia todas as interações de botões no Telegram."""
    query = update.callback_query
    data = query.data
    user_id = str(query.from_user.id)

    await query.answer()  # Confirma o recebimento para evitar carregamento infinito

    # 📌 Confirmação de cadastro
    if data == f"confirmar_{user_id}":
        new_text = "✅ Cadastro confirmado! Seu cadastro foi salvo."
        del cadastro_estado[user_id]["estado"]
        arquivo_post(cadastro_estado[user_id])  # Salva o cadastro
        del cadastro_estado[user_id]

    elif data == f"cancelar_{user_id}":
        new_text = "❌ Cadastro cancelado. Seus dados foram descartados."
        del cadastro_estado[user_id]

    # 📌 Adicionar item ao carrinho
    elif data.startswith("add_"):
        item = data.split("_", 1)[1]  # Pega o nome do prato corretamente
        if user_id not in carrinho:
            carrinho[user_id] = {}
        if item in carrinho[user_id]:
            carrinho[user_id][item] += 1
        else:
            carrinho[user_id][item] = 1
        print(f"Pedidos: {carrinho[user_id]}")
        await query.answer(f"{item} adicionado à sacola! ✅")
        await query.message.reply_text(f"🛍 {item} foi adicionado ao carrinho!\nUse /ver_carrinho para conferir ou utilize /limpar_carrinho para deixar o carrinho vazio.")

    elif data.startswith("rem_"):
        item = data.split("_", 1)[1]  # Pega o nome do prato corretamente
        if user_id in carrinho and item in carrinho[user_id]:
            if carrinho[user_id][item] > 1:
                carrinho[user_id][item] -= 1
            else:
                del carrinho[user_id][item]
            print(f"Pedidos após remoção: {carrinho[user_id]}")
            await query.answer(f"{item} removido da sacola! ✅")
            await query.message.reply_text(f"🛍 {item} foi removido do carrinho!\nUse /ver_carrinho para conferir ou utilize /limpar_carrinho para deixar o carrinho vazio.")
        else:
            await query.answer(f"{item} não está no carrinho!")
            await query.message.reply_text(f"🛍 {item} não foi encontrado no carrinho!")


    # 📌 Finalizar Pedido
    elif data == "confirmar_pedido":
        if cliente_existe(user_id):
            if user_id in carrinho and carrinho[user_id]:
                await query.message.reply_text("✅ Pedido Confirmado! Acompanhe o status pelo chat.")
                lista_pratos = carregar_dados('terminal/pratos.json')
                lista_produtos = []
                preco = ''
                try:
                    with open("pedidos.json", "r") as arquivo:
                        pedidos = json.load(arquivo)
                except:
                    pedidos = []
                for produto, qtd in carrinho[user_id].items():
                    preco = buscar_prato_preco(produto, lista_pratos)
                    lista_produtos.append({'nome_produto': produto, 'quantidade': qtd, 'preco': preco})
                pedido = {'produtos': lista_produtos, 'id': f'{user_id}', 'status': 'Confirmado'}
                pedidos.append(pedido)
                with open("pedidos.json", "w") as arquivo:
                    json.dump(pedidos, arquivo)
                #!gravar no relatório
                del carrinho[user_id]
            else:
                await query.message.reply_text("Seu carrinho está vazio! 🛒")
        else:
            await query.message.reply_text("❌ Você não possui cadastro como cliente! utilize /cadastro para se cadastrar e poder comprar nossos produtos.")

    elif data == "cancelar_pedido":
        if user_id in carrinho and carrinho[user_id]:
            await query.message.reply_text("❌ Pedido cancelado!")
            del carrinho[user_id]
        else:
            await query.message.reply_text("Seu carrinho está vazio! 🛒")


    # Edita a mensagem original para remover os botões (caso seja um cadastro)
    if "confirmar" in data or "cancelar" in data:
        await query.message.edit_text(new_text)


async def comandos(update: Update, context) -> None:
    await update.message.reply_text(f"""
Estes são os comandos (digite ou clique):

/menu : Mostra o cardápio para, mas apenas clientes cadastrados podem comprar.
/ver_carrinho : Mostra o carrinho.
/limpar_carrinho : Limpa todos os produtos no carrinho.
/cadastro : Para clientes que desejam ter vínculo e comprar nossos produtos.
/cancelar_cadastro : Para clientes que iniciaram o cadastro mas desejam cancelar.
/cancelar_cliente : Para clientes cadastrados que desejam cancelar o vínculo.
/avaliar : Avalia nosso atendimento e produtos por meio de uma mensagem.
/comandos : Mostra todos os comandos possíveis.
/ajuda : Explica como o bot funciona de maneira simples.
""")
    

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
carrinho = {}

# Configuração e execução do bot
def main():
    token = "7679897120:AAHO9LD6pfchrKJ8RhVVVHmgpT7dlVLbbLA"
    application = Application.builder().token(token).build()

    #  Registrando comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(CommandHandler("menu", consultar_produtos))
    application.add_handler(CommandHandler("comandos", comandos))
    application.add_handler(CommandHandler("cadastro", cadastro))
    application.add_handler(CommandHandler("cancelar_cadastro", cancelar_cadastro))
    application.add_handler(CommandHandler("cancelar_cliente", cancelar_cliente))
    application.add_handler(CommandHandler("ver_carrinho", ver_carrinho))
    application.add_handler(CommandHandler("limpar_carrinho", limpar_carrinho))

    #  Handlers de mensagens
    application.add_handler(MessageHandler(filters.TEXT, echo))

    #  Handler para botões
    application.add_handler(CallbackQueryHandler(callback_handler))

    print("Bot está rodando...")
    application.run_polling()
main()