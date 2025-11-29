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
            for index in range(len(delimited_text)):
                if delimited_text[index] == "":
                    continue
                if index % 2 != 0:
                    new_nodes.append(TextNode(delimited_text[index], text_type))
                else:
                    new_nodes.append(TextNode(delimited_text[index], TextType.TEXT))
    return new_nodes
# main()