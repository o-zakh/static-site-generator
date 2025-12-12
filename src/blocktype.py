from enum import Enum
import re

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

# The code below previously was here:

# def block_to_block_type(markdown_text_block: str) -> BlockType:
#     if re.search(r'(?<!.)#{1,6}\s', markdown_text_block):
#         return BlockType.heading
#     elif re.search(r'^```.*```$', markdown_text_block, re.DOTALL):
#         return BlockType.code
#     lines = markdown_text_block.splitlines()
#     if lines and all(line.startswith('>') or line.strip() == "" for line in lines):
#         return BlockType.quote
#     if lines and all(line.startswith('- ') or line.strip() == "" for line in lines):
#         return BlockType.unordered_list
#     for i, line in enumerate(lines):
#         if not re.search(fr'^{i+1}\.\s', line):
#             break
#         if i == len(lines)-1:
#             if re.search(fr'^{i+1}\.\s', line):
#                 return BlockType.ordered_list
#     return BlockType.paragraph