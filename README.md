# Bhreus

Bhreus is a very very minimal browser engine. So far all it does is parse a subset of HTML and build a DOM tree thereof.

Named after the Proto-Indo-European root of the English verb "to browse."

## Installation

You can install Bhreus by cloning the repo and running

    sudo pip install bhreus

## Usage

Make a parser (initialized or not):

    >>> p = bhreus.parse.Parser()
    >>> q = bhreus.parse.Parser(html)

Give it some markup to parse:

    >>> p.set_html(html)

Get a DOM tree out of that markup:

    >>> tree = p.parse()

Check out that tree with the DOM element prettyprint function:

    >>> tree.pp()
     <html>
       <body>
         <p id="first-line" class="line">
       	   Thunderbolts and lightning!
       	 </p>
       	 <p id="second-line" class="line">
       	   Very very frightening!
       	 </p>
       </body>
     </html>

Or poke at an individual node. Parser.parse() returns the root node.

    >>> body_node = tree.get_children()[0]
    >>> p2_node = body_node.get_children()[1]
    >>> p2_node.pp()
    <p id="second-line" class="line">
      Very very frightning!
    </p>
    >>>
    >>> print p2_node.element_data.attributes.items()
    [("id", "second-line"), ("class", "line")]

## Tests

Run `nosetests` in Bhreus' root directory to make sure everything's running smoothly.
