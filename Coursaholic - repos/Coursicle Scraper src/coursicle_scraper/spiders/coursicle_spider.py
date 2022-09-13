from scrapy import Spider

from coursicle_scraper.utils.helpers import clean, next_request_or_item


class Mixin:
    start_urls = ['https://www.coursicle.com/']
    allowed_domains = ['coursicle.com']
    catalog_url_t = 'https://www.coursicle.com/{}/courses/'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'COOKIES_ENABLED': False,
    }


class ProfessorParser(Mixin, Spider):
    name = 'professor-parser'

    def parse(self, response, **kwargs):
        item = {}

        item['school'] = self.school(response)
        item['department'] = self.department(response)
        item['name'] = self.professor_name(response)
        item['recent_courses'] = self.recent_courses(response)
        item['recent_semesters_teaching'] = self.recent_semesters_teaching(response)
        item['avg_students_each_semester'] = self.avg_students_each_semester(response)

        return item

    def school(self, response):
        return clean(response.css('#pageInfo ::text'))[0].split(' at ')[-1]

    def department(self, response):
        return clean(response.css('.subItemLabel:contains(Department)+.subItemContent ::text'))[0]

    def professor_name(self, response):
        return clean(response.css('#itemViewHeader ::text'))[0]

    def recent_courses(self, response):
        return clean(response.css('.subItemLabel:contains("Recent Courses")+.subItemContent ::text'))

    def recent_semesters_teaching(self, response):
        return clean(response.css('.subItemLabel:contains("Recent Semesters Teaching")+.subItemContent ::text'))[0]

    def avg_students_each_semester(self, response):
        return clean(response.css('.subItemLabel:contains("Avg. Students Each Semester")+.subItemContent ::text'))[0]


class CoursicleParser(Mixin, Spider):
    name = 'coursicle-parser'
    professor_parser = ProfessorParser()

    def parse(self, response, **kwargs):
        course_item = {}

        course_item['course_school'] = self.course_school(response)
        course_item['department'] = self.department(response)
        course_item['course_name'] = self.course_name(response)
        course_item['description'] = self.description(response)
        course_item['credit'] = self.credits(response)
        course_item['recent_professors'] = []
        course_item['recent_semesters'] = self.recent_semesters(response)
        course_item['offered'] = self.offered(response)
        course_item['avg_class_size'] = self.avg_class_size(response)
        course_item['avg_sections'] = self.avg_sections(response)

        course_item['meta'] = {'requests_queue': self.professors_requests(response)}

        return next_request_or_item(course_item)

    def parse_professor(self, response):
        item = response.meta['item']
        item['recent_professors'].append(self.professor_parser.parse(response))
        return next_request_or_item(item)

    def professors_requests(self, response):
        urls = clean(response.css('.subItemLabel:contains("Recent Professors")+.subItemContent ::attr(href)'))
        return [response.follow(url, self.parse_professor) for url in urls]

    def course_school(self, response):
        return clean(response.css('#pageInfo ::text'))[0].split(' at ')[-1]

    def department(self, response):
        return clean(response.css('#pageInfo ::text'))[0].split(' at ')[0]

    def course_name(self, response):
        return clean(response.css('#itemViewHeader ::text'))[0]

    def description(self, response):
        return clean(response.css('.subItemLabel:contains(Description)+.subItemContent ::text'))[0]

    def credits(self, response):
        return clean(response.css('.subItemLabel:contains(Credits)+.subItemContent ::text'))[0]

    def recent_professors(self, response):
        return clean(response.css('.subItemLabel:contains("Recent Professors")+.subItemContent ::text'),
                     pattern_re=r'\s+|,')

    def recent_semesters(self, response):
        return clean(response.css('.subItemLabel:contains("Recent Semesters")+.subItemContent ::text'))[0]

    def offered(self, response):
        return clean(response.css('.subItemLabel:contains(Offered)+.subItemContent ::text'))[0]

    def avg_class_size(self, response):
        return clean(response.css('.subItemLabel:contains("Avg. Class Size")+.subItemContent ::text'))[0]

    def avg_sections(self, response):
        return clean(response.css('.subItemLabel:contains("Avg. Sections")+.subItemContent ::text'))[0]


class CoursicleCrawler(Mixin, Spider):
    name = 'coursicle-crawler'
    parser = CoursicleParser()

    def parse(self, response, **kwargs):
        college_urls = response.css('.tileElement ::attr(href)').getall()

        for url in college_urls:
            keyword = url.strip('/')
            yield response.follow(self.catalog_url_t.format(keyword), self.parse_college_catalog)

    def parse_college_catalog(self, response):
        department_urls = response.css('.tileElement ::attr(href)').getall()

        for url in department_urls:
            yield response.follow(url, self.parse_department)

    def parse_department(self, response):
        course_urls = response.css('.tileElement ::attr(href)').getall()

        for url in course_urls:
            yield response.follow(url, self.parse_course)

    def parse_course(self, response):
        return self.parser.parse(response)
