import os
import traceback
from tornado import httpserver
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, HTTPError
from tornado.options import define, options
import uuid
import json
from os.path import splitext
# from ai_tutor.get_triples import QuestionGenerator
# from ai_tutor.sentence_selector import SentenceSelection
# from ai_tutor.mind_map import main_concept, GraphBuilder

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
            self.write(json.dumps({
                        'error': flag,
                        'message': self._reason,
                        'traceback': lines
                }))
        else:
            self.write(json.dumps({
                    'error': flag,
                    'message': self._reason
                }))

class fourHandler(RequestHandler):
    def get(self):
        self.render("four.html")


class uploadHandler(RequestHandler):
    def get(self):
        self.render("upload.html")


class MLHandler(RequestHandler):

    @staticmethod
    def upload(fileinfo):
        fname = fileinfo['filename']
        extn = splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        absolute_path = os.path.join(os.path.dirname(__file__), __UPLOADS__ + cname)
        print(absolute_path)
        try:
            fh = open(absolute_path, 'wb')
        except FileNotFoundError:
            os.makedirs('uploads') 
            fh = open(absolute_path, 'wb')
        fh.write(fileinfo['body'])
        fh.close()
        try:
            with open(absolute_path, 'wb') as f:
                f.close()
        except FileNotFoundError:
            return {
                "error": True,
                "message": "there was an error"
            }
        return {"error": False, "message": "File Sucessfully Uploaded", "file_loc": __UPLOADS__ + cname}

    # def post(self):
        # response = self.upload(fileinfo=self.request.files['thefile'][0])
        # if response['error'] == False:
        #     document = response['file_loc']
        #     qgen = QuestionGenerator()
        #     ratio = 0.4
        #     ss = SentenceSelection(ratio=ratio)
        #     sentences = ss.prepare_sentences(document)
        #     sents = sentences.values()[:]
        #     questions = qgen.generate_questions(sents)
        #     mc = main_concept(sents)
        #     G = GraphBuilder(mc=mc)
        #     self.render("answer", questions=questions)


    def get(self):
        self.render('index.html')




if __name__ == "__main__":
    print("listening on port "+str(options.port))
    options.parse_command_line()
    settings = {
        "debug": True,
        "cookie_secret": "LPBDqiL4S8KGi54y5eXFLoSiKE+wz0vajAU6K9aZOJ4="
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
