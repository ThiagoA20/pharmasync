import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("1280x720")
root.configure(fg_color='#0C0055')

side_menu = ctk.CTkFrame(root, width=75, height=720, fg_color='gray')
side_menu.pack(side=ctk.LEFT, padx=10, pady=20)

menus = {
    "main": ctk.CTkFrame(root, width=1205, height=720, fg_color='gray'),
    "drug": ctk.CTkFrame(root, width=1205, height=720, fg_color='gray'),
    "supplier": ctk.CTkFrame(root, width=1205, height=720, fg_color='gray')
}

# Adicionando textos aos menus
# ------------------------------------------------------------------------

ctk.CTkLabel(menus["main"], text="Main Menu").place(x=10, y=10)

# ------------------------------------------------------------------------

def get_current_stock(acquisition_list, consumption_list):
    current_stock = []
    estoque_atual = 0
    for i in range(len(acquisition_list)):
        estoque_atual = estoque_atual + acquisition_list[i] - consumption_list[i]
        current_stock.append(estoque_atual)
    return current_stock

drug_search = ctk.CTkFrame(menus["drug"], width=350, height=650, fg_color='white')
drug_search.place(x=15, y=15)

search_bar = ctk.CTkEntry(master=drug_search, width=300, height=50, placeholder_text='Search')
search_bar.pack(pady=20, padx=25)

searchresults = ctk.CTkScrollableFrame(drug_search, width=350, height=540, fg_color='white')
searchresults.pack()

aquisicoes = 'aquisicoes.xlsx'
consumo = 'consumo.xlsx'

df_aquisicoes = pd.read_excel(aquisicoes)
df_consumo = pd.read_excel(consumo)

# filtro = df_aquisicoes["Name"].str.contains('ACIDO', case=False, na=False)
# df_aquisicoes = df_aquisicoes[filtro]
aquisition_list = list(df_aquisicoes.iloc[0,1:])
consumption_list = list(df_consumo.iloc[1,1:])
current_stock = get_current_stock(aquisition_list, consumption_list)
meses = ['2023-Mar', '2023-Apr', '2023-May', '2023-Jun', '2023-Jul', '2023-Ago', '2023-Set', '2023-Out', '2023-Nov', '2023-Dec', '2024-Jan', '2024-Fev', '2024-Mar', '2024-Apr', '2024-May', '2024-Jun', '2024-Jul', '2024-Ago']

fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('#0C0055')
ax.tick_params(colors='#FFFFFF')
ax.spines['top'].set_color('#FFFFFF')
ax.spines['bottom'].set_color('#FFFFFF')
ax.spines['left'].set_color('#FFFFFF')
ax.spines['right'].set_color('#FFFFFF')

plot_line, = ax.plot(meses, aquisition_list, marker='o', color='r', linestyle='-', label='Acquisition')
plot_line2, = ax.plot(meses, consumption_list, marker='o', color='b', linestyle='-', label='Consumption')
plot_line3, = ax.plot(meses, current_stock, marker='o', color='#52FF00', linestyle='-', label='Stock')

def change_plot(selected_drug):
    global aquisition_list, consumption_list, current_stock, plot_line, plot_line2, plot_line3
    plt.title(selected_drug, color='#FFFFFF')
    aquisition_list = list(df_aquisicoes.loc[df_aquisicoes["Name"] == selected_drug].iloc[0, 1:])
    consumption_list = list(df_consumo.loc[df_consumo["Name"] == selected_drug].iloc[0, 1:])
    current_stock = get_current_stock(aquisition_list, consumption_list)

    plot_line.set_ydata(aquisition_list)
    plot_line2.set_ydata(consumption_list)
    plot_line3.set_ydata(current_stock)

    data = aquisition_list + consumption_list + current_stock

    min_dado = min(data)
    max_dado = max(data)

    # Define o limite superior
    limite_superior = max_dado * 1.1 if max_dado != 0 else 1
    
    # Define o limite inferior com base no contexto
    if min_dado > 0:
        limite_inferior = min_dado * 0.9  # Adiciona margem para positivos
    elif min_dado == 0:
        limite_inferior = -(limite_superior//10)
    else:
        limite_inferior = min_dado * 1.1  # Adiciona margem para negativos
    
    ax.set_ylim(limite_inferior, limite_superior)

    # ax.set_ylim(min(data) * 0.5, max(data) * 1.5)

    canvas.draw()

def truncate_text(text, max_length=20):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def create_buttons():
    # Acessar a coluna diretamente em vez de usar iloc dentro do loop
    # aquisicoes_texto = df_aquisicoes.sort_values(by="Name", ascending=True).iloc[:, 0].values  # Coleta os dados de uma vez, evita o uso de iloc no loop

    aquisicoes_texto = df_aquisicoes.iloc[:, 0].values

    for x, texto in enumerate(aquisicoes_texto):
        button_text = truncate_text(texto, 20)  # Truncando o texto se necessário
        button = ctk.CTkButton(
            searchresults,
            text=button_text,
            command=lambda idx=x: change_plot(aquisicoes_texto[idx])  # Passando o índice de forma eficiente
        )
        button.pack(pady=10, padx=10, fill="x", expand=True)

create_buttons()

plt.title(f'{df_aquisicoes.iloc[0,0]}', color='#FFFFFF')
plt.xlabel('Months', color='#FFFFFF')
plt.ylabel('Stock', color='#FFFFFF')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), labelcolor='#000000')
plt.xticks(rotation=90)
plt.grid(color='#FFFBFB', alpha=0.2)
plt.tight_layout()
# plt.ylim(0, 8000)

