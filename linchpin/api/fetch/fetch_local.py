import os
import sys
import shutil
import urlparse
import tempfile
from fetch import Fetch


class FetchLocal(Fetch):

    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root):
        super(Fetch, self).__init__(ctx, fetch_type, dest, root)

        self.cache_dir = os.path.join(cache_dir, "local")
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        src_parse = urlparse.urlparse(src)
        self.src = os.path.abspath(os.path.join(src_parse.netloc, src_parse.path))

    
        if not os.path.exists(self.src):
            ctx.log_state('{0} is not a valid path'.format(src))
            sys.exit(1)
        if os.path.samefile(self.src, self.dest):
            ctx.log_state("Provide two different locations")
            sys.exit(1)


    def fetch_files(self):
        if self.root is not None:
            for ext in self.root:
                td = tempfile.mkdtemp(prefix="local_", dir=self.cache_dir)
                src = os.path.join(self.src, ext.lstrip('/'))
                self.get_files(src, td)
                self.tempdirs.append(td)
        else:
            tempdir = tempfile.mkdtemp(prefix="local_", dir=self.cache_dir)
            self.get_files(self.src, tempdir)
            self.tempdirs.append(td)

    def get_files(self, src, tempdir):
        for item in os.listdir(src):
            try:
                s = os.path.join(src, item)
                d = os.path.join(tempdir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            except OSEerror as e:
                if e.errno == 17:
                    self.ctx.log_state('The {0} directory already'
                    'exists'.format(item))

