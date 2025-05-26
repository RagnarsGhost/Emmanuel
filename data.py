class VariableNotDefinedError(Exception):
    pass


class Data:
    def __init__(self):
        self.variables = {}

    def _get_name(self, identifier):
        return identifier.value if hasattr(identifier, 'value') else identifier

    def read(self, identifier):
        name = self._get_name(identifier)
        if name in self.variables:
            return self.variables[name]
        raise VariableNotDefinedError(f"Variable '{name}' not defined")

    def write(self, identifier, value):
        name = self._get_name(identifier)
        self.variables[name] = value

    def exists(self, identifier):
        name = self._get_name(identifier)
        return name in self.variables

    def __getitem__(self, name):
        return self.variables[name]

    def __setitem__(self, name, value):
        self.variables[name] = value

    def __contains__(self, name):
        return name in self.variables

    def delete(self, identifier):
        name = self._get_name(identifier)
        if name in self.variables:
            del self.variables[name]
        else:
            raise VariableNotDefinedError(f"Variable '{name}' not defined, cannot delete")

    def all(self):
        return self.variables
