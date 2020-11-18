from flask import Flask, render_template, request, redirect
from operator import itemgetter

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, get_item, add_item, save_item, remove_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = sorted(get_items(), key=itemgetter('status'), reverse=True)
    return render_template("index.html",items=items)

@app.route('/add_new', methods=['POST'])
def addtolist():
    newitemtitle = request.form.get('title')
    add_item(newitemtitle)
    return redirect(request.headers.get('Referer'))

@app.route('/update', methods=['POST'])
def checkcomplete():
    allitems = get_items()
    for item in allitems:
        if request.form.get("updatecheck_" + str(item['id'])) != None and request.form.get("removecheck_" + str(item['id'])) != None:
            continue
        if request.form.get("updatecheck_" + str(item['id'])) != None:
            item['status'] = "Complete"
            save_item(item)
        if request.form.get("removecheck_" + str(item['id'])) != None:
            remove_item(item)
    return redirect(request.headers.get('Referer'))
   

if __name__ == '__main__':
    app.run()
