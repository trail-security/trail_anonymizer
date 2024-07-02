import os

def set_tld_extract_cache_dir():
    #---------------------------------------------------
    # A Hack to set a cache dir for tldextract, so running offline doesn't fail
    # https://github.com/john-kurkowski/tldextract#:~:text=bbc%20co.uk-,Note%20about%20caching,-Beware%20when%20first
    current_file_path = os.path.abspath(__file__)
    package_directory = os.path.dirname(current_file_path)
    cache_directory = os.path.join(package_directory, '.tld_extractor_cache')
    os.environ["TLDEXTRACT_CACHE"] = cache_directory
    #---------------------------------------------------
