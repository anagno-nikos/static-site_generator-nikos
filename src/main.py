from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import *


textnode = TextNode(
    "This is some anchor text",
    TextType.LINK,
    "https://www.boot.dev"
)

print(textnode)


htmlnode = HTMLNode(
    tag = "h1",
    value = "this is a demo text for this </h1> paragraph",
    props = {
        "href": "https://www.google.com"
    }
)

print(htmlnode)

print(htmlnode.props_to_html())


grandchild_node = LeafNode("b", "grandchild")
child_node = ParentNode("span", [grandchild_node])
parent_node = ParentNode("div", [child_node])

print(parent_node)
print(child_node)
print(grandchild_node)