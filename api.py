import helper

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = False

SUCCESS_STATUS_CODE = 200
NOT_FOUND_STATUS_CODE = 404
BAD_REQUEST_STATUS_CODE = 400


@app.route("/api/character/info", methods=["GET"])
def getCharacterInfo():
    # Check if name is present as a query parameter
    if "name" in request.args:
        name = request.args["name"]
        name_exists = helper.check_name_exists(name)
        if name_exists:
            character_dict = helper.get_character_info(name)
            return character_dict, SUCCESS_STATUS_CODE
        error = {
            "message": "No such name."
        }
        return error, NOT_FOUND_STATUS_CODE

    error = {
        "message": "Invalid request."
    }
    return error, BAD_REQUEST_STATUS_CODE


@app.route("/api/character/main", methods=["GET"])
def getMainCharacters():
    main_characters_list = helper.get_main_characters()
    return jsonify(main_characters_list), SUCCESS_STATUS_CODE


@app.route("/api/character/support", methods=["GET"])
def getSupportCharacters():
    support_characters_list = helper.get_support_characters()
    return jsonify(support_characters_list), SUCCESS_STATUS_CODE


@app.route("/api/character/episode", methods=["GET"])
def getEpisodeCharacters():
    episode_characters_list = helper.get_episode_characters()
    return jsonify(episode_characters_list), SUCCESS_STATUS_CODE


@app.route("/api/character/mentions", methods=["GET"])
def getCharacterMentions():
    list_characters = []
    if "name" in request.args:
        name = request.args["name"]
        name_exists = helper.check_name_exists(name)
        if name_exists:
            list_characters = helper.get_character_mentions(name=name)
            return jsonify(list_characters), SUCCESS_STATUS_CODE
        error = {
            "message": "No such name."
        }
        return error, NOT_FOUND_STATUS_CODE

    list_characters = helper.get_character_mentions()
    return jsonify(list_characters), SUCCESS_STATUS_CODE


@app.route("/api/character/comentions", methods=["GET"])
def getCharacterCoMentions():
    if "name_a" and "name_b" in request.args:
        name_a = request.args["name_a"]
        name_b = request.args["name_b"]
        name_a_exists = helper.check_name_exists(name_a)
        name_b_exists = helper.check_name_exists(name_b)
        if name_a_exists and name_b_exists:
            list_co_mentions = helper.get_characters_co_mentions(name_a, name_b)
            return jsonify(list_co_mentions), SUCCESS_STATUS_CODE
        error = {
            "message": "No such name."
        }
        return error, NOT_FOUND_STATUS_CODE
    error = {
        "message": "Invalid request."
    }
    return error, BAD_REQUEST_STATUS_CODE


@app.route("/api/book/info", methods=["GET"])
def getBookInformation():
    if "isbn" in request.args:
        isbn = request.args["isbn"]
        info_dict = helper.get_book_info_from_ISBN(isbn)

        # If there is no such book
        if not info_dict:
            error = {
                "message": "No such book."
            }
            return error, NOT_FOUND_STATUS_CODE

        return info_dict, SUCCESS_STATUS_CODE

    error = {
        "message": "Invalid request."
    }
    return error, BAD_REQUEST_STATUS_CODE


app.run()
