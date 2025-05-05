from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UO_LIST = "unordered list"
    O_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block == "":
            continue
        new_blocks.append(new_block)

    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    for line in lines:
        if line == "":
            lines.remove(line)
    #check if heading
    if f"# {lines[0].strip("# ")}" in lines[0] and lines[0][0] == "#":
        return BlockType.HEADING
    
    #check if code
    if lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE
    
    #check if quote
    is_quote = True
    for line in lines:
        if line[0] != '>':
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    #check if unorder list
    is_uo_list = True
    for line in lines:
        if line[0] != '-' or line[1] != " ":
            is_uo_list = False
            break
    if is_uo_list:
        return BlockType.UO_LIST
        
    #check if ordered list
    is_o_list = True
    line_num = 1
    for line in lines:
        if line[0] != str(line_num) or line[1] != "." or line[2] != " ":
            is_o_list = False
            break
        line_num += 1
    if is_o_list:
        return BlockType.O_LIST
    
    return BlockType.PARAGRAPH


