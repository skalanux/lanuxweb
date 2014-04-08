import string, os, sys, getopt
from xml.dom import minidom


def convert(infile, outdir, authorDirs, categoryDirs):
    # First we parse the XML file into a list of posts.
    # Each post is a dictionary

    dom = minidom.parse(infile)

    blog = [] # list that will contain all posts

    categories = set()

    for node in dom.getElementsByTagName('item'):
        post = dict()

        post["title"] = node.getElementsByTagName('title')[0].firstChild.data
        post["date"] = node.getElementsByTagName('pubDate')[0].firstChild.data
        post["author"] = node.getElementsByTagName(
                        'dc:creator')[0].firstChild.data
        post["id"] = node.getElementsByTagName('wp:post_id')[0].firstChild.data

        if node.getElementsByTagName('content:encoded')[0].firstChild != None:
            post["text"] = node.getElementsByTagName(
                            'content:encoded')[0].firstChild.data
        else:
            post["text"] = ""

        # wp:attachment_url could be use to download attachments

        # Get the categories
        tempCategories = []
        for subnode in node.getElementsByTagName('category'):
             tempCategories.append(subnode.getAttribute('nicename'))
        categories = [x for x in tempCategories if x != '']
        post["categories"] = categories 
        categories.append(categories)
        # Add post to the list of all posts
        blog.append(post)

    # Then we create the directories and HTML files from the list of posts.


def usage(pname):
    """Displays usage information

    keyword arguments:
    pname -- program name (e.g. obtained as argv[0])

    """


    print """python %s [-hac] [-o outdir] infile
    Converts a Wordpress Export File to multiple html files.

    Options:
        -h,--help\tDisplays this information.
        -a,--authors\tCreate different directories for each author.
        -c,--categories\tCreate directory structure from post categories.
        -o,--outdir\tSpecify a directory for the output.

    Example:
    python %s -c -o ~/TEMP ~/wordpress.2008-03-20.xml
        """ % (pname, pname)


def main(argv):
    outdir = ""
    authors = False
    categories = False
    
    try:
        opts, args = getopt.getopt(
            argv[1:], "ha:o:c", ["help", "authors", "outdir", "categories"])    
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv[0])
            sys.exit()
        elif opt in ("-a", "--authors"):
            authors = True
        elif opt in ("-c", "--categories"):
            categories = True
        elif opt in ("-o", "--outdir"):
            outdir = arg
        
    infile = "".join(args)
    
    if infile == "":
        print "Error: Missing Argument: missing wordpress export file."
        usage(argv[0])
        sys.exit(3)
    
    if outdir == "":
        # Use the current directory
        outdir = os.getcwd()
    
    convert(infile, outdir, authors, categories)
    

if __name__ == "__main__":
    main(sys.argv)
