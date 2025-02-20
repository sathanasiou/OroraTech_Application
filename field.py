class Field:
    def __init__(self, name, type, alias, sqlType, domain, defaultValue, length=None):
        self.name = name
        self.type = type
        self.alias = alias
        self.sqlType = sqlType
        self.domain = domain
        self.defaultValue = defaultValue
        self.length = length