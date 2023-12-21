import requests

class Instiz:
    BASE_INSTIZ = "https://www.instiz.net"
    BASE_VOTE = f"{BASE_INSTIZ}/bbs/vote.php"
    BASE_COMMENT = f"{BASE_INSTIZ}/bbs/comment_ok.php"

    def __init__(self, id):
        self.id = id

    def vote(self, postUrl):
        postUrl  = postUrl.replace(self.BASE_INSTIZ, "")[1:]
        category = postUrl[:postUrl.find("/")]
    
        postUrl  = postUrl.replace(category, "")[1:]
        postNo   = postUrl[:postUrl.find("?")]
        vote_web = f"{self.BASE_VOTE}?id={category}&no={postNo}"
        requests.post(vote_web, cookies={"INSTIZID": self.id})

    def write_comment(self, postUrl, text):
        postUrl  = postUrl.replace(self.BASE_INSTIZ, "")[1:]
        category = postUrl[:postUrl.find("/")]
    
        postUrl  = postUrl.replace(category, "")[1:]
        postNo   = postUrl[:postUrl.find("?")]
        comment_web = f"{self.BASE_COMMENT}?id={category}&no={postNo}"
        data = {"memo": text}
        return requests.post(comment_web, data=data, cookies={"INSTIZID": self.id})

    def postList(self, category):
        LIST  = "<list>"
        START = '<tr id="detour">'
        TAG   = "</td></tr>"
        res = requests.get(f"{self.BASE_INSTIZ}/{category}")
        data = res.text[res.text.find(LIST + START) + len(LIST + START):]
        data = data[:data.find("/table")]

        postCount = data.count("minitext listnm")
        postArray = [{}] * postCount

        for i in range(postCount):
            postNo = data[data.find("no=") + len("no="):][1:]
            postNo = postNo[:postNo.find('"')]
            postArray[i] = {"postNo" : postNo}
            data = data[data.find(TAG) + len(TAG):]

        return postArray

###
instizId = "SESSION"
category = "name"
###

instiz = Instiz(instizId)

"""
# get posts from category and vote on them
arr = instiz.postList(category)
for v in arr:
    url = f"{instiz.BASE_INSTIZ}/{category}/{v['postNo']}?page=&category="
    instiz.vote(url)

# write comment
instiz.write_comment("postURL", "new comment")
"""

