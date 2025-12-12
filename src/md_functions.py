import re

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from blocktype import BlockType

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
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
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

def block_to_block_type(markdown_text_block: str) -> BlockType:
    if re.search(r'(?<!.)#{1,6}\s', markdown_text_block):
        return BlockType.heading
    elif re.search(r'^```.*```$', markdown_text_block, re.DOTALL):
        return BlockType.code
    lines = markdown_text_block.splitlines()
    if lines and all(line.startswith('>') or line.strip() == "" for line in lines):
        return BlockType.quote
    if lines and all(line.startswith('- ') or line.strip() == "" for line in lines):
        return BlockType.unordered_list
    for i, line in enumerate(lines):
        if not re.search(fr'^{i+1}\.\s', line):
            break
        if i == len(lines)-1:
            if re.search(fr'^{i+1}\.\s', line):
                return BlockType.ordered_list
    return BlockType.paragraph

def blocktype_to_html_node(blocktype, heading_type=None, block=None):
    if blocktype.name == "paragraph":
        return ParentNode('p', [])
    if blocktype.name == "heading":
        return ParentNode(f'h{heading_type}', [])
    if blocktype.name == "code":
        raise Exception ("ERROR: blocktype.name == 'code'")
    if blocktype.name == "quote":
        return ParentNode('blockquote', [])
    if blocktype.name == "unordered_list":
        return ParentNode('ul', items_in_lists(block))
    if blocktype.name == "ordered_list":
        return ParentNode('ol', items_in_lists(block))
    raise Exception ("ERROR: blocktype is invalid")

def codeblock_to_leafnode(block):
    textlines_list = block.splitlines()
    for i, line in enumerate(textlines_list):
        if (
            line == "```"
        ):
            textlines_list[i] = ""
    return "\n".join(textlines_list)

def items_in_lists(block):
    list_of_items = block.splitlines()
    leafnode_list = []
    for item in list_of_items:
        # print(f'>item is {item}')
        textnodes_in_line = text_to_textnodes(item[item.find(" ")+1:])
        # print(f'>>textnodes_in_line is {textnodes_in_line}')
        
        # Check for inline text formatting
        if (
            len(textnodes_in_line) > 1 or
            textnodes_in_line[0].text_type != TextType.TEXT
        ):
            list_children = []
            for textnode in textnodes_in_line:
                # print(f">>>textnode is {textnode}")
                htmlnode = text_node_to_html_node(textnode)
                # print(f'>>>>htmlnode is {htmlnode}')
                list_children.append(htmlnode)
            leafnode_list.append(ParentNode('li', list_children))
        
        # Simple paragraph string in line
        else:
            leafnode_list.append(LeafNode('li', item[item.find(" ")+1:]))
    return leafnode_list

def markdown_to_html_node(markdown):

    # Split the markdown into blocks
    blocks_list = markdown_to_blocks(markdown)
    parentnode_list = []
    for block in blocks_list:
        if block == "":
            continue

        # Determine the type of block
        blocktype = block_to_block_type(block)
        
        # Unique branch for code blocks
        if blocktype.name == "code":
            leaf_codenode = LeafNode("code", codeblock_to_leafnode(block))
            parent_codenode = ParentNode("pre", [leaf_codenode])
            parentnode_list.append(parent_codenode)
            continue
        
        # Heading number counter, ex. h1, h2, h3
        heading_type = None
        if blocktype.name == "heading":
            heading_type = 0
            while block[heading_type] == "#":
                heading_type += 1
            if (
                heading_type == 0 or
                heading_type == 7
            ):
                raise Exception ("incorrect heading_type")
            block = block.lstrip("# ")
            
        # Unique branch for list blocks (ul, ol)
        if (
            blocktype.name == "ordered_list" or
            blocktype.name == "unordered_list"
        ):
            parentnode = blocktype_to_html_node(blocktype, heading_type, block)
            parentnode_list.append(parentnode)
            continue

        # Based on the type of block, create a new HTMLNode with the proper data
        parentnode = blocktype_to_html_node(blocktype, heading_type)
        block_text_for_inlines = block
        if blocktype.name == "paragraph":
            block_text_for_inlines = block.replace("\n", " ")
        if blocktype.name == "quote":
            block_text_for_inlines = block.replace("> ", "")

        textnodes = text_to_textnodes(block_text_for_inlines)
        for textnode in textnodes:

            # TextNode -> HTMLNode
            htmlnode = text_node_to_html_node(textnode)
            parentnode.children.append(htmlnode)
        parentnode_list.append(parentnode)
    div_parentnode = ParentNode('div',parentnode_list)

    return div_parentnode

