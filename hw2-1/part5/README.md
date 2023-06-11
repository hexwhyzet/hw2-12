## ДЗ 2-1 Часть 5

Собираем контейнер
```bash
docker build -t hw2-1-part5 .
```

Запускаем
```bash
docker run -v $PWD:/app -e FILE=main.py hw2-1-part5
```