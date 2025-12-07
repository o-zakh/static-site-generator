import re

from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    textnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(textnode)

def text_node_to_html_node(text_node):
    try:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        if text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        if text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        if text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}) # value remains None, ask Boots
    except Exception:
        ("ERROR: Incorrect TextNode type")

def split_nodes_delimiter(old_nodes, delimiter, text_type): #splits list of nodes on text nodes with specific types
    new_nodes = []
    delimited_text = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            delimited_text = node.text.split(delimiter)
            if len(delimited_text) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            for i, phrase in enumerate(delimited_text):
                if phrase == "":
                    continue
                if i % 2 != 0:
                    new_nodes.append(TextNode(phrase, text_type))
                else:
                    new_nodes.append(TextNode(phrase, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    alt_link_text = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return alt_link_text

def extract_markdown_links(text):
    anchor_link_text = re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return anchor_link_text

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_links = extract_markdown_images(node.text)
            text_lines = []
            for i in range(len(extracted_links)+1):
                texttype_text = ""
                start = 0
                if i == len(extracted_links):
                    end = len(node.text)
                else:
                    end = node.text.index(f'![{extracted_links[i][0]}]')
                if i != 0:
                    start = node.text.index(f'({extracted_links[i-1][1]})') + len(extracted_links[i-1][1]) + 2 # start from the last link
                texttype_text += node.text[start:end]
                text_lines.append(texttype_text)
            for i, phrase in enumerate(text_lines):
                if phrase != "":
                    new_nodes.append(TextNode(phrase, TextType.TEXT))
                if i != len(text_lines)-1:
                    new_nodes.append(TextNode(extracted_links[i][0], TextType.IMAGE, extracted_links[i][1]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_links = extract_markdown_links(node.text)
            text_lines = []
            for i in range(len(extracted_links)+1):
                texttype_text = ""
                start = 0
                if i == len(extracted_links):
                    end = len(node.text)
                else:
                    end = node.text.index(f'[{extracted_links[i][0]}]')
                if i != 0:
                    start = node.text.index(f'({extracted_links[i-1][1]})') + len(extracted_links[i-1][1]) + 2 # start from the last link
                texttype_text += node.text[start:end]
                text_lines.append(texttype_text)
            for i, phrase in enumerate(text_lines):
                if phrase != "":
                    new_nodes.append(TextNode(phrase, TextType.TEXT))
                if i != len(text_lines)-1:
                    new_nodes.append(TextNode(extracted_links[i][0], TextType.LINK, extracted_links[i][1]))
    return new_nodes            
    
def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    output_node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
    output_node_list = split_nodes_delimiter(output_node_list, "_", TextType.ITALIC)
    output_node_list = split_nodes_delimiter(output_node_list, "`", TextType.CODE)
    output_node_list = split_nodes_image(output_node_list)
    output_node_list = split_nodes_link(output_node_list)
    return output_node_list

def markdown_to_blocks(markdown):
    initial_block_strings_list = []
    initial_block_strings_list = markdown.split("\n\n")
    final_block_list = []
    for block in initial_block_strings_list:
        if "\n" in block:
            list_of_lines = []
            for line in block.split("\n"):
                line = line.strip()
                list_of_lines.append(line)
            block = "\n".join(list_of_lines)
        block = block.strip()
        final_block_list.append(block)
    return final_block_list


# main()