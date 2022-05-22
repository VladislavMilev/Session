from sqlalchemy.orm import sessionmaker
from DAO.engine import engine


class Session:
    """
    Class needed to create a session instance
    """

    def __init__(self):
        self.engine = engine
        self.maker = sessionmaker(self.engine)
        self.session = self.maker()

    def query(self):
        """
        :return: session instance
        """
        return self.session

    def row2dict(self, row):
        """
        Convert SQLAlchemy row object to a Python dict
        :param row: object to generate
        :return: dict with neat object output
        """
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d

    def list2dict(self, lst):
        """
        Convert SQLAlchemy row object to a Python dict
        :param lst: object to generate
        :return: list dict with neat object output
        """
        d = {}
        l = []
        for item in range(len(lst)):
            for column in lst[item].__table__.columns:
                d[column.name] = str(getattr(lst[item], column.name))
            l.append(d)
            d = {}
        return l

    def check_fields_for_update(self, instance, data):
        """
        The method compares the parameters of the updated object with the existing one.
        Leaves the current data and changes the new ones
        :param instance: instance of query result
        :param data: parameters to be updated
        :return: new instance
        """
        for i in self.row2dict(instance).keys():
            if i == 'id' or data.get(i) == None:
                continue
            elif self.row2dict(instance).get(i) != data.get(i):
                setattr(instance, i, data.get(i))
            else:
                return {'error': f'Can not update {instance.__table__} instance'}

        return instance


class SessionCreate(Session):
    """
    Class decorator
    Needed to decorate all transaction function which post some data like: create_user()
    After triggering, adds an instance of the DAO class to the session, commits and closes the session
    Example:
    @SessionQueryPost
    def create_user(name)
        return User(name)
    """

    def __init__(self, function):
        super().__init__()
        self.function = function

    def __call__(self, data: dict):
        try:
            instance = self.function(self, data)
            self.session.add(instance)
            self.session.commit()
            return data
        except Exception as error:
            return {'error': f'{error}'}
        finally:
            self.session.close()


class SessionGet(Session):
    """
    Class decorator
    Needed to decorate all transaction function which get some data like: create_user()
    After triggering, adds an instance of the DAO class to the session, commits and closes the session
    Example:
    @SessionQueryGet
    def get_user_by_id(id)
        return self.session.query(User).filter(User.id == id).first()
    """

    def __init__(self, function):
        super().__init__()
        self.function = function

    def __call__(self, data: dict = None):
        try:
            instance = self.function(self, data)
            return self.row2dict(instance)
        except Exception as error:
            return {'error': f'{error}'}
        finally:
            self.session.close()


class SessionGetAll(Session):
    """
    Class decorator
    Needed to decorate all transaction function which get some data like: create_user()
    After triggering, adds an instance of the DAO class to the session, commits and closes the session
    Example:
    @SessionQueryGet
    def get_user_by_id(id)
        return self.session.query(User).filter(User.id == id).first()
    """

    def __init__(self, function):
        super().__init__()
        self.function = function

    def __call__(self, data: dict = None):
        try:
            instance = self.function(self)
            return self.list2dict(instance)
        except Exception as error:
            return {'error': f'{error}'}
        finally:
            self.session.close()


class SessionUpdate(Session):

    def __init__(self, function):
        super().__init__()
        self.function = function

    def __call__(self, data: dict = None):
        try:
            instance = self.function(self, data)
            self.check_fields_for_update(instance, data)
            self.session.commit()
            return self.row2dict(instance)
        except Exception as error:
            return {'error': f'{error}'}
        finally:
            self.session.close()


class SessionDelete(Session):

    def __init__(self, function):
        super().__init__()
        self.function = function

    def __call__(self):
        try:
            instance = self.function(self)
            self.session.delete(instance)
            self.session.commit()
            return self.row2dict(instance)
        except Exception as error:
            return {'error': f'{error}'}
        finally:
            self.session.close()
