

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not isinstance(self.props, dict) or self.props == {}:
            return ""

        html_props = ""
        for prop in self.props:
            html_props += f" {prop}=\"{self.props[prop]}\""
        return html_props
    
    def __eq__(self, other):
        if (self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props):
            return True
        return False

    def __repr__(self):
        return f"\nHTMLNode(\ntag = {self.tag}\nvalue = {self.value}\nchildren = {self.children}\nprops = {self.props})"