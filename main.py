import bottle
import sqlite3
from datetime import date
from datetime import timedelta

conn = sqlite3.connect("books.db")
cur = conn.cursor()

SECRET_KEY = "this-is-secret"
LIFE_TIME = 120


def get_id(table="BookList"):
    try:
        for row in cur.execute(f'SELECT id FROM {table}'):
            last_id = (row[0])
    except StopIteration:
        last_id = 0
    id = last_id + 1
    return "{:08d}".format(id)


def get_row_by_id(id):
    row = []
    for value in cur.execute('SELECT * FROM BookList WHERE id = ?', (id,)):
        for i in range(7):
            row.append(value[i])

    if row[5] == 0:
        row[5] = "在庫"
    else:
        row[5] = f"{row[5]}まで{row[6]}に貸出中"

    data = {"id": row[0], "title": row[1], "author": row[2], "publisher": row[3],
            "date_of_purchase": row[4], "due_date": row[5]}
    return data


def get_reviews_by_book_id(id):
    cur.execute('SELECT * FROM BookReview WHERE book_id = ?', (id,))
    data = []
    for value in cur.execute('SELECT * FROM BookReview WHERE book_id = ?', (id,)):
        row = {"id": value[0], "book_id": value[1], "user_id": value[2],
               "date_of_review": value[3], "book_review": value[4], "book_star": value[5]}
        data.append(row)

    return data


def get_username():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)
    if username is None:
        bottle.redirect("/login")
    return username


@bottle.route("/entry")
def entry():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)
    data = {}
    data["username"] = username

    return bottle.template("entry", {"data": data})


@bottle.post("/submit")
def submit():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)
    data = {}
    data["username"] = username

    id = bottle.request.params.id
    title = bottle.request.params.title
    author = bottle.request.params.author
    publisher = bottle.request.params.publisher
    date_of_purchase = bottle.request.params.date_of_purchase
    due_date = 0
    data["book"] = {"title": title, "author": author, "publisher": publisher,
                    "date_of_purchase": date_of_purchase}
    print("submit", data)
    if id == "":
        id = get_id()
        cur.execute('INSERT INTO BookList VALUES (?, ?, ?, ?, ?, ?)',
                    (id, title, author, publisher, date_of_purchase, due_date))
        conn.commit()
    else:
        cur.execute(
            'UPDATE BookList SET title=?, author=?, publisher=?, date_of_purchase=? WHERE id=?',
            (title, author, publisher, date_of_purchase, id))
        conn.commit()

    return bottle.template("submit", {"data": data})


@bottle.route("/")
def root():
    username = get_username()

    data = {}
    data["books"] = []
    data["username"] = username
    for row in cur.execute('SELECT * FROM BookList'):
        if row[5] == 0:
            due_date = "在庫"
        else:
            due_date = f"{row[5]}まで{row[6]}に貸出中"

        data["books"].append({"id": row[0], "title": row[1], "author": row[2], "publisher": row[3],
                              "date_of_purchase": row[4], "due_date": due_date})

    return bottle.template("list", {"data": data})


@bottle.post("/confirm")
# @bottle.view("confirm")
def confirm():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)
    data = {}
    data["username"] = username
    data["books"] = []

    ids = bottle.request.forms.getall("selected_row")
    what_to_do = bottle.request.forms.get('what_to_do')
    print("ids", ids)
    if ids == []:
        bottle.redirect("/")

    for id in ids:
        data["books"].append(get_row_by_id(id))
    # print(data)
    if what_to_do == "borrow_or_return":
        if data["books"][0]["due_date"] == "在庫":
            due_date = date.today() + timedelta(days=30)
            due_date_str = str(due_date.strftime('%Y年%m月%d日'))
            data["confirm_str"] = f"本当に借りますか？ 返却期限：{due_date_str}"
            data["confirm_btn"] = "borrow"
        else:
            data["confirm_str"] = "本当に返却しますか？"
            data["confirm_btn"] = "return"
    elif what_to_do == "delete":
        data["confirm_str"] = "本当に削除しますか？"
        data["confirm_btn"] = "delete"
        # print(data)

    return bottle.template("confirm", {"data": data})


