class HTMLNode:
    def __init__(
        self,
        tag=None,  # str
        value=None,  # str
        children=None,  # list
        props=None,  # dict
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # children to override
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        dicy = self.props
        string: str = ""

        if not dicy:
            return string

        return "".join(f' {key}="{value}"' for key, value in dicy.items())
        # for key in self.props:
        #     string += f" {key} {self.props[key]}"
        # return string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError

        string = self.value
        if self.tag:
            string = f"<{self.tag}{self.props_to_html()}>{string}</{self.tag}>"
        return string
