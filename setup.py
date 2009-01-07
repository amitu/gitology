from setuptools import setup, find_packages
setup(
    name = "gitology",
    version = "0.1",
    packages = find_packages('src'),
    package_dir = { '': 'src' },

    scripts = [
        'src/tools/gitology',
        'src/tools/gitology-blog',
        'src/tools/gitology-init',
    ],
    
    test_suite = "gitology.tests.suite", 

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Amit Upadhyay",
    author_email = "gitology@amitu.com",
    description = "Git based blog/wiki system using DJango",
    license = "BSD",
    keywords = "git django blog wiki",
    url = "http://code.google.com/p/gitology/" 
)

