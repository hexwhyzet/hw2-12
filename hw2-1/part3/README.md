## ДЗ 2-1 Часть 3

Собираем контейнер
```bash
docker build -t hw2-1-part3 .
```

Запускаем
```bash
docker run -v $PWD:/app hw2-1-part3 file1.txt
docker run -v $PWD:/app hw2-1-part3 file2.txt
docker run -v $PWD:/app hw2-1-part3 file1.txt
```