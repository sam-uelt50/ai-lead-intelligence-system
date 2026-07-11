const BaseScraper = require('./BaseScraper');

class BuiltWithScraper extends BaseScraper {
    constructor() {
        super();
        this.baseUrl = 'https://builtwith.com';
    }

    async scrapeTechStack(domain) {
        const url = `${this.baseUrl}/${domain}`;
        console.log(`Scraping tech stack: ${url}`);
        
        try {
            const $ = await this.fetchPage(url);
            if (!$) return null;

            const techStack = {
                analytics: this.extractCategory($, 'Analytics'),
                advertising: this.extractCategory($, 'Advertising'),
                widgets: this.extractCategory($, 'Widgets'),
                frameworks: this.extractCategory($, 'Frameworks'),
                cms: this.extractCategory($, 'Content Management System'),
                hosting: this.extractCategory($, 'Hosting'),
                languages: this.extractCategory($, 'Programming Languages'),
                mobile: this.extractCategory($, 'Mobile')
            };

            return techStack;
        } catch (error) {
            console.error(`BuiltWith scraping error: ${error.message}`);
            return null;
        }
    }

    extractCategory($, category) {
        const technologies = [];
        $(`h3:contains("${category}")`).next('table').find('tr').each((i, el) => {
            const tech = $(el).find('td').first().text().trim();
            if (tech) technologies.push(tech);
        });
        return technologies;
    }
}

module.exports = BuiltWithScraper;