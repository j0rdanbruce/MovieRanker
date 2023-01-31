from marshmallow import Schema, fields

class PlainMovieSchema(Schema):
    title = fields.Str(required=True)
    plot = fields.Str(required=True)
    id = fields.Int(required=True)
    img_src = fields.Str(required=True)
    #director = fields.Str(required=True)
    

'''class MovieSchema(PlainMovieSchema):
    movies = fields.List(fields.Nested(PlainMovieSchema(dump_only=True)))'''

'''class MovieSchemaList(PlainMovieSchema):
    '''