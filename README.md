# executar projeto
```sh

git clone https://github.com/alexaleluia12/desafiomb.git

cd desafiomb
pip install -r requirements.txt
python app/load_base.py # executar apenas uma vez para caregar base de dados
python app/app.py
```

# executar testes
```sh
pytest
```

# executar job para atualização da base e verificar consistência
```sh
python app/job.py
```
# api
## endpoint
/:pair/mms
### parâmetros
```txt
from: timestamp data início
to: timestamp data fim
range: periodo data média móvel simples (20, 50, 200)

pair pode ser BRLBTC ou BRLETH
```

# atualização da base
Todo dia as 11 horas faz download de informação de fechamento para cada moeda. Considerando ontem até 200 dias atrás. Calcula novamente as médias móveis e insere um novo registro no banco de dados. Em caso de erro emite um log de erro.