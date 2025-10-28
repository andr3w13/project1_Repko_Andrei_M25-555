import math

import player_actions as pa
from constants import ROOMS
from labyrinth_game.constants import COMMANDS


def describe_current_room(game_state: dict[str, object]) -> None:
    '''
    Функция для вывода описания текущей комнаты
    '''

    current_room = game_state['current_room']
    
    print(f'== {current_room.upper()} ==')
    print(ROOMS[current_room]['description'])
    if ROOMS[current_room]['items']:
        print('Заметные предметы:', *ROOMS[current_room]['items'])
    print(f"Выходы: {ROOMS[current_room]['exits']}")
    if ROOMS[current_room]['puzzle']:
        print('Кажется, здесь есть загадка (используйте команду solve).')


def solve_puzzle(game_state: dict[str, object]) -> None:
    '''
    Функция для решения загадок
    '''
    current_room = game_state['current_room']
    if ROOMS[current_room]['puzzle'] is not None:
        print(ROOMS[current_room]['puzzle'][0])
        user_answer = pa.get_input('Ваш ответ: ').lower()
        match current_room:
            case 'hall':
                if user_answer == '10' or user_answer == 'десять':
                    print('Ответ верный!')
                    ROOMS['hall']['puzzle'] = None
                    print('Вы открываете сундук и находите старинную статуэтку.')
                    game_state['player_inventory'].append('ancient_statuette')
                else:
                    print('Ответ неверный.')
            case 'trap_room':
                if user_answer == ROOMS['trap_room']['puzzle'][1]:
                    print('Ответ верный!')
                    print('Вы избежали попадания в ловушку и в награду ' \
                    'получаете rusty_key от сокровищницы.')
                    game_state['player_inventory'].append('rusty_key')
                    ROOMS['trap_room']['puzzle'] = None
                else:
                    trigger_trap(game_state)
            case 'library':
                if user_answer == ROOMS['library']['puzzle'][1]:
                    print('Ответ верный!')
                    print('В награду вы получаете код от сундука с сокровищами: 10.')
                    ROOMS['library']['puzzle'] = None
                else:
                    print('Ответ неверный.')
            case 'garden':
                if user_answer == '12' or user_answer == 'двенадцать':
                    print('Ответ верный!')
                    ROOMS['garden']['puzzle'] = None
                    print('Ворота открываются и перед вами стоит ухожанный ' \
                    'старинный фонтан, можете пройти к нему, пойдя на восток.')
                    ROOMS['garden']['exits'].update({'east': 'fountain'}) 
                else:
                    print('Ответ неверный.')


def attempt_open_treasure(game_state: dict[str, object]) -> None:
    '''
    Функция открытия сундука с сокровищами
    '''
    current_room = game_state['current_room']
    if 'treasure_key' in game_state['player_inventory']:
        print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
        game_state['player_inventory'].remove('treasure_key')
        print('В сундуке сокровище! Вы победили!')
        game_state['game_over'] = True
    else:
        yn = pa.get_input('Сундук заперт. Ввести код? (да/нет) ')
        match yn:
            case 'да':
                code = pa.get_input('Введите код: ')
                if code == ROOMS[current_room]['puzzle'][1]:
                    print('Сундук открыт! Вы победили!')
                    ROOMS[current_room]['items'].remove('treasure_chest')
                    game_state['game_over'] = True
                else:
                    print('Код неверный. Попробуйте еще раз.')
            case 'нет':
                print('Вы отступаете от сундука.')


def show_help(commands: dict[str, str] = COMMANDS) -> None:
    '''
    Вывод информации о командах
    '''
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")


def pseudo_random(seed: int, modulo: int) -> int:
    '''
    Функция, которая генерирует псевдослучайное число
    '''
    x = math.sin(seed * 28.12903) * 56483.09438
    return math.floor((x - math.floor(x)) * modulo)


def trigger_trap(game_state: dict[str, object]) -> None:
    '''
    Функция, которая активирует ловушку
    '''
    print('Ловушка активирована! Пол стал дрожать.')
    if game_state['player_inventory']:
        ind = pseudo_random(42, len(game_state['player_inventory']))
        item_popped = game_state['player_inventory'].pop(ind)
        print('Вы потеряли ', item_popped)
    else:
        damage = pseudo_random(42, 9)
        if damage < 3:
            print('Вы получили слишком большой урон. Игра закончена.')
            game_state['game_over'] = True
        else:
            print('Вы получили урон, но выжили.')


def random_event(game_state: dict[str, object]) -> None:
    '''
    Функция, которая случайным образом генерирует 
    события при переходе из одной комнаты в другую
    '''
    current_room = game_state['current_room']
    EVENT_PROBABILITY = pseudo_random(42, 10)
    if EVENT_PROBABILITY == 0:
        match pseudo_random(42, 2):
            case 0:
                print('Вы находите монетку на полу.')
                ROOMS[current_room]['items'].append('coin')
            case 1:
                print('Вы слышите шорох...')
                if 'sword' in game_state['player_inventory']:
                    print('Вы отпугнули существо мечом.')
            case 2:
                if current_room == 'trap_room' \
                and 'torch' not in game_state['player_inventory']:
                    print('Опасность!')
                    trigger_trap(game_state)