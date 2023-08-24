from marshmallow import Schema, fields

class PlainMovieSchema(Schema):
    title = fields.Str(required=True)
    plot = fields.Str(required=True)
    id = fields.Int(required=True)
    img_src = fields.Str(required=True)
    #director = fields.Str(required=True)
    

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)