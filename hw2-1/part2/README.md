## ДЗ 2-1 Часть 2

Собираем контейнер
```bash
docker build -t hw2-1-part2 .
```

Запускаем
```bash
docker run -v $PWD/../part1/main.py:/app/main.py hw2-1-part2 .
```