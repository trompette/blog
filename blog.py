#!/usr/bin/env python

import engine
import jinja2
import os

pages_dir = os.path.join(os.getcwd(), 'pages')
posts_dir = os.path.join(os.getcwd(), 'posts')
templates_dir = os.path.join(os.getcwd(), 'templates')
web_dir = os.path.join(os.getcwd(), 'web')

environment = jinja2.Environment(loader=jinja2.FileSystemLoader([pages_dir, posts_dir, templates_dir]))

blog = engine.Blog()

print "Reading posts..."

for post in os.listdir(posts_dir):
    print "Found", post[:-8]
    blog.posts[post] = environment.get_template(post)
    for tag in blog.posts[post].module.tags:
        if not blog.tags.has_key(tag):
            blog.tags[tag] = []
        blog.tags[tag].append(post)

print "Rendering pages..."

for page in os.listdir(pages_dir):
    page_template = environment.get_template(page)
    strategy = page_template.module.strategy
    if 'blog' == strategy:
        with open(os.path.join(web_dir, page[:-3]), 'w') as f:
            f.write(page_template.render(blog=blog))
        print "Dumped", page[:-3]
    elif 'post' == strategy:
        for post, post_template in blog.posts.iteritems():
            with open(os.path.join(web_dir, post[:-3]), 'w') as f:
                f.write(post_template.render())
            print "Dumped", post[:-3]