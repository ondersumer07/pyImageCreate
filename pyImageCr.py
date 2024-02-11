from PIL import Image, ImageDraw, ImageFont
from github import Github
from datetime import date
import requests

# get data from pockethost
api_url = "https://personal-website.pockethost.io/api/collections/poems/records?perPage=67"
response = requests.get(api_url)
data = response.json()

def createPoemImage():
    # get poem number from public api
    poemNumApi = "http://ondersumer07.pythonanywhere.com/randomNumAPI"
    responsePoemNum = requests.get(poemNumApi)
    dataPoemNum = responsePoemNum.json()
    # dataPoemNum["randomNum"]
    poemNum = dataPoemNum["randomNum"]

    # get POEM
    poemData =  data["items"][poemNum]["poem"]

    # CLEAR poem from '\r'
    def clearPoem():
        poem = poemData.translate(str.maketrans('', '', '\r'))
        return poem

    # get POEM LINE COUNT to decide on height
    poemLineCount = clearPoem().count('\n')

    # get LONGEST LINE in poem
    def longestLineFinder(poem):
        lines = poem.splitlines()
        longestline = max(lines, key=len)
        return longestline

    # create FONT OBJECTS
    fontObjectTitle = ImageFont.truetype('C:\\Users\\onder\\Desktop\\pyImageCr\\Inter-ExtraBold.ttf', 40)
    fontObjectPoem = ImageFont.truetype('C:\\Users\\onder\\Desktop\\pyImageCr\\Inter-Regular.ttf', 30)
    fontObjectSource = ImageFont.truetype('C:\\Users\\onder\\Desktop\\pyImageCr\\Inter-LightItalic.otf', 20)

    # calculate the IDEAL HEIGHT of picture and source
    idealHeightofSource = 1500

    if(poemLineCount >= 50):
        idealHeightofSource = 150 + poemLineCount*fontObjectPoem.getmask(clearPoem()).getbbox()[3] - 50
        print(poemLineCount)
    if(poemLineCount < 50):
        idealHeightofSource = 150 + poemLineCount*fontObjectPoem.getmask(clearPoem()).getbbox()[3] + 50
        print(poemLineCount)

    heightOfWebsite = idealHeightofSource + 50
    idealHeightofPic =heightOfWebsite + 120

    # calculate poem TITLE and LONGEST LINE WIDTH to make sure it fits
    pageWidth = 1500
    widthOfTitle = fontObjectTitle.getlength(data["items"][poemNum]["title"])
    longestLineWidth = fontObjectPoem.getlength(longestLineFinder(poemData))

    if(widthOfTitle > 1400):
        pageWidth = int(widthOfTitle) + 200

    if(longestLineWidth > 1400):
        pageWidth = int(longestLineWidth) + 200

    # calculate idealPoemWidth here, so if pageWidth changes it's correct
    idealPoemWidth = (pageWidth - longestLineWidth) / 2

    # CREATE image
    imgObj = Image.new("RGB", (pageWidth,idealHeightofPic), (31,27,24))
    drawingObject = ImageDraw.Draw(imgObj)

    # draw the image
    drawingObject.text((pageWidth/2,75), data["items"][poemNum]["title"], (251,231,209), font=fontObjectTitle, anchor="mt")
    drawingObject.text((idealPoemWidth,150), clearPoem(), (251,231,209), font=fontObjectPoem)
    drawingObject.text((pageWidth/2,idealHeightofSource), "From " + data["items"][poemNum]["source"], (251,231,209), font=fontObjectSource, anchor="mt")
    drawingObject.text((pageWidth/2,idealHeightofSource+100), "ondersumer.com  •  Poem of the day, " + date.today().strftime("%d %b %Y"), (251,231,209), font=fontObjectSource, anchor="mt")

    imgObj.save("todaysPoem.jpg")

    g=Github("Git Token")
repo=g.get_repo("Repo")

file_path = "Image.png"
message = "Commit Message"
branch = "master"

with open(file_path, "rb") as image:
    f = image.read()
    image_data = bytearray(f)

def push_image(path,commit_message,content,branch,update=False):
    if update:
        contents = repo.get_contents(path, ref=branch)
        repo.update_file(contents.path, commit_message, content, sha=contents.sha, branch)
    else:
        repo.create_file(path, commit_message, content, branch)


push_image(file_path,message, bytes(image_data), branch, update=False)

createPoemImage()