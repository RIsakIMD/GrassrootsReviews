
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.review import Review

class User:
    schema="grassroots_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reviews = []

    @classmethod
    def get_user_id(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s AND users.password = %(password1)s"
        results = connectToMySQL(cls.schema).query_db(query, data)
        print(results)
        if not results or not all(results):
            return None
        return cls(results[0])

    @classmethod
    def get_user(cls, user_id):
        results = connectToMySQL(cls.schema).query_db("SELECT * FROM users LEFT JOIN reviews ON reviews.user_id = users.id WHERE users.id = %(user_id)s;", {'user_id': user_id})
        user = cls(results[0]) # create the main class from the first row
        # all rows contain info from the join
        for result in results:
            if result["reviews.id"]:
                review_data = {
                    "id": result["reviews.id"],
                    "media": result["media"],
                    "text": result["text"],
                    "score": result["score"],
                    "user_id": result["user_id"],
                    "created_at": result["reviews.created_at"],
                    "updated_at": result["reviews.updated_at"]
                }
                user.reviews.append(Review(review_data))
        return user

    @classmethod
    def get_all(cls):
        results = connectToMySQL(cls.schema).query_db("SELECT * FROM users;")
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (name, email, password) VALUES (%(name)s, %(email)s, %(password1)s);"
        return connectToMySQL(cls.schema).query_db(query, data)
