#coding=utf-8
import tornado.web as web
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
from tornado.log import enable_pretty_logging
import motor
import os
import json
from bson import ObjectId

enable_pretty_logging()

client = AsyncHTTPClient()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class PoolHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):
        self.write('')
        self.finish()

    @gen.coroutine
    def get(self):
        resp_data = []
        cursor = db.user.find()
        cursor.sort([('id', -1)])
        for document in (yield cursor.to_list(length=999)):
            resp_data.append(document)
        self.write(JSONEncoder().encode(resp_data))
        self.finish()


class PlusOneHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):
        self.write('')
        self.finish()

    @gen.coroutine
    def get(self):
        life = yield db.life.find_one()
        newTime = life['timeRaised'] + 1
        life['timeRaised'] = newTime
        yield db.life.update({'id': 1}, {'$set': {'timeRaised': newTime}})
        self.write(JSONEncoder().encode(life))
        self.finish()


class RemoveHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):
        usr_data = json.loads(self.request.body)
        yield db.user.remove({'id': int(usr_data["id"]), 'mobile': int(usr_data["mobile"])})
        self.finish()

    @gen.coroutine
    def get(self):
        self.write('')
        self.finish()


class UploadHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):
        self.finish()
        usr_data = json.loads(self.request.body)
        print usr_data
        yield db.user.remove({'id': int(usr_data["id"])})
        yield db.follow.remove({'id': int(usr_data["id"])})


        if usr_data["followRing1"] is not None and int(usr_data["followRing1"]) > 0:
            follow_1 = str(int(usr_data["followRing1"]))
            yield db.follow.insert({'id': int(usr_data["id"]), 'follow': int(usr_data["followRing1"])})
        else:
            follow_1 = ''

        if usr_data["followRing2"] is not None and int(usr_data["followRing2"]) > 0:
            follow_2 = str(int(usr_data["followRing2"]))
            yield db.follow.insert({'id': int(usr_data["id"]), 'follow': int(usr_data["followRing2"])})
        else:
            follow_2 = ''

        if usr_data["followRing3"] is not None and int(usr_data["followRing3"]) > 0:
            follow_3 = str(int(usr_data["followRing3"]))
            yield db.follow.insert({'id': int(usr_data["id"]), 'follow': int(usr_data["followRing3"])})
        else:
            follow_3 = ''

        if usr_data["followRing4"] is not None and int(usr_data["followRing4"]) > 0:
            follow_4 = str(int(usr_data["followRing4"]))
            yield db.follow.insert({'id': int(usr_data["id"]), 'follow': int(usr_data["followRing4"])})
        else:
            follow_4 = ''

        if usr_data["followRing5"] is not None and int(usr_data["followRing5"]) > 0:
            follow_5 = str(int(usr_data["followRing5"]))
            yield db.follow.insert({'id': int(usr_data["id"]), 'follow': int(usr_data["followRing5"])})
        else:
            follow_5 = ''

        ad = ''
        if usr_data["ad"] is not None:
            ad = usr_data["ad"]

        yield db.user.insert({'id': int(usr_data["id"]), 'mobile': int(usr_data["mobile"]), 'ad': ad})


        sms_mobile = str(int(usr_data["mobile"]))
        sms_follow = follow_1 + '/' + follow_2 + '/' + follow_3 + '/' + follow_4 + '/' + follow_5
        visit_index = HTTPRequest(
            url="http://222.73.117.158/msg/HttpBatchSendSM?account=anhuidudai_kdys&pswd=Ustcring2016&mobile=" + sms_mobile + "&msg=【科大戒指】你成功关注了" + sms_follow + "号戒指&needstatus=true",
            method='GET',
            headers={'User-Agent': 'Firefox'}
        )
        yield gen.Task(client.fetch, visit_index)

        notice_users = []
        cursor = db.follow.find({'follow': int(usr_data["id"])})
        for document in (yield cursor.to_list(length=int(100))):
            notice_users.append(document)

        for user in notice_users:
            print user['id']
            user_info = yield db.user.find_one({'id': int(user['id'])})
            if user_info is not None and user_info['mobile'] is not None:
                sms_mobile = str(int(user_info["mobile"]))
                sms_id = str(usr_data["id"])
                visit_index = HTTPRequest(
                    url="http://222.73.117.158/msg/HttpBatchSendSM?account=anhuidudai_kdys&pswd=Ustcring2016&mobile=" + sms_mobile + "&msg=【科大戒指】有同学发布了" + sms_id + "号戒指&needstatus=true",
                    method='GET',
                    headers={'User-Agent': 'Firefox'}
                )
                yield gen.Task(client.fetch, visit_index)

    @gen.coroutine
    def get(self):
        self.write('')
        self.finish()


def make_app(static_path):
    return web.Application([
        (r"/pool", PoolHandler),
        (r"/upload", UploadHandler),
        (r"/remove", RemoveHandler),
        (r"/plus-one", PlusOneHandler),
        (r"/", web.RedirectHandler, {'url': 'index.html'}),
        (r"/(.*)", StaticFileHandler, {'path': static_path}),
    ], db=db)


if __name__ == "__main__":

    static_path = os.path.dirname(os.path.realpath(__file__)) + '/public'
    ip = '127.0.0.1'
    port = 8969

    dbclient = motor.MotorClient(ip, 27017)
    # database is ustcRing
    db = dbclient.ustcRing

    app = make_app(static_path)
    app.listen(port)
    IOLoop.instance().start()
