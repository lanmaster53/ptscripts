import sys, urllib2, re, gzip
from urlparse import urlparse
from StringIO import StringIO

#=================================================
# MAIN FUNCTION
#=================================================

def main():
    import optparse
    usage = "%prog [options]\n\n%prog - Tim Tomes (@LaNMaSteR53) (www.lanmaster53.com)"
    parser = optparse.OptionParser(usage=usage, version="%prog 1.1")
    parser.add_option('-v', help='Enable verbose mode.', dest='verbose', default=False, action='store_true')
    parser.add_option('-i', help='File of URLs to test.', dest='infilename', type='string', action='store')
    parser.add_option('-o', help='Output results to a file.', dest='outfilename', type='string', action='store')
    (opts, args) = parser.parse_args()

    if not opts.infilename:
        parser.error("[!] Must provide an input file.")
    else:
        targets = open(opts.infilename).read().split()
    if opts.outfilename:
        # check if file can be created
        # will fail and die if not
        try:
            outfile = open(opts.outfilename, 'w')
            outfile.close()
        except IOError:
            parser.error('\n[!] Error writing to output file location: %s\n[!] Make sure the location exists, is writeable and try using an absolute path.' % opts.outfilename)

    files = [('robots.txt','User-agent:'),('sitemap.xml','<?xml'),('sitemap.xml.gz','<?xml')]
    try:
        for target in targets:
            # build legitimate target url
            target = formatTarget(target)
            if opts.verbose: print target
            doesExist(target, files, opts)
    except KeyboardInterrupt:
        sys.exit()

#=================================================
# SUPPORT FUNCTIONS
#=================================================

def formatTarget(target):
    prefix = ''
    # best guess at protocol prefix
    if not re.match('http[sS]*?:', target):
        if target.find(':') == -1: target += ':80'
        prefix = 'http://'
        if target.split(':')[1].find('443') != -1:
            prefix = 'https://'
    # drop port suffix where not needed
    if target.endswith(':80'): target = ':'.join(target.split(':')[:-1])
    if target.endswith(':443'): target = ':'.join(target.split(':')[:-1])
    return prefix + target

def doesExist(target, files, opts):
    server = urlparse(target)
    # set up request for getting info
    base_url = server.geturl()
    opener = urllib2.build_opener(SmartRedirectHandler)
    urllib2.install_opener(opener)
    for file in files:
        url = '%s/%s' % (base_url, file[0])
        req = urllib2.Request(url)
        # spoof user-agent
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
        req.add_header('User-agent', user_agent)
        # retrieve header information
        try:
            res = urllib2.urlopen(req, None, 3)
            #import pdb;pdb.set_trace()
            content = res.read()
            # check for proper file type since sometimes custom 404s are returned as 200s
            if file[0].lower() == 'sitemap.xml' and not file[1].lower() in content.lower():
                if opts.verbose: print '[%d] %s - Not a valid XML file' % (res.getcode(), url)
                continue
            if file[0].lower() == 'robots.txt' and not file[1].lower() in content.lower():
                if opts.verbose: print '[%d] %s - Not a valid robots.txt file' % (res.getcode(), url)
                continue
            if file[0].lower() == 'sitemap.xml.gz' and not file[1].lower() in uncompress(content).lower():
                if opts.verbose: print '[%d] %s - Not a valid gzipped file' % (res.getcode(), url)
                continue
            print '[+] %s' % url
            if opts.outfilename:
                outfile = open(opts.outfilename, 'a')
                outfile.write('%s\n' % url)
                outfile.close()
        except Exception as res:
            if opts.verbose:
                try:
                    print '[%d] %s - %s' % (res.getcode(), url, res.msg)
                except:
                    if res.args[0][0] == 'timed out':
                        print '[000] %s - %s' % (url, res.args[0][0])
                    else:
                        print '[%s] %s - %s' % (res.args[0][0], url, res.args[0][1])

def uncompress(data_gz):
    inbuffer = StringIO(data_gz)
    data_ct = ''
    f = gzip.GzipFile(mode='rb', fileobj=inbuffer)
    try:
        data_ct = f.read()
    except IOError:
        pass
    f.close()
    return data_ct

#=================================================
# CUSTOM CLASS WRAPPERS
#=================================================

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        pass
        #return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

#=================================================
# START
#=================================================

if __name__ == "__main__": main()
