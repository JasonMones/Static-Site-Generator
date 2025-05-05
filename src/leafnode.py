from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if self.value == None:
            raise ValueError("Leaf Node must have a value")
        
    def to_html(self):
        
        
        if self.tag == None:
            return self.value #raw text
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" #<tag props>value</tag>