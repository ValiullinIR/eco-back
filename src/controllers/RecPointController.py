import json
from flask import request, jsonify
from flask_restful import Resource, reqparse
import src.models.RecPointModel as RecPoint
from ast import literal_eval
from bson import ObjectId
from pprint import pprint

parser = reqparse.RequestParser()

class RecPointController(Resource):
    """RecPointController [summary]
        Path: */api/rec_points*
    Arguments:
        Resource {[type]} -- [description]
    """

    # def get(self):
    #     """[GET]

    #     Returns:
    #         `[
    #             {
    #                 _id: {
    #                     $oid: string
    #                 },
    #                 name: string,
    #                 var_name: string,
    #                 image: string
    #             },
    #             ...
    #         ]`
    #     """

    def get(self):
        """[GET]
                ...
        :return
    [
    {
        "_id": "5fff7f15e2e6656197a4d036",
        "accept_types": [
            {
                "_id": "5ffc873e883d492d54ead8f3",
                "key_words": [
                    "Стеклянные бутылки",
                    "Оконные стекла"
                ],
                "name": "Стекло",
                "var_name": "FILTER"
            },
            {
                "_id": "5ff8de6ca2443b0828e04115",
                "key_words": [],
                "name": "second filter",
                "var_name": "FILTER"
            }
        ],
        "address": "г. Казань, ул.Большая Красная, 22",
        "contacts": "",
        "coords": {
            "lat": 49.286027,
            "lon": 55.665665
        },
        "description": "",
        "getBonus": true,
        "name": "six",
        "partner": {
            "_id": "5ff8c19ff6d94774d2309734",
            "name": "filter",
            "points": []
        },
        "photo_path": "",
        "reception_target": {
            "_id": "5fff4852786f93d19a5412bc",
            "name": "Переработка"
        },
        "reception_type": {
            "_id": "5fff48a3786f93d19a5412be",
            "name": "Платный прием"
        },
        "work_time": {
            "ВТ": {
                "1": "8:00-12:00",
                "2": "13:00-18:00"
            },
            "ПН": {
                "1": "8:00-12:00",
                "2": "13:00-18:00"
            }
        }
    },
    ]
        """
        args = request.args.to_dict()
        print(args)

        if "id" in args:
            rec_point = RecPoint.find_by_id(args['id'])
            if not rec_point:
                return {"message": "RecPoint not found id={}".format(args['id'])}, 404
            return rec_point.to_jsony()
        elif "coords" in args:
            coords = literal_eval(args["coords"])
            rec_points = RecPoint.read(coords)
            return jsonify([i.to_jsony() for i in rec_points])
        else:
            rec_points = RecPoint.read()
            return jsonify([i.to_jsony() for i in rec_points])

    def post(self):
        """[POST]
        That request body template

        Returns:
            {
            "name": "one",
            "address": "г. Казань, ул.Большая Красная, 22",
            "partner": "5ff8c19ff6d94774d2309734",
            "accept_types": [
            "5ff8b5e658bdaf20f718f2d1",
            "5ff8de6ca2443b0828e04115"
            ],
            "description": "",
            "reception_target": "5fff4852786f93d19a5412bc",
            "reception_type": "5fff48a3786f93d19a5412be",
            "getBonus": 1,
            "photo_path": "",
            "contacts": "",
            "work_time": {
                "ПН": {
                    "1": "8:00-12:00",
                    "2": "13:00-18:00"
                },
                "ВТ": {
                    "1": "8:00-12:00",
                    "2": "13:00-18:00"
                    }
                },
            "coords": {
                "lat": 49.286027,
                "lon": 55.665665
                    }
            }
            `
        """
    
        __rec_point = request.form.to_dict()


        if "work_time" in __rec_point:
            print("ok")
            print(__rec_point)
            _w_t = literal_eval(__rec_point["work_time"])
            w_t = _w_t
            __rec_point["work_time"] = w_t
        
        if "accept_types" in __rec_point:
            __rec_point["accept_types"] = literal_eval(__rec_point["accept_types"])
        if "coords" in __rec_point:
            __rec_point["coords"] = literal_eval(__rec_point["coords"])

        _rec_point = __rec_point
        print(_rec_point)
        # partner

        # if 'partner_id' in _rec_point:
        #     partner = Partner.objects(id=_rec_point['partner_id']).first()
        #     if not partner:
        #         return {"message": "Filter not found id={}"}, 404
        rec_point = RecPoint.create(_rec_point).to_jsony()
        return rec_point

    def put(self):
        """[PUT]
        Returns:
            [type] -- [description]
        """

        updates = request.json
        args = request.args.to_dict()

        updates = to_document_type(updates)

        rec_point = RecPoint.update(args['id'], updates)
        if not rec_point:
            return {"message": "RecPoint not found id={}".format(args['id'])}, 404

        return rec_point.to_jsony()

    def delete(self):

        args = request.args.to_dict()

        if "id" not in args:
            return {"message": "Not passed query parameter id"}, 403

        rec_point = RecPoint.delete(args['id'])
        if not bool(rec_point):
            return {"message": "RecPoint not found id={}".format(args['id'])}, 404
        return rec_point.to_jsony()



def to_document_type(updates: dict):
    '''
    Method to convert JSON object to RecPoint type

    :param updates:
    :return:
        dict : updated rec_point
    '''
    if 'partner' in updates:
        updates['partner'] = ObjectId(updates['partner'])

    if 'reception_target' in updates:
        updates['reception_target'] = ObjectId(updates['reception_target'])

    if 'reception_type' in updates:
        updates['reception_type'] = ObjectId(updates['reception_type'])

    if 'getBonus' in updates:
        updates['getBonus'] = bool(updates['getBonus'])

    if "accept_types" in updates:
        for i in range(len(updates['accept_types'])):
            updates['accept_types'][i] = ObjectId(updates['accept_types'][i])
    return updates