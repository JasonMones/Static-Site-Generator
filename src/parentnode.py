from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if self.tag == None:
            raise ValueError("tag is required for parent node")
        
        if self.children == None:
            raise ValueError("children are required for parent node")
        
        if not isinstance(self.children, list):
            raise TypeError("paramater 'children' must be a list")
        
        self.children = list(filter(lambda node: isinstance(node, HTMLNode), self.children))
        if self.children == []:
            raise ValueError("children(HTMLNode) are required for parent node")

    def to_html(self):
        html = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            html += node.to_html()

        return f"{html}</{self.tag}>"
