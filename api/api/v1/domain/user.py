import colander


class RoleList(colander.SequenceSchema):
    role = colander.SchemaNode(colander.String())


class User(colander.MappingSchema):
    username = colander.SchemaNode(colander.String())
    password = colander.SchemaNode(colander.String())
    roles = RoleList()
    token = colander.SchemaNode(colander.String(), missing=colander.drop)
