# Flask imports
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap

# Forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# NLP
import spacy
from spacy import displacy

# General
import json

# app
from tddner.ner_client import NamedEntityClient

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)

nlp = spacy.load("en_core_web_sm")
ner_client = NamedEntityClient(nlp, displacy)


class NerForm(FlaskForm):
    ner_sentence = StringField(
        id="input-text",
        render_kw={"class": "form-control", "data-test-id": "input-text"},
        validators=[DataRequired()],
    )

    ner_submit = SubmitField(
        label="Find Named Entities",
        id="find-button",
        render_kw={
            "class": "btn btn-outline-primary btn-block",
            "data-test-id": "find-button",
        },
    )


@app.route("/", methods=["GET", "POST"])
def index():
    form = NerForm()
    if form.validate_on_submit():
        pass
    return render_template("index.j2", form=form)


@app.route("/ner", methods=["POST"])
def get_named_ents():
    data = request.get_json()
    result = ner_client.get_ents(data["sentence"])
    response = {"entities": result.get("ents"), "html": result.get("html")}
    return json.dumps(response)


if __name__ == "__main__":
    app.run(debug=True)
