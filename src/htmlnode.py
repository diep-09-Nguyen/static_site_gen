class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    # children to override
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        return (
            "".join(f' {key}="{value}"' for key, value in self.props.items())
            if self.props
            else ""
        )

    def __eq__(self, other) -> bool:
        if not (isinstance(other, HTMLNode)):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict | None = None,
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Expects a value")

        return (
            f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            if self.tag
            else self.value
        )


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode expects a tag")
        if not self.children:
            raise ValueError("ParentNode expects children")
        string = f"<{self.tag}>"
        for child in self.children:
            string += f"{child.to_html()}"
        string += f"</{self.tag}>"
        return string
