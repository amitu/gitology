from gitology.config import settings as gsettings

from datetime import datetime

def blog_document(document, url, blog="main", dtime=None):
    if not dtime: dtime = datetime.now()
    blog_file = gsettings.LOCAL_REPO_PATH.joinpath(
        "blogs"
    ).joinpath(blog).joinpath("%04d" % dtime.year).joinpath(
        "%02d" % dtime.month
    ).joinpath("%02d.lst" % dtime.day)
    print blog_file
    # blog_file.makedirs()
    if not blog_file.parent.exists(): blog_file.parent.makedirs()
    blog_file.open("w+").write(
        "%s %s %s\n" % (url, document.name, str(dtime))
    )
