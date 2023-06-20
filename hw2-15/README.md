Сори что без докера, не успеваю его собрать и проверить :(
### Поднимаем Temporal
```shell
git clone https://github.com/temporalio/docker-compose.git
cd docker-compose
docker compose up
```

### Создаем venv
```shell
python3.9 -m venv ./venv
. /venv/bin/activate
pip install -r requirements.txt
```

### Поднимаем воркер
```shell
python worker
```

### Поднимаем api
```shell
python app
```