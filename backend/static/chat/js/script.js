class Field {
    constructor(field, role) {
        this.field = field;
        this.role = role;

        var count = 0,
            userCount = 0,
            rivalCount = 20;
        var userHint = document.getElementById('user-hint'),
            rivalHint = document.getElementById('rival-hint');

        userHint.innerText = userCount;
        rivalHint.innerText = rivalCount;

        this.fire = (target) => {
            userCount = document.querySelectorAll('#field-rival .broken').length;
            if (target.classList.contains('sheep')) {
                target.classList.add('broken');
                userCount += 1;

            } else {
                target.classList.add('missed');
                count += 1;
            }
            if(userCount == 20) {
                alert('You WIN!!!!')
            }
            this.backFire();
            userHint.innerText = userCount;
            rivalHint.innerText = rivalCount;
        }

        this.backFire = () => {
            // функция устанавливает значение на поле юзера
            var targets = document.querySelectorAll('#field-user div');
            var sheeps = document.querySelectorAll('#field-user .sheep');
            if (count == 1 && sheeps.length > 0) {
                let firedItemIndex = Math.floor(Math.random() * targets.length);
                this.fire(targets[firedItemIndex]);
                rivalCount = sheeps.length - document.querySelectorAll('#field-user .broken').length;
                count = 0;
            }
            if (sheeps.length === 0) {
                alert('You LOST')
            }
        }
    }

    render() {
        var fieldBlock = document.getElementById('field-' + this.role)
        for (let i = 0; i < this.field.length; i++) {
            for (let j = 0; j < this.field[i].length; j++) {
                var block = document.createElement('div');
                if (this.field[i][j] === 1) {
                    block.classList.add('sheep');
                };
                if (this.role === 'rival') {
                    block.addEventListener('click', (event) => this.fire(event.target));
                };
                fieldBlock.appendChild(block)
            }
        }
    }
}

let userField = {{userField}}
let rivalField = {{rivalField}}

var gameUser = new Field(userField, 'user')
gameUser.render();

var gameRival = new Field(rivalField, 'rival')
gameRival.render();