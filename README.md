## Тема курсового проекта - "Разработка системы автоматизации работы театра"

**Реализованный на текущий момент функционал:**
1. Реализовано два типа пользователей: admin, user. При регистрации автоматически присвается тип пользователя - user. Если необходимо добавить новую учетную запись типа admin, необходимо в базе данных в столбце role изменить значение на admin. 
2. Реализована регистрация пользователей: ввод почты(обязательное наличие "@"), ввод имени, ввод пароля (не меньше 6 символов), повторный ввод пароля.
3. После регистрации пользователя переносит на страницу, где указаны все пьессы и реализован функционал покупки билета, также реализован поиск пьесс по дате.
4. На этой же странице с пьессами для admin реализован функционал добавления новой пьессы, изменения уже существующих пьесс и их удаления.
5. В правом верхнем углу находится кнопка "Аккаунт", при нажатии на которую всплывает выпадающее окно -> мой профиль, выйти.
6. На странице мой профиль можно посмотреть информацию о профиле: имя, почта, роль, баланс. Также реализован функционал пополнения баланса и смены пароля.  На странице можно посмотреть купленные билеты и при необходимости их вернуть.
---
7. Сохранение и просмотр транзакций (страница добавлена в главное меню)
8. Добавлена таблица Transaction
9. Если мероприятие будет проходить не сегодня, а завтра и позднее, то при возврате билета на баланс пользователя возвращается 100% стоимости билета. Однако, если мероприятие запланировано сегодня, то возвращается только 50% стоимости билета.

**пояснительную записку прикрепила вместе с письмом на почте**

