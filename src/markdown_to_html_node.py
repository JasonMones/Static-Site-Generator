from block_methods import *
from markdown_conversion_methods import text_to_textnodes
from textnode import *
from parentnode import *
from leafnode import *

def determine_heading_tag(block):  #helper method for remove_markdown() and block_to_html_node() for header blocks
    if block_to_block_type(block) != BlockType.HEADING:
        raise ValueError("must be a heading block")
    
    num_of_hashtags = 0
    for char in block:
        if char == "#":
            num_of_hashtags += 1
        else:
            break

    match (num_of_hashtags):
        case 1:
            return "h1"
        case 2:
            return "h2"
        case 3:
            return "h3"
        case 4:
            return "h4"
        case 5:
            return "h5"
        case 6:
            return "h6"
        case _:
            raise ValueError("incorrect number of hashtags for heading block syntax")
        
def text_to_children(text): #helper method for block_to_html_node()
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for textnode in text_nodes:
        leaf_nodes.append(textnode.text_node_to_html_node())
    return leaf_nodes

def get_list_children(block): #helper method for UO_LIST and O_LIST blocks in block_to_html_node()
        block_type = block_to_block_type(block)
        if block_type != BlockType.UO_LIST and block_type != BlockType.O_LIST:
            raise ValueError("block must be of type unordered list or ordered list")
        
        lines = block.split("\n")

        parent_nodes = []
        for line in lines:
            if line == "":
                lines.remove(line)
                continue
            if block_type == BlockType.UO_LIST:
                parent_nodes.append(ParentNode("li", text_to_children(line[2:])))
            else:
                parent_nodes.append(ParentNode("li", text_to_children(line[3:])))

        return parent_nodes


def remove_markdown(block, block_type): #helper method for block_to_html_node()
    if block_to_block_type(block) != block_type:
        raise ValueError("incorrect blocktype parameter")
    
    match (block_type):
        case BlockType.PARAGRAPH:
            return block
        case BlockType.HEADING:
            num_of_hashtags = int(determine_heading_tag(block)[1:])
            return block[num_of_hashtags + 1:]
        case BlockType.CODE:
            lines = block.split("\n")
            lines.pop(0)
            lines.pop(-1)
            return "\n".join(lines)
        case BlockType.QUOTE:
            lines = block.split("\n")

            new_lines = []
            for line in lines:
                new_lines.append(line[2:])
            return "\n".join(new_lines)
        case BlockType.UO_LIST:
            lines = block.split("\n")

            new_lines = []
            for line in lines:
                new_lines.append(line[2:])
            return "\n".join(new_lines)
        case BlockType.O_LIST:
            lines = block.split("\n")

            new_lines = []
            for line in lines:
                new_lines.append(line[3:])
            return "\n".join(new_lines)

def block_to_html_node(old_block): #helper method for markdown_to_html_node()
    block_type = block_to_block_type(old_block)

    block = remove_markdown(old_block, block_type)
    match (block_type):
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block))
        case BlockType.HEADING:
            return ParentNode(determine_heading_tag(old_block), text_to_children(block))
        case BlockType.CODE:
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, block)])])
        case BlockType.QUOTE:
            return ParentNode("blockquote", text_to_children(block))
        case BlockType.UO_LIST:
            return ParentNode("ul", get_list_children(old_block))
        case BlockType.O_LIST:
            return ParentNode("ol", get_list_children(old_block))
        case _:
            raise ValueError("invalid block type")


#puts everything together to go from a markdown document to html
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []
    for block in blocks:
        block_nodes.append(block_to_html_node(block))

    return ParentNode("div", block_nodes)

