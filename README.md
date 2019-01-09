# Sample python API with sqlite

- Create virtualenv

    ```pthon
    virtualenv flask
    ```
- Install flask

    ```python
    flask/bin/pip install flask
    flask/bin/pip install flask-httpauth
    flask/bin/pip install Flask-SQLAlchemy
    flask/bin/pip install flask-migrate
    ```

- Testing models while develop

    ```bash
    flask/bin/python
    ```

    ```python
    >>> from app import application, db
    >>> from app.models import AppStatus as a
    >>> import time
    >>> row1 = a(app_name='APP 1', app_version='12.123', updated_date=time.time(), updated_by='kuba')
    >>> db.session.add(row1)
    >>> db.session.commit()
    >>> a.query.order_by(a.id.desc()).first()
    ```

- Init the database

    ```bash
    flask/bin/flask db init
    ```
- Make first migration

    ```bash
    flask/bin/flask db migrate -m "tasks table"
    flask/bin/flask db upgrade
    ```

- Run app

    ```bash
    ./app.py
    ```

- Basic reqiest

  - Add task(Basic auth require)

      ```bash
      curl -i -H "Content-Type: application/json" -X POST -d '{"app_name": "Python API", "app_version": "0.12"}' http://127.0.0.1:5000/api/app/new -u kuba:test
      ```
  - Get specific app information

      ```bash
      curl -i http://127.0.0.1:5000/api/app/2
      ```

  - Get all app info(Basic auth require)

      ```bash
      curl -i http://127.0.0.1:5000/api/apps -u kuba:test
      ```

  - Get update data(Basic auth require)

      ```bash
      curl -i -H "Content-Type: application/json" -X PUT -d '{"app_version": "1.1"}'  http://127.0.0.1:5000/api/app/2 -u kuba:test
      ```

  - Delete on app record(Basic auth require)

      ```bash
      curl -i -X DELETE http://127.0.0.1:5000/api/app/2 -u kuba:test
      ```

