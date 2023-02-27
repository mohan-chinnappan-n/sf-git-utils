#--- constants

API_VERSION="57.0"

PKG_PREFIX = f'''<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
  <version>{API_VERSION}</version>
'''

PKG_SUFFIX = "</Package>"


EMPTY_PACKAGE_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
  <version>{API_VERSION}</version>
</Package>
'''

#----