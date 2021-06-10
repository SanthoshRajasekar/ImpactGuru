import scrapy


class ImpactguruSpider(scrapy.Spider):
    """Name of Spider"""

    name = "impactguru"
    allowed_domains = ["impactguru.com"]

    def start_requests(self):
        yield scrapy.Request(
            "https://www.impactguru.com/fundraisers/", callback=self.parse_search
        )

    def parse_search(self, response):
        """Parsing Fundraiser urls"""
        urls = response.css("#campaignCards a#bf-card-fundraiser::attr('href')")
        for url in urls:
            yield response.follow(url, callback=self.parse_page)

        """ Parsing Next Page url id """

        loadmore = response.css("#loadMoreBtn")
        if loadmore:
            data_page = loadmore.css("button::attr('data-page')").get()
            yield scrapy.Request(
                f"https://www.impactguru.com/fundraisers?page={data_page}",
                callback=self.parse_search,
            )

    def parse_page(self, response):

        """Creating a dict and storing the values"""
        data = {}
        data["Title"] = response.css("#campaignTitle::text").get("").strip()
        data["Amount_Raised"] = (
            response.css(".custom-raisedAmount::text").get("").strip()
        )
        data["total_amount_in_need"] = response.css(
            ".box-stick__color-light::text"
        ).re_first("of (.*)")
        data["Campaigner_Name"] = (
            response.xpath(
                "//div[div/div/h5[contains(., 'Campaigner Details')]]/div[@class='description']/div[1]/text()"
            )
            .get("")
            .strip()
        )
        data["Campaigner_Details"] = (
            response.xpath(
                "//div[div/div/h5[contains(., 'Campaigner Details')]]/div[@class='description']/div[2]/text()"
            )
            .get("")
            .strip()
        )
        data["Campaigner_Location"] = (
            response.xpath(
                "//div[div/div/h5[contains(., 'Campaigner Details')]]/div[@class='description']//i[contains(@class,'fa-map-marker-alt')]/following-sibling::text()"
            )
            .get("")
            .strip()
        )
        data["Beneficiary_Name"] = (
            response.xpath(
                "//div[div/div/h5[contains(., 'Beneficiary Details')]]/div[@class='description']/div[1]/text()"
            )
            .get("")
            .strip()
        )
        data["Beneficiary_Status"] = (
            response.xpath(
                "//div[div/div/h5[contains(., 'Beneficiary Details')]]/div[@class='description']/div[2]/text()"
            )
            .get("")
            .strip()
        )
        data["Admitted_at"] = (
            response.xpath(
                "//div[div/div/h5[contains(., 'Beneficiary Details')]]/div[@class='description']//div[@class='font-weight-bold']/text()"
            )
            .get("")
            .strip()
        )
        data["Account_number"] = (
            response.xpath(
                "//div[@id='payment-options']//*[contains(., 'Account number')]/span[@class='b-level']/text()"
            )
            .get("")
            .strip()
        )
        data["Account_Name"] = (
            response.xpath(
                "//div[@id='payment-options']//*[contains(., 'Account name')]/span[@class='b-level']/text()"
            )
            .get("")
            .strip()
        )
        data["IFSC"] = (
            response.xpath(
                "//div[@id='payment-options']//*[contains(., 'IFSC code')]/span[@class='b-level']/text()"
            )
            .get("")
            .strip()
        )
        yield data
