#  Multiplayer sea battle game

## Stack: ##

- **Django**
  - channels (+redis)
- Docker

## Usage: ##

  ```sh
  git clone git@github.com:DanilTka/Sea_battle.git

  cd Sea_battle
  
  docker-compose up --build
  ```
## Additional: ##
1. auto recconect to the server (game state will be saved).
2. guaranteed message delivery.

## Game frames: ##
### Lobby
![](https://i.ibb.co/QPTJK6W/lobby.png)
### Room
![](https://i.ibb.co/tXS7S0c/game.png)
### Chat
![](https://i.ibb.co/VBwkjwm/chat.png)
