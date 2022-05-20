# Session Framework
Session framework for SQLAlchemy transactions

## Why?
The session classes are written to shift the burden of working with the SQLAlchemy session onto the decorator classes. While in methods for transactions, you will only need to work with useful queries to the database.

## Example
    class UserDAO(Session):

    @SessionQueryCreate
    def create_user(self, data: dict):
        name = data.get('name')
        username = data.get('username')
        age = data.get('age')
        email = data.get('email')

        return User(name=name, username=username, age=age, email=email)

    @SessionQueryGet
    def get_user_by_id(self, data: dict):
        id = data.get('id')

        return self.session.query(User).filter(User.id == id).first()

    @SessionQueryGetAll
    def get_users(self):
        return self.session.query(User).all()

    @SessionQueryUpdate
    def update_user(self, data: dict):
        user = self.session.query(User).filter(User.id == data.get('id')).first()

        return user

###### Version 1.0