# Bot do Canal Central de Tudo
http://telegram.me/centraldetudo

## Instalação

### Para clonar o repositório em seu computador:
```
git clone git@github.com:GabrielRF/CentralDeTudo.git
cd CentralDeTudo
```
### Para instalar todos os componentes necessários ao funcionamento do bot:
```
pip install -r requirements.txt
```
### Crie o arquivo `bot.conf` e altere-o usando o editor de sua preferência:
```
cp bot.conf_sample bot.conf
```
`token`: Token do bot. Obtido com o [@BotFather](http://telegram.me/BotFather).

`dest`: Destino das mensagens. Exemplo: `@CentralDeTudo`.

`admin`: Os administradores do bot. Quem tem autorização para adicionar links à fila.

`file`: Arquivo que contém a fila de links.

### Crie o arquivo `fila.txt`:

É importante que o caminho do arquivo seja o mesmo indicado no passo anterior.

```
touch fila.txt
```

## Uso

### Para criar o processo que recebe os links, execute:
```
python line.py
```
### Para enviar um link presente na fila, execute:
```
python send.py
```
