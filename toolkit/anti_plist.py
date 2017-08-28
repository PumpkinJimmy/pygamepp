import xml.etree.ElementTree as ET
import sys, os, re
import pygame
from pygame.locals import *
from pprint import pprint


def tree_to_dict(tree):
    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index + 1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index + 1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index + 1])
    return d


def get_box_from_plist(plist_filename):
    root = ET.parse(plist_filename).getroot()
    plist_dict = tree_to_dict(root[0])
    to_list = lambda x: x.replace('{', '').replace('}', '').split(',')
    rect_on_big = []
    result_box = []
    offsets = []
    for k, v in plist_dict['frames'].items():
        rectlist = to_list(v['frame'])
        width = int(rectlist[3] if v['rotated'] else rectlist[2])
        height = int(rectlist[2] if v['rotated'] else rectlist[3])
        x = int(rectlist[0])
        y = int(rectlist[1])
        box = Rect(0, 0, 0, 0)
        if v['rotated'] == 'true':
            box.topleft = (x, y)
            box.width = height
            box.height = width
        else:
            box.bottomleft = (x, y)
            box.width = width
            box.height = height
        rect_on_big.append(box)
        sizelist = [int(x) for x in to_list(v['sourceSize'])]
        result_box.append(sizelist)
        offset = [int(x) for x in to_list(v['offset'])]
        offsets.append(offset)
    return rect_on_big, result_box, offsets


def to_list(x):
    return x.replace('{', '').replace('}', '').split(',')


def get_rect_from_dict(plist_dict):
    rect_on_big = {}
    for k, v in plist_dict['frames'].items():
        rectlist = to_list(v['frame'])
        width = int(rectlist[3] if v['rotated'] else rectlist[2])
        height = int(rectlist[2] if v['rotated'] else rectlist[3])
        x = int(rectlist[0])
        y = int(rectlist[1])
        box = Rect(0, 0, 0, 0)
        if v['rotated'] == 'true':
            box.topleft = (x, y)
            box.width = height
            box.height = width
        else:
            box.bottomleft = (x, y)
            box.width = width
            box.height = height
        rect_on_big[k] = box
    return rect_on_big


def get_images_from_plist(plist_filename, texture):
    root = ET.parse(plist_filename).getroot()
    plist_dict = tree_to_dict(root[0])
    rects = get_rect_from_dict(plist_dict)
    #texture = get_texture_from_dict(plist_dict, plist_filename)
    # images = [texture.subsurface(rects[key]) for key in rects]
    images = []
    pat = re.compile(r"run([0-9]+?)\.png")
    keys = sorted(rects.keys(), key=lambda p: int(re.search(pat, p).group(1)))
    for key in keys:
        tmp = texture.subsurface(rects[key])
        rect = tmp.get_rect()
        image = pygame.Surface(list(map(int, to_list(plist_dict["frames"][key]["sourceSize"]))))
        image.fill((255, 255, 255, 0))
        offset = list(map(int, to_list(plist_dict["frames"][key]["offset"])))
        rect.center = image.get_rect().center
        if plist_dict["frames"][key]["rotated"]:
            rect.centerx -= offset[0]
            rect.centery -= offset[1]
        else:
            rect.centerx += offset[0]
            rect.centery -= offset[1]
        image.blit(tmp, rect)
        if plist_dict["frames"][key]["rotated"]:
            image = pygame.transform.rotate(image, 90)
        images.append(image)
    return images


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    plist_fname = r"resource\boys.plist"
    texture = pygame.image.load(r"resource\boys.png").convert_alpha()
    images = get_images_from_plist(plist_fname, texture)

    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.time.set_timer(USEREVENT, 1000)
    fid = -1
    clock = pygame.time.Clock()
    while 1:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            # elif event.type == USEREVENT:
            #     fid += 1
            #     if fid >= len(images):
            #         sys.exit()
            #     screen.blit(images[fid], images[fid].get_rect())
        fid += 1
        if fid >= len(images): fid = -1
        screen.blit(images[fid], images[fid].get_rect())
        pygame.display.flip()
