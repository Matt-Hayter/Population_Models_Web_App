from biological_models_app import db
from flask import jsonify, request, Blueprint

pred_prey = Blueprint("pred_prey", __name__)

@pred_prey.route("/PredPrey/AlterPresets", methods=["POST"])
def add_PredPrey_preset():
    response = {"server status": "success"}
    preset = request.get_json() #Retrieve payload from client
    if request.method == "POST": #Adding a preset
        #First get id of user with active email
        query = "SELECT id FROM users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (preset.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        presetData = preset.get("presetData")
        #Now insert preset into presets table, with the correct Foreign key
        query = "INSERT INTO pred_prey_presets (owner_id, preset_name, N0, a, b, P0, c, d, date) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
        cursor.execute(query, (activeid, preset.get("presetName"), presetData[0], presetData[1],
            presetData[2], presetData[3], presetData[4], presetData[5]))
        cursor.close()
        db.commit()
        response["message"] = "Added PredPrey preset"
    return jsonify(response)

@pred_prey.route("/PredPrey/AlterPresets/<preset_id>", methods=["DELETE"])
def delete_PredPrey_preset(preset_id):
    response = {"server status": "success"}
    if request.method == "DELETE":
        query = "DELETE FROM pred_prey_presets WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(query, (int(preset_id),))
        cursor.close()
        db.commit()
        response["message"] = "Deleted PredPrey preset"
    return jsonify(response)

@pred_prey.route("/PredPrey/AllPresets", methods=["POST"])
def all_PredPrey_presets():
    response = {"server status": "success"}
    post_data = request.get_json()
    if request.method == "POST": #Grab user's presets
        #First get user id, given email
        query = "SELECT id FROM users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (post_data.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        #Now grab all pred prey presets for that user
        query = "SELECT id, preset_name, date FROM pred_prey_presets WHERE owner_id = %s"
        cursor.execute(query, (activeid,))
        response["presets"] = cursor.fetchall()
        cursor.close()
        response["message"] = "Grabbed all of user's pred-prey presets"
    return jsonify(response)

@pred_prey.route("/PredPrey/PresetParams/<preset_id>", methods=["GET"])
def PredPrey_preset_params(preset_id):
    response = {"server status": "success"}
    if request.method == "GET":
        #Grab data for requested preset
        query = "SELECT N0, a, b, P0, c, d FROM pred_prey_presets WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(query, (preset_id,))
        response["preset_params"] = cursor.fetchone()
        cursor.close()
        response["message"] = "Grabbed data for selected pred prey preset"
    return jsonify(response)