import utils
from constants import ROOMS


def show_inventory(game_state: dict[str, object]) -> None:
    '''
    Функция, которая показывает, что есть в инвентаре игрока
    '''
    player_inventory = game_state['player_inventory']
    if player_inventory:
        print(*player_inventory)
    else:
        print('Инвентарь пуст.')


def get_input(prompt: str = "> ") -> str:
    '''
    Функция, которая считывает ввод
    '''
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict[str, object], direction: str) -> None:
    '''
    Функция перехода в другую комнату
    '''
    current_room = game_state['current_room']
    if direction in ROOMS[current_room]['exits'].keys():
        if ROOMS[current_room]['exits'][direction] == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print('Вы используете найденный ключ, чтобы открыть путь ' \
                'в комнату сокровищ.')
            else:
                print('Дверь заперта. Нужен ключ, чтобы пройти дальше.')
                return
        game_state['current_room'] = ROOMS[current_room]['exits'][direction]
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
        utils.random_event(game_state)
    else:
        print('Нельзя пойти в этом направлении.')


def take_item(game_state: dict[str, object], item_name: str) -> None:
    '''
    Функция для поднятия предмета
    '''
    current_room = game_state['current_room']
    if item_name in ROOMS[current_room]['items']:
        if item_name != 'treasure_chest':
            game_state['player_inventory'].append(item_name)
            ROOMS[current_room]['items'].remove(item_name)
            print('Вы подняли:', item_name)
        else:
            print('Вы не можете поднять сундук, он слишком тяжелый.')
    else:
        print('Такого предмета здесь нет.')


def use_item(game_state: dict[str, object], item_name: str) -> None:
    '''
    Функция для использования предмета
    '''
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                print('Стало светлее.')
            case 'sword':
                print('Теперь я чувствую себя увереннее.')
            case 'bronze_box':
                print('Шкатулка открыта.')
                if 'rusty_key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')  
            case _:
                print('Я не знаю, что с этим делать.')
    else:
        print('У вас нет такого предмета.')