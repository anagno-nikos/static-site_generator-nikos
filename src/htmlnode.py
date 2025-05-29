class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")

        if self.tag is None:
            return self.value
        
        html_rendered = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_rendered
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing from ParentNode")
        
        if self.children is None:
            raise ValueError("a LeafNode must always have at least one children HTMLNode. Maybe you need a LeafNode or you did not specify the children nodes")

        html_rendered = f"<{self.tag}>"
        for child_node in self.children:
            
            html_rendered += child_node.to_html()

        html_rendered += f"</{self.tag}>"
        
        return html_rendered