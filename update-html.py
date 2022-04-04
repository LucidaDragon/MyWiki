import os, re

SiteName = "MyWiki"
SiteDisplayName = "My Wiki"
Author = "Anonymous"
GitHub = "anonymous"
ImageHost = f"https://{GitHub}.github.io/{SiteName}/images/"
CharSet = "<meta charset=\"UTF-8\">"
ScriptTag = f"<script src=\"/{SiteName}/loader.js\"></script>"
NoScript = "<noscript>JavaScript is required to load this page.</noscript>"

def AddCamelSpaces(s):
	escape = True
	i = 0
	while i < len(s):
		c = s[i]
		upper = c.upper()
		if (i > 0 and (not escape) and c == upper and c.lower() != upper):
			s = s[0:i] + " " + s[i:]
			i += 1
		elif (s[i] == '$'):
			prefix = s[0:i]
			s = "(" + prefix + ")" + s[i + 1:]
			i += 1
		escape = False
		if c == '-': escape = True
		i += 1
	return s

def FindImageURI(lines):
	imageName = None
	for line in lines:
		match = re.match("\\[image\\:([^\\]]+)\\]", line)
		if match != None:
			imageName = match[1]
			break
	if imageName == None: return None
	return ImageHost + imageName

def GetHTML(title, description, imageURI):
	titleMeta = "<meta name=\"og:title\" content=\"" + title + "\">"
	authorMeta = f"<meta name=\"author\" content=\"{Author}\"><meta name=\"article:author\" content=\"{Author}\">"
	siteNameMeta = f"<meta name=\"og:site_name\" content=\"{SiteDisplayName}\">"
	typeMeta = "<meta name=\"og:type\" content=\"article\">"
	descriptionMeta = ""
	if description != None: descriptionMeta = f"<meta name=\"description\" content=\"{description}\"><meta name=\"og:description\" content=\"{description}\">"
	imageMeta = ""
	if imageURI != None: imageMeta = "<meta name=\"og:image\" content=\"" + imageURI + "\">"
	return "<!DOCTYPE html><html><head>" + CharSet + siteNameMeta + titleMeta + typeMeta + authorMeta + descriptionMeta + imageMeta + ScriptTag + "</head><body>" + NoScript + "</body></html>"

if not os.path.exists("./wiki"):
	print(f"Script must be run from the root {SiteName} directory.")
	exit(1)

for subdir, dirs, files in os.walk("./wiki"):
	for file in files:
		if file == "index.html" and os.path.exists(os.path.join(subdir, "content.txt")):
			path = os.path.join(subdir, file)
			stream = open(path, mode="r")
			if ScriptTag in stream.read():
				stream.close()
				content = open(os.path.join(subdir, "content.txt"), mode="r")
				lines = content.readlines()
				content.close()
				if len(lines) > 0:
					descLine = lines[0].strip()
					if not descLine[0].isalpha(): descLine = None
					name = AddCamelSpaces(os.path.basename(subdir))
					if name == "wiki": name = "Home"
					stream = open(path, mode="w")
					stream.write(GetHTML(name, descLine, FindImageURI(lines)))
					stream.close()
			else:
				stream.close()
