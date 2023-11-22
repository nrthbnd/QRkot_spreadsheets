# Приложение для Благотворительного фонда поддержки Cat Charity Fund

### Автор:

- [Анастасия Боль · GitHub](https://github.com/nrthbnd)

### Описание проекта
Проект **Cat Charity Fund** - это веб-приложение, которое представляет собой фонд,
собирающий пожертвования на различные целевые проекты, связанные с
поддержкой кошачьей популяции. Фонд может иметь несколько проектов,
каждый из которых имеет своё название, описание и сумму, которую
необходимо собрать.
Пожертвования в проекты поступают по принципу *First In*, *First Out*,
то есть все пожертвования идут в проект, открытый раньше других.
Когда этот проект набирает необходимую сумму и закрывается,
пожертвования начинают поступать в следующий проект.

Также есть возможность формирования отчета в google-таблицах. В таблицу вносятся
**закрытые** проекты, отсортированные по скорости сбора средств:
сначала проекты, закрытые быстрее всех, далее проекты,
которые долго собирали необходимую сумму.

Основной целью проекта является помощь кошачьей популяции и
привлечение внимания к проблеме бездомных животных.
Проект Cat Charity Fund предоставляет удобный и прозрачный механизм для
сбора пожертвований и распределения их между различными проектами.

### Использование
Для использования приложения *Cat Charity Fund* вам необходимо выполнить
следующие шаги:

1. Клонируйте репозиторий cat_charity_fund в свою рабочую директорию на компьютере.
2. Создайте и активируйте виртуальное окружение `source venv/Scripts/activate`.
3. Установите все необходимые пакеты из файла requirements.txt
    `pip install -r requirements.txt`.
4. Запустите приложение с помощью команды `uvicorn app.main:app --reload`.
5. Теперь вы можете открыть веб-браузер и перейти по адресу http://localhost:8000,
чтобы получить доступ к приложению Cat Charity Fund.

### Особенности
Любой пользователь может видеть список всех проектов, включая требуемые
и уже внесенные суммы.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать
список своих пожертвований.

Процесс "инвестирования" запускается сразу после создания нового проекта
или пожертвования. Если создан новый проект, а в базе были "свободные"
(не распределенные по проектам) суммы пожертвований - они автоматически
инвестируются в новый проект (в ответе API эти суммы учтены).
То же касается и создания пожертвований: если в момент пожертвования есть
открытые проекты, эти пожертвования автоматически зачислияются на их счета.
