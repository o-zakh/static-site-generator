class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        complete_string = ''
        if self.props:
            for key, value in self.props.items():
                complete_string += f' {key}="{value}"'
        return complete_string
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
                
    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('ValueError: No "tag" value assigned')
        if not self.children:
            raise ValueError('ValueError: No "children" value assigned')
        result_string = ''
        for child in self.children:
            result_string += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{result_string}</{self.tag}>'