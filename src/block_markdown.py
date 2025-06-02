from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    
    block_strings = markdown.split("\n\n")

    block_strings = list(map(str.strip, block_strings))
    
    block_strings = [block_string for block_string in block_strings if block_string != ""]
    
    return block_strings
    

def block_to_block_type(block:str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("-"):
        for line in lines:
            if not line.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1."):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}."):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
        
    return ParentNode("div", children, None)
        
        
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise Exception("invalid block type")
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise Exception("invalid code block format")
    text_block = block[4 : -3]
    raw_text_node = TextNode(text_block, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])
    

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char =="#":
            level += 1
        else:
            break
    text = block[level+1 : ]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for list_item in items:
        stripped_list_item = list_item[3:]
        
        text_node_item = text_to_children(stripped_list_item)
        html_items.append(ParentNode("li", text_node_item))
    
    
    return ParentNode("ol", html_items)    

def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for list_item in items:
        stripped_list_item = list_item[2:]
        
        text_node_item = text_to_children(stripped_list_item)
        html_items.append(ParentNode("li", text_node_item))
    
    
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise Exception("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    joined_lines = " ".join(new_lines)
    children = text_to_children(joined_lines)
    return ParentNode("blockquote", children)

