#!/usr/bin/env python
from constants import ROOMS
import utils
import player_actions as pa


game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}


def process_command(game_state: dict[str, object], command: str) -> None:
    command_splitted = command.split()
    match command_splitted[0]:
        case 'look':
            utils.describe_current_room(game_state)
        case 'use':
            pa.use_item(game_state, command_splitted[1])
        case 'go':
            pa.move_player(game_state, command_splitted[1])
        case 'take':
            pa.take_item(game_state, command_splitted[1])
        case 'inventory':
            pa.show_inventory(game_state)
        case 'quit':
            game_state['game_over'] = True
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                utils.attempt_open_treasure(game_state)
                # print('Вы победили!')
                # game_state['game_over'] = True
            else:
                utils.solve_puzzle(game_state)
        case 'help':
            utils.show_help()
        case 'north' | 'south' | 'east' | 'west':
            pa.move_player(game_state, command_splitted[0])
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main() -> None:
    print('Добро пожаловать в Лабиринт сокровищ!')
    utils.describe_current_room(game_state)
    while not game_state['game_over']:
        player_input = pa.get_input()
        process_command(game_state, player_input)
        


# Точка входа при запуске как модуля
if __name__ == "__main__":
    main()

