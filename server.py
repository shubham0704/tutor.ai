import os
import traceback
from tornado import httpserver
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, HTTPError
from tornado.options import define, options
import uuid
import json
from os.path import splitext
from ai_tutor.get_triples import QuestionGenerator
from ai_tutor.sentence_selector import SentenceSelection
from ai_tutor.mind_map import main_concept, GraphBuilder
from tornado.gen import coroutine

__UPLOADS__ = "uploads/"
define("port", default=8080, help="runs on the given port", type=int)


class MyAppException(HTTPError):
    pass


class BaseHandler(RequestHandler):

    def write_error(self, flag, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self.render("500.html", data={'error': flag, 'message': self._reason, 'traceback': lines})
        else:
            self.render("500.html", data={'error': flag, 'message': self._reason, 'traceback': None})

class fourHandler(RequestHandler):
    def get(self):
        self.render("four.html")


class uploadHandler(RequestHandler):
    def get(self):
        self.render("upload.html")


class MLHandler(BaseHandler):

    @staticmethod
    def upload(fileinfo):
        fname = fileinfo['filename']
        extn = splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        absolute_path = os.path.join(os.path.dirname(__file__), __UPLOADS__ + cname)
        print(absolute_path)
        try:
            fh = open(absolute_path, 'wb')
        except Exception as e:
            os.makedirs('uploads')
            fh = open(absolute_path, 'wb')
        fh.write(fileinfo['body'])
        fh.close()
        try:
            with open(absolute_path, 'rb') as f:
                f.read()
        except Exception as e:
            print (e)
            return {
                "error": True,
                "message": "there was an error"
            }
        return {"error": False, "message": "File Sucessfully Uploaded", "file_loc": __UPLOADS__ + cname}

    @coroutine
    def post(self):
        response = self.upload(fileinfo=self.request.files['thefile'][0])
        print(response)
        if response['error'] == False:
            document = os.path.join(os.path.dirname(__file__),response['file_loc'])
            qgen = QuestionGenerator()
            ratio = 0.4
            ss = SentenceSelection(ratio=ratio)
            sentences = ss.prepare_sentences(document)
            sents = list(sentences.values())[:]
            print("sents here ",sents)
            questions, answers = qgen.generate_questions(sents)
            print(questions, " ",answers)
            mc = main_concept(sents)
            G =  GraphBuilder(mc=mc)
            try:
                yield G.gen_giant_graph(sents)
                js = G.get_json()
                js = json.dumps(js)
                print ("LOGS question length", len(questions))
                self.render("graph.html", questions=questions, answers=answers, jsonZ=js)
            except:
                js = G.get_json()
                js = json.dumps(js)
                print ("LOGS question length",len(questions))
                self.render("graph.html", questions=questions, answers=answers, jsonZ=js)

    def get(self):
        self.render('index.html')

class myfourHandler(BaseHandler):
    def get(self):
        self.render("404.html")


if __name__ == "__main__":
    print("listening on port "+str(options.port))
    options.parse_command_line()
    settings = {
        "debug": True,
        "cookie_secret": "LPBDqiL4S8KGi54y5eXFLoSiKE+wz0vajAU6K9aZOJ4=",
        "default_handler_class": myfourHandler
    }
    app = Application(handlers=[
        (r"/", MLHandler),
        (r"/upload", uploadHandler),
        (r"/four", fourHandler)
    ],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        **settings
    )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(os.environ.get("PORT", options.port))
    IOLoop.instance().start()
