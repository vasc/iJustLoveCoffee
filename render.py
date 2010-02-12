def main(page = 1):
    main_file = open('main.tmpl', 'r')
    main = main_file.read()
    dedication_file = open('dedication.tmpl', 'r')
    dedication = dedication_file.read()
    send_html(main)

def single(dedication):
    main_file = open('main.tmpl', 'r')
    main = main_file.read()
    dedication_file = open('dedication.tmpl', 'r')
    dedication = dedication_file.read()
    send_html('single')

def page_404():
    page_404_file = open('404.tmpl', 'r')
    page_404 = page_404_file.read()
    print 'Status: 404 Not Found'
    send_html(page_404)
#
    
def send_html(name):
    print 'Content-type: text/html'
    print
    print str(name)
