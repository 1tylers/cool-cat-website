from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

# creates blueprint object views, blueprint registers my flask routes
views = Blueprint('views', __name__)

# variables to keep track of quiz answers
click_count = 0
score_tracker = 0
extrotrait = 0
flowtrait = 0
realtrait = 0

# home route
@views.route('/')
def home():
    return render_template("home.html")

# test start page route
@views.route('/test/start')
def startpage():
    return render_template("starttest.html")

# route to redirect to the test
@views.route('/test/begin')
def start():
    return redirect(url_for('views.test'))

# test page route
@views.route('/test', methods=['POST'])
def test():
    return render_template("test.html")

# route to change and update buttons after being pressed
# POST method means a route that handles the data after being submitted, which is the button press data in this case
@views.route('/test/update_buttons', methods=['POST'])
def update_buttons():

    global click_count, score_tracker, progress, extrotrait, realtrait, flowtrait

    # process the button being pressed
    button_name = request.form.get('buttonName')

    # keep track if first option was pressed
    if button_name == 'button1':
        score_tracker += 1
    
    # list containing the options for the first button
    button1_texts = [
        f'I begin and figure things out along the way.',
        f'I bounce back quickly and continue.',
        f'I enjoy being the center of attention.',
        f'I prefer to follow the directions of my group members.',
        f'I stay calm and think of the best way to respond.',
        f'By initiating conversation first.',
        f'Do what I feel like at any given time throughout the day.',
        f'I rely soley on reason and evidence.'
    ]

    # list containing the options for the second button
    button2_texts = [
        f'I make sure I have a detailed plan before beginning.',
        f'I take time to get over it before moving forward.',
        f'I dislike when all eyes are on me.',
        f'I take initiative and lead the group.',
        f'I tend to let my emotions take over.',
        f'By waiting for them to come up to me first.',
        f'Have a set plan of activites I will do throughout the day.',
        f'I trust my feelings and instincts.'
    ]

    # list containing the questions
    questions_text = [
        f'When starting a new project:',
        f'After experiencing a failure:',
        f'At a social gathering:',
        f'When given a group project:',
        f'When faced with a challenging or stressful situation:',
        f'I normally talk to people:',
        f'When going about my day I tend to:',
        f'When making difficult decisions: '
    ]

    # this resets the trait variables if the test is refreshed or exited
    # session essentially sets the data to the current variables of the session, if they don't exist (meaning refreshed or left) then reset back to 0
    extrotrait = session.get('extrotrait', 0)
    flowtrait = session.get('flowtrait', 0)
    realtrait = session.get('realtrait', 0)

    # increment the trait variables if button 1 is clicked
    if button_name == 'button1':
        if click_count == 0 or click_count == 3 or click_count == 6:
            extrotrait += 1
        elif click_count == 1 or click_count == 4 or click_count == 7:
            flowtrait += 1
        elif click_count == 2 or click_count == 5 or click_count == 8:
            realtrait += 1
    
    # determine which cat based on the results of the test
    if extrotrait > 1:
        if flowtrait > 1:
            if realtrait > 1:
                image = "/static/seabreezecatresults.png"
                cat_text = 'Sea Breeze Cat'
            else:
                image ="/static/sunshinecatresults.png"
                cat_text = 'Sunshine Cat'    
        else:
            if realtrait > 1:
                image ="/static/clementinecatresults.png"
                cat_text = 'Clementine Cat'
            else:
                image ="/static/strawberrycatresults.png"
                cat_text = 'Strawberry Cat'
    else:
        if flowtrait > 1:
            if realtrait > 1:
                image ="/static/cloudycatresults.png"
                cat_text = 'Cloudy Cat'
            else:
                image ="/static/cherryblossomcatresults.png"
                cat_text = 'Cherry Blossom Cat'
        else:
            if realtrait > 1:
                image ="/static/lavendercatresults.png"
                cat_text = 'Lavender Cat'
            else:
                image ="/static/cucumbercatresults.png"
                cat_text = 'Cucumber Cat'


    # resets click count if refreshed or exited
    click_count = session.get('click_count', 0)

    # sets the buttons and question to update each time
    new_text_button1 = button1_texts[click_count % len(button1_texts)]
    new_text_button2 = button2_texts[click_count % len(button2_texts)]
    new_question = questions_text[click_count % len(questions_text)]

    # increment click count when button is pressed
    click_count += 1

    # if click count is 9 (meaning test is complete) redirect to test results and send the cat data
    if click_count == 9:
        # reset variables before redirecting
        click_count = 0
        session.pop('click_count', None)
        session.pop('extrotrait', None)
        session.pop('flowtrait', None)
        session.pop('realtrait', None)
        session['score_tracker'] = score_tracker
        return redirect(url_for('views.testresults', image=image, cat_text=cat_text))
    
    # keep track of session data
    session['click_count'] = click_count
    session['score_tracker'] = score_tracker
    session['extrotrait'] = extrotrait
    session['flowtrait'] = flowtrait
    session['realtrait'] = realtrait

    # keep track of progress for progress bar
    progress = (click_count + 1)

    # returns data to update progress bar, questions, and buttons
    return jsonify({'status': 'success', 'new_text_button1': new_text_button1, 'new_text_button2': new_text_button2, 'new_question': new_question, 'progress': progress})

# if session is reset, reset the variables
@views.route('/test/reset_session', methods=['GET'])
def reset_session():
    global score_tracker
    score_tracker = 0
    session.pop('click_count', None)
    session.pop('score_tracker', None)
    session.pop('extrotrait', None)
    session.pop('flowtrait', None)
    session.pop('realtrait', None)

    return jsonify({'status': 'success'})

# test results route
@views.route('/test/results', methods=['GET'])
def testresults():
    # retrieve the image and cat name
    image = request.args.get('image')
    cat_text = request.args.get('cat_text')

    # render the results page
    return render_template ('results.html', image=image, cat_text=cat_text)

# Cat Encyclopedia route
@views.route('/catinfo')
def catinfo():
    return render_template("catinfo.html")



