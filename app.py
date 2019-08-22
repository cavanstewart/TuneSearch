#!/usr/bin/python3

from flask import Flask, render_template, request, url_for

import search

application = app = Flask(__name__)
app.debug = True



    
@app.route('/search', methods=["GET"])
def dosearch():
    query = request.args['query']
    qtype = request.args['query_type']
    page = request.args.get('page', default=0, type=int)
    
    """
    TODO:
    Use request.args to extract other information
    you may need for pagination.
    """
    np = page + 1
    mp = page - 1

 
    search.search(query, qtype)
    num_results = search.get_length()
    search_results = search.page_results(page)


    
    nx = url_for('dosearch',query_type=qtype, query=query, page=np)
    pr = url_for('dosearch',query_type=qtype, query=query, page=mp)

    if mp == -1:
        pr = None
    if np >= (num_results/20):
        nx = None
    return render_template('results.html',
            query=query,
                           results=num_results,
                           nx=nx,
                           pr=pr,
                           page=page,
                           search_results=search_results)


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        pass
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
