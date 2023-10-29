"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:your_new_password@localhost:5432/blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'


with app.app_context():
    connect_db(app)
    db.create_all()
    new_user = User(first_name="Kids", last_name="Perfects", image_url="https://www.freeiconspng.com/uploads/face-head-woman-female-icon-23.png")
    db.session.add(new_user)
    db.session.commit()
    new_post = Post(title="Hello There People Siblings", content="This is my ninth post", user_id = 1)
    db.session.add(new_post)
    db.session.commit()



# **GET */ :*** Redirect to list of users. (We’ll fix this in a later step).
@app.route('/')
def root():
    """Homepage will redirect to the user list."""
    return redirect("/users")


# **GET */users :*** Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
@app.route('/users')
def users_index():
    """Show information for all users."""

    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users/index.html', users=users)


# **GET */users/new :*** Show an add form for users
@app.route('/users/new', methods=["GET"])
def users_add_form():
    """Display a form for adding a new user."""

    return render_template('users/add_user.html')


# **POST */users/new :*** Process the add form, adding a new user and going back to ***/users***
@app.route("/users/new", methods=["POST"])
def users_add():
    """Process the form submission for adding a new user."""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


# **GET */users/[user-id] :***Show information about the given user. Have a button to get to their edit page, and to delete the user.
@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/show_user.html', user=user)


# **GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show the edit page for an existing user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


# **POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Process the edit form for updating an existing user."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


# **POST */users/[user-id]/delete :*** Delete the user.
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Process form for deleting an existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

### POSTS ###
# **GET */users/[user-id]/posts/new :*** Show form to add a post for that user.
@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)


# **POST */users/[user-id]/posts/new :*** Handle add form; add post and redirect to the user detail page.
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


# **GET */posts/[post-id] :*** Show a post. Show buttons to edit and delete the post.
@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show post and buttons to edit and delete the post."""

    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('posts/show.html', post=post, user=user)


# **GET */posts/[post-id]/edit :*** Show form to edit a post, and to cancel (back to user page).
@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)
                           

# **POST */posts/[post-id]/edit :*** Handle editing of a post. Redirect back to the post view.
@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


# **POST */posts/[post-id]/delete :*** Delete the post.
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting a post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")
