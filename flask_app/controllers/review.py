
from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.review import Review
from flask_app.models.user import User

@app.route('/')
def root():
    media = {}

    for review in Review.get_all():
        if not review.media in media:
            media[review.media] = int(review.score)
        else:
            media[review.media] += int(review.score)

    if not media:
        return render_template("root.html")

    sorted_media = sorted(media.items(), key=lambda x:x[1], reverse=True)
    top_media = {
        'media': sorted_media[0][0],
        'score_count': 0,
        'avg_score': 0.0,
        'scores' : {}
    }

    total_score = sorted_media[0][1]

    for review in Review.get_all():
        if review.media == top_media['media']:
            if not review.score in top_media['scores']:
                top_media['scores'][review.score] = 1
            else:
                top_media['scores'][review.score] += 1

    for score in top_media['scores']:
        top_media['score_count'] += top_media['scores'][score]

    avg = total_score / top_media['score_count']
    top_media['avg_score'] = float(f'{avg:.2f}')

    return render_template("root.html", top_media=top_media, reviews=Review.get_latest())

@app.route('/latest')
def latest():
    return render_template("latest.html", reviews=Review.get_latest())

@app.route('/reviews/<int:review_id>')
def review_details(review_id):
    review = Review.get_one(review_id)
    user = User.get_user(review.user_id)

    return render_template("review.html", review=review, user=user)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    success = True

    review_data = dict(request.form)
    review_data['user_id'] = session['user']

    if len(review_data['media']) < 1:
        success = False
        flash("Media cannot be blank")

    if len(review_data['text']) < 10:
        success = False
        flash("Review must be longer than 10")

    if review_data['score']:
        score = int(review_data['score'])
    else:
        score = -1

    if score > 5 or score < 0:
        success = False
        flash("Score must be between 0 and 5")

    if success:
        Review.add_review(review_data)
        return redirect('/account')

    return redirect('/account')

@app.route('/update_review/<int:review_id>/', methods=['POST'])
def update_review(review_id):
    data = {
        "id" : review_id,
        "media" : request.form["media"],
        "text" : request.form["text"],
        "score" : request.form["score"],
        "user_id" : session['user']
    }
    Review.update_review(data)
    return redirect(f'/reviews/{review_id}')

@app.route('/delete_review/<int:review_id>/')
def delete_review(review_id):
    Review.delete_review(review_id)
    return redirect('/account')