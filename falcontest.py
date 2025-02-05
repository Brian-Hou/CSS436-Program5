import falcon

class QuoteResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = [
            'quote', (
                "I've always been more interested in ",
                "the future than in the past."
            ),
            'author', 'Grace Hopper'
        ]

        resp.media = quote


application = falcon.API()
application.add_route('/quote', QuoteResource())