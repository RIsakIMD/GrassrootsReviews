
from flask_app.config.mysqlconnection import connectToMySQL

class Review:
    schema="grassroots_schema"

    def __init__(self, data):
        self.id = data['id']
        self.media = data['media']
        self.text = data['text']
        self.score = data['score']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_review(cls, data):
        query = "INSERT INTO reviews (media, text, score, user_id) VALUES (%(media)s, %(text)s, %(score)s, %(user_id)s);"
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def get_one(cls, review_id):
        results = connectToMySQL(cls.schema).query_db("SELECT * FROM reviews WHERE reviews.id = %(review_id)s;", {'review_id': review_id})
        return cls(results[0])

    @classmethod
    def get_all(cls):
        results = connectToMySQL(cls.schema).query_db("SELECT * FROM reviews")
        reviews = []
        for review in results:
            reviews.append(cls(review))
        return reviews

    @classmethod
    def get_latest(cls):
        results = connectToMySQL(cls.schema).query_db("SELECT * FROM reviews ORDER BY created_at DESC LIMIT 5;")
        reviews = []
        for review in results:
            reviews.append(cls(review))
        return reviews

    @classmethod
    def update_review(cls, data):
        query = """
        UPDATE reviews SET
        media = %(media)s,
        text = %(text)s,
        score = %(score)s,
        user_id = %(user_id)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def delete_review(cls, id):
        return connectToMySQL(cls.schema).query_db("DELETE FROM reviews WHERE id = %(id)s", {'id': id})

