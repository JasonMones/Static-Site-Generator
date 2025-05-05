from textnode import *
import re

STOP_SCANNING = "stop scanning"

def get_delimiter_indices(text, delimiter):
    global STOP_SCANNING
    try:
        first_delimiter_index = text.index(delimiter)
    except ValueError:
        return STOP_SCANNING, None
        
    try:
        second_delimiter_index = text.index(delimiter, first_delimiter_index + 1) + len(delimiter)
    except ValueError:
        raise Exception("invalid markdown syntax")
    return first_delimiter_index, second_delimiter_index

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = old_nodes.copy()
    new_nodes = []

    for node in nodes:
        text = node.text
        if node.text_type != TextType.TEXT or not delimiter in text:
            new_nodes.append(node)
            continue
        
        global STOP_SCANNING
        while True:
            first_delimiter_index, second_delimiter_index = get_delimiter_indices(text, delimiter)
            if first_delimiter_index == STOP_SCANNING:
                new_nodes.append(TextNode(text, TextType.TEXT))
                break
                
            new_nodes.append(TextNode(text[:first_delimiter_index], TextType.TEXT))
            new_nodes.append(TextNode(text[first_delimiter_index+len(delimiter):second_delimiter_index-len(delimiter)], text_type))
            text = text[second_delimiter_index:]


    return new_nodes

def extract_markdown_images(text): #helper method for image_or_link_parameters
    alt_text_regex = r"\!\[(.*?)\]"
    url_text_regex = r"\((.*?)\)"
    alt_text = re.findall(alt_text_regex, text)
    url_text = re.findall(url_text_regex, text)

    return list(zip(alt_text, url_text))

def extract_markdown_links(text): #helper method for image_or_link_parameters
    anchor_text_regex = r"\[(.*?)\]"
    url_text_regex = r"\((.*?)\)"
    anchor_text = re.findall(anchor_text_regex, text)
    url_text = re.findall(url_text_regex, text)

    return list(zip(anchor_text, url_text))



def image_or_link_parameters(text, type): #helper method for split_nodes_image and split_nodes_link
                                          #returns list of tuples in order (alt text/anchor text, url)
    correct_syntax = []

    if type == TextType.IMAGE:
        text_url = extract_markdown_images(text)
    elif type == TextType.LINK:
        text_url = extract_markdown_links(text)

    if text_url == []:
        return None

    for pair in text_url:
        if type == TextType.LINK and f"[{pair[0]}]({pair[1]})" in text:
            if f"![{pair[0]}]({pair[1]})" in text:
                raise ValueError("requires link, not image")
            correct_syntax.append(pair)
        elif type == TextType.IMAGE and f"[{pair[0]}]({pair[1]})" in text:
            correct_syntax.append(pair)
        else:
            raise ValueError("incorrect image or link syntax")
        
    return correct_syntax


def split_nodes_image(old_nodes):
    if not isinstance(old_nodes, list) or old_nodes == []:
        raise ValueError("not list or empty list")
    new_nodes = []

    nodes = old_nodes.copy()
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #find how many instances of correct syntax for images exist
        text = node.text
        correct_syntax = image_or_link_parameters(text, TextType.IMAGE)

        if correct_syntax == None:
            new_nodes.append(node)
            continue

        #add all new nodes to new_nodes
        for pair in correct_syntax:
            image_start = text.index(f"![{pair[0]}")
            image_end = text.index(f"{pair[1]})") + len(f"{pair[1]})")
            if pair == correct_syntax[-1]:  
                new_nodes.append(TextNode(text[:image_start], TextType.TEXT))
                new_nodes.append(TextNode(pair[0], TextType.IMAGE, pair[1]))
                new_nodes.append(TextNode(text[image_end:], TextType.TEXT))
            else:
                new_nodes.append(TextNode(text[:image_start], TextType.TEXT))
                new_nodes.append(TextNode(pair[0], TextType.IMAGE, pair[1]))

            text = text[image_end:]
    return new_nodes

def split_nodes_link(old_nodes):  #same thing as split_nodes_image with small tweaks to use for links
    if not isinstance(old_nodes, list) or old_nodes == []:
        raise ValueError("not list or empty list")
    new_nodes = []

    nodes = old_nodes.copy()
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #find how many instances of correct syntax for images exist
        text = node.text
        correct_syntax = image_or_link_parameters(text, TextType.LINK)

        if correct_syntax == None:
            new_nodes.append(node)
            continue

        #add all new nodes to new_nodes
        for pair in correct_syntax:
            image_start = text.index(f"[{pair[0]}")
            image_end = text.index(f"{pair[1]})") + len(f"{pair[1]})")
            if pair == correct_syntax[-1]:  
                new_nodes.append(TextNode(text[:image_start], TextType.TEXT))
                new_nodes.append(TextNode(pair[0], TextType.LINK, pair[1]))
                new_nodes.append(TextNode(text[image_end:], TextType.TEXT))
            else:
                new_nodes.append(TextNode(text[:image_start], TextType.TEXT))
                new_nodes.append(TextNode(pair[0], TextType.LINK, pair[1]))

            text = text[image_end:]
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)   
    return nodes