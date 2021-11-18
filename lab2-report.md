# Лабораторная работа №2
> Цель работы: Поиск и устранение SQL Injection.
> Исходный текст задания: https://github.com/SergeyMirvoda/secure-web-development-21/blob/main/lab2.md

## Выполнение
Те, кто делает лабораторную на своём языке программирования, должны сначала восстановить в точности этот пример
> Выбран язык программирования Python 3.8

## Задание 1
0. Запустить сайт
> Исходный код сайта: https://github.com/Tyz3/WebApp/commit/c5df4961ab424570edf3c27a20231748fa45f144
![image](https://user-images.githubusercontent.com/21179689/142441085-83c8b735-a6dd-4332-9c4f-1d385370e4d6.png)
![image](https://user-images.githubusercontent.com/21179689/142441190-6366483f-fb05-4903-bbc2-ba237ec167bc.png)
1. Обход установленного фильтра
> Проверим, уязвима ли форма и выводит ли сайт лог ошибки, если передать в качестве значения симовлы, нарушающие синтаксис SQL ``''``.
![image](https://user-images.githubusercontent.com/21179689/142445240-1e8a31ba-cab3-4529-8997-7e97ceb62655.png)
2. Получение данных из другой таблицы
> Попробуем получить данные из другой таблицы с помощью UNION SELECT, соблюдая количество полей для вывода и их типы (особенность PostgreSQL)
> Вводим в поле фильтра ``' UNION SELECT 1, name, pass FROM users --`` и нажимаем **Применить**
![image](https://user-images.githubusercontent.com/21179689/142441862-8b204521-f5f6-477d-b493-9197e2da70b9.png)
3. Похищение пароля пользователя
> Зная md5 хэш пароля пользователя, воспользуемся сайтами-декодерами (базы данных хэшей) md5 для определения исходного пароля пользователя.
4. Исправить уязвимость
> Для исправления уязвимости избавимся от классической конкатенации строк в пользу параметризации запроса.
> Также отключён вывод ошибок пользователю (теперь только для сайта)
![image](https://user-images.githubusercontent.com/21179689/142448284-0ad4ad1f-2ad0-452a-b49d-d2003d5ab10a.png)

Результат: https://github.com/Tyz3/WebApp/commit/2fe7ec4cc54d2d4f5d54324a5939fbbcdb1830c1