# Treasures Maze

**Treasures Maze** — это консольная приключенческая игра, в которой игрок исследует лабиринт, ищет сокровища и старается выбраться живым.  
Цель игры — собрать все сокровища и найти выход из лабиринта.

---

## Установка

Перед началом убедитесь, что установлен **Python 3.10+** и **Poetry**.

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/<твой-логин>/project1_Repko_Andrei_M25-555.git
cd project1_Repko_Andrei_M25-555

### 2. Установите зависимости
```bash
poetry install

или через Makefile
```bash
make install

### 3. Запуск игры
```bash
poetry run project

или
```bash
make project

После запуска появится приглашение командной строки.
Используйте текстовые команды для перемещения, взаимодействия с предметами и победы.

Примеры команд:
look 
go north/west/east/south
take "имя предмета"
solve
quit

### 4. Пример игрового процесса
[![asciinema demo](https://asciinema.org/a/z2thhf471pIleEUYskJvZWEva)](https://asciinema.org/a/z2thhf471pIleEUYskJvZWEva)






