# importando a biblioteca Tkinter para criação de interface gráfica
import tkinter as tk 
import random as rd
from tkinter import ttk

#tocar animação da mão
def play_hand_animation():
    #retomando as globais definidas em event_manager
    global index_frame
    global stop_animation_at
    #lista de animações da CPU e do player
    cpu_hand_animations = ["cpu_hand_images/static_and_rock_cpu_hand.png", "cpu_hand_images/new_frame_cpu_hand.png"]
    player_hand_animations = ["player_hand_images/static_and_rock_player_hand.png", "player_hand_images/new_frame_player_hand.png"]
    #condição de parada da animação: 6 pela velocidade da animação. O dobro do número padrão de repetições na vida real
    if stop_animation_at < 6:
        #criando a próxima imagem da animação da mão da cpu e do player (Frame)
        next_frame_cpu_hand_animation_image = tk.PhotoImage(file=cpu_hand_animations[index_frame])
        next_frame_player_hand_animation_image = tk.PhotoImage(file=player_hand_animations[index_frame])
        #configurando a nova imagem da mão da CPU e do player e referenciando a nova imagem para o label padrão em render_game()
        cpu_hand_image_lbl.config(image=next_frame_cpu_hand_animation_image)
        cpu_hand_image_lbl.image = next_frame_cpu_hand_animation_image
    
        player_hand_image_lbl.config(image=next_frame_player_hand_animation_image)
        player_hand_image_lbl.image = next_frame_player_hand_animation_image
        #calculando o índice do próximo frame
        index_frame = (index_frame + 1) % len(cpu_hand_animations)
        game.after(200, play_hand_animation) #Sincronizando as animações das mãos com agendamento de funções
        
        play_selected_option_btn.config(state="disabled")
        playable_options_cbx.config(state="disabled")
        stop_animation_at += 1
    else:
        play_selected_option_btn.config(state="active")
        playable_options_cbx.config(state="active")
        playable_options_cbx.config(state="readonly")
        stop_animation_at = 0
    
#obtem as jogadas
def get_play_choice():
    #definindo a imagem final da mão como global para uso em outra função(mesma coisa para variaveis de obtenção de índice)
    global cpu_hand_final_move_image
    global player_hand_final_move_image
    global cpu_choice_index_on_arr
    global player_choice_index_on_arr
    #listas de opções jogáveis para o jogador e a cpu. OBS: Jogador a imagem é espelhada em relação a CPU
    cpu_playable_image_options = ["cpu_hand_images/static_and_rock_cpu_hand.png", "cpu_hand_images/paper_cpu_hand.png", "cpu_hand_images/scissor_cpu_hand.png"]
    player_playable_image_options = ["player_hand_images/static_and_rock_player_hand.png", "player_hand_images/paper_player_hand.png", "player_hand_images/scissor_player_hand.png"]
    #obtendo indice da jogada dos jogadores na lista de imagens
    cpu_choice_index_on_arr = rd.randint(0, 2)
    player_choice_index_on_arr = playable_options_cbx.current()
    #recebendo jogadas em forma de imagem para o player e a cpu
    cpu_hand_final_move_image = cpu_playable_image_options[cpu_choice_index_on_arr]
    player_hand_final_move_image = player_playable_image_options[player_choice_index_on_arr]

#carrega as imagens das jogadas 
def load_play_choice_from_image():
    
    #atualizando a imagem da jogada escolhida da CPU
    final_move_cpu_hand_image = tk.PhotoImage(file=cpu_hand_final_move_image)
    cpu_hand_image_lbl.config(image=final_move_cpu_hand_image)
    cpu_hand_image_lbl.image = final_move_cpu_hand_image
    
    #atualizando a imagem da jogada escolhida do player
    final_move_player_hand_image = tk.PhotoImage(file=player_hand_final_move_image)
    player_hand_image_lbl.config(image=final_move_player_hand_image)
    player_hand_image_lbl.image = final_move_player_hand_image   

