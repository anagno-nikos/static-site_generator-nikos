from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):

    new_nodes = []
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = []
        sections = old_node.text.split(delimiter)
        

        if len(sections) % 2 == 0:
            raise Exception(f"invalid Markdown syntax, {delimiter} not suitable for {text_type.name}: {text_type.value}")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    regex_list = re.findall(r'\!\[(.*?)\]\((.*?)\)', text)    
    return regex_list


def extract_markdown_links(text):
    regex_list = re.findall(r'\[(.*?)\]\((.*?)\)', text)
    return regex_list


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        # ignore old node in the list that are not of TEXT text type
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)

        # ignore old node in the list if it doesn't contain any valid links and add it as is
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        # split the section for each link. 
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise Exception("non valid link found in the text")

            # if 1st link is in the beginning, bypass this if and create the link textnode
            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0],
                        TextType.TEXT
                    )
                )
            # create the link text node irrespective of the before and after text
            new_nodes.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            # get the remaining text, after the split link, and loop
            original_text = sections[1]
        
        #check last section after loop, can be empty if last link in at the end of the text
        if original_text != "":
            new_nodes.append(
                TextNode(
                    original_text,
                    TextType.TEXT
                )
            )

    return new_nodes
    
def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        # ignore old node in the list that are not of TEXT text type
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)

        # ignore old node in the list if it doesn't contain any valid images and add it as is
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        # split the section for each image. 
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise Exception("non valid image found in the text")

            # if 1st image is in the beginning, bypass this if and create the image textnode
            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0],
                        TextType.TEXT
                    )
                )
            # create the image text node irrespective of the before and after text
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            # get the remaining text, after the split image, and loop
            original_text = sections[1]
        
        #check last section after loop, can be empty if last image in at the end of the text
        if original_text != "":
            new_nodes.append(
                TextNode(
                    original_text,
                    TextType.TEXT
                )
            )

    return new_nodes


def text_to_textnodes(text):
    old_node_tmp = TextNode(text, TextType.TEXT)
    new_node = []
    new_node = split_nodes_image([old_node_tmp])
    new_node = split_nodes_link(new_node)
    new_node = split_nodes_delimiter(new_node, "**", TextType.BOLD)
    new_node = split_nodes_delimiter(new_node, "_", TextType.ITALIC)
    new_node = split_nodes_delimiter(new_node, "`", TextType.CODE)
    
    
    return new_node
