import uuid
from taranis import publish
from taranis.abstract import Factory, DomainEvent
import logging

logger = logging.getLogger(__name__)


class Respondent():
    class Created(DomainEvent):
        type = "Respondent.Created"

    class NewResponse(DomainEvent):
        type = "NewResponse.Created"

    def add_response(self, questions):
        event_id = str(uuid.uuid4())

        for question in questions:
            event = Respondent.NewResponse(id=event_id,
                                           question_id=question['id'],
                                           response_id=question['response'],
                                           aggregate_id=event_id)

            publish(event)


class RespondentFactory(Factory):
    """Respondent factory"""

    def build(self, data):
        logger.debug("Building new unit")

        event_id = str(uuid.uuid4())

        event = Respondent.Created(id=event_id,
                                   code=data['survey_code'],
                                   device_id=data['device_id'],
                                   aggregate_id=event_id)

        publish(event)

        var
        config = {"preload": "none", "src": [{
                                                 "src": "https://cfcdn1.lan.screen9.com/media/m/X/mXan6lKSoqb0EdBydy3HWA_auto_hls.ssl.m3u8?auth=NljKSazQ2sR23LjWaiPMnuPyIUp48A8JFJZiKlMAfJUr6vLelSGjpD1kZyRQqo3qUVtoGDmy00F_0gVJN4n4hg&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZmNkbjEubGFuLnNjcmVlbjkuY29tL21lZGlhL20vWC9tWGFuNmxLU29xYjBFZEJ5ZHkzSFdBX2F1dG9faGxzLnNzbC5tM3U4P2F1dGg9TmxqS1NhelEyc1IyM0xqV2FpUE1udVB5SVVwNDhBOEpGSlppS2xNQWZKVXI2dkxlbFNHanBEMWtaeVJRcW8zcVVWdG9HRG15MDBGXzBnVkpONG40aGciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjIxNDc0NzIwMDB9fX1dfQ__&Signature=kS8xNCZJSBdWOrfUneeBnbGgCMwStNvK1UGgh8fwYZZN3K0CRU6kmNea9NumqvzZRSSH3FX00ONlhlvNccwE5H1yS3q3oHXd3Kikwft5p-RkfIMnvAfFpiohE674qX4BHpkIOQghDEHnmSJciugKZL8eL~qcI8PPV~9pFQXYfsLxkgWganLFmy7e22vV4T3LclsEvZXo4gkCXXgT-QflZmI9k~~YHQ3HkVev959C0IUH0Z5wFZI7TrW615e2HNZAIs7CVxrTq2TK9-NyZKGAvRuXz1N8qxQLvXkcZ32w07uSFgsMWegq16xE8BiSp~HwWzszPeyh5-p6GMd9GVvGiw__&Key-Pair-Id=BBBBBBBBBBBBBBBBBBBB",
                                                 "type": "application/x-mpegURL"},
                                             {
                                                 "src": "https://cfcdn1.lan.screen9.com/media/m/X/mXan6lKSoqb0EdBydy3HWA_240p_h264h.mp4?auth=1RaAX2wiJId_ZMUy0h3sTjzVcXZkYcxC7jDtkchWLoNxVcMkRgKkgrNnEb88lH3tbYzkWMlA-uCw2clSfIhFKw&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZmNkbjEubGFuLnNjcmVlbjkuY29tL21lZGlhL20vWC9tWGFuNmxLU29xYjBFZEJ5ZHkzSFdBXzI0MHBfaDI2NGgubXA0P2F1dGg9MVJhQVgyd2lKSWRfWk1VeTBoM3NUanpWY1haa1ljeEM3akR0a2NoV0xvTnhWY01rUmdLa2dyTm5FYjg4bEgzdGJZemtXTWxBLXVDdzJjbFNmSWhGS3ciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjIxNDc0NzIwMDB9fX1dfQ__&Signature=CC67HChOp76l~qRV~SmPRDj7lSow5eGVL5FuYYfC4002GUxvRiuev~ir96gDRPaZ4316fMXRIWWNkFd1gq32F1zx0K0ZS~m45FCaQcyL7CyRW4wMe-G0mUrGHU4ixTSWnD~WQg0GGZae6DcQAt2QYAjbQjhu-Pg-kDXsde-yhJb4YYZQmD9W92hnR2UnEPErIutz8j6kX3fQmgodTn9jd1QII5c028E8fyc6fSdkYtgJyjmNOpkMgMsobNMSvNEdSEvXXU4U6HMvEBEQIbCkIqaVaxKdiABNBD2sMVfI-9FzxCJOD3Lcox13sKOg2FHm-pVyRpQ0RiNx20ibNTcGXg__&Key-Pair-Id=BBBBBBBBBBBBBBBBBBBB",
                                                 "type": "video/mp4"}],
                  "mediaid": "mXan6lKSoqb0EdBydy3HWA",
                  "containerid": "videoContainer",
                  "techOrder": ["chromecast", "html5"],
                  "poster": "https://sharetest1.lan.screen9.com/img/m/X/a/n/image_mXan6lKSoqb0EdBydy3HWA/2.jpg?v=0",
                  "fluid": true, "controls": true, "iframe": true,
                  "plugins": {"chromecast": {}, "airplay": {},
                              "chapters": {"cuepoints": []},
                              "title": {"description": "",
                                        "title": "Clip from videoplayback"}},
                  "aspectRatio": "4:3", "loop": false, "autoplay": false};

