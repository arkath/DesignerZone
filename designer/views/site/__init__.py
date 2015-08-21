__author__ = 'anurag'

from designer.app import flaskapp
from flask import session, g, request, jsonify, render_template
from designer.services.utils import login_required, login_user_session, setup_context
from designer.services.extractors.user import UserExtractor

@flaskapp.before_request
def before_request():
    from designer.models.user import User
    session.permanent = True
    if session.get('user') is not None:
        g.user = User.objects(pk=session['user']).first()
    else:
        g.user = None
    if session.get('just_logged_in', False):
        g.just_logged_in = True
        session['just_logged_in'] = False

@flaskapp.route('/editors/invoke', methods=['POST'])
def editor_invoke():
    try:
        message = request.get_json(force=True)
        from designer.services.editors.base import BaseEditor
        editor = BaseEditor.factory(message)
        response = editor._invoke()
        return jsonify(response)
    except Exception, e:
        return jsonify(dict(status='error', message='Something went wrong', exception=str(e)), context=setup_context())

# @flaskapp.route('/extractors/invoke', methods=['POST'])
# def extractor_invoke():
#     try:
#         message = request.get_json(force=True)
#         from designer.services.extractors.base import BaseExtractor
#         extractor = BaseExtractor.factory(message)
#         response = extractor._invoke()
#         return jsonify(response)
#     except Exception, e:
#         return jsonify(dict(status='error', message='Something went wrong', exception=str(e)), context=setup_context())



@flaskapp.route("/")
def render_home_template():
    try:
        return render_template('templates/main_landing.html')
    except Exception,e:
        raise e


@flaskapp.route("/login", methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            from designer.models.user import User
            message = request.get_json(force=True)
            email, password = message['email'], message['password']
            user = User.authenticate(email, password)
            if user and user.id:
                login_user_session(user)
                target = request.args.get('target', None)
                response =  jsonify(dict(status='success', message='Successfully logged in', node=user, my_page=target if target is not None and len(target) > 0 else user.slug))
                return response
            else:
                return jsonify(dict(status='error', message='Invalid EmailId and/or Password'))
        else:
            return render_template('pages/sign-in.html')
    except Exception,e:
        raise e

@flaskapp.route("/register")
def register():
    try:
        return render_template('pages/register.html')
    except Exception,e:
        raise e


@flaskapp.route("/user/<slug>")
def get_user_by_id(slug):
    node = UserExtractor.get_by_slug(slug)
    if node is not None:
        return render_template('templates/profile.html', user=node, model=node)
    else:
        return jsonify(dict(status='failure', message='User not found'))


@flaskapp.route("/portfolio/<id>", methods=["GET"])
def get_portfolio_by_id(id):
    from designer.models.creatives import Portfolio
    node = Portfolio(pk=id)
    if node is not None:
        return render_template('pages/portfolio.html', model=node)
    else:
        return jsonify(dict(status='failure', message='Portfolio not found'))