canvas = FigureCanvasTkAgg(fig, master=menus["drug"])
canvas.draw()
canvas.get_tk_widget().place(x=450, y=15)

def update_legend():
    handles, labels = ax.get_legend_handles_labels()  # Obtém as entradas de legenda
    visible_handles_labels = [(handle, label) for handle, label in zip(handles, labels) if handle.get_visible()]  # Filtra entradas visíveis

    # Atualiza a legenda com apenas as linhas visíveis
    ax.legend(*zip(*visible_handles_labels), loc='upper left', bbox_to_anchor=(1, 1), labelcolor='#000000')
    plt.draw()  # Redesenha o gráfico para refletir as mudanças na legenda

def update_plot(plot):
    plot.set_visible(not plot.get_visible())
    update_legend()
    canvas.draw()

test_button = ctk.CTkButton(master=menus["drug"], text="Acquisition", command=lambda plot=plot_line: update_plot(plot))
test_button.place(x=450, y=600)

test_button2 = ctk.CTkButton(master=menus["drug"], text="Consumption", command=lambda plot=plot_line2: update_plot(plot))
test_button2.place(x=650, y=600)

test_button3 = ctk.CTkButton(master=menus["drug"], text="Stock", command=lambda plot=plot_line3: update_plot(plot))
test_button3.place(x=850, y=600)

# ------------------------------------------------------------------------

ctk.CTkLabel(menus["supplier"], text="Supplier Menu").place(x=10, y=10)

# ------------------------------------------------------------------------

# Lista para armazenar informações sobre botões
buttons = []

# Função para atualizar o layout
def update_layout(active_menu):
    # Gerenciar exibição dos menus
    for menu_name, frame in menus.items():
        if menu_name == active_menu:
            frame.pack(pady=20, padx=10)
        else:
            frame.pack_forget()

    # Atualizar as cores dos botões
    for btn_data in buttons:
        if btn_data["menu"] == active_menu:
            btn_data["button"].configure(fg_color="blue")  # Cor para botão ativo
        else:
            btn_data["button"].configure(fg_color="gray")  # Cor para botões inativos

# Dados para os botões e menus correspondentes
button_data = [
    {"text": "Main", "menu": "main"},
    {"text": "Drug", "menu": "drug"},
    {"text": "Supplier", "menu": "supplier"}
]

# Criando os botões dinamicamente
for i, btn_data in enumerate(button_data):
    button = ctk.CTkButton(
        side_menu,
        text=btn_data["text"],
        command=lambda menu=btn_data["menu"]: update_layout(menu),
        width=65,
        height=65
    )
    button.place(x=5, y=10 + i * 75)
    btn_data["button"] = button
    buttons.append(btn_data)  # Adicionar botão à lista

# Inicializar com o menu principal ativo
update_layout("drug")


"""
def login():
    print("Test")
    button.pack_forget()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login System")
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Download", command=login)
button.pack(pady=12, padx=10)

def sliding(value):
    my_label.configure(text=int(value))

my_slider = customtkinter.CTkSlider(
    master=frame,
    from_=0, 
    to=100,
    number_of_steps=10, 
    command=sliding,
    # fg_color="blue",
    # progress_color="white",
    # button_color="gray",
    # button_hover_color="orange",
    # width=400,
    # height=50
)

my_slider.pack(pady=40)
my_slider.set(0)

my_label = customtkinter.CTkLabel(frame, text=int(my_slider.get()))
my_label.pack(pady=20)
"""

root.title('PharmaSync')
root.mainloop()