@bottle.post("/delete")
def delete():
    bottle.request.get_cookie("account", secret=SECRET_KEY)

    ids = bottle.request.forms.getall("selected_row")
    print("delete", ids)
    for id in ids:
        cur.execute('DELETE FROM BookList WHERE id = ?', (id,))
    conn.commit()
    bottle.redirect("/")


@bottle.post("/borrow")
def borrow():
    bottle.request.get_cookie("account", secret=SECRET_KEY)

    ids = bottle.request.forms.getall("selected_row")
    username = bottle.request.forms.getall("username")[0]
    due_date = date.today() + timedelta(days=30)
    due_date_str = str(due_date.strftime('%Y-%m-%d'))

    print(username)
    print("borrow", ids)
    for id in ids:
        cur.execute('UPDATE BookList SET due_date = ?, who_has_this = ? WHERE id = ?',
                    (due_date_str, username, id))
    conn.commit()
    bottle.redirect("/")


@bottle.post("/return")
def return_book():
    bottle.request.get_cookie("account", secret=SECRET_KEY)

    ids = bottle.request.forms.getall("selected_row")
    print("return", ids)
    for id in ids:
        cur.execute('UPDATE BookList SET due_date = 0 WHERE id = ?', (id,))
    conn.commit()
    bottle.redirect("/")


@bottle.route('/detail', method='GET')
def detail():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)
    data = {}
    data["username"] = username

    id = bottle.request.query.get('id')
    data["book"] = get_row_by_id(id)
    data["reviews"] = get_reviews_by_book_id(id)
    print("detail", data)
    return bottle.template("detail", {"data": data})


@bottle.post("/edit")
def edit():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)
    data = {}
    data["username"] = username

    id = bottle.request.params.selected_row
    data["book"] = get_row_by_id(id)
    print("edit", data)
    return bottle.template("edit", {"data": data})


@bottle.post("/review/entry")
def review_entry():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)

    id = bottle.request.forms.get('book_id')
    data = {"id": id, "username": username}
    print("review/entry data=", data)
    return bottle.template("review/entry", data)


@bottle.post("/review/submit")
def review_submit():
    username = bottle.request.get_cookie("account", secret=SECRET_KEY)

    book_id = bottle.request.forms.get('book_id')
    book_review = bottle.request.params.book_review
    data = get_row_by_id(book_id)

    data["username"] = username
    data["book_review"] = book_review  # .replace('\r\n', '<br>')
    data["date_of_review"] = str(date.today())

    data["user_id"] = username
    data["book_star"] = 5
    print("review/submit data=", data)

    id = get_id(table="BookReview")
    cur.execute('INSERT INTO BookReview VALUES (?, ?, ?, ?, ?, ?)',
                (id, book_id, data["user_id"], data["date_of_review"], data["book_review"], data["book_star"]))
    conn.commit()

    return bottle.template("review/submit", {"data": data})


@bottle.route("/login")
def login():
    return bottle.static_file("login.html", root="./static")


@bottle.post("/dologin")
def dologin():
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    if check_login(username, password):
        bottle.response.set_cookie("account", username,
                                   secret=SECRET_KEY, path="/", max_age=LIFE_TIME)
        bottle.redirect("/")
    else:
        bottle.redirect("/login")


def check_login(username, password):
    row = []
    for value in cur.execute('SELECT * FROM UserList WHERE user_id = ?', (username,)):
        for i in range(len(value)):
            row.append(value[i])
    data = {"id": row[0], "user_id": row[1], "password": row[2]}

    if password == data["password"]:
        return True
    return False


@bottle.route("/logout")
@bottle.post("/logout")
def logout():
    bottle.response.delete_cookie("account")
    bottle.redirect("/")


# bottle.run()
bottle.run(host="0.0.0.0", port=8080, debug=True, reloader=True)
