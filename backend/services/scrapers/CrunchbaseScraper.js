const BaseScraper = require('./BaseScraper');

class CrunchbaseScraper extends BaseScraper {
    constructor() {
        super();
        this.baseUrl = 'https://www.crunchbase.com/organization';
    }

    async scrapeCompany(companyName) {
        const companyUrl = `${this.baseUrl}/${this.slugify(companyName)}`;
        console.log(`Scraping Crunchbase: ${companyUrl}`);
        
        try {
            const $ = await this.fetchPage(companyUrl);
            if (!$) return null;

            return {
                name: this.extractName($),
                description: this.extractDescription($),
                website: this.extractWebsite($),
                crunchbaseUrl: companyUrl,
                funding: this.extractFunding($),
                investors: this.extractInvestors($),
                acquisitions: this.extractAcquisitions($),
                headquarters: this.extractHeadquarters($),
                foundedYear: this.extractFoundedYear($),
                employees: this.extractEmployees($),
                industries: this.extractIndustries($),
                fundingRounds: this.extractFundingRounds($)
            };
        } catch (error) {
            console.error(`Crunchbase scraping error: ${error.message}`);
            return null;
        }
    }

    extractFunding($) {
        const fundingText = $('.funding').text();
        const match = fundingText.match(/\$([\d\.]+)([MBK])?/);
        if (match) {
            let amount = parseFloat(match[1]);
            const multiplier = match[2];
            if (multiplier === 'B') amount *= 1000000000;
            else if (multiplier === 'M') amount *= 1000000;
            else if (multiplier === 'K') amount *= 1000;
            return amount;
        }
        return null;
    }

    extractInvestors($) {
        const investors = [];
        $('.investor-name').each((i, el) => {
            investors.push($(el).text().trim());
        });
        return investors;
    }

    extractFundingRounds($) {
        const rounds = [];
        $('.funding-round').each((i, el) => {
            const round = {
                date: $(el).find('.date').text().trim(),
                amount: $(el).find('.amount').text().trim(),
                type: $(el).find('.round-type').text().trim(),
                investors: $(el).find('.investors').text().trim().split(', ')
            };
            rounds.push(round);
        });
        return rounds;
    }
}

module.exports = CrunchbaseScraper;