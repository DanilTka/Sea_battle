#  Multiplayer sea battle game

## Stack: ##

- **Django**
  - channels (+redis)
- Docker

## Usage: ##

  ```sh
  git clone git@gitlab.com:tovarischduraley/seabattle.git

  cd Sea_battle

  docker-compose build

  docker-compose up
  ```
## Additional: ##
1. auto recconect to the server (game state will be saved).
2. guaranteed message delivery.
