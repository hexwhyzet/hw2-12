## ДЗ 2-1 Часть 9

Собираем контейнер
```bash
docker build -t hw2-1-part9 .
```

Запускаем
```bash
docker run -v $PWD/main.py:/app/main.py -it hw2-1-part9
```