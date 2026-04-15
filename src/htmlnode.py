class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or self.props == "":
            return ""

        else:
            string = ""
            for k in self.props:
                string += f' {k}="{self.props[k]}"'
            return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    # def __str__(self):
    #     string = f"HTMLNode: \n Tag - {self.tag}\n Value - {self.value}\n"
    #     if(self.children is None):
    #         string = string + " Children - \n"
    #     else:
    #         for c in self.children:
    #             string += f" Children - {c}\n"
    #
    #     if(self.props is None):
    #         string = string + " Props - \n"
    #     else:
    #         for k, v in self.props.items():
    #             string += f" Props - {k}:{v}\n"
    #     return string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return f"{self.value}"

        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            string = f"<{self.tag}"
            for k, v in self.props.items():
                string += f' {k}="{v}"'
            string += f">{self.value}</{self.tag}>"
            return string

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag attribute found.")

        if self.children is None:
            raise ValueError("No children found on ParentNode.")

        if self.props is None:
            string = f"<{self.tag}>"
        else:
            string = f"<{self.tag}"
            for k, v in self.props.items():
                string += f' {k}="{v}"'
            string += f">{self.value}"

        for c in self.children:
            string += c.to_html()

        string += f"</{self.tag}>"
        return string
