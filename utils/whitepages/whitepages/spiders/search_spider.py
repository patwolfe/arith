import scrapy
from string import ascii_lowercase as lowercase
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from whitepages.items import WhitepagesItem

SITE = "https://whitepages.tufts.edu/"

# If you really want to do this in one pass you should switch between
# the first letter of the first name and the last name, probably get a better
# distribution and avoid the matt problem
# Also just the built in duplication filter catch stuff

class SearchSpider(scrapy.Spider):
    name = "whitepages"

    def start_requests(self):
        return self.search("")

    def search(self, cur_str):
        print("searching with ", cur_str)
        return [
            scrapy.FormRequest(
                url=SITE + "asearchresults.cgi",
                formdata={
                    "type": "Students",
                    "FirstOption": "starts",
                    "getFirst": cur_str + letter,
                },
                callback=self.after_search,
                cb_kwargs=dict(letters=cur_str + letter),
            )
            for letter in lowercase
        ]

    def after_search(self, response, letters):
        print("Checking ", letters)
        warning = response.xpath(
            '//div[contains(., "Warning: Your search returned too many results")]'
        ).get()
        # Do a more specific search if there are too many results
        if warning is not None:
            requests = self.search(letters)
            for request in requests:
                yield request
        # Otherwise just scrape
        else:
            la = response.xpath(
                '//tr[contains(., "College of Liberal Arts")]/td/a/@href'
            ).getall()
            eng = response.xpath(
                '//tr[contains(., "School of Engineering")]/td/a/@href'
            ).getall()
            urls = la + eng
            for url in urls:
                yield scrapy.Request(url=SITE + url, callback=self.parse_student)

    def parse_student(self, response):
        year = response.xpath('//tr[contains(., "Class Year:")]/td[2]/text()').get()
        if year.strip() == "20":
            student = WhitepagesItem()
            name = response.xpath('//tr[contains(., "Name:")]/td[2]/text()').get()
            student["name"] = name.strip()
            email = response.xpath(
                '//tr[contains(., "Email Address:")]/td[2]/a/text()'
            ).get()
            if email is not None:
                student["email"] = email.strip()
            major = response.xpath('//tr[contains(., "Major:")]/td[2]/text()').get()
            if major is not None:
                student["major"] = major.strip()
            return student


class FuckMatt(SearchSpider):
    """ This is what happens when you don't think algorithms through """

    name = "common_names"

    def start_requests(self):
        # These names either have too many entries or are common beginings of other names
        # Cycling though all of these + last name first letters is excessive for some of
        # these but whatever
        common_names = [
            "michael",
            "matt",
            "matthew",
            "chris",
            "will",
            "sam",
            "daniel",
            "dan",
            "ben",
            "benjamin",
            "emily",
            "sara",
            "sarah",
            "alex",
            "alexa",
            "ann",
        ]
        for name in common_names:
            for letter in lowercase:
                yield scrapy.FormRequest(
                    url=SITE + "asearchresults.cgi",
                    formdata={
                        "type": "Students",
                        "FirstOption": "is",
                        "getFirst": name,
                        "LastOption": "starts",
                        "getLast": letter,
                    },
                    callback=self.after_search,
                    # This is bad, but hopefully never used
                    cb_kwargs=dict(letters=name),
                )
