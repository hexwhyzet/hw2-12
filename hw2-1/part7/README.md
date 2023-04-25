## ДЗ 2-1 Часть 7

Собираем контейнер
```bash
docker build -t hw2-1-part7 .
```

Запускаем контейнер
```bash
docker run -d --name test -it hw2-1-part7
```

Заходим в контейнер
```bash
docker exec -it test bash
```

Запускаем тесты тестов
```bash
root@3f4cc6a8837c:/app# python test.py
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```