#verifica quem venceu
def check_winner():
    #retomando as globais de atribuição mutável
    global player_score
    global cpu_score
    
    #realizando checagem de vitória por índice -> 0 - pedra, 1 - papel e 2 - tesoura. Nos respectivos Arrays | Verificação de vitória do player
    if (player_choice_index_on_arr == 0 and cpu_choice_index_on_arr == 2) or (player_choice_index_on_arr == 1 and cpu_choice_index_on_arr == 0) or (player_choice_index_on_arr == 2 and cpu_choice_index_on_arr == 1):
        player_score += 1
        player_score_lbl.config(text=f"PLACAR JOGADOR: {player_score}")
    #mesma coisa pra CPU
    elif (cpu_choice_index_on_arr == 0 and player_choice_index_on_arr == 2) or (cpu_choice_index_on_arr == 1 and player_choice_index_on_arr == 0) or (cpu_choice_index_on_arr == 2 and player_choice_index_on_arr == 1):
        cpu_score += 1
        cpu_score_lbl.config(text=f"PLACAR CPU: {cpu_score}")   
    
#função para gerenciar eventos de cliques, frames e etc
def event_manager():
    #Rodando a animação da mão repetidamente
    play_hand_animation()
    #obtendo jogada
    get_play_choice()
    #Aguardando 1280 MS para chamar a função set_play_choice_from_image() na qual irá carregar as imagens das escolhas dos jogadores
    game.after(1280, load_play_choice_from_image)
    #Aguardando a função de carregamento da imagem da mão escolhida para chamar a função de checagem de vitória
    game.after(1290, check_winner)
    

#função para renderizar o jogo
def render_game():
    #definição de variáveis globais de eventos/lógica
    global player_score
    global cpu_score
    global index_frame
    global stop_animation_at
    #iniciando variáveis de eventos globais
    stop_animation_at = 0
    index_frame = 0
    player_score = 0
    cpu_score = 0
    #definindo variáveis globais de renderização(label, botões, comboboxes)
    global playable_options_cbx
    global player_score_lbl
    global cpu_score_lbl
    global cpu_hand_image_lbl
    global player_hand_image_lbl
    global play_selected_option_btn
    global game
    #criando configurações iniciais da janela
    game = tk.Tk()
    game.geometry("300x300")
    game.title("RPS GAME")
    game.resizable(False, False)
    
    #definindo subtitulo
    sub_title_lbl = tk.Label(game, text="Rock, Paper & Scissor", font="Arial 12")
    sub_title_lbl.place(x=70, y=0)
    #definindo o texto "jogador"
    player_lbl = tk.Label(game, text="JOGADOR", font="Arial 12")
    player_lbl.place(x=0, y=35)
    
    #definindo o texto "computador"
    cpu_lbl = tk.Label(game, text="COMPUTADOR", font="Arial 12")
    cpu_lbl.place(x=180, y=35)
    
    #definindo botão de "JOGAR"
    play_selected_option_btn = tk.Button(game, text="JOGAR", command=event_manager)
    play_selected_option_btn.place(x=118, y=200)
    #definindo o texto dinâmico de pontuação(score) do jogador
    player_score_lbl = tk.Label(game, text="PLACAR JOGADOR: 0", font="Arial 12")
    player_score_lbl.place(x=0, y=255)
    
    #definindo o texto dinâmico de pontuação(score) do computador
    cpu_score_lbl = tk.Label(game, text="PLACAR CPU: 0", font="Arial 12")
    cpu_score_lbl.place(x=0, y=275)
    
    #definindo as escolhas do jogador(combobox)
    playable_options_cbx = ttk.Combobox(game, values=["Pedra", "Papel", "Tesoura"],width=10, state="readonly")
    playable_options_cbx.place(x=100, y=170)
    
    #definindo imagem inicial da mão do computador
    cpu_hand_image_loader = tk.PhotoImage(file="cpu_hand_images/static_and_rock_cpu_hand.png")
    cpu_hand_image_lbl = tk.Label(image=cpu_hand_image_loader)
    cpu_hand_image_lbl.place(x=180, y=68)
    
    #definindo imagem inicial da mão do player
    player_hand_image_loader = tk.PhotoImage(file="player_hand_images/static_and_rock_player_hand.png")
    player_hand_image_lbl = tk.Label(image=player_hand_image_loader)
    player_hand_image_lbl.place(x=10, y=65)
    game.mainloop()
    
render_game()